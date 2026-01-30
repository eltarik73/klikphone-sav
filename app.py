# app.py
# ------------------------------------------------------------
# Klikphone • SAV — Single file Streamlit app (Premium UI)
# ------------------------------------------------------------

import sqlite3
from datetime import datetime
from contextlib import contextmanager

import pandas as pd
import streamlit as st

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Klikphone • SAV",
    page_icon="🧾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Premium CSS (UI-only)
# -----------------------------
PREMIUM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root{
  --bg: #0B0F17;
  --panel: #0F1624;
  --panel-2: #0C1220;
  --text: #EAF0FF;
  --muted: rgba(234,240,255,.70);
  --border: rgba(234,240,255,.10);

  --primary: #7C5CFF;
  --primary-2: #43C6FF;

  --radius: 16px;
  --radius-sm: 12px;

  --shadow-soft: 0 4px 10px rgba(0,0,0,.25);
}

html, body, [class*="css"]{
  font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, sans-serif !important;
}

.stApp{
  background: radial-gradient(1200px 800px at 10% 0%, rgba(124,92,255,.18), transparent 55%),
              radial-gradient(1000px 700px at 90% 10%, rgba(67,198,255,.12), transparent 50%),
              var(--bg);
  color: var(--text);
}

.block-container{
  padding-top: 1.25rem !important;
  padding-bottom: 2rem !important;
  max-width: 1320px;
}

/* remove Streamlit chrome */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
[data-testid="stToolbar"]{ display: none !important; }
[data-testid="stStatusWidget"]{ display: none !important; }
[data-testid="stDecoration"]{ display:none !important; }

/* sidebar */
section[data-testid="stSidebar"]{
  background: linear-gradient(180deg, rgba(255,255,255,.03), rgba(255,255,255,0)) !important;
  border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] > div{ padding-top: 1.0rem; }

.small-muted{ color: var(--muted); font-size: 0.95rem; }

/* cards */
.premium-card{
  background: linear-gradient(180deg, rgba(255,255,255,.04), rgba(255,255,255,.02));
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.0rem 1.05rem;
  box-shadow: var(--shadow-soft);
  margin-bottom: 1rem;
}
.premium-card--tight{ padding: .85rem .95rem; }
.premium-card__title{
  display:flex; align-items:center; justify-content:space-between;
  margin-bottom: .75rem;
}
.premium-card__title h3{
  margin:0; font-size: 1.05rem; font-weight: 700; letter-spacing: -0.01em;
}
.premium-divider{
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--border), transparent);
  margin: .75rem 0 1rem 0;
}

/* buttons */
.stButton>button{
  border-radius: 12px !important;
  border: 1px solid rgba(255,255,255,.12) !important;
  background: linear-gradient(135deg, rgba(124,92,255,1), rgba(67,198,255,.75)) !important;
  color: #06101A !important;
  font-weight: 800 !important;
  padding: .68rem 1rem !important;
  box-shadow: 0 8px 20px rgba(124,92,255,.18);
  transition: transform .08s ease, filter .2s ease;
}
.stButton>button:hover{ filter: brightness(1.06); }
.stButton>button:active{ transform: translateY(1px); }

.premium-secondary .stButton>button{
  background: rgba(255,255,255,.04) !important;
  color: var(--text) !important;
  border: 1px solid rgba(255,255,255,.14) !important;
  box-shadow: none;
}

/* inputs */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stDateInput"] input,
[data-testid="stSelectbox"] div[role="combobox"]{
  background: rgba(255,255,255,.03) !important;
  border: 1px solid rgba(255,255,255,.12) !important;
  border-radius: 12px !important;
  color: var(--text) !important;
}
[data-testid="stTextInput"] label,
[data-testid="stNumberInput"] label,
[data-testid="stTextArea"] label,
[data-testid="stDateInput"] label,
[data-testid="stSelectbox"] label{
  color: var(--muted) !important;
  font-weight: 650 !important;
}

/* metrics */
[data-testid="stMetric"]{
  background: rgba(255,255,255,.03);
  border: 1px solid rgba(255,255,255,.10);
  border-radius: 14px;
  padding: .85rem .9rem;
  box-shadow: 0 6px 14px rgba(0,0,0,.22);
}
[data-testid="stMetricLabel"]{ color: var(--muted) !important; font-weight: 650 !important; }
[data-testid="stMetricValue"]{ color: var(--text) !important; font-weight: 850 !important; }

