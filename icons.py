import base64

BOT_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
<defs>
  <linearGradient id="goldBot" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#f4d59a"/>
    <stop offset="100%" stop-color="#bd873e"/>
  </linearGradient>
  <linearGradient id="faceBot" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#292b30"/>
    <stop offset="100%" stop-color="#111318"/>
  </linearGradient>
</defs>
<circle cx="32" cy="32" r="30" fill="#17191e" stroke="url(#goldBot)" stroke-width="1.5"/>
<path d="M32 8 V17" stroke="url(#goldBot)" stroke-width="2.5" stroke-linecap="round"/>
<circle cx="32" cy="7" r="3" fill="url(#goldBot)"/>
<rect x="15" y="19" width="34" height="29" rx="9" fill="url(#faceBot)" stroke="#e2b76f" stroke-width="1.5"/>
<path d="M15 27 H11 V39 H15 M49 27 H53 V39 H49" fill="none" stroke="url(#goldBot)" stroke-width="2.5" stroke-linejoin="round"/>
<rect x="21" y="29" width="7" height="5" rx="2.5" fill="#e9c17c"/>
<rect x="36" y="29" width="7" height="5" rx="2.5" fill="#e9c17c"/>
<path d="M25 40 Q32 44 39 40" fill="none" stroke="#d6a85f" stroke-width="1.8" stroke-linecap="round"/>
<path d="M23 49 L19 55 M41 49 L45 55" stroke="url(#goldBot)" stroke-width="2.5" stroke-linecap="round"/>
<path d="M25 49 H39" stroke="#e2b76f" stroke-width="2" stroke-linecap="round"/>
</svg>"""

USER_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
<defs>
  <linearGradient id="goldUser" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#f4d59a"/>
    <stop offset="100%" stop-color="#bd873e"/>
  </linearGradient>
</defs>
<circle cx="32" cy="32" r="30" fill="#17191e" stroke="url(#goldUser)" stroke-width="1.5"/>
<circle cx="32" cy="24" r="9" fill="#eee9df"/>
<path d="M13 51 C14 40 21 35 32 35 C43 35 50 40 51 51 Q32 64 13 51Z" fill="#eee9df"/>
<path d="M19 53 Q32 59 45 53" fill="none" stroke="#d6a85f" stroke-width="1" opacity=".7"/>
</svg>"""


def svg_uri(svg):
    """Превръща SVG код в адрес, който Streamlit приема за аватар."""
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode("utf-8")).decode("ascii")


BOT_AVATAR = svg_uri(BOT_SVG)
USER_AVATAR = svg_uri(USER_SVG)