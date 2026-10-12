import argparse
import json
import os
import queue
import tempfile
import threading
import time
import uuid
from collections import OrderedDict, defaultdict, deque
from pathlib import Path

import soundfile as sf
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from kaa_omnivoice import BUNDLED_VOICES, SAMPLE_RATE, KaraKalpakOmniVoice, load_voices, model_args, resolve_model
from kaa_script import HERE, KAA_RULES, KAA_TABLE, config_path

DEFAULT_EXAMPLES = config_path("kaa_tts_demo_texts.jsonl")
WEB = HERE / "web"
SAMPLES = HERE / "samples"


class SpeakRequest(BaseModel):
    text: str
    voice: str | None = None
    speed: float = 1.0


class Job:
    def __init__(self, request):
        self.id = uuid.uuid4().hex
        self.request = request
        self.status = "queued"
        self.created = time.time()
        self.started = None
        self.audio = None
        self.error = None


class RateLimiter:
    def __init__(self, limit, window_s):
        self.limit, self.window_s = limit, window_s
        self.hits = defaultdict(deque)
        self.lock = threading.Lock()

    def check(self, key):
        if not self.limit:
            return
        now = time.time()
        with self.lock:
            hits = self.hits[key]
            while hits and now - hits[0] > self.window_s:
                hits.popleft()
            if len(hits) >= self.limit:
                raise HTTPException(429, {"code": "rate_limited", "retry_after_s": round(self.window_s - (now - hits[0]))})
            hits.append(now)
            for stale in [k for k, v in self.hits.items() if not v]:
                del self.hits[stale]


class SpeechQueue:
    def __init__(self, tts, voices, workers, max_queue, keep, initial_estimate_s, out_dir):
        self.tts, self.voices, self.out_dir = tts, voices, Path(out_dir)
        self.pending = queue.Queue(maxsize=max_queue)
        self.jobs = OrderedDict()
        self.keep = keep
        self.workers = workers
        self.lock = threading.Lock()
        self.estimate_s = initial_estimate_s
        for _ in range(workers):
            threading.Thread(target=self._work, daemon=True).start()

    def submit(self, request):
        job = Job(request)
        try:
            self.pending.put_nowait(job)
        except queue.Full:
            raise HTTPException(429, {"code": "queue_full"})
        with self.lock:
            self.jobs[job.id] = job
            while len(self.jobs) > self.keep:
                _, old = self.jobs.popitem(last=False)
                if old.audio:
                    Path(old.audio).unlink(missing_ok=True)
        return job

    def position(self, job):
        with self.lock:
            waiting = [j for j in self.jobs.values() if j.status == "queued"]
        return waiting.index(job) + 1 if job in waiting else 0

    def remaining_s(self, job):
        return max(self.estimate_s - (time.time() - job.started), 0)

    def eta_s(self, job):
        if job.status == "running":
            return self.remaining_s(job)
        if job.status == "queued":
            with self.lock:
                running = [self.remaining_s(j) for j in self.jobs.values() if j.status == "running"]
            return (sum(running) + self.estimate_s * self.position(job)) / self.workers
        return 0

    def _work(self):
        while True:
            job = self.pending.get()
            job.status, job.started = "running", time.time()
            try:
                ref_audio, ref_text = self.voices.get(job.request.voice, (None, None))
                audio = self.tts.synthesize(job.request.text, ref_audio, ref_text, job.request.speed)
                path = self.out_dir / f"{job.id}.wav"
                sf.write(path, audio, SAMPLE_RATE)
                job.audio, job.status = str(path), "done"
            except Exception as error:
                job.error, job.status = str(error), "error"
            self.estimate_s = 0.7 * self.estimate_s + 0.3 * (time.time() - job.started)


def client_key(request, trust_proxy):
    if trust_proxy:
        forwarded = request.headers.get("x-real-ip") or request.headers.get("x-forwarded-for", "").split(",")[0].strip()
        if forwarded:
            return forwarded
    return request.client.host if request.client else "unknown"