/* tabs */
.stTabs [data-baseweb="tab-list"]{
  gap: .35rem;
  background: rgba(255,255,255,.02);
  border: 1px solid rgba(255,255,255,.08);
  padding: .35rem;
  border-radius: 14px;
}
.stTabs [data-baseweb="tab"]{
  border-radius: 12px !important;
  padding: .55rem .8rem !important;
  color: var(--muted) !important;
}
.stTabs [aria-selected="true"]{
  background: rgba(124,92,255,.18) !important;
  color: var(--text) !important;
}

/* dataframe */
[data-testid="stDataFrame"], [data-testid="stTable"]{
  border-radius: 14px;
  overflow: hidden;
  border: 1px solid rgba(255,255,255,.10);
  box-shadow: 0 8px 18px rgba(0,0,0,.22);
}

/* alerts */
.stAlert{
  border-radius: 14px !important;
  border: 1px solid rgba(255,255,255,.12) !important;
  background: rgba(255,255,255,.03) !important;
}
a{ color: rgba(67,198,255,.95); }
</style>
"""
st.markdown(PREMIUM_CSS, unsafe_allow_html=True)

# -----------------------------
# UI helpers (visual only)
# -----------------------------
def ui_section(title: str, subtitle: str | None = None):
    st.markdown(
        f"""
        <div class="premium-card premium-card--tight">
          <div class="premium-card__title">
            <h3>{title}</h3>
          </div>
          {f'<div class="small-muted">{subtitle}</div>' if subtitle else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )

@contextmanager
def ui_card(title: str | None = None, right: str | None = None, tight: bool = False):
    cls = "premium-card premium-card--tight" if tight else "premium-card"
    st.markdown(f'<div class="{cls}">', unsafe_allow_html=True)
    if title:
        st.markdown(
            f"""
            <div class="premium-card__title">
              <h3>{title}</h3>
              {f'<div class="small-muted">{right}</div>' if right else ''}
            </div>
            <div class="premium-divider"></div>
            """,
            unsafe_allow_html=True,
        )
    try:
        yield
    finally:
        st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# DB (SQLite)
# -----------------------------
DB_PATH = "sav.db"

def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_code TEXT UNIQUE,
            client_id INTEGER NOT NULL,
            device TEXT NOT NULL,
            imei_or_sn TEXT,
            issue TEXT,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY(client_id) REFERENCES clients(id)
        )
    """)
    conn.commit()
    conn.close()

init_db()

def now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def upsert_client(name: str, phone: str, email: str) -> int:
    """Retourne l'id client. Réutilise un client existant (phone+email) sinon crée."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT id FROM clients WHERE phone = ? AND email = ? LIMIT 1",
        (phone.strip(), email.strip().lower()),
    )
    row = cur.fetchone()
    if row:
        conn.close()
        return int(row["id"])

    cur.execute(
        "INSERT INTO clients (name, phone, email, created_at) VALUES (?, ?, ?, ?)",
        (name.strip(), phone.strip(), email.strip().lower(), now_iso()),
    )
    cid = cur.lastrowid
    conn.commit()
    conn.close()
    return int(cid)

def create_ticket(client_id: int, device: str, imei_or_sn: str | None, issue: str | None) -> str:
    """
    Génération ticket_code anti-bug :
    1) INSERT sans ticket_code
    2) id = lastrowid
    3) UPDATE ticket_code = KP26-000001
    """
    conn = get_conn()
    cur = conn.cursor()
    ts = now_iso()
    cur.execute(
        """
        INSERT INTO tickets (ticket_code, client_id, device, imei_or_sn, issue, status, created_at, updated_at)
        VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)
        """,
        (client_id, device.strip(), (imei_or_sn or "").strip() or None, (issue or "").strip() or None, "Reçu", ts, ts),
    )
    ticket_id = cur.lastrowid
    code = f"KP26-{ticket_id:06d}"
    cur.execute("UPDATE tickets SET ticket_code = ? WHERE id = ?", (code, ticket_id))
    conn.commit()
    conn.close()
    return code

