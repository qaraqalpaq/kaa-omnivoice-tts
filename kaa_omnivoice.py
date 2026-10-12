import argparse
import json
import os
from pathlib import Path

import numpy as np
import soundfile as sf

from kaa_script import HERE, KAA_RULES, KAA_TABLE, KaaToKazakhScript, config_path

SAMPLE_RATE = 24000
MODEL_SPEC = config_path("model.json")
BUNDLED_VOICES = HERE / "voices" / "voices.json"


def resolve_model(source=None, revision=None, cache_dir=None, spec_path=MODEL_SPEC):
    spec = json.loads(Path(spec_path).read_text())
    source = source or spec["repo_id"]
    if Path(source).is_dir():
        return str(source)
    from huggingface_hub import snapshot_download
    return snapshot_download(source, revision=revision or spec["revision"], cache_dir=cache_dir,
                             allow_patterns=spec.get("allow_patterns"))


def default_device():
    import torch
    return "cuda:0" if torch.cuda.is_available() else "cpu"


class KaraKalpakOmniVoice:
    def __init__(self, model, table=KAA_TABLE, rules=KAA_RULES, alphabet=None, device=None, dtype=None, num_step=None):
        import torch
        from omnivoice import OmniVoice
        spec = json.loads(Path(rules).read_text())
        load = {"torch_dtype": getattr(torch, dtype)} if dtype else {}
        self.model = OmniVoice.from_pretrained(model, device_map=device or default_device(), **load)
        self.convert = KaaToKazakhScript(table, set(alphabet or spec["kazakh_alphabet"]), rules)
        self.language = spec.get("omnivoice_language", "kk")
        self.chars_per_sec = spec.get("omnivoice_chars_per_sec")
        self.generation = {"num_step": num_step} if num_step else {}

    def _say(self, text, extra, speed):
        pace = {"duration": len(text) / (self.chars_per_sec * speed)} if self.chars_per_sec else {"speed": speed}
        audio = self.model.generate(text=text, language=self.language, **pace, **self.generation, **extra)[0]
        return np.asarray(audio, dtype=np.float32)

    def synthesize(self, text, ref_audio=None, ref_text=None, speed=1.0):
        extra = {"ref_audio": ref_audio, "ref_text": ref_text} if ref_audio else {}
        pause = np.zeros(int(self.convert.pause_s * SAMPLE_RATE), np.float32)
        parts = [self._say(self.convert(chunk), extra, speed) for chunk in self.convert.chunks(text)]
        return np.concatenate([x for p in parts for x in (p, pause)][:-1]) if parts else np.zeros(0, np.float32)


def load_voices(path):
    if not path or not Path(path).is_file():
        return {}
    base = Path(path).parent
    return {name: (str(base / v["audio"]), v.get("text")) for name, v in json.loads(Path(path).read_text()).items()}


def model_args(parser):
    env = os.environ.get
    parser.add_argument("--model", default=env("KAA_TTS_MODEL"), help="Hugging Face repo id or local model directory")
    parser.add_argument("--model-revision", default=env("KAA_TTS_MODEL_REVISION"))
    parser.add_argument("--cache-dir", default=env("KAA_TTS_CACHE_DIR"))


def main():
    p = argparse.ArgumentParser()
    model_args(p)
    p.add_argument("--table", default=str(KAA_TABLE), help="Karakalpak Latin to Cyrillic json")
    p.add_argument("--rules", default=str(KAA_RULES))
    p.add_argument("--voices", default=str(BUNDLED_VOICES), help="json: name -> {audio, text} reference clips")
    p.add_argument("--voice")
    p.add_argument("--ref-audio", help="your own reference clip instead of --voice")
    p.add_argument("--ref-text", help="transcript of --ref-audio")
    p.add_argument("--speed", type=float, default=1.0)
    p.add_argument("--num-step", type=int)
    p.add_argument("--device")
    p.add_argument("--dtype", choices=["float32", "bfloat16", "float16"])
    p.add_argument("--text")
    p.add_argument("--texts", help="jsonl with a text field")
    p.add_argument("--out", required=True)
    a = p.parse_args()

    model = resolve_model(a.model, a.model_revision, a.cache_dir)
    tts = KaraKalpakOmniVoice(model, a.table, a.rules, device=a.device, dtype=a.dtype, num_step=a.num_step)
    ref_audio, ref_text = (a.ref_audio, a.ref_text) if a.ref_audio else load_voices(a.voices).get(a.voice, (None, None))
    texts = [a.text] if a.text else [json.loads(l)["text"] for l in open(a.texts) if l.strip()]
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    for i, text in enumerate(texts):
        sf.write(out / f"{i:04d}.wav", tts.synthesize(text, ref_audio, ref_text, a.speed), SAMPLE_RATE)


if __name__ == "__main__":
    main()
