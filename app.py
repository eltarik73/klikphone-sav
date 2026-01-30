import streamlit as st

# -----------------------------
# PREVIEW HOME — UI/UX PREMIUM
# -----------------------------

st.set_page_config(page_title="Klik Tickets — Preview Home", page_icon="🟠", layout="wide")

st.markdown("""
<style>
/* ---- Premium Light tokens ---- */
:root{
  --bg:#F6F7FB;
  --card:#FFFFFF;
  --text:#0F172A;
  --muted:#667085;
  --border:#E6E8F0;
  --shadow: 0 10px 25px rgba(16,24,40,.08);
  --shadow2: 0 6px 18px rgba(16,24,40,.10);
  --accent:#FF6A00;
  --accent2:#FF7A1A;
  --radius:18px;
}

/* Background + spacing */
.stApp{
  background: var(--bg);
}

/* Hide Streamlit chrome for a "custom app" feel */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Layout container */
.home-wrap{max-width:1100px;margin:0 auto;padding:12px 0 0 0;}
.home-head{display:flex;align-items:flex-end;justify-content:space-between;margin:8px 0 18px 0;}
.home-title{font-size:30px;font-weight:900;letter-spacing:-0.03em;color:var(--text);line-height:1.05}
.home-sub{color:var(--muted);margin-top:6px;font-size:13.5px}
.home-pill{
  display:inline-flex;align-items:center;gap:8px;
  padding:8px 12px;border:1px solid var(--border);border-radius:999px;
  background:rgba(255,255,255,.72);backdrop-filter: blur(8px);
  color:#344054;font-weight:800;font-size:12px;
}

/* Grid */
.home-grid{display:grid;grid-template-columns: repeat(3, 1fr);gap:16px;}
@media (max-width: 900px){ .home-grid{grid-template-columns:1fr;} }

/* Card shell (Streamlit button becomes the card) */
.home-card .stButton>button{
  width:100%;
  min-height:150px;
  border-radius:var(--radius) !important;
  border:1px solid var(--border) !important;
  background: linear-gradient(180deg, #FFFFFF 0%, #FBFCFF 100%) !important;
  box-shadow: var(--shadow) !important;
  text-align:left !important;
  padding:18px 18px 16px 18px !important;
  transition: transform .12s ease, box-shadow .12s ease, border-color .12s ease, background .12s ease;
  white-space: normal !important;
  line-height: 1.25 !important;
}
.home-card .stButton>button:hover{
  transform: translateY(-2px);
  box-shadow: var(--shadow2) !important;
  border-color:#D9DCE8 !important;
}
.home-card .stButton>button:active{
  transform: translateY(0px);
}

/* Inner content rendered as HTML above each button */
.home-meta{display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;}
.home-tag{
  display:inline-flex;align-items:center;
  padding:6px 10px;border-radius:999px;
  background: rgba(255,106,0,.10);
  color: #B54708;
  font-weight:900;font-size:12px;
  border:1px solid rgba(255,106,0,.18);
}
.home-icon{
  width:44px;height:44px;border-radius:14px;
  display:flex;align-items:center;justify-content:center;
  background: linear-gradient(180deg, rgba(255,106,0,.18), rgba(255,122,26,.10));
  border:1px solid rgba(255,106,0,.22);
  font-size:20px;
}
.home-h{font-size:19px;font-weight:950;color:var(--text);margin:0 0 3px 0;letter-spacing:-.015em;}
.home-p{font-size:13.2px;color:var(--muted);margin:0;}

/* Small section cards below */
.quick-wrap{max-width:1100px;margin:18px auto 0 auto;}
.quick-card{
  border:1px solid var(--border);
  background: var(--card);
  border-radius: var(--radius);
  box-shadow: 0 6px 16px rgba(16,24,40,.06);
  padding:14px 16px;
}
.quick-title{font-weight:900;color:var(--text);letter-spacing:-.01em;margin-bottom:6px}
.quick-row{display:flex;gap:10px;flex-wrap:wrap}
.pill{
  display:inline-flex;align-items:center;gap:8px;
  padding:9px 12px;border-radius:999px;
  border:1px solid var(--border);
  background:#fff;
  font-weight:800;color:#344054;font-size:12px;
}
.pill:hover{border-color:#D9DCE8}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="home-wrap">
  <div class="home-head">
    <div>
      <div class="home-title">Klik Tickets</div>
      <div class="home-sub">Choisissez votre espace</div>
    </div>
    <div class="home-pill">🟠 Mode boutique • accès rapide</div>
  </div>
</div>
""", unsafe_allow_html=True)

# --- GRID of 3 big cards ---
st.markdown('<div class="home-wrap"><div class="home-grid">', unsafe_allow_html=True)

# CLIENT card (visual + button)
st.markdown("""
<div class="home-card">
  <div class="home-meta">
    <div class="home-icon">👤</div>
    <div class="home-tag">Totem / iPad</div>
  </div>
  <div class="home-h">Espace Client</div>
  <div class="home-p">Créer un ticket en 30 secondes • QR optionnel</div>
</div>
""", unsafe_allow_html=True)
if st.button("Ouvrir Client", key="home_client"):
    st.toast("Preview : ouverture Espace Client", icon="👤")

# ACCUEIL card
st.markdown("""
<div class="home-card">
  <div class="home-meta">
    <div class="home-icon">🏪</div>
    <div class="home-tag">Comptoir</div>
  </div>
  <div class="home-h">Accueil</div>
  <div class="home-p">Recherche • devis • encaissement • suivi</div>
</div>
""", unsafe_allow_html=True)
if st.button("Ouvrir Accueil", key="home_accueil"):
    st.toast("Preview : ouverture Accueil", icon="🏪")

# TECH card
st.markdown("""
<div class="home-card">
  <div class="home-meta">
    <div class="home-icon">🛠️</div>
    <div class="home-tag">Atelier</div>
  </div>
  <div class="home-h">Technicien</div>
  <div class="home-p">Diagnostic • pièces • statuts • notes internes</div>
</div>
""", unsafe_allow_html=True)
if st.button("Ouvrir Technicien", key="home_tech"):
    st.toast("Preview : ouverture Technicien", icon="🛠️")

st.markdown('</div></div>', unsafe_allow_html=True)

# --- Optional "quick actions" strip (purely visual) ---
st.markdown("""
<div class="quick-wrap">
  <div class="quick-card">
    <div class="quick-title">Raccourcis</div>
    <div class="quick-row">
      <div class="pill">➕ Nouveau ticket</div>
      <div class="pill">🔎 Rechercher</div>
      <div class="pill">🧾 Devis</div>
      <div class="pill">📦 Pièces</div>
      <div class="pill">🖨️ Impression</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

st.info("Ceci est une preview (UI uniquement). Pour l’intégrer dans ton app, on remplace la page d’accueil actuelle par ce bloc et on garde ta logique de navigation.", icon="ℹ️")
