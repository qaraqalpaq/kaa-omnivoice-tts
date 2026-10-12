import argparse
import json
import resource
import time
from pathlib import Path

import soundfile as sf
import torch

from kaa_omnivoice import BUNDLED_VOICES, SAMPLE_RATE, KaraKalpakOmniVoice, load_voices, model_args, resolve_model


def peak_rss_gb():
    return round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024 ** 2, 2)


def read_texts(path):
    return [json.loads(l) for l in open(path) if l.strip()]


def timed(tts, text, ref, speed=1.0):
    start = time.perf_counter()
    audio = tts.synthesize(text, *ref, speed)
    wall = time.perf_counter() - start
    return audio, round(wall, 2), round(len(audio) / SAMPLE_RATE, 2)


def main():
    p = argparse.ArgumentParser()
    model_args(p)
    p.add_argument("--voices", default=str(BUNDLED_VOICES))
    p.add_argument("--voice", required=True)
    p.add_argument("--texts", required=True, help="jsonl with id and text")
    p.add_argument("--dtype", choices=["float32", "bfloat16"], default="float32")
    p.add_argument("--threads", default="8", help="comma-separated torch thread counts")
    p.add_argument("--num-step", type=int)
    p.add_argument("--repeat", type=int, default=1)
    p.add_argument("--tag", default="run")
    p.add_argument("--out", required=True)
    a = p.parse_args()

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    start = time.perf_counter()
    tts = KaraKalpakOmniVoice(resolve_model(a.model, a.model_revision, a.cache_dir), device="cpu", dtype=a.dtype, num_step=a.num_step)
    load_s = round(time.perf_counter() - start, 1)
    ref = load_voices(a.voices)[a.voice]
    texts = read_texts(a.texts)
    log = open(out / "results.jsonl", "a")
    base = {"tag": a.tag, "dtype": a.dtype, "num_step": a.num_step or 32, "load_s": load_s, "rss_after_load_gb": peak_rss_gb()}
    torch.set_num_threads(int(a.threads.split(",")[0]))
    timed(tts, texts[0]["text"], ref)
    for threads in map(int, a.threads.split(",")):
        torch.set_num_threads(threads)
        for row in texts:
            for r in range(a.repeat):
                audio, wall, dur = timed(tts, row["text"], ref)
                sf.write(out / f"{a.tag}_t{threads}_{row['id']}_{r}.wav", audio, SAMPLE_RATE)
                log.write(json.dumps({**base, "threads": threads, "id": row["id"], "chars": len(row["text"]), "wall_s": wall,
                                      "audio_s": dur, "rtf": round(wall / dur, 3), "peak_rss_gb": peak_rss_gb()}) + "\n")
                log.flush()


if __name__ == "__main__":
    main()
