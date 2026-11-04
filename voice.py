from pathlib import Path

import streamlit.components.v1 as components

HTML = r"""<!doctype html>
<html lang="bg">
<head>
<meta charset="utf-8">
<style>
  body { margin: 0; font-family: system-ui, sans-serif; }
  #pill { display: inline-flex; align-items: center; gap: 10px; padding: 8px 16px;
          border-radius: 999px; background: #141c33; color: #e9edf7; font-size: 14px;
          border: 1px solid #26324f; }
  #dot { width: 10px; height: 10px; border-radius: 50%; background: #6b7390; }
  .on #dot { background: #e2b76f; animation: pulse 1.2s infinite; }
  .err #dot { background: #d9534f; }
  @keyframes pulse { 0%,100% { opacity: .35; } 50% { opacity: 1; } }
</style>
</head>
<body>
<div id="pill"><span id="dot"></span><span id="msg">Стартирам микрофона…</span></div>
<script>
  // Минимален Streamlit компонент без допълнителни библиотеки.
  function send(type, data) {
    window.parent.postMessage(Object.assign({ isStreamlitMessage: true, type: type }, data), "*");
  }
  function setValue(v) { send("streamlit:setComponentValue", { value: v, dataType: "json" }); }

  const pill = document.getElementById("pill");
  const msg = document.getElementById("msg");
  function status(text, cls) { msg.textContent = text; pill.className = cls || ""; }

  send("streamlit:componentReady", { apiVersion: 1 });
  send("streamlit:setFrameHeight", { height: 48 });

  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SR) {
    status("Този браузър не поддържа гласово разпознаване (ползвайте Chrome или Edge)", "err");
  } else {
    let want = true;
    const rec = new SR();
    rec.lang = "bg-BG";
    rec.continuous = true;
    rec.interimResults = false;

    rec.onstart = () => status("Слушам… кажи „да“ или „не“", "on");
    rec.onresult = (e) => {
      const res = e.results[e.results.length - 1];
      if (res.isFinal) {
        const text = res[0].transcript.trim();
        if (text) setValue({ text: text, id: Date.now() + "-" + Math.random() });
      }
    };
    rec.onerror = (e) => {
      if (e.error === "not-allowed" || e.error === "service-not-allowed") {
        want = false;
        status("Разрешете микрофона в браузъра и презаредете страницата", "err");
      }
    };
    rec.onend = () => { if (want) setTimeout(() => { try { rec.start(); } catch (_) {} }, 300); };

    try { rec.start(); } catch (_) {}
  }
</script>
</body>
</html>
"""

_DIR = Path(__file__).parent / "voice_ui"
_DIR.mkdir(exist_ok=True)
_FILE = _DIR / "index.html"
if not _FILE.exists() or _FILE.read_text(encoding="utf-8") != HTML:
    _FILE.write_text(HTML, encoding="utf-8")

_component = components.declare_component("voice_listener", path=str(_DIR))


def listen(key="voice"):
    """Слуша постоянно. Връща {"text": ..., "id": ...} за последното чуто изказване или None."""
    return _component(key=key, default=None)