import re

from tree import TREE, ROOT

YES_WORDS = {"да", "д", "ага", "yes", "y"}
NO_WORDS = {"не", "н", "no", "n"}

GREETING = ("Здравей! Аз съм СпортБот. Помисли си някакъв спорт, "
            "а аз ще го позная. Отговаряй с „Да“ или „Не“.")
PLAY_AGAIN = "Искаш ли да играем пак? Натисни „Нова игра“."
NOT_UNDERSTOOD = "Не те разбрах. Моля, отговори с „Да“ или „Не“."


def parse_answer(text):
    """Връща 'yes', 'no' или None, ако текстът не е ясен отговор.

    Работи по думи, за да се справя и с гласово разпознаване: „Да.“, „да, да“, „не знам“.
    Ако има и „да“, и „не“ едновременно, отговорът е неясен.
    """
    words = set(re.findall(r"\w+", text.lower()))
    yes = bool(words & YES_WORDS)
    no = bool(words & NO_WORDS)
    if yes and not no:
        return "yes"
    if no and not yes:
        return "no"
    return None


def start():
    """Начало на игра: (id на текущия въпрос, съобщения на бота)."""
    return ROOT, [GREETING, TREE[ROOT]["q"]]


def step(current, choice):
    """Един ход. Връща (нов id на въпрос или None при край, съобщения на бота)."""
    nxt = TREE[current][choice]
    leaf = TREE[nxt]
    if "q" in leaf:
        return nxt, [leaf["q"]]
    text = f"Това е **{leaf['answer']}**!" if leaf["found"] else leaf["answer"]
    return None, [text, PLAY_AGAIN]


def broken_links():
    """Проверка на дървото: връзки към несъществуващи възли."""
    return [(k, c) for k, v in TREE.items() if "q" in v
            for c in (v["yes"], v["no"]) if c not in TREE]