def fetch_tickets(search: str | None = None) -> pd.DataFrame:
    conn = get_conn()
    q = """
    SELECT
      t.ticket_code,
      t.status,
      t.device,
      COALESCE(t.imei_or_sn, '') AS imei_or_sn,
      COALESCE(t.issue, '') AS issue,
      c.name AS client_name,
      c.phone AS client_phone,
      c.email AS client_email,
      t.created_at,
      t.updated_at
    FROM tickets t
    JOIN clients c ON c.id = t.client_id
    """
    params = ()
    if search and search.strip():
        s = f"%{search.strip()}%"
        q += """
        WHERE
          t.ticket_code LIKE ?
          OR c.name LIKE ?
          OR c.phone LIKE ?
          OR c.email LIKE ?
          OR t.device LIKE ?
          OR COALESCE(t.imei_or_sn,'') LIKE ?
        """
        params = (s, s, s, s, s, s)
    q += " ORDER BY t.id DESC"
    df = pd.read_sql_query(q, conn, params=params)
    conn.close()
    return df

def update_ticket_status(ticket_code: str, new_status: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "UPDATE tickets SET status = ?, updated_at = ? WHERE ticket_code = ?",
        (new_status, now_iso(), ticket_code.strip().upper()),
    )
    conn.commit()
    conn.close()

def get_ticket_for_client(ticket_code: str, phone_or_email: str) -> dict | None:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT
          t.ticket_code, t.status, t.device, COALESCE(t.imei_or_sn,'') AS imei_or_sn,
          COALESCE(t.issue,'') AS issue, t.created_at, t.updated_at,
          c.name AS client_name, c.phone AS client_phone, c.email AS client_email
        FROM tickets t
        JOIN clients c ON c.id = t.client_id
        WHERE t.ticket_code = ?
          AND (c.phone = ? OR c.email = ?)
        LIMIT 1
        """,
        (
            ticket_code.strip().upper(),
            phone_or_email.strip(),
            phone_or_email.strip().lower(),
        ),
    )
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

# -----------------------------
# Sidebar (nav)
# -----------------------------
st.sidebar.markdown("### Klikphone • SAV")
st.sidebar.markdown('<div class="small-muted">Interface premium — démo Streamlit</div>', unsafe_allow_html=True)

pages = {
    "Accueil (création ticket)": "accueil",
    "Staff (suivi + MAJ statut)": "staff",
    "Client (suivi réparation)": "client",
}
choice = st.sidebar.radio("Navigation", list(pages.keys()), index=0)
page = pages[choice]

# -----------------------------
# Header
# -----------------------------
ui_section("Klikphone • Gestion SAV", "Rapide • Fiable • Expérience client premium")

# -----------------------------
# Page: Accueil
# -----------------------------
if page == "accueil":
    cols = st.columns([1.2, 0.8])
    with cols[0]:
        with ui_card("Créer un ticket", right="Totem / Accueil"):
            st.markdown('<div class="small-muted">Champs obligatoires : nom, téléphone, email.</div>', unsafe_allow_html=True)

            name = st.text_input("Nom / Prénom *")
            phone = st.text_input("Téléphone *")
            email = st.text_input("Email *")

            st.markdown("<div class='premium-divider'></div>", unsafe_allow_html=True)

            device = st.text_input("Modèle / Appareil *", placeholder="Ex: iPhone 13 Pro Max")
            imei = st.text_input("IMEI / Numéro de série (optionnel)")
            issue = st.text_area("Panne / Demande (optionnel)", height=120)

            create_btn = st.button("Créer le ticket")

            if create_btn:
                if not name.strip() or not phone.strip() or not email.strip() or not device.strip():
                    st.error("Merci de compléter les champs obligatoires.")
                else:
                    cid = upsert_client(name, phone, email)
                    code = create_ticket(cid, device, imei, issue)
                    st.success(f"Ticket créé : **{code}**")
                    st.info("Copie ce code et donne-le au client pour le suivi.")

    with cols[1]:
        with ui_card("Aperçu du jour", right=datetime.now().strftime("%d/%m/%Y")):
            df = fetch_tickets()
            total = len(df)
            en_cours = int((df["status"] != "Prêt").sum()) if total else 0
            prets = int((df["status"] == "Prêt").sum()) if total else 0

            m1, m2, m3 = st.columns(3)
            m1.metric("Tickets", total)
            m2.metric("En cours", en_cours)
            m3.metric("Prêts", prets)

            st.markdown("<div class='premium-divider'></div>", unsafe_allow_html=True)
            st.markdown('<div class="small-muted">Astuce : la page Staff permet de modifier le statut.</div>', unsafe_allow_html=True)

# -----------------------------
# Page: Staff
# -----------------------------
elif page == "staff":
    with ui_card("Suivi / Recherche", right="Backoffice"):
        search = st.text_input("Rechercher (ticket, nom, tel, email, modèle, IMEI/SN)", placeholder="Ex: KP26-000012 ou 0612345678")
        df = fetch_tickets(search)

        st.dataframe(df, use_container_width=True, hide_index=True)

    with ui_card("Mise à jour statut", right="Sans changer la logique"):
        left, right = st.columns([0.9, 1.1])

        with left:
            ticket_code = st.text_input("Ticket code", placeholder="Ex: KP26-000012").strip().upper()
            status = st.selectbox(
                "Nouveau statut",
                ["Reçu", "Diagnostic", "En réparation", "En attente pièce", "Prêt", "Restitué"],
                index=0,
            )

            st.markdown('<div class="premium-secondary">', unsafe_allow_html=True)
            apply_btn = st.button("Appliquer statut")
            st.markdown("</div>", unsafe_allow_html=True)

            if apply_btn:
                if not ticket_code:
                    st.error("Entre un ticket code.")
                else:
                    update_ticket_status(ticket_code, status)
                    st.success(f"Statut mis à jour : **{ticket_code} → {status}**")

        with right:
            st.markdown("#### Bonnes pratiques")
            st.markdown(
                """
