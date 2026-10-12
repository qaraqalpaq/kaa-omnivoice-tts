# Karakalpak OmniVoice TTS

Text-to-speech for **Karakalpak** (qaraqalpaq tili) built on [k2-fsa/OmniVoice](https://huggingface.co/k2-fsa/OmniVoice), with no fine-tuning. OmniVoice does not support Karakalpak, so this project maps Karakalpak text into the Kazakh alphabet, which OmniVoice reads well. The voice is cloned from a short clip of a real Karakalpak speaker.

**Live demo:** https://kaa-tts-cpu-0f4cac-0bff79.tun.aralcloud.uz. It runs on a shared CPU server, so a sentence takes about 1.5 minutes; the ready-made samples on the page play instantly.

> The OmniVoice weights are licensed **CC-BY-NC**: this project and any audio it produces are for **non-commercial use only**. See [Licence](#licence).

## Samples

12 sentences, each read with 3 reference voices. Click ▶ to play.

| Text | Voice 1 | Voice 2 | Voice 3 |
|---|---|---|---|
| Assalawma áleykum! Sizge qanday járdem bere alaman? | [▶](https://github.com/qaraqalpaq/kaa-omnivoice-tts/raw/main/samples/greet_voice1.mp3) | [▶](https://github.com/qaraqalpaq/kaa-omnivoice-tts/raw/main/samples/greet_voice2.mp3) | [▶](https://github.com/qaraqalpaq/kaa-omnivoice-tts/raw/main/samples/greet_voice3.mp3) |
| Pasport alıw ushın mámleketlik xızmetler orayına barıwıńız kerek. | [▶](https://github.com/qaraqalpaq/kaa-omnivoice-tts/raw/main/samples/gov_voice1.mp3) | [▶](https://github.com/qaraqalpaq/kaa-omnivoice-tts/raw/main/samples/gov_voice2.mp3) | [▶](https://github.com/qaraqalpaq/kaa-omnivoice-tts/raw/main/samples/gov_voice3.mp3) |
| Búgin hawa rayı jaqsı, temperatura jigirma bes gradus. | [▶](https://github.com/qaraqalpaq/kaa-omnivoice-tts/raw/main/samples/weather_voice1.mp3) | [▶](https://github.com/qaraqalpaq/kaa-omnivoice-tts/raw/main/samples/weather_voice2.mp3) | [▶](https://github.com/qaraqalpaq/kaa-omnivoice-tts/raw/main/samples/weather_voice3.mp3) |
| Telefon nomerim: toqsan bir, júz jigirma úsh, qırq bes, altımıs jeti. | [▶](https://github.com/qaraqalpaq/kaa-omnivoice-tts/raw/main/samples/numbers_voice1.mp3) | [▶](https://github.com/qaraqalpaq/kaa-omnivoice-tts/raw/main/samples/numbers_voice2.mp3) | [▶](https://github.com/qaraqalpaq/kaa-omnivoice-tts/raw/main/samples/numbers_voice3.mp3) |
| Siz qay jerde jasaysız? | [▶](https://github.com/qaraqalpaq/kaa-omnivoice-tts/raw/main/samples/question_voice1.mp3) | [▶](https://github.com/qaraqalpaq/kaa-omnivoice-tts/raw/main/samples/question_voice2.mp3) | [▶](https://github.com/qaraqalpaq/kaa-omnivoice-tts/raw/main/samples/question_voice3.mp3) |
| Ráhmet, kúnińiz jaqsı ótsin! | [▶](https://github.com/qaraqalpaq/kaa-omnivoice-tts/raw/main/samples/thanks_voice1.mp3) | [▶](https://github.com/qaraqalpaq/kaa-omnivoice-tts/raw/main/samples/thanks_voice2.mp3) | [▶](https://github.com/qaraqalpaq/kaa-omnivoice-tts/raw/main/samples/thanks_voice3.mp3) |
| Qaraqalpaqstan Respublikası Ámiwdárya deltasında jaylasqan bolıp, onıń paytaxtı Nókis qalası esaplanadı. | [▶](https://github.com/qaraqalpaq/kaa-omnivoice-tts/raw/main/samples/long_voice1.mp3) | [▶](https://github.com/qaraqalpaq/kaa-omnivoice-tts/raw/main/samples/long_voice2.mp3) | [▶](https://github.com/qaraqalpaq/kaa-omnivoice-tts/raw/main/samples/long_voice3.mp3) |
| Aldın arza tolturıń, keyin hújjetlerdi tapsırasız. | [▶](https://github.com/qaraqalpaq/kaa-omnivoice-tts/raw/main/samples/dialog_voice1.mp3) | [▶](https://github.com/qaraqalpaq/kaa-omnivoice-tts/raw/main/samples/dialog_voice2.mp3) | [▶](https://github.com/qaraqalpaq/kaa-omnivoice-tts/raw/main/samples/dialog_voice3.mp3) |
| Balalar mektepke kúnde saat segizde baradı. | [▶](https://github.com/qaraqalpaq/kaa-omnivoice-tts/raw/main/samples/school_voice1.mp3) | [▶](https://github.com/qaraqalpaq/kaa-omnivoice-tts/raw/main/samples/school_voice2.mp3) | [▶](https://github.com/qaraqalpaq/kaa-omnivoice-tts/raw/main/samples/school_voice3.mp3) |
| Arzańız qabıl etildi, nátiyjesi úsh kún ishinde málim boladı. | [▶](https://github.com/qaraqalpaq/kaa-omnivoice-tts/raw/main/samples/status_voice1.mp3) | [▶](https://github.com/qaraqalpaq/kaa-omnivoice-tts/raw/main/samples/status_voice2.mp3) | [▶](https://github.com/qaraqalpaq/kaa-omnivoice-tts/raw/main/samples/status_voice3.mp3) |
| Keshirersiz, sizdi jaqsı esitpedim, qaytalap aytıp jibere alasız ba? | [▶](https://github.com/qaraqalpaq/kaa-omnivoice-tts/raw/main/samples/repeat_voice1.mp3) | [▶](https://github.com/qaraqalpaq/kaa-omnivoice-tts/raw/main/samples/repeat_voice2.mp3) | [▶](https://github.com/qaraqalpaq/kaa-omnivoice-tts/raw/main/samples/repeat_voice3.mp3) |
| Bizdiń xızmetimizden paydalanǵanıńız ushın ráhmet. | [▶](https://github.com/qaraqalpaq/kaa-omnivoice-tts/raw/main/samples/bye_voice1.mp3) | [▶](https://github.com/qaraqalpaq/kaa-omnivoice-tts/raw/main/samples/bye_voice2.mp3) | [▶](https://github.com/qaraqalpaq/kaa-omnivoice-tts/raw/main/samples/bye_voice3.mp3) |

## How it works

1. **Numbers to words.** Digits are spelled out in Karakalpak (`2026` → `eki mıń jigirma altı`) using `configs/kaa_kazakh_script.json`.
2. **Chunking.** Text is split at punctuation. Each chunk is synthesised separately and the chunks are joined with a short pause.
3. **Kazakh-script bridge.** Karakalpak Latin (or Cyrillic) is mapped to Kazakh Cyrillic: `Qaraqalpaqstan` → `қарақалпақстан`, `Nókis` → `нөкіс`. The table is `configs/kaa_latn_to_cyrl.json`. Letters Kazakh lacks are replaced with the closest Kazakh letters, for example ў → у, ҳ → һ, ч → тш.
4. **Synthesis.** OmniVoice runs in Kazakh mode (`language="kk"`), cloning the chosen reference voice. The duration is set from the text length (13.5 characters per second), which keeps the pace natural.

On 30 held-out Karakalpak sentences scored with a Karakalpak ASR model, the character error rate is 6.1% mean (5.3% median), against 15.1% for MMS-TTS Kazakh. The output keeps a slight Kazakh accent and intonation.

## Quick start

```bash
git clone https://github.com/qaraqalpaq/kaa-omnivoice-tts
cd kaa-omnivoice-tts
pip install torch torchaudio
pip install -r requirements.txt
```

On first run the model (about 3.1 GB) downloads from Hugging Face at a pinned revision (`configs/model.json`) into the Hugging Face cache.

### Command line

```bash
python kaa_omnivoice.py --voice kaa_voice_1 --text "Assalawma áleykum! Sizge qanday járdem bere alaman?" --out out/
python kaa_omnivoice.py --voice kaa_voice_2 --texts configs/kaa_tts_demo_texts.jsonl --out out/
python kaa_omnivoice.py --ref-audio my_voice.wav --ref-text "transcript of my_voice.wav" --text "Ráhmet!" --out out/
```

Each text is written as `out/0000.wav`, `out/0001.wav` and so on, at 24 kHz.

| Flag | Meaning |
|---|---|
| `--voice` | A reference voice from `voices/voices.json`: `kaa_voice_1` … `kaa_voice_5` |
| `--ref-audio`, `--ref-text` | Your own reference clip (5–15 s of clean speech) and its transcript |
| `--speed` | Speaking rate; `1.0` is 13.5 characters per second |
| `--num-step` | Generation steps (default 32); fewer is faster |
| `--device`, `--dtype` | `cuda:0` or `cpu`; `float32`, `bfloat16` or `float16` |
| `--model`, `--model-revision`, `--cache-dir` | A Hugging Face repo id or a local model directory, its revision, and the download cache |

The model options can also be set with `KAA_TTS_MODEL`, `KAA_TTS_MODEL_REVISION` and `KAA_TTS_CACHE_DIR`. To run offline, download once and set `HF_HUB_OFFLINE=1`, or point `--model` at a local copy.

### Python

```python
import soundfile as sf
from kaa_omnivoice import BUNDLED_VOICES, SAMPLE_RATE, KaraKalpakOmniVoice, load_voices, resolve_model

tts = KaraKalpakOmniVoice(resolve_model())
ref_audio, ref_text = load_voices(BUNDLED_VOICES)["kaa_voice_1"]
audio = tts.synthesize("Ráhmet, kúnińiz jaqsı ótsin!", ref_audio, ref_text, speed=1.0)
sf.write("out.wav", audio, SAMPLE_RATE)
```

### Web demo

```bash
python app.py
```

The demo serves a small web page on `127.0.0.1:7861`. Requests go through a job queue: every HTTP call returns at once and the page polls for the result, so it keeps working behind tunnels and proxies that cut long requests.

| Endpoint | Purpose |
|---|---|
| `POST /api/speak` | `{"text", "voice", "speed"}` → a job (`202`); `429` when the queue is full or the per-IP limit is reached |
| `GET /api/jobs/{id}` | Status: `queued`, `running`, `done` or `error`, with queue position and ETA |
| `GET /api/jobs/{id}/audio` | The finished WAV |
| `GET /api/config`, `GET /health` | Voices, examples and limits; liveness |

All settings are environment variables; `.env.example` lists them with their meaning in the table below.

| Variable | Default | Meaning |
|---|---|---|
| `KAA_TTS_DEVICE`, `KAA_TTS_DTYPE` | GPU if available; `float32` | Device and precision |
| `KAA_TTS_NUM_STEP` | 32 | Generation steps |
| `KAA_TTS_THREADS` | torch default | CPU threads |
| `KAA_TTS_CONCURRENCY`, `KAA_TTS_MAX_QUEUE` | 1, 8 | Parallel generations; waiting requests |
| `KAA_TTS_MAX_CHARS` | 400 | Longest accepted text |
| `KAA_TTS_RATE_LIMIT`, `KAA_TTS_RATE_WINDOW_S` | 0 (off), 600 | Requests per client IP per window |
| `KAA_TTS_TRUST_PROXY` | 1 | Read the client IP from `X-Real-IP` / `X-Forwarded-For` |
| `KAA_TTS_ESTIMATE_S` | 10 | Seconds per request assumed until the first one finishes |
| `KAA_TTS_NOTE` | empty | Message shown above the form |
| `KAA_TTS_HOST`, `KAA_TTS_PORT` | `127.0.0.1`, `7861` | Listen address |

## Docker

The image contains the code, voices and samples. The model downloads on first start into the `/cache` volume and is reused after that.

```bash
cp .env.example .env
docker compose --profile cpu up -d --build
docker compose --profile gpu up -d --build
```

Use the first command for CPU and the second for GPU; the GPU profile needs the NVIDIA Container Toolkit.

Without compose:

```bash
docker build -t kaa-omnivoice-tts:cpu .
docker run -d --name kaa-tts --restart unless-stopped --cpus=4 --memory=5g \
  -p 127.0.0.1:7861:7861 -v kaa-tts-cache:/cache \
  -e KAA_TTS_DEVICE=cpu -e KAA_TTS_NUM_STEP=8 -e KAA_TTS_THREADS=4 \
  kaa-omnivoice-tts:cpu
```

For a GPU image, build with `--build-arg DEVICE=cuda` (CUDA PyTorch wheels) and run with `--gpus 1 -e KAA_TTS_DEVICE=cuda:0`. The container runs as a non-root user and reports healthy once `/health` answers. It listens only on `127.0.0.1`; publish it through a reverse proxy with TLS or a tunnel.

## Performance

**GPU** (one data-centre GPU, 32 steps): 7–8 s for a short sentence (28–51 characters) after warm-up, using about 4.5 GB of VRAM. Measured through the demo API, so these times include the network round trip. The Docker GPU image itself has not been run on a GPU yet.

**CPU** (Intel Xeon Platinum 8570, GPU hidden, float32). RTF is wall time divided by audio length.

| Torch threads | 41 chars (3.4 s audio) | 120 chars (9.2 s) | 282 chars (22.8 s) |
|---|---|---|---|
| 16 | 65 s · RTF 19 | 86 s · RTF 9.3 | 292 s · RTF 12.8 |
| 8 | 94 s · RTF 28 | 113 s · RTF 12.5 | 395 s · RTF 17.3 |
| 4 | 100 s · RTF 29 | 137 s · RTF 14.9 | 542 s · RTF 23.8 |

- **Memory:** about 0.8 GB after loading and 3.7 GB peak while generating; give the container 5 GB.
- **`--num-step 8`:** about 2× faster than 32, with character error rate 16.5% against 15.4% under the same scorer.
- **Shared server:** on the public demo (4 CPUs of a busy 8-vCPU server, 8 steps), a sentence takes 80–100 s.
- **Concurrency:** parallel workers on the same CPU barely raise throughput; scale out across machines instead.

CPU is fine for batch work, not for live conversation. `kaa_cpu_bench.py` reproduces these numbers.

## Tests

```bash
pip install pytest
pytest -q
```

The tests cover the transliteration, number spelling and chunking rules and the bundled assets. They do not need the model.

## Limits

- **Non-commercial:** the OmniVoice weights are CC-BY-NC.
- **Kazakh accent:** OmniVoice has no Karakalpak voice data. Karakalpak words are read through Kazakh spelling, so some sounds are approximated and the intonation is Kazakh.
- **No streaming:** each chunk is generated whole before audio is returned.
- **Consent:** the reference voices are real people from an open corpus. Do not use this to imitate anyone without their consent.

## Licence

- **Code:** [MIT](LICENSE). The MIT licence applies to the code only.
- **Model:** [k2-fsa/OmniVoice](https://huggingface.co/k2-fsa/OmniVoice) weights are CC-BY-NC; OmniVoice code is Apache-2.0. The model is downloaded at run time and is not part of this repository.
- **Reference voices:** clips from the [Karakalpak Speech Corpus](https://huggingface.co/datasets/atikuwu/karakalpak-speech-corpus) by atikuwu, CC-BY-4.0.
- **Samples:** generated audio, non-commercial under the model licence.

Full details are in [ATTRIBUTION.md](ATTRIBUTION.md).
