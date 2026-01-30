import streamlit as st

# --------------------------------------------
# HOME PREMIUM — 3 BIG BLOCKS + SUIVI + FOOTER
# (preview / intégrable dans ton app)
# --------------------------------------------
st.set_page_config(page_title="Klik Tickets — Home", page_icon="🟠", layout="wide")

# Simule un clic (cartes cliquables)
role = st.query_params.get("role", None)
if role:
    label = {
        "client": "Espace Client",
        "accueil": "Accueil",
        "tech": "Technicien",
        "suivi": "Suivi de réparation",
    }.get(role, "Page")
    st.toast(f"Ouverture : {label}", icon="✅")
    # Reset pour pouvoir recliquer facilement
    st.query_params.clear()

st.markdown(r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

:root{
  --bg0:#060A12;
  --bg1:#0B1220;
  --panel:#0F1A2E;
  --panel2:#0B1426;
  --text:#ECF2FF;
  --muted:rgba(236,242,255,.74);
  --muted2:rgba(236,242,255,.58);
  --border:rgba(255,255,255,.10);
  --border2:rgba(255,255,255,.14);
  --shadow: 0 18px 60px rgba(0,0,0,.42);
  --shadow2: 0 26px 86px rgba(0,0,0,.60);
  --accent:#FF6A00;
  --accent2:#FF8A3D;
  --radius:24px;
}

html, body, [class*="css"]{
  font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
}

/* Background */
.stApp{
  background:
    radial-gradient(1100px 700px at 14% -10%, rgba(255,106,0,.22), transparent 62%),
    radial-gradient(900px 600px at 85% 0%, rgba(114,255,230,.13), transparent 58%),
    radial-gradient(900px 900px at 60% 90%, rgba(45,140,255,.10), transparent 62%),
    linear-gradient(180deg, var(--bg1), var(--bg0) 78%);
}

/* Hide Streamlit chrome */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Layout container */
.wrap{max-width:1180px;margin:0 auto;padding:20px 0 0 0;}
.top{display:flex;align-items:flex-end;justify-content:space-between;gap:16px;margin:6px 0 18px 0;}
.title{font-size:36px;font-weight:950;letter-spacing:-0.05em;line-height:1.02;color:var(--text);}
.sub{color:var(--muted);font-size:13.8px;margin-top:7px;}
.pill{
  display:inline-flex;align-items:center;gap:10px;
  padding:10px 13px;border-radius:999px;
  border:1px solid var(--border);
  background: rgba(255,255,255,.045);
  color: rgba(236,242,255,.84);
  font-weight:850;font-size:12px;
  backdrop-filter: blur(10px);
}

/* Grid */
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;}
@media (max-width: 980px){ .grid{grid-template-columns:1fr;} }

/* Card (fully clickable) */
.card{
  position:relative; display:block; text-decoration:none; color:inherit;
  min-height:205px;
  border-radius:var(--radius);
  background: linear-gradient(180deg, rgba(255,255,255,.07), rgba(255,255,255,.03));
  border: 1px solid var(--border);
  box-shadow: var(--shadow);
  overflow:hidden;
  transform: translateY(0);
  transition: transform .14s ease, box-shadow .14s ease, border-color .14s ease, filter .14s ease;
}
.card:hover{
  transform: translateY(-3px);
  box-shadow: var(--shadow2);
  border-color: var(--border2);
  filter: saturate(1.05);
}

/* Accent ring (subtle) */
.card::before{
  content:"";
  position:absolute; inset:-2px;
  background:
    radial-gradient(520px 260px at 18% 0%, rgba(255,106,0,.38), transparent 62%),
    radial-gradient(520px 260px at 82% 22%, rgba(255,138,61,.20), transparent 62%);
  opacity:.62;
  pointer-events:none;
}

/* Inner panel */
.card::after{
  content:"";
  position:absolute; inset:1px;
  border-radius:calc(var(--radius) - 1px);
  background: linear-gradient(180deg, rgba(15,26,46,.96), rgba(8,14,28,.94));
  pointer-events:none;
}

.inner{position:relative; z-index:2; padding:18px 18px 16px 18px; height:100%;
  display:flex; flex-direction:column; justify-content:space-between; gap:10px;}

.meta{display:flex;align-items:flex-start;justify-content:space-between;gap:12px;}
.tag{
  display:inline-flex;align-items:center;gap:8px;
  padding:8px 11px;border-radius:999px;
  border:1px solid rgba(255,255,255,.12);
  background: rgba(255,255,255,.05);
  color: rgba(236,242,255,.86);
  font-size:12px;font-weight:900;
}
.icon{
  width:48px;height:48px;border-radius:16px;
  display:flex;align-items:center;justify-content:center;
  background:
    radial-gradient(90px 90px at 30% 20%, rgba(255,106,0,.40), rgba(255,255,255,.06));
  border:1px solid rgba(255,255,255,.14);
  box-shadow: 0 10px 34px rgba(0,0,0,.28);
}

/* SVG icons */
.icon svg{width:22px;height:22px;opacity:.95;fill:rgba(236,242,255,.92);}

.h{font-size:20.5px;font-weight:950;letter-spacing:-0.02em;color:var(--text);margin:0;}
.p{margin:0;color:var(--muted2);font-size:13.5px;line-height:1.38;}

/* CTA row */
.cta{display:flex;align-items:center;justify-content:space-between;margin-top:4px;}
.go{display:inline-flex;align-items:center;gap:10px;color:rgba(236,242,255,.92);font-weight:950;font-size:13px;letter-spacing:.01em;}
.dot{width:10px;height:10px;border-radius:999px;background:linear-gradient(180deg,var(--accent),var(--accent2));
  box-shadow: 0 12px 28px rgba(255,106,0,.22);}
