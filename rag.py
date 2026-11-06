import re

from tree import TREE, ROOT

# Всяко свойство е въпрос от мрежата: (твърдение при „Да“, твърдение при „Не“).
STATEMENTS = {
    "topka": ("използва се топка", "не се използва топка"),
    "race": ("играе се с ръце", "не се играе с ръце"),
    "vrata": ("има врата", "няма врата"),
    "mrezha": ("има мрежа", "няма мрежа"),
    "zabiva": ("топката се забива", "топката не се забива"),
    "otbor": ("отборен спорт е", "не е отборен спорт"),
    "ledsnyag": ("играе се на лед или сняг", "не се играе на лед или сняг"),
    "kunki": ("използват се кънки", "не се използват кънки"),
    "stik": ("използва се стик", "не се използва стик"),
    "voda": ("спортът е във вода", "спортът не е във вода"),
    "lodka": ("използва се лодка", "не се използва лодка"),
    "boen": ("боен спорт е", "не е боен спорт"),
    "rakavici": ("използват се ръкавици", "не се използват ръкавици"),
    "samorace": ("използват се само ръце", "не се използват само ръце"),
    "snyag": ("практикува се на сняг", "не се практикува на сняг"),
    "dyska": ("използва се дъска", "не се използва дъска"),
    "prepyatstvia": ("има препятствия", "няма препятствия"),
}

# Ключови думи (начало на думата), по които се разпознава свойството във въпроса.
KEYWORDS = {
    "topka": ["топк"], "race": ["ръце"], "vrata": ["врат"], "mrezha": ["мреж"],
    "zabiva": ["заби"], "otbor": ["отбо"], "ledsnyag": ["лед"], "kunki": ["кънк"],
    "stik": ["стик"], "voda": ["вода", "води", "водн"], "lodka": ["лодк"],
    "boen": ["боен", "бойн"], "rakavici": ["ръка"], "snyag": ["сняг", "снег"],
    "dyska": ["дъск"], "prepyatstvia": ["препя"],
}

# Как се разпознава името на всеки спорт (по-специфичните първи).
SPORT_PATTERNS = [
    ("kikboks", r"кик[\s\-]*бокс\w*"),
    ("shafetno", r"шафетн\w*\s+бяган\w*"),
    ("beg", r"бяган\w*\s+(?:с\s+)?препятств\w*"),
    ("kayak", r"кану[\s\-]*каяк\w*|каяк\w*|кану\w*"),
    ("ski", r"ски(?:[\s\-]+пързал\w*)?"),
    ("futbol", r"футбол\w*"), ("handbal", r"хандбал\w*"), ("voleibol", r"волейбол\w*"),
    ("basketbol", r"баскетбол\w*"), ("bouling", r"боулинг\w*"), ("kurling", r"кърлинг\w*"),
    ("hokei", r"хоке\w*"), ("pluvane", r"плуван\w*"), ("karate", r"карате\w*"),
    ("boks", r"бокс\w*"), ("snoubord", r"сноуборд\w*"),
]

NEGATIONS = {"не", "няма", "нямат", "без", "нито"}
# След такава дума отрицанието не важи („без топка, но с лед“).
BREAKERS = {"но", "а", "обаче", "докато"}


def _collect(node_id, path, out):
    node = TREE[node_id]
    if "q" in node:
        _collect(node["yes"], path + [(node_id, True)], out)
        _collect(node["no"], path + [(node_id, False)], out)
    elif node["found"]:
        out.append((node["answer"], dict(path), [k for k, _ in path]))


def build_cards():
    """Карта за всеки спорт: име, свойства (id -> True/False) и твърдения по реда на мрежата."""
    leaves = []
    _collect(ROOT, [], leaves)
    names = {v["answer"]: k for k, v in TREE.items() if "answer" in v and v["found"]}
    cards = {}
    for name, feats, order in leaves:
        facts = [STATEMENTS[f][0 if feats[f] else 1] for f in order]
        cards[names[name]] = {"id": names[name], "name": name, "features": feats, "facts": facts}
    return cards


