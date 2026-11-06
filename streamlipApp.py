from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

import rag
from icons import BOT_AVATAR, USER_AVATAR
from voice import listen

st.set_page_config(page_title="СпортБот")

css = (Path(__file__).parent / "style.css").read_text(encoding="utf-8")
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

GREETING = (
    "Здравей! Питай ме за даден спорт и ще се опитам да ти дам информация. Например:\n\n"
    "- Какво е волейбол?\n"
    "- Кои спортове имат мрежа?\n"
    "- Кои спортове са без топка и не са отборни?\n"
    "- Каква е разликата между бокс и кик-бокс?"
)


def ask(question):
    """Добавя въпроса и отговора. Всяко съобщение е (роля, текст, източници)."""
    text, cards = rag.answer(question)
    st.session_state.messages.append(("user", question, []))
    st.session_state.messages.append(("assistant", text, cards))


if "messages" not in st.session_state:
    st.session_state.messages = [("assistant", GREETING, [])]

st.title("СпортБот")
st.markdown('<div class="tagline">Питай ме за спортовете.</div>', unsafe_allow_html=True)

AVATARS = {"assistant": BOT_AVATAR, "user": USER_AVATAR}
for role, text, cards in st.session_state.messages:
    with st.chat_message(role, avatar=AVATARS[role]):
        st.markdown(text)
        if cards:
            st.caption("Източник в мрежата: " + ", ".join(c["name"] for c in cards))

# Гласово управление: казаното се третира като въпрос. Когато е изключено, микрофонът не се пуска.
st.toggle("Гласово управление", key="voice_on")
if st.session_state.voice_on:
    heard = listen()
    if heard and heard["id"] != st.session_state.get("last_voice_id"):
        st.session_state.last_voice_id = heard["id"]
        ask(heard["text"])
        st.rerun()

question = st.chat_input("Задай въпрос за спортовете…")
if question:
    ask(question)
    st.rerun()

# Скролване до най-долу след всяко ново съобщение.
st.markdown('<div id="end-anchor"></div>', unsafe_allow_html=True)
components.html(
    f"""<script>
    const n = {len(st.session_state.messages)};
    setTimeout(() => {{
      const a = window.parent.document.getElementById("end-anchor");
      if (a) a.scrollIntoView({{ behavior: "smooth", block: "end" }});
    }}, 250);
    </script>""",
    height=0,
)