.arrow{
  width:30px;height:30px;border-radius:12px;
  border:1px solid rgba(255,255,255,.12);
  background: rgba(255,255,255,.06);
  display:flex;align-items:center;justify-content:center;
  color: rgba(236,242,255,.92);
  font-weight:950;
}

/* Full-width card (suivi) */
.full{grid-column: 1 / -1; min-height:170px;}
.full .inner{padding:18px 20px 16px 20px;}
.full .icon{width:52px;height:52px;border-radius:18px;}
.full .h{font-size:19.5px;}

/* Footer */
.footer{
  margin: 18px 0 10px 0;
  text-align:center;
  color: rgba(236,242,255,.55);
  font-size: 12px;
  font-weight: 800;
  letter-spacing: .02em;
}
</style>
""", unsafe_allow_html=True)

# Inline SVG icons (clean, no emoji dependency)
ICON_CLIENT = """
<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 12a4.2 4.2 0 1 0-4.2-4.2A4.2 4.2 0 0 0 12 12Zm0 2.2c-4.23 0-7.8 2.06-7.8 4.6A2 2 0 0 0 6.1 21h11.8a2 2 0 0 0 1.9-2.2c0-2.54-3.57-4.6-7.8-4.6Z"/></svg>
"""
ICON_STORE = """
<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21 7.5 19.6 4.6A2 2 0 0 0 17.8 3.5H6.2A2 2 0 0 0 4.4 4.6L3 7.5v1.2A3 3 0 0 0 6 11.7a3.2 3.2 0 0 0 2.5-1.2A3.2 3.2 0 0 0 11 11.7a3.2 3.2 0 0 0 2.5-1.2A3.2 3.2 0 0 0 16 11.7a3 3 0 0 0 3-3V7.5Zm-2 6.3V20.5H5V13.8a4.8 4.8 0 0 0 1 .1 5.1 5.1 0 0 0 3-1 5.4 5.4 0 0 0 6 0 5.1 5.1 0 0 0 3 1 4.8 4.8 0 0 0 1-.1Z"/></svg>
"""
ICON_TOOLS = """
<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21.1 7.9a6.1 6.1 0 0 1-7.8 7.8l-6.1 6.1a1.7 1.7 0 0 1-2.4-2.4l6.1-6.1A6.1 6.1 0 0 1 16.1 3a4.7 4.7 0 0 0-1.2 4l-2.2 2.2 2.1 2.1 2.2-2.2a4.7 4.7 0 0 0 4.1-1.2Z"/></svg>
"""
ICON_QR = """
<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 3h8v8H3V3Zm2.2 2.2v3.6h3.6V5.2H5.2ZM13 3h8v8h-8V3Zm2.2 2.2v3.6h3.6V5.2h-3.6ZM3 13h8v8H3v-8Zm2.2 2.2v3.6h3.6v-3.6H5.2ZM13 13h2.4v2.4H13V13Zm3.6 0H21v4.8h-2.4v-2.4h-2V13Zm-3.6 3.6h4.8V21H13v-4.4Zm6.8 1.2H21V21h-2.2v-3.2Z"/></svg>
"""

st.markdown(f"""
<div class="wrap">
  <div class="top">
    <div>
      <div class="title">Klik Tickets</div>
      <div class="sub">Choisissez votre espace — interface boutique premium</div>
    </div>
    <div class="pill">🟠 Accès rapide • Home</div>
  </div>

  <div class="grid">
    <a class="card" href="?role=client">
      <div class="inner">
        <div class="meta">
          <div class="icon">{ICON_CLIENT}</div>
          <div class="tag">Totem / iPad</div>
        </div>
        <div>
          <p class="h">Espace Client</p>
          <p class="p">Création de ticket simple, rapide et guidée.</p>
        </div>
        <div class="cta">
          <div class="go"><span class="dot"></span> Ouvrir</div>
          <div class="arrow">→</div>
        </div>
      </div>
    </a>

    <a class="card" href="?role=accueil">
      <div class="inner">
        <div class="meta">
          <div class="icon">{ICON_STORE}</div>
          <div class="tag">Comptoir</div>
        </div>
        <div>
          <p class="h">Accueil</p>
          <p class="p">Recherche, devis, encaissement et suivi des tickets.</p>
        </div>
        <div class="cta">
          <div class="go"><span class="dot"></span> Ouvrir</div>
          <div class="arrow">→</div>
        </div>
      </div>
    </a>

    <a class="card" href="?role=tech">
      <div class="inner">
        <div class="meta">
          <div class="icon">{ICON_TOOLS}</div>
          <div class="tag">Atelier</div>
        </div>
        <div>
          <p class="h">Technicien</p>
          <p class="p">Diagnostic, pièces, statuts, notes internes.</p>
        </div>
        <div class="cta">
          <div class="go"><span class="dot"></span> Ouvrir</div>
          <div class="arrow">→</div>
        </div>
      </div>
    </a>

    <a class="card full" href="?role=suivi">
      <div class="inner">
        <div class="meta">
          <div class="icon">{ICON_QR}</div>
          <div class="tag">Suivi / QR</div>
        </div>
        <div>
          <p class="h">Suivi de réparation</p>
          <p class="p">Consulter l’avancement d’un ticket (code / QR) : statut, diagnostic, et dernières notes.</p>
        </div>
        <div class="cta">
          <div class="go"><span class="dot"></span> Ouvrir</div>
          <div class="arrow">→</div>
        </div>
      </div>
    </a>
  </div>

  <div class="footer">klikphone révolution project by TKconcept26</div>
</div>
""", unsafe_allow_html=True)
