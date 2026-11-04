from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

import engine
from icons import BOT_AVATAR, USER_AVATAR
from voice import listen

st.set_page_config(page_title="СпортБот")

# Външният вид е в отделния файл style.css
css = (Path(__file__).parent / "style.css").read_text(encoding="utf-8")
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def say(role, *texts):
    for t in texts:
        st.session_state.messages.append((role, t))


def reset():
    st.session_state.messages = []
    current, bot = engine.start()
    st.session_state.current = current
    say("assistant", *bot)


def answer(choice, label=None):
    say("user", label or ("Да" if choice == "yes" else "Не"))
    current, bot = engine.step(st.session_state.current, choice)
    st.session_state.current = current
    say("assistant", *bot)


def handle_typed(text):
    choice = engine.parse_answer(text)
    if choice:
        answer(choice, text)
    else:
        say("user", text)
        say("assistant", engine.NOT_UNDERSTOOD)


if "messages" not in st.session_state:
    reset()

st.title("Спортбот")
st.markdown('<div class="tagline">Намисли си спорт – аз ще го позная.</div>', unsafe_allow_html=True)

AVATARS = {"assistant": BOT_AVATAR, "user": USER_AVATAR}
for role, text in st.session_state.messages:
    with st.chat_message(role, avatar=AVATARS[role]):
        st.markdown(text)

if st.session_state.current:
    voice_on = st.toggle("Гласово управление", key="voice_on")
    if voice_on:
        heard = listen()
        if heard and heard["id"] != st.session_state.get("last_voice_id"):
            st.session_state.last_voice_id = heard["id"]
            choice = engine.parse_answer(heard["text"])
            if choice:
                answer(choice, heard["text"])
                st.rerun()

    typed = st.chat_input("Кажете или напишете „да“ или „не“")
    if typed:
        handle_typed(typed)
        st.rerun()
else:
    st.button("Нова игра", on_click=reset)