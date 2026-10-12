import json

from kaa_script import HERE, config_path


def test_model_spec_pins_a_revision():
    spec = json.loads(config_path("model.json").read_text())
    assert spec["repo_id"] == "k2-fsa/OmniVoice"
    assert len(spec["revision"]) == 40


def test_voices_exist_and_carry_licence():
    voices = json.loads((HERE / "voices" / "voices.json").read_text())
    assert voices
    for voice in voices.values():
        assert (HERE / "voices" / voice["audio"]).is_file()
        assert voice["text"] and voice["license"] and voice["source"]


def test_samples_index_matches_files():
    rows = [json.loads(line) for line in (HERE / "samples" / "samples.jsonl").read_text().splitlines() if line]
    assert rows
    for row in rows:
        assert (HERE / "samples" / row["audio"]).is_file()
        assert row["text"] and row["voice"]
