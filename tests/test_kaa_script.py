import json

import pytest

from kaa_script import KAA_RULES, KAA_TABLE, KaaNumbers, KaaToKazakhScript, longest_first

SPEC = json.loads(KAA_RULES.read_text())


@pytest.fixture(scope="module")
def convert():
    return KaaToKazakhScript(KAA_TABLE, set(SPEC["kazakh_alphabet"]), KAA_RULES)


@pytest.fixture(scope="module")
def numbers():
    return KaaNumbers(SPEC["numbers"])


@pytest.mark.parametrize("latin, kazakh", [
    ("Qaraqalpaqstan", "қарақалпақстан"),
    ("Nókis", "нөкіс"),
    ("Assalawma áleykum!", "ассалаума әлейкум!"),
    ("ráhmet", "рәһмет"),
    ("shólkem", "шөлкем"),
    ("Ózbekstan", "өзбекстан"),
    ("hújjetlerdi", "хүжжетлерді"),
])
def test_latin_maps_to_kazakh_cyrillic(convert, latin, kazakh):
    assert convert(latin) == kazakh


@pytest.mark.parametrize("cyrillic, kazakh", [
    ("Чимбай", "тшімбай"),
    ("Ўзбекстан", "узбекстан"),
])
def test_karakalpak_cyrillic_is_normalised(convert, cyrillic, kazakh):
    assert convert(cyrillic) == kazakh


def test_output_uses_only_kazakh_letters(convert):
    alphabet = set(SPEC["kazakh_alphabet"]) | set("!?.,;:'\"()")
    text = "Qaraqalpaqstan Respublikası Ámiwdárya deltasında jaylasqan, onıń paytaxtı Nókis qalası."
    assert set(convert(text)) <= alphabet


@pytest.mark.parametrize("value, words", [
    (0, "nol"),
    (7, "jeti"),
    (15, "on bes"),
    (21, "jigirma bir"),
    (100, "júz"),
    (123, "júz jigirma úsh"),
    (1000, "mıń"),
    (1995, "mıń toǵız júz toqsan bes"),
    (2026, "eki mıń jigirma altı"),
    (1000000, "bir million"),
])
def test_numbers_are_spelled_in_karakalpak(numbers, value, words):
    assert numbers.words(value) == words


def test_numbers_inside_text(numbers):
    assert numbers("2026 jılı 25 adam") == "eki mıń jigirma altı jılı jigirma bes adam"


def test_chunks_split_on_punctuation_and_spell_numbers(convert):
    assert convert.chunks("Sálem! Qalay? 25 adam keldi, ráhmet.") == ["Sálem", "Qalay", "jigirma bes adam keldi", "ráhmet"]


def test_longest_first_prefers_longer_keys():
    assert longest_first({"s": "x", "sh": "y"})("shs") == "yx"
    assert longest_first({})("same") == "same"
