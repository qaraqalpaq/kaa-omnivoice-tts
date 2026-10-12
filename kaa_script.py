import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent


def config_path(name):
    candidates = [HERE / "configs" / name, HERE.parent / "configs" / name]
    return next((p for p in candidates if p.exists()), candidates[-1])


KAA_RULES = config_path("kaa_kazakh_script.json")
KAA_TABLE = config_path("kaa_latn_to_cyrl.json")
KAA_PRE_MAP = {" h": " x", "uw": "uu", "iw": "ıu", "aw": "au", "ow": "ou", "ew": "eu", "ў": "y"}


def longest_first(mapping):
    if not mapping:
        return lambda text: text
    keys = sorted(mapping, key=len, reverse=True)
    pattern = re.compile("|".join(re.escape(k) for k in keys))
    return lambda text: pattern.sub(lambda m: mapping[m.group(0)], text)


class KaaNumbers:
    def __init__(self, spec):
        self.units, self.tens, self.hundred, self.scales = spec["units"], spec["tens"], spec["hundred"], spec["scales"]

    def below_thousand(self, n):
        words = []
        if n >= 100:
            words += ([self.units[n // 100]] if n // 100 > 1 else []) + [self.hundred]
            n %= 100
        if n >= 10:
            words.append(self.tens[n // 10])
            n %= 10
        if n:
            words.append(self.units[n])
        return words

    def words(self, n):
        if n == 0:
            return self.units[0]
        out = []
        for value, name in self.scales:
            if n >= value:
                count = n // value
                out += ([] if count == 1 and value == 1000 else self.below_thousand(count)) + [name]
                n %= value
        return " ".join(out + self.below_thousand(n))

    def __call__(self, text):
        return re.sub(r"\d+", lambda m: self.words(int(m.group(0))), text)


class KaaToKazakhScript:
    def __init__(self, table_path, vocab, rules_path=KAA_RULES):
        rules = json.loads(Path(rules_path).read_text())
        self.numbers = KaaNumbers(rules["numbers"]) if rules.get("numbers") else str
        self.pre = longest_first(KAA_PRE_MAP)
        self.table = longest_first(json.loads(Path(table_path).read_text()))
        candidates = {**rules["post"], **({"у": rules["vowel_u"]} if rules.get("vowel_u") else {})}
        post = {src: next((c for c in options if all(ch in vocab for ch in c)), src) for src, options in candidates.items()}
        self.post = longest_first({k: v for k, v in post.items() if k != v})
        self.split = re.compile(rules["split_pattern"])
        self.pause_s = rules["pause_s"]

    def chunks(self, text):
        return [c.strip() for c in self.split.split(self.numbers(text)) if c.strip()]

    def __call__(self, text):
        return self.post(self.table(self.pre(" " + text))[1:].lower())