- Utilise **“En attente pièce”** quand tu bloques sur un fournisseur.
- Passe à **“Prêt”** quand le téléphone est OK et que le client peut venir.
- **“Restitué”** quand le client a récupéré l’appareil.
                """,
            )

# -----------------------------
# Page: Client
# -----------------------------
elif page == "client":
    cols = st.columns([1, 1])
    with cols[0]:
        with ui_card("Suivre ma réparation", right="Portail client"):
            ticket_code = st.text_input("Mon code ticket", placeholder="Ex: KP26-000012").strip().upper()
            auth = st.text_input("Mon téléphone OU mon email", placeholder="Ex: 0612345678 ou client@mail.com")

            btn = st.button("Afficher le statut")

            if btn:
                if not ticket_code or not auth.strip():
                    st.error("Merci de saisir le code ticket + téléphone ou email.")
                else:
                    t = get_ticket_for_client(ticket_code, auth)
                    if not t:
                        st.error("Ticket introuvable ou informations de vérification incorrectes.")
                    else:
                        st.success(f"Ticket : **{t['ticket_code']}**")
                        st.markdown("<div class='premium-divider'></div>", unsafe_allow_html=True)

                        m1, m2, m3 = st.columns(3)
                        m1.metric("Statut", t["status"])
                        m2.metric("Créé le", t["created_at"])
                        m3.metric("Mis à jour", t["updated_at"])

                        st.markdown("<div class='premium-divider'></div>", unsafe_allow_html=True)
                        st.markdown(f"**Appareil :** {t['device']}")
                        if t["imei_or_sn"]:
                            st.markdown(f"**IMEI/SN :** {t['imei_or_sn']}")
                        if t["issue"]:
                            st.markdown(f"**Demande :** {t['issue']}")

    with cols[1]:
        with ui_card("Informations", right="Conseils"):
            st.markdown(
                """
<div class="small-muted">
Ce portail affiche uniquement l’état du ticket.  
Pour toute question, contactez la boutique.
</div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown("<div class='premium-divider'></div>", unsafe_allow_html=True)
            st.markdown("**Statuts possibles :**")
            st.markdown(
                """
- Reçu  
- Diagnostic  
- En réparation  
- En attente pièce  
- Prêt  
- Restitué
                """
            )

# -----------------------------
# Footer (soft)
# -----------------------------
st.markdown(
    """
<div class="small-muted" style="text-align:center; padding: 1rem 0;">
  Klikphone • SAV — Demo Streamlit (UI Premium)
</div>
""",
    unsafe_allow_html=True,
)