def create_app(speech, limiter, trust_proxy, examples, note, max_chars, speed_range):
    app = FastAPI(docs_url=None, redoc_url=None)

    def find(job_id):
        job = speech.jobs.get(job_id)
        if not job:
            raise HTTPException(404, {"code": "not_found"})
        return job

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.get("/api/config")
    def config():
        return {"voices": list(speech.voices), "examples": examples, "note": note, "max_chars": max_chars,
                "speed": speed_range, "estimate_s": round(speech.estimate_s), "queue": speech.pending.qsize()}

    @app.post("/api/speak", status_code=202)
    def speak(request: SpeakRequest, http: Request):
        text = request.text.strip()
        if not text:
            raise HTTPException(400, {"code": "empty_text"})
        if len(text) > max_chars:
            raise HTTPException(413, {"code": "text_too_long"})
        if request.voice and request.voice not in speech.voices:
            raise HTTPException(400, {"code": "unknown_voice"})
        limiter.check(client_key(http, trust_proxy))
        speed = min(max(request.speed, speed_range[0]), speed_range[1])
        job = speech.submit(SpeakRequest(text=text, voice=request.voice, speed=speed))
        return status(job.id)

    @app.get("/api/jobs/{job_id}")
    def status(job_id: str):
        job = find(job_id)
        return {"id": job.id, "status": job.status, "position": speech.position(job), "eta_s": round(speech.eta_s(job)),
                "audio_url": f"/api/jobs/{job.id}/audio" if job.status == "done" else None, "error": job.error}

    @app.get("/api/jobs/{job_id}/audio")
    def audio(job_id: str):
        job = find(job_id)
        if job.status != "done":
            raise HTTPException(409, {"code": job.status})
        return FileResponse(job.audio, media_type="audio/wav", filename="qaraqalpaqsha.wav")

    if SAMPLES.is_dir():
        app.mount("/samples", StaticFiles(directory=SAMPLES), name="samples")
    app.mount("/", StaticFiles(directory=WEB, html=True), name="web")
    return app


def main():
    env = os.environ.get
    p = argparse.ArgumentParser()
    model_args(p)
    p.add_argument("--table", default=env("KAA_TTS_TABLE", str(KAA_TABLE)))
    p.add_argument("--rules", default=env("KAA_TTS_RULES", str(KAA_RULES)))
    p.add_argument("--voices", default=env("KAA_TTS_VOICES", str(BUNDLED_VOICES)))
    p.add_argument("--examples", default=env("KAA_TTS_EXAMPLES", str(DEFAULT_EXAMPLES)))
    p.add_argument("--device", default=env("KAA_TTS_DEVICE"))
    p.add_argument("--dtype", default=env("KAA_TTS_DTYPE"), choices=["float32", "bfloat16", "float16"])
    p.add_argument("--num-step", type=int, default=int(env("KAA_TTS_NUM_STEP", "0")) or None)
    p.add_argument("--threads", type=int, default=int(env("KAA_TTS_THREADS", "0")) or None)
    p.add_argument("--concurrency", type=int, default=int(env("KAA_TTS_CONCURRENCY", "1")))
    p.add_argument("--max-queue", type=int, default=int(env("KAA_TTS_MAX_QUEUE", "8")))
    p.add_argument("--keep-jobs", type=int, default=int(env("KAA_TTS_KEEP_JOBS", "100")))
    p.add_argument("--max-chars", type=int, default=int(env("KAA_TTS_MAX_CHARS", "400")))
    p.add_argument("--estimate-s", type=float, default=float(env("KAA_TTS_ESTIMATE_S", "10")))
    p.add_argument("--rate-limit", type=int, default=int(env("KAA_TTS_RATE_LIMIT", "0")))
    p.add_argument("--rate-window-s", type=int, default=int(env("KAA_TTS_RATE_WINDOW_S", "600")))
    p.add_argument("--trust-proxy", type=int, default=int(env("KAA_TTS_TRUST_PROXY", "1")))
    p.add_argument("--note", default=env("KAA_TTS_NOTE", ""))
    p.add_argument("--host", default=env("KAA_TTS_HOST", "127.0.0.1"))
    p.add_argument("--port", type=int, default=int(env("KAA_TTS_PORT", "7861")))
    a = p.parse_args()

    if a.threads:
        import torch
        torch.set_num_threads(a.threads)
    model = resolve_model(a.model, a.model_revision, a.cache_dir)
    tts = KaraKalpakOmniVoice(model, a.table, a.rules, device=a.device, dtype=a.dtype, num_step=a.num_step)
    examples = [json.loads(l)["text"] for l in open(a.examples) if l.strip()] if os.path.isfile(a.examples) else []
    out_dir = tempfile.mkdtemp(prefix="kaa_tts_")
    speech = SpeechQueue(tts, load_voices(a.voices), a.concurrency, a.max_queue, a.keep_jobs, a.estimate_s, out_dir)
    limiter = RateLimiter(a.rate_limit, a.rate_window_s)
    app = create_app(speech, limiter, bool(a.trust_proxy), examples, a.note, a.max_chars, [0.7, 1.3])
    uvicorn.run(app, host=a.host, port=a.port, log_level="warning")


if __name__ == "__main__":
    main()