CARDS = build_cards()
FEATURE_ORDER = list(STATEMENTS)


def _lower_first(s):
    return s[:1].lower() + s[1:]


def describe(card):
    return f"**{card['name']}** – " + "; ".join(card["facts"]) + "."


def find_sports(text):
    """Спортове, наречени по име във въпроса (запазва реда, не бърка бокс с кик-бокс)."""
    found = []
    for sport_id, pattern in SPORT_PATTERNS:
        m = re.search(r"(?<!\w)(?:" + pattern + r")", text)
        if m and sport_id in CARDS:
            found.append((m.start(), sport_id))
            text = text[:m.start()] + " " * (m.end() - m.start()) + text[m.end():]
    return [s for _, s in sorted(found)]


def find_features(text):
    """Свойства във въпроса като {id: True/False}; „не/без/няма“ пред думата обръща значението."""
    feats = {}
    m = re.search(r"(?<!\w)((?:не\s+)?)само\s+(?:с\s+)?ръце", text)
    if m:
        feats["samorace"] = not m.group(1)
        text = text[:m.start()] + " " + text[m.end():]
    tokens = [t for t in re.findall(r"\w+", text) if len(t) > 1 or t == "а"]
    for i, tok in enumerate(tokens):
        for feat, prefixes in KEYWORDS.items():
            if any(tok.startswith(p) for p in prefixes):
                negated = False
                for prev in reversed(tokens[max(0, i - 3):i]):
                    if prev in BREAKERS:
                        break
                    if prev in NEGATIONS:
                        negated = True
                        break
                feats[feat] = not negated
    return feats


def compare(a, b):
    same, diff = [], []
    for f in FEATURE_ORDER:
        if f in a["features"] and f in b["features"]:
            sa = STATEMENTS[f][0 if a["features"][f] else 1]
            sb = STATEMENTS[f][0 if b["features"][f] else 1]
            if a["features"][f] == b["features"][f]:
                same.append(sa)
            else:
                diff.append(f"- {a['name']}: {sa}; {b['name']}: {sb}")
    text = f"Разлики между **{a['name']}** и **{b['name']}**:\n" + ("\n".join(diff) if diff else
           "- по мрежата няма свойство, по което се различават")
    if same:
        text += "\n\nОбщо: " + "; ".join(same) + "."
    return text


def answer(question):
    """Връща (отговор, карти, използвани като източник)."""
    q = question.lower().strip()
    names = find_sports(q)

    if len(names) >= 2:
        cards = [CARDS[n] for n in names]
        if re.search(r"разлик|различ|сравн|между|или", q) and len(cards) == 2:
            return compare(*cards), cards
        return "\n\n".join(describe(c) for c in cards), cards
    if len(names) == 1:
        return describe(CARDS[names[0]]), [CARDS[names[0]]]

    feats = find_features(q)
    if feats:
        matched = [c for c in CARDS.values() if all(c["features"].get(f) == v for f, v in feats.items())]
        cond = ", ".join(STATEMENTS[f][0 if v else 1] for f, v in feats.items())
        if not matched:
            return f"В мрежата няма спорт, за който да е известно, че: {cond}.", []
        if len(matched) == 1:
            return f"Според мрежата ({cond}) това е само:\n\n" + describe(matched[0]), matched
        names_list = ", ".join(c["name"] for c in matched)
        return f"Според мрежата ({cond}) това са:\n\n**{names_list}**", matched

    if re.search(r"всички|какви спортове|кои спортове|списък|какво знаеш", q):
        return "В мрежата са: **" + ", ".join(c["name"] for c in CARDS.values()) + "**.", list(CARDS.values())

    return ("Не намерих това в мрежата. Опитайте например: „Какво е волейбол?“, "
            "„Кои спортове имат мрежа?“ или „Каква е разликата между бокс и кик-бокс?“."), []