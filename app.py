#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KLIKPHONE SAV - Design inspiré du portail officiel
Couleurs orange, style moderne Tailwind
"""

import streamlit as st
import sqlite3
from datetime import datetime
import urllib.parse

# =============================================================================
# CONFIG
# =============================================================================
st.set_page_config(
    page_title="Klikphone SAV",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

DB_PATH = "klikphone_sav.db"

# Logo Klikphone en base64
LOGO_B64 = "iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAMAAABHPGVmAAAAIGNIUk0AAHomAACAhAAA+gAAAIDoAAB1MAAA6mAAADqYAAAXcJy6UTwAAAIEUExURf9mAP5mAP9nAv1eAPzTuP////76+PzNrv5dAP9lAP5nAf9kAf1iBPzTt/79/P7+/v39/crKyv1oBvzp3f78+/zk1f1lAf1hA/zMq/7////9/MvLy5OTk/9hAPx5I/37+v7+/f349Px1HP9iAP5mAfvOrv/+/pKSkpqamv5nA/9dAPyRS//9/fyLQf9eAP5nAvvNrv78+pubm/5lAP9oBP5bAPusef/8+/umbv9oA5mZmf5cAPzIqPzCnf1kAPzi0fzcyP1hAPxyGP328f3y6v1uEf9jAPyHO//+/f3///yBMv9fAP5oA/9bAPulbf/8+vyfYvuNRP36+PyIPP9oAv5aAPuPSv3+/v38+/uJQf9pBP1ZAPvIqPvCnv5YAP9cAPueZP/6+PuYWfyORvyIO/yCMvyHOvyBMPzOrv1iA/9kAP1iAvvNrfvAmf7+//ubX/yCMfxtE/zt4vyBMf9gAPuqd/uWVv/7+fyPTP1lAvzj0v79/f1bAPvNsP77+PvHpv///v5ZAPuVVfuQTPuhZf5fAPuEOPzz7PuAMP9pBvy4i9XV1ZGRkf1xFPzv5vzr3/xtDvzDnqysrJaWlv14Iv77+f339Px0G/39/Px9KfyUT/uORfyUUP/9+/uORvzi0v5qBv5oBPxtEvubXvvAmP9lAf1hAvvMrPzNrfvLq/1hBPzTtv0V+7gAAAABYktHRAX4b+nHAAAACXBIWXMAAABIAAAASABGyWs+AAAAB3RJTUUH6gEcAQUILspFkwAAAHd0RVh0UmF3IHByb2ZpbGUgdHlwZSA4YmltAAo4YmltCiAgICAgIDQwCjM4NDI0OTRkMDQwNDAwMDAwMDAwMDAwMDM4NDI0OTRkMDQyNTAwMDAwMDAwMDAxMGQ0MWQ4Y2Q5OGYwMGIyMDRlOTgwMDk5OAplY2Y4NDI3ZQqmU8OOAAADkklEQVRo3rXa+VPTQBQH8Ka6QqoS1HosiIJgEdTGUivWeqMVbBAV8MCjKuKBqIh4IN73fd/3ff6TblNmbJ3J5r23If01mU+/+zabvMz6fM6H5h8xko1iBYV+zQc+9MDoMWNZkcHsw2BGMRsnO1/Tx09gQTZxkg5HhDF5Ci/JNUqnyi4IlE2bzspZxYzKKowxkwd5KCdH9SzZFTW1s8V/msPnhk1glIwxj0d4KJRj1MmQ6PzYAl5v1POFsTgMcTAWyUoSTyxmwVCQLQEiToYsieZbuowVid/yFT4I4mjIkKrKlQ2i7uVs1eokoPLOhgwxw2t4ozg51LQ2ZaoYEkSzmtfxFnF6C1/fbKkYMsRMbdgochisotU1idSQTuG29k2bRUm2bI21Rd2NAkdDejNGO7ZtF2vXjp0dAMM5hxzRrfQuvpvvSVtqhhQR60onr+etYVPNkCNmeC8v4V3ysrsbbsg+3ti0X4pkjANyQxmBGKqIMA66GooIKIciYhvM1VBCss9ad0MFARsKCNygIwiDjGAMKgKcu0oIKgcRydznCIOEYA0KgjYICLIeJMTOAVivVBD8WOERwlihEZqBQyj1wCKkeiAR4lihED3QTcuBQHRNP9RDM+CI5i88zCNHKAYYicYTR3mLQTIgSK9AtKrksT7Rq5AMFySVQY73myJI7IR4wacZbv3JSX6Kn661RNUHzrBBoiHvtOJnz7Hz7EJ7R9RMdTWFjIs2gjakPWP80mXRY4earrRbVvNVXp/99GMYWEOCRP3XrjeI7rec3bjZfyt2m0Wyo1XM7tzFGRKkKnnvPhsU86mIPXjoSzxiwaHRYo+f1KEMCRIoe/pMBGGikX/+onuYEDPVy0OGPZ1evkomhme4rPTr7Gc+o4S/6S/MLXypZ4W30m/5uyHkfaosbwojFRjSGfYPfGBF/25GnAJEaj/+t6ygFCjyKfm5z57QFAWK1MQTX/KXeoQCRsRD6yuP0BQwomvfvv/If/yCFTBiv6z8pClwREFBIHQFg2QVhldQCDULDiEqSISmYBGSgkYoCh4hKAQEr1AQtEJCsAoNQSpEBKdQEZRCRjAKHUEoCghcUUHAihJiKz3uihoCVBQRmKKKgBRlBKKoIwDFA8Rd8QJxVTxB3BRvEBfFI0SueIVIFc8QmeIdIlE8RJwVLxFHxVPESfEWGdpmkLf1qrTaa8RWfsE3kdGQjPL7T/52uNK/Zd9DQV9nvogAAABEZVhJZk1NACoAAAAIAAGHaQAEAAAAAQAAABoAAAAAAAOgAQADAAAAAQABAACgAgAEAAAAAQAAB9CgAwAEAAAAAQAAB9AAAAAAxqEN6QAAABF0RVh0ZXhpZjpDb2xvclNwYWNlADEPmwJJAAAAEnRFWHRleGlmOkV4aWZPZmZzZXQAMjZTG6JlAAAAGXRFWHRleGlmOlBpeGVsWERpbWVuc2lvbgAyMDAw1StfagAAABl0RVh0ZXhpZjpQaXhlbFlEaW1lbnNpb24AMjAwMGzQhIIAAAAASUVORK5CYII="

CATEGORIES = ["Smartphone", "Tablette", "PC Portable", "Console"]

PANNES = ["Écran casse", "Batterie", "Connecteur de charge", 
          "Camera avant", "Camera arriere", 
          "Bouton volume", "Bouton power", 
          "Haut-parleur (je n'entends pas les gens ou la musique)", 
          "Microphone (les gens ne m'entendent pas)", 
          "Vitre arriere", "Désoxydation", "Problème logiciel", "Diagnostic", "Autre"]

STATUTS = ["En attente de diagnostic", "En cours de réparation", 
           "Réparation terminée", "Rendu au client", "Clôturé"]

MARQUES = {
    "Smartphone": ["Apple", "Samsung", "Xiaomi", "Huawei", "OnePlus", "Google", "Oppo", "Autre"],
    "Tablette": ["Apple", "Samsung", "Huawei", "Lenovo", "Microsoft", "Autre"],
    "PC Portable": ["Apple", "HP", "Dell", "Lenovo", "Asus", "Acer", "MSI", "Autre"],
    "Console": ["Sony", "Microsoft", "Nintendo", "Autre"]
}

MODELES = {
    ("Smartphone", "Apple"): [
        "iPhone 16 Pro Max", "iPhone 16 Pro", "iPhone 16 Plus", "iPhone 16",
        "iPhone 15 Pro Max", "iPhone 15 Pro", "iPhone 15 Plus", "iPhone 15",
        "iPhone 14 Pro Max", "iPhone 14 Pro", "iPhone 14 Plus", "iPhone 14",
        "iPhone 13 Pro Max", "iPhone 13 Pro", "iPhone 13", "iPhone 13 Mini",
        "iPhone 12 Pro Max", "iPhone 12 Pro", "iPhone 12", "iPhone 12 Mini",
        "iPhone 11 Pro Max", "iPhone 11 Pro", "iPhone 11",
        "iPhone XS Max", "iPhone XS", "iPhone XR",
        "iPhone X", "iPhone 8 Plus", "iPhone 8", "iPhone 7 Plus", "iPhone 7",
        "iPhone 6s Plus", "iPhone 6s", "iPhone 6 Plus", "iPhone 6",
        "iPhone SE 2022", "iPhone SE 2020", "iPhone SE",
        "Autre"
    ],
    ("Smartphone", "Samsung"): [
        "Galaxy S24 Ultra", "Galaxy S24+", "Galaxy S24",
        "Galaxy S23 Ultra", "Galaxy S23+", "Galaxy S23",
        "Galaxy S22 Ultra", "Galaxy S22+", "Galaxy S22",
        "Galaxy S21 Ultra", "Galaxy S21+", "Galaxy S21",
        "Galaxy Z Fold 5", "Galaxy Z Fold 4", "Galaxy Z Fold 3",
        "Galaxy Z Flip 5", "Galaxy Z Flip 4", "Galaxy Z Flip 3",
        "Galaxy A54", "Galaxy A53", "Galaxy A34", "Galaxy A14",
        "Autre"
    ],
    ("Smartphone", "Xiaomi"): [
        "Xiaomi 14 Ultra", "Xiaomi 14 Pro", "Xiaomi 14",
        "Xiaomi 13 Ultra", "Xiaomi 13 Pro", "Xiaomi 13",
        "Redmi Note 13 Pro", "Redmi Note 13", "Redmi Note 12",
        "POCO F5", "POCO X5 Pro",
        "Autre"
    ],
    ("Smartphone", "Huawei"): [
        "P60 Pro", "P50 Pro", "P40 Pro", "P30 Pro", "P30",
        "Mate 60 Pro", "Mate 50 Pro", "Mate 40 Pro",
        "Nova 11", "Nova 10",
        "Autre"
    ],
    ("Tablette", "Apple"): [
        "iPad Pro 12.9 M2", "iPad Pro 11 M2",
        "iPad Pro 12.9 M1", "iPad Pro 11 M1",
        "iPad Air M2", "iPad Air M1",
        "iPad 10", "iPad 9", "iPad 8",
        "iPad Mini 6", "iPad Mini 5",
        "Autre"
    ],
    ("Tablette", "Samsung"): [
        "Galaxy Tab S9 Ultra", "Galaxy Tab S9+", "Galaxy Tab S9",
        "Galaxy Tab S8 Ultra", "Galaxy Tab S8+", "Galaxy Tab S8",
        "Galaxy Tab A9", "Galaxy Tab A8",
        "Autre"
    ],
    ("PC Portable", "Apple"): [
        "MacBook Pro 16 M3", "MacBook Pro 14 M3",
        "MacBook Pro 16 M2", "MacBook Pro 14 M2",
        "MacBook Pro 16 M1", "MacBook Pro 14 M1",
        "MacBook Air 15 M3", "MacBook Air 13 M3",
        "MacBook Air 15 M2", "MacBook Air 13 M2",
        "MacBook Air M1",
        "Autre"
    ],
    ("Console", "Sony"): ["PlayStation 5", "PlayStation 5 Digital", "PlayStation 4 Pro", "PlayStation 4", "PS Vita", "Autre"],
    ("Console", "Nintendo"): ["Switch OLED", "Switch V2", "Switch V1", "Switch Lite", "3DS XL", "3DS", "2DS", "Autre"],
    ("Console", "Microsoft"): ["Xbox Series X", "Xbox Series S", "Xbox One X", "Xbox One S", "Xbox One", "Autre"],
}

# =============================================================================
# CSS STYLE KLIKPHONE
# =============================================================================
def load_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    --klik-orange: #fb923c;
    --klik-orange-dark: #f97316;
    --klik-orange-light: #fed7aa;
    --klik-bg: #f0f2f5;
    --klik-white: #ffffff;
    --klik-gray-100: #f9fafb;
    --klik-gray-200: #e5e7eb;
    --klik-gray-300: #d1d5db;
    --klik-gray-500: #6b7280;
    --klik-gray-700: #374151;
    --klik-gray-900: #1f2937;
    --klik-red: #ef4444;
    --klik-green: #10b981;
    --klik-blue: #2563eb;
    --klik-yellow: #fbbf24;
}

* { font-family: 'Inter', sans-serif !important; }

.stApp { background-color: var(--klik-bg) !important; }

#MainMenu, footer, header, .stDeployButton { display: none !important; }

/* Container style portail */
.staff-container {
    background-color: var(--klik-white);
    padding: 2rem;
    border-radius: 12px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    max-width: 1200px;
    margin: 1.5rem auto;
}

/* Titre page style */
.page-title {
    text-align: center;
    font-size: 1.75rem;
    font-weight: 700;
    color: var(--klik-orange-dark);
    margin-bottom: 2rem;
}

/* Section title */
.section-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--klik-gray-900);
    margin-bottom: 1rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid var(--klik-gray-200);
}

/* Boutons orange Klikphone */
.stButton > button {
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    padding: 0.75rem 1.5rem !important;
    border-radius: 8px !important;
    transition: all 0.3s ease !important;
    border: none !important;
}

.stButton > button[kind="primary"],
.stButton > button[data-testid="baseButton-primary"] {
    background-color: var(--klik-orange) !important;
    color: white !important;
}

.stButton > button[kind="primary"]:hover,
.stButton > button[data-testid="baseButton-primary"]:hover {
    background-color: var(--klik-orange-dark) !important;
}

.stButton > button[kind="secondary"],
.stButton > button[data-testid="baseButton-secondary"] {
    background-color: var(--klik-gray-500) !important;
    color: white !important;
}

/* Inputs style portail */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    border: 2px solid var(--klik-gray-300) !important;
    padding: 0.85rem 1rem !important;
    border-radius: 8px !important;
    background-color: white !important;
    transition: all 0.3s ease !important;
    font-size: 16px !important;
    color: var(--klik-gray-900) !important;
}

/* Selectbox ameliore */
.stSelectbox > div > div {
    border: 2px solid var(--klik-gray-300) !important;
    border-radius: 8px !important;
    background-color: white !important;
}

.stSelectbox > div > div > div {
    padding: 0.85rem 1rem !important;
    font-size: 16px !important;
    color: var(--klik-gray-900) !important;
    min-height: 50px !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus,
.stSelectbox > div > div:focus-within {
    border-color: var(--klik-orange) !important;
    box-shadow: 0 0 0 3px rgba(251,146,60,0.2) !important;
    background-color: white !important;
}

/* Labels */
.label-text {
    font-weight: 500;
    color: var(--klik-gray-700);
    margin-bottom: 0.5rem;
    display: block;
    font-size: 0.875rem;
}

/* Status badges */
.status-badge {
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    white-space: nowrap;
    display: inline-block;
}

.status-diagnostic { background-color: #fef3c7; color: #d97706; }
.status-encours { background-color: #dbeafe; color: #2563eb; }
.status-termine { background-color: #d1fae5; color: #065f46; }
.status-rendu { background-color: #10b981; color: #ffffff; }
.status-clôturé { background-color: #f3f4f6; color: #6b7280; }

/* Table style portail */
.repair-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 1rem;
}

.repair-table th, .repair-table td {
    border: 1px solid var(--klik-gray-200);
    padding: 0.75rem;
    text-align: left;
    vertical-align: middle;
    font-size: 0.9rem;
}

.repair-table th {
    background-color: var(--klik-gray-100);
    font-weight: 600;
    color: var(--klik-gray-700);
}

.repair-table tr:hover {
    background-color: var(--klik-gray-100);
}

/* Summary items */
.summary-item {
    margin-bottom: 0.75rem;
    display: flex;
}

.summary-label {
    font-weight: 600;
    color: var(--klik-gray-700);
    min-width: 140px;
}

.summary-value {
    color: var(--klik-gray-500);
}

/* Welcome screen fullscreen */
.fullscreen-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: var(--klik-white);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    padding: 2rem;
    text-align: center;
}

.fullscreen-title {
    font-size: 2.2rem;
    font-weight: 700;
    color: var(--klik-gray-900);
    margin-bottom: 1rem;
}

.fullscreen-message {
    font-size: 1.15rem;
    color: var(--klik-gray-500);
    margin-bottom: 2.5rem;
    max-width: 550px;
    line-height: 1.7;
}

/* Form container style */
.form-container {
    background-color: var(--klik-white);
    padding: 2.5rem;
    border-radius: 16px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.12);
    max-width: 800px;
    margin: 2rem auto;
    border-top: 6px solid var(--klik-orange);
}

/* Klikphone header */
.klik-header {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 1.5rem;
}

.klik-title {
    font-size: 2.8rem;
    font-weight: 700;
    color: var(--klik-orange-dark);
}

.klik-subtitle {
    text-align: center;
    color: var(--klik-gray-500);
    font-size: 1.1rem;
    margin-bottom: 2rem;
}

/* Pattern grid */
.pattern-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 18px;
    width: 140px;
    margin: 0.5rem auto;
    padding: 10px;
    border: 1px solid var(--klik-gray-200);
    border-radius: 8px;
    background-color: var(--klik-gray-100);
}

.pattern-dot {
    width: 28px;
    height: 28px;
    background-color: var(--klik-gray-200);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.7rem;
    color: white;
    font-weight: bold;
}

.pattern-dot.active {
    background-color: var(--klik-orange);
}

/* Success screen */
.success-overlay {
    background: linear-gradient(135deg, #10b981, #059669);
    color: white;
    padding: 3rem;
    border-radius: 16px;
    text-align: center;
    margin: 2rem 0;
}

.success-overlay h1 {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}

.success-overlay .ticket-code {
    font-size: 2rem;
    font-weight: 700;
    background: rgba(255,255,255,0.2);
    padding: 1rem 2rem;
    border-radius: 8px;
    display: inline-block;
    margin: 1rem 0;
}

/* Ticket impression */
.ticket-container {
    background-color: var(--klik-white);
    padding: 1rem;
    border-radius: 6px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    max-width: 400px;
    margin: 1rem auto;
    border: 1px solid var(--klik-gray-200);
    font-size: 0.85rem;
}

.ticket-container h1 {
    color: var(--klik-gray-900);
    font-size: 1.4rem;
    font-weight: 700;
    text-align: center;
    margin-bottom: 0.4rem;
}

.ticket-container h2 {
    color: var(--klik-gray-900);
    font-size: 1rem;
    font-weight: 700;
    border-bottom: 1px solid #000;
    padding-bottom: 0.5rem;
    margin-top: 1rem;
    margin-bottom: 0.5rem;
    text-align: center;
}

.info-item {
    font-size: 0.85rem;
    color: var(--klik-gray-500);
    margin-bottom: 0.3rem;
}

.info-item strong {
    color: var(--klik-gray-900);
    font-weight: 500;
}

.disclaimer {
    font-size: 0.65rem;
    font-style: italic;
    color: var(--klik-gray-500);
    margin-top: 1rem;
    padding-top: 0.5rem;
    border-top: 1px dashed var(--klik-gray-300);
    line-height: 1.3;
}

.closing-message {
    text-align: center;
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--klik-gray-900);
    margin-top: 1rem;
}

/* Staff section jaune */
.staff-section {
    background-color: #fffbeb;
    border: 1px solid var(--klik-yellow);
    border-radius: 6px;
    padding: 1rem;
    margin: 0.5rem 0;
}

/* Progress bar orange */
.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--klik-orange), var(--klik-orange-dark)) !important;
}

/* Tabs orange */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.5rem;
    background: transparent;
    border-bottom: 2px solid var(--klik-gray-200);
}

.stTabs [data-baseweb="tab"] {
    padding: 0.75rem 1.5rem;
    font-weight: 500;
    color: var(--klik-gray-500);
    border: none;
    background: none;
    border-bottom: 2px solid transparent;
    margin-bottom: -2px;
}

.stTabs [aria-selected="true"] {
    color: var(--klik-orange-dark) !important;
    border-bottom-color: var(--klik-orange) !important;
    background: none !important;
}

/* Expander */
.streamlit-expanderHeader {
    background: var(--klik-gray-100) !important;
    border-radius: 8px !important;
}

/* Mobile */
@media (max-width: 768px) {
    .stButton > button {
        min-height: 50px !important;
        font-size: 14px !important;
    }
    input, textarea, select {
        font-size: 16px !important;
    }
    .klik-title {
        font-size: 2rem;
    }
    .form-container, .staff-container {
        margin: 1rem;
        padding: 1.5rem;
    }
}
</style>
""", unsafe_allow_html=True)

# =============================================================================
# DATABASE
# =============================================================================
def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    
    c.execute("""CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT, prenom TEXT, telephone TEXT UNIQUE, email TEXT,
        date_creation TEXT DEFAULT CURRENT_TIMESTAMP)""")
    
    c.execute("""CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_code TEXT UNIQUE,
        client_id INTEGER,
        categorie TEXT, marque TEXT, modele TEXT, modele_autre TEXT,
        imei TEXT,
        panne TEXT, panne_detail TEXT,
        pin TEXT, pattern TEXT,
        notes_client TEXT, notes_internes TEXT,
        commentaire_client TEXT,
        reparation_supp TEXT, prix_supp REAL,
        devis_estime REAL, acompte REAL DEFAULT 0, tarif_final REAL,
        personne_charge TEXT,
        statut TEXT DEFAULT 'En attente de diagnostic',
        date_depot TEXT DEFAULT CURRENT_TIMESTAMP,
        date_maj TEXT DEFAULT CURRENT_TIMESTAMP,
        date_cloture TEXT)""")
    
    c.execute("""CREATE TABLE IF NOT EXISTS params (
        id INTEGER PRIMARY KEY, cle TEXT UNIQUE, valeur TEXT)""")
    
    c.execute("""CREATE TABLE IF NOT EXISTS catalog_marques (
        id INTEGER PRIMARY KEY, categorie TEXT, marque TEXT, UNIQUE(categorie, marque))""")
    
    c.execute("""CREATE TABLE IF NOT EXISTS catalog_modeles (
        id INTEGER PRIMARY KEY, categorie TEXT, marque TEXT, modele TEXT, 
        UNIQUE(categorie, marque, modele))""")
    
    # Migration: ajouter commentaire_client si n'existe pas
    try:
        c.execute("ALTER TABLE tickets ADD COLUMN commentaire_client TEXT")
    except:
        pass
    
    # Migration: ajouter imei si n'existe pas
    try:
        c.execute("ALTER TABLE tickets ADD COLUMN imei TEXT")
    except:
        pass
    
    # Migration: ajouter reparation_supp et prix_supp
    try:
        c.execute("ALTER TABLE tickets ADD COLUMN reparation_supp TEXT")
    except:
        pass
    try:
        c.execute("ALTER TABLE tickets ADD COLUMN prix_supp REAL")
    except:
        pass
    
    conn.commit()
    
    # Params défaut
    params = {
        "PIN_ACCUEIL": "2626", "PIN_TECH": "2626",
        "TEL_BOUTIQUE": "04 79 60 89 22",
        "ADRESSE_BOUTIQUE": "79 Place Saint Léger, 73000 Chambéry",
        "NOM_BOUTIQUE": "Klikphone",
        "URL_SUIVI": "https://klikphone-sav.streamlit.app",
        "SMTP_HOST": "",
        "SMTP_PORT": "587",
        "SMTP_USER": "",
        "SMTP_PASS": "",
        "SMTP_FROM": "",
        "SMTP_FROM_NAME": "Klikphone"
    }
    for k, v in params.items():
        c.execute("INSERT OR IGNORE INTO params (cle, valeur) VALUES (?, ?)", (k, v))
    
    # Catalogue
    c.execute("SELECT COUNT(*) FROM catalog_marques")
    if c.fetchone()[0] == 0:
        for cat, marques in MARQUES.items():
            for m in marques:
                c.execute("INSERT OR IGNORE INTO catalog_marques (categorie, marque) VALUES (?, ?)", (cat, m))
        for (cat, marque), modeles_list in MODELES.items():
            for m in modeles_list:
                c.execute("INSERT OR IGNORE INTO catalog_modeles (categorie, marque, modele) VALUES (?, ?, ?)", (cat, marque, m))
    
    conn.commit()
    conn.close()

def get_param(k):
    conn = get_db()
    r = conn.cursor().execute("SELECT valeur FROM params WHERE cle=?", (k,)).fetchone()
    conn.close()
    return r["valeur"] if r else ""

def set_param(k, v):
    conn = get_db()
    conn.cursor().execute("INSERT OR REPLACE INTO params (cle, valeur) VALUES (?, ?)", (k, v))
    conn.commit()
    conn.close()

def get_marques(cat):
    conn = get_db()
    r = [row["marque"] for row in conn.cursor().execute(
        "SELECT marque FROM catalog_marques WHERE categorie=? ORDER BY marque", (cat,)).fetchall()]
    conn.close()
    return r if r else ["Autre"]

def get_modeles(cat, marque):
    conn = get_db()
    r = [row["modele"] for row in conn.cursor().execute(
        "SELECT modele FROM catalog_modeles WHERE categorie=? AND marque=? ORDER BY modele", 
        (cat, marque)).fetchall()]
    conn.close()
    return r if r else ["Autre"]

def ajouter_marque(cat, marque):
    try:
        conn = get_db()
        conn.cursor().execute("INSERT INTO catalog_marques (categorie, marque) VALUES (?, ?)", (cat, marque))
        conn.commit()
        conn.close()
        return True
    except: return False

def ajouter_modele(cat, marque, modele):
    try:
        conn = get_db()
        conn.cursor().execute("INSERT INTO catalog_modeles (categorie, marque, modele) VALUES (?, ?, ?)", (cat, marque, modele))
        conn.commit()
        conn.close()
        return True
    except: return False

# =============================================================================
# MÉTIER
# =============================================================================
def get_or_create_client(nom, tel, prenom="", email=""):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT id FROM clients WHERE telephone=?", (tel,))
    r = c.fetchone()
    if r:
        cid = r["id"]
        c.execute("UPDATE clients SET nom=?, prenom=?, email=? WHERE id=?", (nom, prenom, email, cid))
    else:
        c.execute("INSERT INTO clients (nom, prenom, telephone, email) VALUES (?,?,?,?)", (nom, prenom, tel, email))
        cid = c.lastrowid
    conn.commit()
    conn.close()
    return cid

def creer_ticket(client_id, cat, marque, modele, modele_autre, panne, panne_detail, pin, pattern, notes, imei=""):
    conn = get_db()
    c = conn.cursor()
    c.execute("""INSERT INTO tickets 
        (client_id, categorie, marque, modele, modele_autre, imei, panne, panne_detail, pin, pattern, notes_client, statut) 
        VALUES (?,?,?,?,?,?,?,?,?,?,?,'En attente de diagnostic')""", 
        (client_id, cat, marque, modele, modele_autre, imei, panne, panne_detail, pin, pattern, notes))
    tid = c.lastrowid
    code = f"KP-{tid:06d}"
    c.execute("UPDATE tickets SET ticket_code=? WHERE id=?", (code, tid))
    conn.commit()
    conn.close()
    return code

def get_ticket(tid=None, code=None):
    conn = get_db()
    c = conn.cursor()
    if tid: c.execute("SELECT * FROM tickets WHERE id=?", (tid,))
    elif code: c.execute("SELECT * FROM tickets WHERE ticket_code=?", (code,))
    else: return None
    r = c.fetchone()
    conn.close()
    return dict(r) if r else None

def get_ticket_full(tid=None, code=None):
    conn = get_db()
    c = conn.cursor()
    q = """SELECT t.*, c.nom as client_nom, c.prenom as client_prenom, 
           c.telephone as client_tel, c.email as client_email 
           FROM tickets t JOIN clients c ON t.client_id=c.id"""
    if tid: c.execute(q + " WHERE t.id=?", (tid,))
    elif code: c.execute(q + " WHERE t.ticket_code=?", (code,))
    else: return None
    r = c.fetchone()
    conn.close()
    return dict(r) if r else None

def update_ticket(tid, **kw):
    if not kw: return
    conn = get_db()
    c = conn.cursor()
    fields = ", ".join([f"{k}=?" for k in kw.keys()])
    vals = list(kw.values()) + [datetime.now().strftime("%Y-%m-%d %H:%M:%S"), tid]
    c.execute(f"UPDATE tickets SET {fields}, date_maj=? WHERE id=?", vals)
    conn.commit()
    conn.close()

def changer_statut(tid, statut):
    conn = get_db()
    c = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if statut == "Clôturé":
        c.execute("UPDATE tickets SET statut=?, date_maj=?, date_clôturé=? WHERE id=?", (statut, now, now, tid))
    else:
        c.execute("UPDATE tickets SET statut=?, date_maj=? WHERE id=?", (statut, now, tid))
    conn.commit()
    conn.close()

def chercher_tickets(statut=None, tel=None, code=None, nom=None):
    conn = get_db()
    c = conn.cursor()
    q = """SELECT t.*, c.nom as client_nom, c.prenom as client_prenom, c.telephone as client_tel 
           FROM tickets t JOIN clients c ON t.client_id=c.id WHERE 1=1"""
    p = []
    if statut: q += " AND t.statut=?"; p.append(statut)
    if tel: q += " AND c.telephone LIKE ?"; p.append(f"%{tel}%")
    if code: q += " AND t.ticket_code LIKE ?"; p.append(f"%{code}%")
    if nom: q += " AND (c.nom LIKE ? OR c.prenom LIKE ?)"; p.extend([f"%{nom}%", f"%{nom}%"])
    q += " ORDER BY t.date_depot DESC"
    c.execute(q, p)
    r = [dict(row) for row in c.fetchall()]
    conn.close()
    return r

def ajouter_note(tid, note):
    t = get_ticket(tid=tid)
    if not t: return
    ts = datetime.now().strftime("%d/%m %H:%M")
    n = f"[{ts}] {note}"
    notes = t.get("notes_internes") or ""
    notes = notes + "\n" + n if notes else n
    update_ticket(tid, notes_internes=notes)

# =============================================================================
# UTILS
# =============================================================================
def fmt_date(d):
    if not d: return "N/A"
    try: return datetime.strptime(d[:19], "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y %H:%M")
    except: return d

def fmt_prix(p):
    return f"{p:.2f} €" if p else "N/A"

def qr_url(data):
    return f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={urllib.parse.quote(data)}"

def wa_link(tel, msg):
    t = "".join(filter(str.isdigit, tel))
    if t.startswith("0"): t = "33" + t[1:]
    return f"https://wa.me/{t}?text={urllib.parse.quote(msg)}"

def get_status_class(statut):
    if "diagnostic" in statut.lower(): return "status-diagnostic"
    elif "cours" in statut.lower(): return "status-encours"
    elif "terminée" in statut.lower(): return "status-termine"
    elif "rendu" in statut.lower(): return "status-rendu"
    else: return "status-clôturé"

def sms_link(tel, msg):
    """Genere un lien SMS"""
    t = "".join(filter(str.isdigit, tel))
    if t.startswith("0"): t = "+33" + t[1:]
    return f"sms:{t}?body={urllib.parse.quote(msg)}"

def email_link(email, sujet, msg):
    """Genere un lien mailto"""
    return f"mailto:{email}?subject={urllib.parse.quote(sujet)}&body={urllib.parse.quote(msg)}"

def envoyer_email(destinataire, sujet, message, html_content=None):
    """Envoie un email via SMTP avec option HTML"""
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    
    # Récupérer les paramètres SMTP
    smtp_host = get_param("SMTP_HOST")
    smtp_port = get_param("SMTP_PORT")
    smtp_user = get_param("SMTP_USER")
    smtp_pass = get_param("SMTP_PASS")
    smtp_from = get_param("SMTP_FROM")
    smtp_from_name = get_param("SMTP_FROM_NAME") or "Klikphone"
    
    if not smtp_host or not smtp_user or not smtp_pass:
        return False, "Configuration SMTP incomplète. Allez dans Config > Email."
    
    try:
        # Créer le message
        msg = MIMEMultipart('alternative')
        msg['From'] = f"{smtp_from_name} <{smtp_from or smtp_user}>"
        msg['To'] = destinataire
        msg['Subject'] = sujet
        
        # Corps du message en texte
        msg.attach(MIMEText(message, 'plain', 'utf-8'))
        
        # Corps en HTML si fourni
        if html_content:
            msg.attach(MIMEText(html_content, 'html', 'utf-8'))
        
        # Connexion et envoi
        server = smtplib.SMTP(smtp_host, int(smtp_port or 587))
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_from or smtp_user, destinataire, msg.as_string())
        server.quit()
        
        return True, "Email envoyé avec succès!"
    except Exception as e:
        return False, f"Erreur d'envoi: {str(e)}"

def envoyer_sms_api(tel, message):
    """Placeholder pour API SMS (à configurer selon fournisseur)"""
    return False, "API SMS non configurée. Utilisez le lien SMS."

def get_messages_predefs(t):
    """Retourne les messages prédéfinis pour un ticket"""
    prénom = t.get('client_prenom', '') or 'Client'
    nom = t.get('client_nom', '')
    marque = t.get('marque', '') or 'votre appareil'
    modèle = t.get('modele', '')
    code = t.get('ticket_code', '')
    devis = t.get('devis_estime')
    tarif = t.get('tarif_final')
    
    # Formater le montant
    if tarif and tarif > 0:
        montant = f"{tarif} €"
    elif devis and devis > 0:
        montant = f"{devis} €"
    else:
        montant = "Nous consulter"
    
    # Formater le devis
    devis_txt = f"{devis} €" if devis and devis > 0 else "Nous consulter"
    
    messages = {
        "-- Choisir un message --": "",
        
        "Appareil reçu": f"""Bonjour {prénom},

Nous vous informons que votre appareil {marque} {modèle} a bien été réceptionné à la boutique Klikphone.

Numéro de suivi : {code}

Nous allons procéder au diagnostic et reviendrons vers vous dans les plus brefs délais.

Cordialement,
L'équipe Klikphone
04 79 60 89 22""",

        "Diagnostic en cours": f"""Bonjour {prénom},

Nous vous informons que le diagnostic de votre appareil {marque} {modèle} est actuellement en cours à la boutique Klikphone.

Numéro de suivi : {code}

Nous reviendrons vers vous rapidement avec le résultat du diagnostic.

Cordialement,
L'équipe Klikphone
04 79 60 89 22""",

        "Devis à valider": f"""Bonjour {prénom},

Le diagnostic de votre appareil {marque} {modèle} est terminé.

Devis de réparation : {devis_txt}

Merci de nous confirmer votre accord pour procéder à la réparation en répondant à ce message ou en nous appelant.

Cordialement,
L'équipe Klikphone
04 79 60 89 22""",

        "En cours de réparation": f"""Bonjour {prénom},

Nous vous informons que votre appareil {marque} {modèle} est actuellement en cours de réparation à la boutique Klikphone.

Numéro de suivi : {code}

Nous vous prévenons dès que la réparation sera terminée.

Cordialement,
L'équipe Klikphone
04 79 60 89 22""",

        "Attente de pièce": f"""Bonjour {prénom},

Nous vous informons que nous sommes en attente d'une pièce pour la réparation de votre appareil {marque} {modèle}.

Délai estimé : 2 à 5 jours ouvrables.

Nous vous prévenons dès réception de la pièce.

Cordialement,
L'équipe Klikphone
04 79 60 89 22""",

        "Appareil prêt": f"""Bonjour {prénom},

Nous vous informons que votre appareil {marque} {modèle} est prêt à être récupéré à la boutique Klikphone.

Montant à régler : {montant}

Adresse : 79 Place Saint Léger, 73000 Chambéry
Horaires : Lundi-Samedi 10h-19h

N'oubliez pas votre pièce d'identité.

Cordialement,
L'équipe Klikphone
04 79 60 89 22""",

        "Relance récupération": f"""Bonjour {prénom},

Nous vous rappelons que votre appareil {marque} {modèle} est prêt et vous attend à la boutique Klikphone depuis plusieurs jours.

Merci de venir le récupérer dans les meilleurs délais.

Adresse : 79 Place Saint Léger, 73000 Chambéry
Horaires : Lundi-Samedi 10h-19h

Cordialement,
L'équipe Klikphone
04 79 60 89 22""",

        "Non réparable": f"""Bonjour {prénom},

Après diagnostic approfondi, nous avons le regret de vous informer que votre appareil {marque} {modèle} n'est malheureusement pas réparable.

Vous pouvez venir le récupérer à la boutique. Aucun frais ne vous sera facturé pour le diagnostic.

Nous restons à votre disposition pour toute question.

Cordialement,
L'équipe Klikphone
04 79 60 89 22""",

        "Rappel RDV": f"""Bonjour {prénom},

Nous vous rappelons votre rendez-vous à la boutique Klikphone pour votre appareil {marque} {modèle}.

Adresse : 79 Place Saint Léger, 73000 Chambéry

À bientôt !

L'équipe Klikphone
04 79 60 89 22""",

        "Personnalisé": ""
    }
    return messages

# =============================================================================
# TICKETS HTML
# =============================================================================
def ticket_client_html(t):
    """Ticket client style Klikphone - format impression 58mm"""
    panne = t.get("panne", "")
    if t.get("panne_detail"): panne += f" ({t['panne_detail']})"
    modele_txt = t.get("modele", "")
    if t.get("modele_autre"): modele_txt += f" ({t['modele_autre']})"
    
    # Tarifs
    devis = t.get('devis_estime')
    tarif = t.get('tarif_final')
    acompte = t.get('acompte')
    
    tarif_section = ""
    if devis or tarif:
        tarif_section = f"""
    <div style="border-top: 1px solid #000; padding-top: 8px; margin-top: 8px;">
        <div style="font-weight: bold; margin-bottom: 5px;">TARIFICATION</div>
        {"<div>Devis: " + str(devis) + " €</div>" if devis else ""}
        {"<div>Tarif final: " + str(tarif) + " €</div>" if tarif else ""}
        {"<div>Acompte versé: " + str(acompte) + " €</div>" if acompte else ""}
        {"<div style='font-weight:bold; margin-top:5px;'>Reste à payer: " + str(round((tarif or 0) - (acompte or 0), 2)) + " €</div>" if tarif else ""}
    </div>
        """
    
    # URL de suivi
    url_suivi = get_param("URL_SUIVI") or "https://klikphone-sav.streamlit.app"
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=100x100&data={urllib.parse.quote(url_suivi)}"
    
    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: 'Courier New', monospace; font-size: 12px; margin: 0; padding: 15px; }}
        .ticket {{ max-width: 300px; margin: 0 auto; background: #fff; border: 2px dashed #ccc; border-radius: 8px; padding: 15px; }}
        .logo {{ text-align: center; margin-bottom: 5px; }}
        .logo img {{ width: 50px; height: 50px; }}
        .header {{ text-align: center; font-weight: bold; font-size: 18px; color: #f97316; margin-bottom: 5px; }}
        .contact {{ text-align: center; font-size: 10px; color: #666; margin-bottom: 10px; padding-bottom: 10px; border-bottom: 1px solid #000; }}
        .ticket-num {{ text-align: center; font-weight: bold; font-size: 14px; margin: 10px 0; padding: 5px; background: #fff3e0; border: 1px solid #f97316; }}
        .date {{ text-align: center; font-size: 10px; color: #666; margin-bottom: 10px; }}
        .section {{ border-top: 1px solid #000; padding-top: 8px; margin-top: 8px; }}
        .section-title {{ font-weight: bold; margin-bottom: 5px; }}
        .qr-section {{ text-align: center; margin-top: 15px; padding-top: 10px; border-top: 1px dashed #000; }}
        .qr-section img {{ width: 80px; height: 80px; }}
        .qr-section p {{ font-size: 9px; color: #666; margin-top: 5px; }}
        .conditions {{ border-top: 1px dashed #000; padding-top: 10px; margin-top: 15px; font-size: 8px; color: #666; line-height: 1.3; }}
        .footer {{ text-align: center; font-weight: bold; margin-top: 15px; padding-top: 10px; border-top: 1px solid #000; }}
        .print-btn {{ display: block; width: 100%; padding: 10px; margin-top: 15px; background: #fb923c; color: white; border: none; border-radius: 5px; font-size: 14px; cursor: pointer; }}
        .print-btn:hover {{ background: #f97316; }}
        @media print {{
            .print-btn {{ display: none; }}
            body {{ padding: 0; }}
            .ticket {{ border: none; max-width: 58mm; }}
        }}
    </style>
</head>
<body>
    <div class="ticket">
        <div class="logo"><img src="data:image/png;base64,{LOGO_B64}" alt="Klikphone"></div>
        <div class="header">KLIKPHONE</div>
        <div class="contact">
            Spécialiste Apple<br>
            79 Place Saint Léger, 73000 Chambéry<br>
            Tél: 04 79 60 89 22
        </div>
        
        <div class="ticket-num">TICKET N° {t['ticket_code']}</div>
        <div class="date">{fmt_date(t.get('date_depot',''))}</div>
        
        <div class="section">
            <div class="section-title">CLIENT</div>
            <div>Nom: {t.get('client_nom','')} {t.get('client_prenom','')}</div>
            <div>Tél: {t.get('client_tel','')}</div>
        </div>
        
        <div class="section">
            <div class="section-title">APPAREIL</div>
            <div>{t.get('marque','')} {modele_txt}</div>
        </div>
        
        <div class="section">
            <div class="section-title">MOTIF DU DÉPÔT</div>
            <div>{panne}</div>
        </div>
        
        {tarif_section}
        
        <div class="qr-section">
            <img src="{qr_url}" alt="QR Code">
            <p>Scannez pour suivre votre réparation</p>
        </div>
        
        <div class="conditions">
            <div class="section-title">CONDITIONS GÉNÉRALES</div>
            <p style="margin: 3px 0;">Klikphone ne consulte pas et n'accède pas aux données présentes dans votre appareil.</p>
            <p style="margin: 3px 0;">Une perte de données reste possible — pensez à sauvegarder.</p>
            <p style="margin: 3px 0;">Klikphone décline toute responsabilité en cas de perte de données ou de panne apparaissant après réparation (oxydation, choc, FaceID, etc.).</p>
        </div>
        
        <div class="footer">Merci de votre confiance !</div>
        
        <button class="print-btn" onclick="window.print()">IMPRIMER LE TICKET</button>
    </div>
</body>
</html>
"""

def ticket_staff_html(t):
    """Ticket staff format impression"""
    panne = t.get("panne", "")
    if t.get("panne_detail"): panne += f" ({t['panne_detail']})"
    modèle = t.get("modele", "")
    if t.get("modele_autre"): modèle += f" ({t['modele_autre']})"
    
    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: 'Courier New', monospace; font-size: 11px; margin: 0; padding: 15px; }}
        .ticket {{ max-width: 320px; margin: 0 auto; background: #fffbeb; border: 2px solid #f97316; border-radius: 8px; padding: 15px; }}
        .header {{ text-align: center; background: #f97316; color: white; padding: 8px; margin: -15px -15px 10px -15px; font-weight: bold; }}
        .ticket-num {{ text-align: center; font-weight: bold; font-size: 16px; margin-bottom: 10px; }}
        .status {{ background: #fef3c7; padding: 8px; border-radius: 4px; margin-bottom: 10px; text-align: center; }}
        .section {{ border: 1px solid #f97316; padding: 8px; margin: 8px 0; border-radius: 4px; }}
        .section-title {{ font-weight: bold; margin-bottom: 5px; }}
        .security {{ background: #fef3c7; }}
        .print-btn {{ display: block; width: 100%; padding: 10px; margin-top: 15px; background: #f97316; color: white; border: none; border-radius: 5px; font-size: 14px; cursor: pointer; }}
        .print-btn:hover {{ background: #ea580c; }}
        @media print {{
            .print-btn {{ display: none; }}
            body {{ padding: 0; }}
            .ticket {{ border: 1px solid #000; max-width: 58mm; background: white; }}
            .header {{ background: #000; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
        }}
    </style>
</head>
<body>
    <div class="ticket">
        <div class="header">TICKET STAFF</div>
        
        <div class="ticket-num">{t['ticket_code']}</div>
        
        <div class="status">
            <strong>STATUT:</strong> {t.get('statut','')}
        </div>
        
        <div class="section">
            <div class="section-title">CLIENT</div>
            <div>{t.get('client_nom','')} {t.get('client_prenom','')}</div>
            <div>Tel: {t.get('client_tel','')}</div>
            <div>Email: {t.get('client_email') or '-'}</div>
        </div>
        
        <div class="section">
            <div class="section-title">APPAREIL</div>
            <div>{t.get('categorie','')}</div>
            <div>{t.get('marque','')} {modèle}</div>
        </div>
        
        <div class="section security">
            <div class="section-title">SECURITE</div>
            <div>PIN: {t.get('pin') or 'Aucun'}</div>
            <div>Schéma: {t.get('pattern') or 'Aucun'}</div>
        </div>
        
        <div class="section">
            <div class="section-title">PANNE</div>
            <div>{panne}</div>
        </div>
        
        <div class="section">
            <div class="section-title">TARIFS</div>
            <div>Devis: {fmt_prix(t.get('devis_estime'))}</div>
            <div>Acompte: {fmt_prix(t.get('acompte'))}</div>
            <div>Final: {fmt_prix(t.get('tarif_final'))}</div>
        </div>
        
        <div class="section">
            <div class="section-title">NOTES</div>
            <pre style="white-space: pre-wrap; font-size: 10px; margin: 0;">{t.get('notes_internes') or '-'}</pre>
        </div>
        
        <div style="text-align: center; font-size: 10px; color: #666; margin-top: 10px;">
            Date depot: {fmt_date(t.get('date_depot',''))}
        </div>
        
        <button class="print-btn" onclick="window.print()">IMPRIMER LE TICKET</button>
    </div>
</body>
</html>
"""

# =============================================================================
# INTERFACE CLIENT - STYLE PORTAIL KLIKPHONE
# =============================================================================
def reset_client():
    st.session_state.step = 1
    st.session_state.data = {}
    st.session_state.pattern = []
    st.session_state.done = None
    if "success_timestamp" in st.session_state:
        del st.session_state.success_timestamp

def ui_client():
    import time
    
    if "step" not in st.session_state: reset_client()
    
    # Écran de succès
    if st.session_state.done:
        code = st.session_state.done
        t = get_ticket_full(code=code)
        url = get_param("URL_SUIVI")
        
        # Initialiser le timestamp si pas encore fait
        if "success_timestamp" not in st.session_state:
            st.session_state.success_timestamp = time.time()
        
        # Calculer le temps ecoule
        elapsed = time.time() - st.session_state.success_timestamp
        remaining = max(0, 20 - int(elapsed))
        
        # Si 20 secondes ecoulees, reset automatique
        if remaining <= 0:
            reset_client()
            st.rerun()
        
        st.markdown(f"""
        <div class="success-overlay">
            <h1>Demande enregistree !</h1>
            <p>Votre numéro de ticket</p>
            <div class="ticket-code">{code}</div>
            <p>Conservez ce numéro pour suivre votre réparation</p>
        </div>
        """, unsafe_allow_html=True)
        
        # QR Code
        st.markdown(f"""
        <div style="text-align:center; margin:1.5rem 0;">
            <img src="{qr_url(f'{url}?ticket={code}')}" style="margin:0.5rem 0;"/>
            <p style="color:#6b7280; font-size:0.85rem;">{url}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if t:
            with st.expander("Voir le ticket"):
                st.components.v1.html(ticket_client_html(t), height=500, scrolling=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # GROS BOUTON PROCHAIN CLIENT
        if st.button("PROCHAIN CLIENT", type="primary", use_container_width=True, key="next_client"):
            reset_client()
            st.rerun()
        
        # Afficher compte a rebours
        st.markdown(f"""
        <p style="text-align:center; color:#6b7280; margin-top:1rem; font-size:1rem;">
            Retour automatique dans <strong>{remaining}</strong> secondes...
        </p>
        """, unsafe_allow_html=True)
        
        # Forcer un rerun toutes les secondes pour mettre a jour le compteur
        time.sleep(1)
        st.rerun()
        
        return
    
    # Header Klikphone
    st.markdown("""
    <div class="klik-header">
        <span class="klik-title">Klikphone</span>
    </div>
    <p class="klik-subtitle">Une minute pour redonner vie à votre appareil.<br>Decrivez simplement le souci rencontre, on s'occupe du reste !</p>
    """, unsafe_allow_html=True)
    
    # Progress
    step = st.session_state.step
    st.progress(step / 6)
    étapes = ["", "Type d'appareil", "Marque", "Modèle", "Problème", "Sécurité", "Coordonnees"]
    st.markdown(f"<p style='text-align:center; color:#6b7280; margin-bottom:1.5rem;'>Étape {step}/6 : {étapes[step]}</p>", unsafe_allow_html=True)
    
    if step == 1: client_step1()
    elif step == 2: client_step2()
    elif step == 3: client_step3()
    elif step == 4: client_step4()
    elif step == 5: client_step5()
    elif step == 6: client_step6()

def client_step1():
    st.markdown("<p class='section-title'>Quel type d'appareil deposez-vous ?</p>", unsafe_allow_html=True)
    
    cols = st.columns(2)
    for i, cat in enumerate(CATEGORIES):
        with cols[i % 2]:
            if st.button(cat, key=f"cat_{cat}", use_container_width=True):
                st.session_state.data["cat"] = cat
                st.session_state.step = 2
                st.rerun()

def client_step2():
    cat = st.session_state.data.get("cat", "")
    st.markdown(f"<p class='section-title'>Quelle est la marque ?</p>", unsafe_allow_html=True)
    
    if st.button("Retour", key="back2"): st.session_state.step = 1; st.rerun()
    
    marques = get_marques(cat)
    cols = st.columns(3)
    for i, m in enumerate(marques):
        with cols[i % 3]:
            if st.button(m, key=f"m_{m}", use_container_width=True):
                st.session_state.data["marque"] = m
                st.session_state.step = 3
                st.rerun()

def client_step3():
    cat = st.session_state.data.get("cat", "")
    marque = st.session_state.data.get("marque", "")
    st.markdown(f"<p class='section-title'>Quel est le modèle ?</p>", unsafe_allow_html=True)
    
    if st.button("Retour", key="back3"): st.session_state.step = 2; st.rerun()
    
    # Si "Autre" marque, demander directement le modèle
    if marque == "Autre":
        st.markdown("**Precisez la marque et le modèle :**")
        modele_autre = st.text_input("Ex: Huawei P30 Pro", key="input_modele_autre", label_visibility="collapsed")
        if st.button("Continuer", type="primary", use_container_width=True):
            if modele_autre:
                st.session_state.data["modèle"] = "Autre"
                st.session_state.data["modele_autre"] = modele_autre
                st.session_state.step = 4
                st.rerun()
            else:
                st.warning("Veuillez préciser le modèle")
    else:
        # Récupérer les modèles et mettre "Autre" en dernier
        modeles_db = get_modeles(cat, marque)
        modeles_list = [m for m in modeles_db if m != "Autre"]
        modeles_list.append("Autre")
        # Ajouter placeholder en premier
        modeles_final = ["-- Choisir le modèle --"] + modeles_list
        
        mod = st.selectbox("Modèle", modeles_final, key="select_modele", label_visibility="collapsed")
        
        # Si "Autre" est sélectionné, afficher champ texte
        modele_autre = ""
        if mod == "Autre":
            st.markdown("**Précisez le modèle :**")
            modele_autre = st.text_input("Ex: iPhone 14 Pro Max", key="input_autre", label_visibility="collapsed")
        
        if st.button("Continuer", type="primary", use_container_width=True):
            if mod == "-- Choisir le modèle --":
                st.warning("Veuillez sélectionner un modèle")
            elif mod == "Autre" and not modele_autre:
                st.warning("Veuillez préciser le modèle")
            else:
                st.session_state.data["modèle"] = mod
                st.session_state.data["modele_autre"] = modele_autre
                st.session_state.step = 4
                st.rerun()

def client_step4():
    st.markdown("<p class='section-title'>Quel est le problème rencontre ?</p>", unsafe_allow_html=True)
    
    if st.button("Retour", key="back4"): st.session_state.step = 3; st.rerun()
    
    cols = st.columns(3)
    for i, p in enumerate(PANNES):
        with cols[i % 3]:
            if st.button(p, key=f"p_{p}", use_container_width=True):
                st.session_state.data["panne"] = p
                if p == "Autre" or p == "Diagnostic":
                    st.session_state.data["show_detail"] = True
                    st.rerun()
                else:
                    st.session_state.step = 5
                    st.rerun()
    
    if st.session_state.data.get("show_detail"):
        detail = st.text_area("Decrivez le problème rencontre")
        if st.button("Continuer", type="primary"):
            st.session_state.data["panne_detail"] = detail
            st.session_state.step = 5
            st.rerun()

def client_step5():
    st.markdown("<p class='section-title'>Code de deverrouillage</p>", unsafe_allow_html=True)
    st.markdown("<p style='color:#6b7280;'>Pour permettre au technicien de tester l'appareil</p>", unsafe_allow_html=True)
    
    if st.button("Retour", key="back5"): st.session_state.step = 4; st.rerun()
    
    choix = st.radio("Type de verrouillage", ["Code PIN", "Schéma", "Aucun"], horizontal=True, label_visibility="collapsed")
    
    if choix == "Code PIN":
        pin = st.text_input("Entrez votre code", type="password", placeholder="••••")
        if st.button("Continuer", type="primary"):
            st.session_state.data["pin"] = pin
            st.session_state.step = 6
            st.rerun()
    
    elif choix == "Schéma":
        st.markdown("Cliquez sur les points dans l'ordre :")
        if "pattern" not in st.session_state: st.session_state.pattern = []
        
        cols = st.columns([1,2,1])
        with cols[1]:
            for row in range(3):
                row_cols = st.columns(3)
                for col in range(3):
                    n = row * 3 + col + 1
                    with row_cols[col]:
                        if n in st.session_state.pattern:
                            pos = st.session_state.pattern.index(n) + 1
                            st.button(f"●{pos}", key=f"pt_{n}", disabled=True, use_container_width=True)
                        else:
                            if st.button("○", key=f"pt_{n}", use_container_width=True):
                                st.session_state.pattern.append(n)
                                st.rerun()
        
        if st.session_state.pattern:
            st.markdown(f"**Séquence:** {'-'.join(map(str, st.session_state.pattern))}")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Effacer", use_container_width=True):
                    st.session_state.pattern = []
                    st.rerun()
            with c2:
                if st.button("Valider", type="primary", use_container_width=True):
                    st.session_state.data["pattern"] = "-".join(map(str, st.session_state.pattern))
                    st.session_state.step = 6
                    st.rerun()
    
    else:
        if st.button("Continuer sans code", type="primary"):
            st.session_state.step = 6
            st.rerun()

def client_step6():
    st.markdown("<p class='section-title'>Vos coordonnees</p>", unsafe_allow_html=True)
    
    if st.button("Retour", key="back6"): st.session_state.step = 5; st.rerun()
    
    col1, col2 = st.columns(2)
    with col1:
        prenom = st.text_input("Prénom *")
        telephone = st.text_input("Téléphone *", placeholder="06 12 34 56 78")
    with col2:
        nom = st.text_input("Nom *")
        email = st.text_input("Email")
    
    notes = st.text_area("Remarques", placeholder="Accessoires laisses, precisions sur le problème...")
    
    st.markdown("---")
    
    # CGV avec lien pour lire
    col_check, col_link = st.columns([4, 1])
    with col_check:
        consent = st.checkbox("J'accepte les conditions générales de depot et de réparation")
    with col_link:
        if st.button("Lire les CGV", key="read_cgv"):
            st.session_state.show_cgv = True
    
    # Afficher les CGV si demande
    if st.session_state.get("show_cgv"):
        cgv_html = """<div style="background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 8px; padding: 1rem; margin: 1rem 0; max-height: 300px; overflow-y: auto; font-size: 0.85rem;">
<h4 style="margin-top:0;">CONDITIONS GENERALES DE DEPOT ET DE REPARATION - KLIKPHONE</h4>
<p><b>1. OBJET</b><br>Les presentes conditions générales regissent les relations entre la societe Klikphone et ses clients pour tout depot d'appareil en vue d'une réparation.</p>
<p><b>2. DEPOT DE L'APPAREIL</b><br>- Le client s'engage a fournir des informations exactes concernant son appareil et le problème rencontre.<br>- Le client doit imperativement sauvegarder ses donnees avant le depot. Klikphone ne saurait etre tenu responsable de toute perte de donnees.<br>- Le client doit fournir les codes d'acces (PIN, schéma) necessaires au diagnostic et a la réparation.</p>
<p><b>3. DIAGNOSTIC ET DEVIS</b><br>- Un diagnostic est effectue avant toute réparation.<br>- Un devis est communique au client pour validation avant intervention.<br>- Le diagnostic est gratuit si la réparation est effectuee. En cas de refus du devis, des frais de diagnostic peuvent s'appliquer.</p>
<p><b>4. REPARATION</b><br>- Les délais de réparation sont donnes a titre indicatif et dependent de la disponibilité des pièces.<br>- Klikphone utilise des pièces de qualite pour ses réparations.<br>- Une garantie de 3 mois est appliquee sur les réparations effectuees (hors casse, oxydation, mauvaise utilisation).</p>
<p><b>5. RESPONSABILITE</b><br>- Klikphone ne consulte pas et n'accede pas aux donnees presentes dans l'appareil du client.<br>- Klikphone decline toute responsabilite en cas de perte de donnees.<br>- Klikphone decline toute responsabilite en cas de panne apparaissant apres réparation liee a une cause exterieure (oxydation, choc, dysfonctionnement FaceID/TouchID lie au changement d'écran, etc.).</p>
<p><b>6. RETRAIT DE L'APPAREIL</b><br>- L'appareil doit etre retire dans un délai de 30 jours apres notification de fin de réparation.<br>- Passe ce délai, des frais de garde peuvent s'appliquer.<br>- Tout appareil non récupére dans un délai de 6 mois sera considere comme abandonne.</p>
<p><b>7. PAIEMENT</b><br>- Le paiement s'effectue au retrait de l'appareil.<br>- Un acompte peut etre demande pour certaines réparations.</p>
<p style="margin-bottom:0;"><b>KLIKPHONE - 79 Place Saint Léger, 73000 Chambéry - 04 79 60 89 22</b></p>
</div>"""
        st.markdown(cgv_html, unsafe_allow_html=True)
        if st.button("Fermer les CGV", key="close_cgv"):
            st.session_state.show_cgv = False
            st.rerun()
    
    if st.button("ENVOYER LA DEMANDE", type="primary", use_container_width=True):
        if not nom or not prenom or not telephone:
            st.error("Le nom, prénom et téléphone sont obligatoires")
        elif not consent:
            st.error("Veuillez accepter les conditions générales")
        else:
            d = st.session_state.data
            cid = get_or_create_client(nom, telephone, prenom, email)
            code = creer_ticket(cid, d.get("cat",""), d.get("marque",""), d.get("modele",""),
                               d.get("modele_autre",""), d.get("panne",""), d.get("panne_detail",""),
                               d.get("pin",""), d.get("pattern",""), notes)
            st.session_state.done = code
            st.rerun()

# =============================================================================
# INTERFACE STAFF (ACCUEIL) - STYLE PORTAIL STAFF
# =============================================================================
def ui_accueil():
    col1, col2 = st.columns([5, 1])
    with col1:
        st.markdown("<h1 class='page-title'>Liste des Demandes de Réparation</h1>", unsafe_allow_html=True)
    with col2:
        if st.button("Deconnexion", key="logout_acc"):
            st.session_state.mode = None
            st.session_state.auth = False
            st.rerun()
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Demandes", "Nouvelle", "Attestation non-reparabilite", "Config"])
    
    with tab1:
        staff_liste_demandes()
    with tab2:
        staff_nouvelle_demande()
    with tab3:
        staff_attestation()
    with tab4:
        staff_config()

def staff_liste_demandes():
    # Si un ticket est sélectionné, afficher directement le traitement
    if st.session_state.get("edit_id"):
        staff_traiter_demande(st.session_state.edit_id)
        return
    
    # Filtres et tri
    col1, col2, col3, col4, col5 = st.columns([2, 1.5, 1.5, 1.5, 1.5])
    with col1:
        f_statut = st.selectbox("Statut", ["Tous"] + STATUTS, key="f_statut")
    with col2:
        f_code = st.text_input("N Ticket", key="f_code")
    with col3:
        f_tel = st.text_input("Téléphone", key="f_tel")
    with col4:
        f_nom = st.text_input("Nom", key="f_nom")
    with col5:
        tri = st.selectbox("Trier", ["Recent", "Ancien", "Statut"], key="f_tri")
    
    # Recherche
    tickets = chercher_tickets(
        statut=f_statut if f_statut != "Tous" else None,
        code=f_code or None, tel=f_tel or None, nom=f_nom or None
    )
    
    # Appliquer le tri
    if tri == "Ancien":
        tickets = sorted(tickets, key=lambda x: x.get('date_depot', ''))
    elif tri == "Statut":
        ordre_statut = {s: i for i, s in enumerate(STATUTS)}
        tickets = sorted(tickets, key=lambda x: ordre_statut.get(x.get('statut', ''), 99))
    
    # Pagination
    ITEMS_PER_PAGE = 5
    total_pages = max(1, (len(tickets) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE)
    
    if "accueil_page" not in st.session_state:
        st.session_state.accueil_page = 1
    
    current_page = st.session_state.accueil_page
    start_idx = (current_page - 1) * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    tickets_page = tickets[start_idx:end_idx]
    
    st.markdown(f"**{len(tickets)} demande(s)** - Page {current_page}/{total_pages}")
    st.markdown("---")
    
    # En-tete du tableau
    st.markdown("""
    <div style="display:flex; background:#f1f5f9; padding:10px; border-radius:8px; margin-bottom:10px; font-weight:bold; font-size:0.9rem;">
        <div style="flex:1.2;">Ticket</div>
        <div style="flex:1.5;">Client</div>
        <div style="flex:1.5;">Appareil</div>
        <div style="flex:1;">Date</div>
        <div style="flex:1.5;">Statut</div>
        <div style="flex:1;">Message</div>
        <div style="flex:0.8;">Action</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Liste des tickets
    for t in tickets_page:
        status_class = get_status_class(t.get('statut', ''))
        modèle = f"{t.get('marque','')} {t.get('modele','')}"
        if t.get('modele_autre'): modèle += f" ({t['modele_autre']})"
        
        # Message technicien a transmettre ?
        has_message = t.get('commentaire_client')
        
        col1, col2, col3, col4, col5, col6, col7 = st.columns([1.2, 1.5, 1.5, 1, 1.5, 1, 0.8])
        with col1:
            st.markdown(f"**{t['ticket_code']}**")
        with col2:
            st.write(f"{t.get('client_nom','')} {t.get('client_prenom','')[:10]}")
        with col3:
            st.write(modèle[:20])
        with col4:
            st.write(fmt_date(t.get('date_depot',''))[:10])
        with col5:
            st.markdown(f"<span class='status-badge {status_class}'>{t.get('statut','')[:15]}</span>", unsafe_allow_html=True)
        with col6:
            if has_message:
                st.markdown("<span style='color:red; font-weight:bold;'>A TRANSMETTRE</span>", unsafe_allow_html=True)
            else:
                st.write("-")
        with col7:
            if st.button("Ouvrir", key=f"process_{t['id']}"):
                st.session_state.edit_id = t['id']
                st.rerun()
        st.markdown("<hr style='margin:5px 0;border-color:#eee;'>", unsafe_allow_html=True)
    
    # Navigation pagination
    if total_pages > 1:
        st.markdown("---")
        col_prev, col_pages, col_next = st.columns([1, 3, 1])
        with col_prev:
            if current_page > 1:
                if st.button("< Précédent", key="accueil_prev"):
                    st.session_state.accueil_page = current_page - 1
                    st.rerun()
        with col_pages:
            st.markdown(f"<div style='text-align:center;'>Page {current_page} / {total_pages}</div>", unsafe_allow_html=True)
        with col_next:
            if current_page < total_pages:
                if st.button("Suivant >", key="accueil_next"):
                    st.session_state.accueil_page = current_page + 1
                    st.rerun()

def staff_traiter_demande(tid):
    t = get_ticket_full(tid=tid)
    if not t:
        st.error("Demande non trouvée")
        return
    
    # Bouton retour en haut
    col_back, col_title = st.columns([1, 5])
    with col_back:
        if st.button("← Retour", key="close_process", type="secondary"):
            st.session_state.edit_id = None
            st.rerun()
    with col_title:
        st.markdown(f"### Ticket {t['ticket_code']}")
    
    status_class = get_status_class(t.get('statut', ''))
    st.markdown(f"<span class='status-badge {status_class}' style='font-size:1.1rem;'>{t.get('statut','')}</span>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<p class='section-title'>Resume Client</p>", unsafe_allow_html=True)
        
        modèle = f"{t.get('marque','')} {t.get('modele','')}"
        if t.get('modele_autre'): modèle += f" ({t['modele_autre']})"
        panne = t.get('panne', '')
        if t.get('panne_detail'): panne += f" ({t['panne_detail']})"
        
        st.markdown(f"""
        <div class="summary-item"><span class="summary-label">Nom:</span><span class="summary-value">{t.get('client_nom','')} {t.get('client_prenom','')}</span></div>
        <div class="summary-item"><span class="summary-label">Téléphone:</span><span class="summary-value">{t.get('client_tel','')}</span></div>
        <div class="summary-item"><span class="summary-label">Email:</span><span class="summary-value">{t.get('client_email') or 'N/A'}</span></div>
        <div class="summary-item"><span class="summary-label">Appareil:</span><span class="summary-value">{modèle}</span></div>
        <div class="summary-item"><span class="summary-label">Motif:</span><span class="summary-value">{panne}</span></div>
        """, unsafe_allow_html=True)
        
        if t.get('pin') or t.get('pattern'):
            st.markdown(f"""
            <div style="background: #fffbeb; border: 1px solid #fbbf24; border-radius: 6px; padding: 1rem; margin: 1rem 0;">
                <strong>SECURITE</strong><br>
                <div style="margin-top: 0.5rem;">Code PIN: {t.get('pin') or 'Aucun'}</div>
                <div>Schéma: {t.get('pattern') or 'Aucun'}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Notes internes
        st.markdown("<p class='section-title' style='margin-top:1.5rem;'>Notes internes</p>", unsafe_allow_html=True)
        st.text_area("", value=t.get('notes_internes') or "", disabled=True, height=100, key=f"notes_view_{tid}", label_visibility="collapsed")
        
        note = st.text_input("Ajouter une note", key=f"new_note_{tid}")
        if st.button("Ajouter", key=f"add_note_{tid}"):
            if note:
                ajouter_note(tid, note)
                st.success("Note ajoutee")
                st.rerun()
        
        # Commentaire pour le client (du technicien)
        st.markdown("<p class='section-title' style='margin-top:1.5rem;'>Message du technicien (a transmettre au client)</p>", unsafe_allow_html=True)
        comment_client = st.text_area("", value=t.get('commentaire_client') or "", height=80, 
                                      placeholder="Ex: Écran change, test OK. Batterie a surveiller...",
                                      key=f"comment_client_{tid}", label_visibility="collapsed")
        if st.button("Enregistrer message", key=f"save_comment_client_{tid}"):
            update_ticket(tid, commentaire_client=comment_client)
            st.success("Message enregistre!")
            st.rerun()
    
    with col2:
        st.markdown("<p class='section-title'>Informations de Réparation</p>", unsafe_allow_html=True)
        
        # Type de réparation (panne)
        panne_actuelle = t.get('panne', PANNES[0])
        idx_panne = PANNES.index(panne_actuelle) if panne_actuelle in PANNES else 0
        new_panne = st.selectbox("Type de Réparation", PANNES, index=idx_panne, key=f"rep_type_{tid}")
        
        # Personne en charge
        personne = st.text_input("Personne en charge", value=t.get('personne_charge') or "", key=f"personne_{tid}")
        
        # Commentaire interne (notes)
        comment = st.text_area("Commentaire interne", value="", height=80, key=f"comment_{tid}")
        
        # Tarifs
        col_a, col_b = st.columns(2)
        with col_a:
            devis = st.number_input("Devis Estimé (€)", value=float(t.get('devis_estime') or 0), min_value=0.0, step=5.0, key=f"devis_{tid}")
        with col_b:
            tarif = st.number_input("Tarif Final (€)", value=float(t.get('tarif_final') or 0), min_value=0.0, step=5.0, key=f"tarif_{tid}")
        
        acompte = st.number_input("Acompte (€)", value=float(t.get('acompte') or 0), min_value=0.0, step=5.0, key=f"acompte_{tid}")
        
        # Statut
        statut_actuel = t.get('statut', STATUTS[0])
        idx_statut = STATUTS.index(statut_actuel) if statut_actuel in STATUTS else 0
        new_statut = st.selectbox("Statut de la réparation", STATUTS, index=idx_statut, key=f"statut_{tid}")
        
        # Boutons
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("ENREGISTRER", type="primary", use_container_width=True, key=f"save_{tid}"):
                update_ticket(tid, panne=new_panne, personne_charge=personne, 
                             devis_estime=devis, tarif_final=tarif, acompte=acompte)
                if comment:
                    ajouter_note(tid, comment)
                if new_statut != statut_actuel:
                    changer_statut(tid, new_statut)
                st.success("Demande mise à jour !")
                st.rerun()
        with col_btn2:
            if st.button("Ticket Client", use_container_width=True, key=f"print_client_{tid}"):
                st.session_state[f"show_ticket_{tid}"] = "client"
                st.rerun()
        
        if st.button("Ticket Staff", use_container_width=True, key=f"print_staff_{tid}"):
            st.session_state[f"show_ticket_{tid}"] = "staff"
            st.rerun()
        
        # Section Messagerie complete
        st.markdown("---")
        st.markdown("**Contacter le client**")
        
        tel = t.get('client_tel', '')
        email = t.get('client_email', '')
        
        # Messages prédéfinis
        messages = get_messages_predefs(t)
        
        # Afficher le commentaire du technicien s'il existe
        if t.get('commentaire_client'):
            st.markdown("""
            <div style="background: #dbeafe; border: 1px solid #3b82f6; border-radius: 8px; padding: 1rem; margin-bottom: 1rem;">
                <strong>Message du technicien a transmettre:</strong><br>
                <span style="font-style:italic;">{}</span>
            </div>
            """.format(t.get('commentaire_client')), unsafe_allow_html=True)
        
        type_msg = st.selectbox("Message prédéfini", list(messages.keys()), key=f"msg_type_{tid}")
        
        # Mettre a jour le message quand le type change
        msg_key = f"msg_text_{tid}"
        if f"last_msg_type_{tid}" not in st.session_state:
            st.session_state[f"last_msg_type_{tid}"] = type_msg
        
        # Si le type de message a change, mettre a jour la valeur
        if st.session_state[f"last_msg_type_{tid}"] != type_msg:
            st.session_state[f"last_msg_type_{tid}"] = type_msg
            st.session_state[msg_key] = messages[type_msg]
        
        # Valeur par defaut si pas encore definie
        if msg_key not in st.session_state:
            st.session_state[msg_key] = messages[type_msg]
        
        # Zone de texte editable
        msg_custom = st.text_area("Message a envoyer", value=st.session_state[msg_key], height=200, key=msg_key)
        
        if msg_custom:
            st.markdown("**Envoyer via:**")
            col_wa, col_sms, col_email, col_email_direct = st.columns(4)
            
            with col_wa:
                if tel:
                    st.markdown(f"""
                    <a href="{wa_link(tel, msg_custom)}" target="_blank" style="
                        display: block; text-align: center; padding: 10px; 
                        background: #25D366; color: white; border-radius: 8px; 
                        text-decoration: none; font-weight: bold;">
                        WhatsApp
                    </a>
                    """, unsafe_allow_html=True)
                else:
                    st.button("WhatsApp", disabled=True, use_container_width=True)
            
            with col_sms:
                if tel:
                    st.markdown(f"""
                    <a href="{sms_link(tel, msg_custom)}" target="_blank" style="
                        display: block; text-align: center; padding: 10px; 
                        background: #3b82f6; color: white; border-radius: 8px; 
                        text-decoration: none; font-weight: bold;">
                        SMS
                    </a>
                    """, unsafe_allow_html=True)
                else:
                    st.button("SMS", disabled=True, use_container_width=True)
            
            with col_email:
                if email:
                    sujet = f"Réparation {t.get('ticket_code','')} - Klikphone"
                    st.markdown(f"""
                    <a href="{email_link(email, sujet, msg_custom)}" target="_blank" style="
                        display: block; text-align: center; padding: 10px; 
                        background: #6b7280; color: white; border-radius: 8px; 
                        text-decoration: none; font-weight: bold;">
                        Mailto
                    </a>
                    """, unsafe_allow_html=True)
                else:
                    st.button("Mailto", disabled=True, use_container_width=True)
            
            with col_email_direct:
                if email and get_param("SMTP_HOST"):
                    if st.button("Envoyer Email", key=f"send_email_{tid}", type="primary", use_container_width=True):
                        sujet = f"Réparation {t.get('ticket_code','')} - Klikphone"
                        success, result = envoyer_email(email, sujet, msg_custom)
                        if success:
                            st.success("Email envoye!")
                            ajouter_note(tid, f"[EMAIL] Message envoye a {email}")
                        else:
                            st.error(result)
                elif email:
                    st.button("Email (config)", disabled=True, use_container_width=True, help="Configurez SMTP dans Config > Email")
                else:
                    st.button("Email", disabled=True, use_container_width=True)
        
        if not tel and not email:
            st.warning("Aucun moyen de contact disponible")
    
    # Affichage ticket dans popup/dialogue
    if st.session_state.get(f"show_ticket_{tid}") == "client":
        st.markdown("---")
        st.markdown("""
        <div style="background: rgba(0,0,0,0.1); padding: 10px; border-radius: 8px; margin-bottom: 10px;">
            <strong>TICKET CLIENT</strong> - Cliquez sur "IMPRIMER" dans le ticket ci-dessous
        </div>
        """, unsafe_allow_html=True)
        st.components.v1.html(ticket_client_html(t), height=700, scrolling=True)
        if st.button("Fermer", key=f"close_ticket_client_{tid}", type="primary", use_container_width=True):
            del st.session_state[f"show_ticket_{tid}"]
            st.rerun()
    
    if st.session_state.get(f"show_ticket_{tid}") == "staff":
        st.markdown("---")
        st.markdown("""
        <div style="background: rgba(249,115,22,0.1); padding: 10px; border-radius: 8px; margin-bottom: 10px;">
            <strong>TICKET STAFF</strong> - Cliquez sur "IMPRIMER" dans le ticket ci-dessous
        </div>
        """, unsafe_allow_html=True)
        st.components.v1.html(ticket_staff_html(t), height=800, scrolling=True)
        if st.button("Fermer", key=f"close_ticket_staff_{tid}", type="primary", use_container_width=True):
            del st.session_state[f"show_ticket_{tid}"]
            st.rerun()

def staff_attestation():
    """Générer une attestation de non-reparabilite"""
    st.markdown("<p class='section-title'>Attestation de Non-Reparabilite</p>", unsafe_allow_html=True)
    st.markdown("Generez une attestation pour les appareils économiquement irréparables (utile pour les assurances).")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        att_nom = st.text_input("Nom du client *", key="att_nom")
        att_prenom = st.text_input("Prénom du client *", key="att_prenom")
        att_adresse = st.text_input("Adresse du client", key="att_adresse", placeholder="73000 Chambéry")
        att_email = st.text_input("Email du client", key="att_email", placeholder="client@email.com")
    with col2:
        att_marque = st.selectbox("Marque *", ["Apple", "Samsung", "Xiaomi", "Huawei", "Autre"], key="att_marque")
        att_modele = st.text_input("Modèle *", key="att_modele", placeholder="iPhone 11 Pro")
        att_imei = st.text_input("Numéro IMEI / Serie *", key="att_imei", placeholder="353833102642466")
    
    st.markdown("---")
    att_etat = st.text_area("État de l'appareil au moment du depot", key="att_etat", 
                           placeholder="Ex: Chassis arriere endommage et écran fissure")
    att_motif = st.text_area("Motif du depot", key="att_motif",
                            placeholder="Ex: iPhone ayant subi un choc violent")
    att_compte_rendu = st.text_area("Compte rendu du technicien *", key="att_cr",
                                   placeholder="Ex:\n- Afficheur endommage entrainant la perte d'affichage\n- Chassis endommage\n- Carte mere trop endommagee")
    
    st.markdown("---")
    
    if st.button("GENERER L'ATTESTATION", type="primary", use_container_width=True):
        if not att_nom or not att_prenom or not att_modele or not att_imei or not att_compte_rendu:
            st.error("Veuillez remplir tous les champs obligatoires (*)")
        else:
            # Générer l'attestation HTML
            from datetime import datetime
            date_jour = datetime.now().strftime("%d/%m/%Y")
            
            attestation_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; font-size: 12px; margin: 40px; line-height: 1.6; }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .logo {{ font-size: 28px; font-weight: bold; color: #f97316; }}
        .contact {{ font-size: 11px; color: #666; margin-top: 5px; }}
        .titre {{ text-align: center; font-weight: bold; font-size: 16px; text-decoration: underline; margin: 30px 0; }}
        .section {{ margin: 20px 0; }}
        .section-title {{ font-weight: bold; text-decoration: underline; margin-bottom: 10px; }}
        .destinataire {{ margin: 20px 0; padding: 10px; background: #f5f5f5; }}
        ul {{ margin: 10px 0; padding-left: 20px; }}
        .footer {{ margin-top: 40px; font-style: italic; }}
        .signature {{ margin-top: 30px; text-align: right; }}
        .print-btn {{ display: block; width: 200px; margin: 30px auto; padding: 12px; background: #f97316; color: white; border: none; border-radius: 8px; font-size: 14px; cursor: pointer; }}
        .email-btn {{ display: block; width: 200px; margin: 10px auto; padding: 12px; background: #3b82f6; color: white; border: none; border-radius: 8px; font-size: 14px; cursor: pointer; text-decoration: none; text-align: center; }}
        @media print {{ .print-btn, .email-btn {{ display: none; }} }}
    </style>
</head>
<body>
    <div class="header">
        <div class="logo">KLIKPHONE</div>
        <div class="contact">
            79 Place Saint Léger, 73000 Chambéry<br>
            Tel: 04 79 60 89 22 - contact@klikphone.com<br>
            SIREN: 795334523
        </div>
    </div>
    
    <div class="destinataire">
        <u>Attestation delivree a :</u><br>
        <strong>M. {att_nom.upper()} {att_prenom.upper()}</strong><br>
        {att_adresse or "73000 Chambéry"}
    </div>
    
    <div class="titre">COMPTE RENDU TECHNICIEN</div>
    
    <div class="section">
        <p>La societe <strong>Klikphone</strong>, specialiste en réparation de smartphones et tablettes, basee au 79 Place Saint Léger a Chambéry;</p>
        
        <p>Atteste que l'appareil <strong>{att_marque} {att_modele}</strong> comportant le numéro IMEI/Serie suivant: <strong>{att_imei}</strong> a bien ete depose a notre atelier pour réparation.</p>
    </div>
    
    <div class="section">
        <div class="section-title">État de l'appareil au moment du depot :</div>
        <p>{att_etat or "Non precise"}</p>
    </div>
    
    <div class="section">
        <div class="section-title">Motif du depot :</div>
        <p>{att_motif or "Diagnostic demande"}</p>
    </div>
    
    <div class="section">
        <div class="section-title">Compte rendu du technicien :</div>
        <ul>
            {"".join([f"<li>{line.strip()}</li>" for line in att_compte_rendu.split(chr(10)) if line.strip()])}
        </ul>
    </div>
    
    <div class="section">
        <div class="section-title">Estimation des réparations :</div>
        <p><strong>Apres expertise, nous attestons que cet appareil est économiquement irréparable.</strong></p>
    </div>
    
    <div class="section">
        <div class="section-title">Valeur de l'appareil :</div>
        <p>Se referer a la facture d'achat / devis de remplacement</p>
    </div>
    
    <div class="footer">
        <p>Cette attestation fait office de justificatif pour votre assurance.</p>
        <p>Tous nos diagnostics et nos réparations sont garantis et realises par un technicien certifie.</p>
    </div>
    
    <div class="signature">
        Fait a Chambéry, le {date_jour}
    </div>
    
    <button class="print-btn" onclick="window.print()">IMPRIMER L'ATTESTATION</button>
</body>
</html>
"""
            st.session_state.attestation_html = attestation_html
            st.session_state.attestation_email = att_email
            st.success("Attestation générée!")
            st.rerun()
    
    # Afficher l'attestation si générée
    if st.session_state.get("attestation_html"):
        st.markdown("---")
        st.markdown("### Apercu de l'attestation")
        st.components.v1.html(st.session_state.attestation_html, height=800, scrolling=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Nouvelle attestation", key="new_attestation"):
                del st.session_state.attestation_html
                if "attestation_email" in st.session_state:
                    del st.session_state.attestation_email
                st.rerun()
        with col2:
            att_email_saved = st.session_state.get("attestation_email", "")
            if att_email_saved and get_param("SMTP_HOST"):
                if st.button("Envoyer par email", key="send_attestation_email", type="primary"):
                    sujet = "Attestation de non-réparabilité - Klikphone"
                    message = "Bonjour,\n\nVeuillez trouver ci-dessous votre attestation de non-réparabilité.\n\nCordialement,\nL'équipe Klikphone\n04 79 60 89 22"
                    html_attestation = st.session_state.get("attestation_html", "")
                    success, result = envoyer_email(att_email_saved, sujet, message, html_attestation)
                    if success:
                        st.success(f"Email envoyé à {att_email_saved}!")
                    else:
                        st.error(result)
            elif att_email_saved:
                st.info("Configurez SMTP dans Config > Email pour envoyer par email")

def staff_nouvelle_demande():
    st.markdown("<p class='section-title'>Nouvelle demande manuelle</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        prenom = st.text_input("Prénom *", key="n_prenom")
        tel = st.text_input("Téléphone *", key="n_tel")
    with col2:
        nom = st.text_input("Nom *", key="n_nom")
        email = st.text_input("Email", key="n_email")
    
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        cat = st.selectbox("Catégorie", CATEGORIES, key="n_cat")
    with col2:
        marque = st.selectbox("Marque", get_marques(cat), key="n_marque")
    with col3:
        modele = st.selectbox("Modèle", get_modeles(cat, marque), key="n_modele")
    
    modele_autre = ""
    if modele == "Autre" or marque == "Autre":
        modele_autre = st.text_input("Précisez le modèle", key="n_modele_autre")
    
    imei = st.text_input("IMEI / Numéro de série (optionnel)", key="n_imei", placeholder="Ex: 353833102642466")
    
    panne = st.selectbox("Problème", PANNES, key="n_panne")
    panne_detail = ""
    if panne in ["Autre", "Diagnostic"]:
        panne_detail = st.text_area("Détails", key="n_panne_detail")
    
    col1, col2 = st.columns(2)
    with col1:
        pin = st.text_input("Code PIN", type="password", key="n_pin")
    with col2:
        pattern = st.text_input("Schéma (ex: 1-2-3)", key="n_pattern")
    
    col1, col2 = st.columns(2)
    with col1:
        devis = st.number_input("Devis estimé (€)", min_value=0.0, step=5.0, key="n_devis")
    with col2:
        acompte = st.number_input("Acompte (€)", min_value=0.0, step=5.0, key="n_acompte")
    
    notes = st.text_area("Notes", key="n_notes")
    
    if st.button("CRÉER LA DEMANDE", type="primary", use_container_width=True):
        if not nom or not prenom or not tel:
            st.error("Nom, prénom et téléphone obligatoires")
        else:
            cid = get_or_create_client(nom, tel, prenom, email)
            code = creer_ticket(cid, cat, marque, modèle, modele_autre, panne, panne_detail, pin, pattern, notes, imei)
            t = get_ticket(code=code)
            if t and (devis or acompte):
                update_ticket(t['id'], devis_estime=devis, acompte=acompte)
            st.success(f"Demande créée : {code}")

def staff_config():
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Boutique", "Email", "Messages", "Catalogue", "Sécurité"])
    
    with tab1:
        st.markdown("### Informations de la boutique")
        nom = st.text_input("Nom boutique", value=get_param("NOM_BOUTIQUE") or "Klikphone")
        adresse = st.text_input("Adresse", value=get_param("ADRESSE_BOUTIQUE") or "79 Place Saint Léger, 73000 Chambéry")
        tel = st.text_input("Téléphone", value=get_param("TEL_BOUTIQUE") or "04 79 60 89 22")
        email_boutique = st.text_input("Email boutique", value=get_param("EMAIL_BOUTIQUE") or "contact@klikphone.com")
        horaires = st.text_input("Horaires", value=get_param("HORAIRES_BOUTIQUE") or "Lundi-Samedi 10h-19h")
        url = st.text_input("URL suivi (QR code)", value=get_param("URL_SUIVI"))
        
        st.markdown("---")
        st.markdown("### Conditions générales (ticket)")
        cgv_ticket = st.text_area("Conditions affichées sur le ticket", 
            value=get_param("CGV_TICKET") or """- Klikphone ne consulte pas et n'accède pas aux données présentes dans votre appareil.
- Une perte de données reste possible — pensez à sauvegarder.
- Klikphone décline toute responsabilité en cas de perte de données ou de panne apparaissant après réparation (oxydation, choc, FaceID, etc.).""",
            height=120)
        
        if st.button("Enregistrer", key="save_config", type="primary"):
            set_param("NOM_BOUTIQUE", nom)
            set_param("ADRESSE_BOUTIQUE", adresse)
            set_param("TEL_BOUTIQUE", tel)
            set_param("EMAIL_BOUTIQUE", email_boutique)
            set_param("HORAIRES_BOUTIQUE", horaires)
            set_param("URL_SUIVI", url)
            set_param("CGV_TICKET", cgv_ticket)
            st.success("Configuration enregistrée!")
    
    with tab2:
        st.markdown("### Configuration Email (SMTP)")
        st.markdown("Pour envoyer des emails directement depuis l'application")
        
        smtp_host = st.text_input("Serveur SMTP", value=get_param("SMTP_HOST"), placeholder="smtp.gmail.com")
        smtp_port = st.text_input("Port", value=get_param("SMTP_PORT") or "587", placeholder="587")
        smtp_user = st.text_input("Email / Utilisateur", value=get_param("SMTP_USER"), placeholder="votre@email.com")
        smtp_pass = st.text_input("Mot de passe", value=get_param("SMTP_PASS"), type="password")
        smtp_from = st.text_input("Email expéditeur (optionnel)", value=get_param("SMTP_FROM"), placeholder="contact@klikphone.com")
        smtp_from_name = st.text_input("Nom expéditeur", value=get_param("SMTP_FROM_NAME") or "Klikphone")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Enregistrer config email", key="save_smtp", type="primary"):
                set_param("SMTP_HOST", smtp_host)
                set_param("SMTP_PORT", smtp_port)
                set_param("SMTP_USER", smtp_user)
                set_param("SMTP_PASS", smtp_pass)
                set_param("SMTP_FROM", smtp_from)
                set_param("SMTP_FROM_NAME", smtp_from_name)
                st.success("Configuration email enregistrée!")
        
        with col2:
            if st.button("Tester l'envoi", key="test_smtp"):
                if smtp_host and smtp_user:
                    success, msg = envoyer_email(smtp_user, "Test Klikphone", "Ceci est un email de test depuis l'application Klikphone SAV.")
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)
                else:
                    st.warning("Remplissez d'abord la configuration")
        
        st.markdown("---")
        st.markdown("""
        **Aide configuration:**
        - **Gmail**: smtp.gmail.com, port 587, activer "Mots de passe d'application"
        - **OVH**: ssl0.ovh.net, port 587
        - **Outlook**: smtp.office365.com, port 587
        """)
    
    with tab3:
        st.markdown("### Messages prédéfinis personnalisés")
        st.markdown("Personnalisez les messages envoyés aux clients. Variables disponibles: `{prenom}`, `{marque}`, `{modele}`, `{code}`, `{montant}`")
        
        msg_recu = st.text_area("Message: Appareil reçu", 
            value=get_param("MSG_APPAREIL_RECU") or "", 
            placeholder="Laissez vide pour utiliser le message par défaut",
            height=100)
        
        msg_pret = st.text_area("Message: Appareil prêt", 
            value=get_param("MSG_APPAREIL_PRET") or "", 
            placeholder="Laissez vide pour utiliser le message par défaut",
            height=100)
        
        msg_non_reparable = st.text_area("Message: Non réparable", 
            value=get_param("MSG_NON_REPARABLE") or "", 
            placeholder="Laissez vide pour utiliser le message par défaut",
            height=100)
        
        signature = st.text_area("Signature des messages", 
            value=get_param("SIGNATURE_MSG") or "Cordialement,\nL'équipe Klikphone\n04 79 60 89 22",
            height=80)
        
        if st.button("Enregistrer messages", key="save_messages", type="primary"):
            set_param("MSG_APPAREIL_RECU", msg_recu)
            set_param("MSG_APPAREIL_PRET", msg_pret)
            set_param("MSG_NON_REPARABLE", msg_non_reparable)
            set_param("SIGNATURE_MSG", signature)
            st.success("Messages enregistrés!")
    
    with tab4:
        st.markdown("### Ajouter une marque")
        col1, col2 = st.columns(2)
        with col1:
            cat_m = st.selectbox("Catégorie", CATEGORIES, key="cat_marque")
            new_m = st.text_input("Nouvelle marque", key="new_marque")
        with col2:
            if st.button("Ajouter marque", key="add_marque"):
                if new_m and ajouter_marque(cat_m, new_m):
                    st.success("Marque ajoutée!")
                    st.rerun()
        
        st.markdown("---")
        st.markdown("### Ajouter un modèle")
        col1, col2 = st.columns(2)
        with col1:
            cat_mo = st.selectbox("Catégorie", CATEGORIES, key="cat_modele")
            marque_mo = st.selectbox("Marque", get_marques(cat_mo), key="marque_modele")
            new_mo = st.text_input("Nouveau modèle", key="new_modele")
        with col2:
            if st.button("Ajouter modèle", key="add_modele"):
                if new_mo and ajouter_modele(cat_mo, marque_mo, new_mo):
                    st.success("Modèle ajouté!")
                    st.rerun()
        
        st.markdown("---")
        st.markdown("### Types de pannes")
        st.markdown("Pannes actuelles: " + ", ".join(PANNES[:5]) + "...")
        new_panne = st.text_input("Nouvelle panne (avec description)", placeholder="Ex: Caméra floue (photos pas nettes)")
        if st.button("Ajouter panne", key="add_panne"):
            st.info("Pour ajouter des pannes, modifiez la liste PANNES dans le code source.")
    
    with tab5:
        st.markdown("### Codes PIN d'accès")
        pin_acc = st.text_input("PIN Accueil", type="password", value=get_param("PIN_ACCUEIL"))
        pin_tech = st.text_input("PIN Technicien", type="password", value=get_param("PIN_TECH"))
        if st.button("Enregistrer PIN", key="save_pin", type="primary"):
            set_param("PIN_ACCUEIL", pin_acc)
            set_param("PIN_TECH", pin_tech)
            st.success("PIN mis à jour!")

# =============================================================================
# INTERFACE TECHNICIEN
# =============================================================================
def ui_tech():
    col1, col2 = st.columns([5, 1])
    with col1:
        st.markdown("<h1 class='page-title'>Espace Technicien</h1>", unsafe_allow_html=True)
    with col2:
        if st.button("Deconnexion", key="logout_tech"):
            st.session_state.mode = None
            st.session_state.auth = False
            st.rerun()
    
    # Si un ticket est sélectionné, afficher directement le detail
    if st.session_state.get("tech_selected"):
        tech_detail_ticket(st.session_state.tech_selected)
        return
    
    # Filtres et tri
    col_f1, col_f2, col_f3 = st.columns([2, 2, 2])
    with col_f1:
        filtre_statut = st.selectbox("Filtrer par statut", ["Tous"] + STATUTS, key="tech_filtre_statut")
    with col_f2:
        tri = st.selectbox("Trier par", ["Plus recent", "Plus ancien", "Statut", "Client"], key="tech_tri")
    with col_f3:
        recherche = st.text_input("Rechercher", placeholder="Ticket, nom, tel...", key="tech_recherche")
    
    st.markdown("---")
    
    # Récupérer les tickets
    if filtre_statut == "Tous":
        tickets = chercher_tickets()
    else:
        tickets = chercher_tickets(statut=filtre_statut)
    
    # Filtrer par recherche
    if recherche:
        recherche_lower = recherche.lower()
        tickets = [t for t in tickets if 
                   recherche_lower in t.get('ticket_code', '').lower() or
                   recherche_lower in t.get('client_nom', '').lower() or
                   recherche_lower in t.get('client_prenom', '').lower() or
                   recherche_lower in t.get('client_tel', '').lower()]
    
    # Trier
    if tri == "Plus ancien":
        tickets = sorted(tickets, key=lambda x: x.get('date_depot', ''))
    elif tri == "Statut":
        ordre_statut = {s: i for i, s in enumerate(STATUTS)}
        tickets = sorted(tickets, key=lambda x: ordre_statut.get(x.get('statut', ''), 99))
    elif tri == "Client":
        tickets = sorted(tickets, key=lambda x: x.get('client_nom', '').lower())
    
    # Pagination
    ITEMS_PER_PAGE = 5
    total_pages = max(1, (len(tickets) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE)
    
    if "tech_page" not in st.session_state:
        st.session_state.tech_page = 1
    
    current_page = st.session_state.tech_page
    start_idx = (current_page - 1) * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    tickets_page = tickets[start_idx:end_idx]
    
    st.markdown(f"**{len(tickets)} réparation(s)** - Page {current_page}/{total_pages}")
    
    # En-tete du tableau
    st.markdown("""
    <div style="display:flex; background:#f1f5f9; padding:10px; border-radius:8px; margin-bottom:10px; font-weight:bold;">
        <div style="flex:1.5;">Ticket</div>
        <div style="flex:2;">Client</div>
        <div style="flex:2;">Appareil</div>
        <div style="flex:1.5;">Statut</div>
        <div style="flex:1;">Action</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Affichage en liste avec boutons
    for t in tickets_page:
        tid = t['id']
        status_class = get_status_class(t.get('statut', ''))
        modèle = f"{t.get('marque','')} {t.get('modele','')}"
        if t.get('modele_autre'): modèle += f" ({t['modele_autre']})"
        
        # Message technicien en attente?
        has_message = t.get('commentaire_client')
        
        col1, col2, col3, col4, col5 = st.columns([1.5, 2, 2, 1.5, 1])
        with col1:
            st.markdown(f"**{t['ticket_code']}**")
        with col2:
            st.write(f"{t.get('client_nom','')} {t.get('client_prenom','')}")
        with col3:
            st.write(modèle[:25])
        with col4:
            st.markdown(f"<span class='status-badge {status_class}'>{t.get('statut','')[:15]}</span>", unsafe_allow_html=True)
        with col5:
            if st.button("Ouvrir", key=f"tech_open_{tid}", use_container_width=True):
                st.session_state.tech_selected = tid
                st.rerun()
        
        st.markdown("<hr style='margin:5px 0; border-color:#eee;'>", unsafe_allow_html=True)
    
    # Navigation pagination
    if total_pages > 1:
        st.markdown("---")
        col_prev, col_pages, col_next = st.columns([1, 3, 1])
        with col_prev:
            if current_page > 1:
                if st.button("< Précédent", key="tech_prev"):
                    st.session_state.tech_page = current_page - 1
                    st.rerun()
        with col_pages:
            st.markdown(f"<div style='text-align:center;'>Page {current_page} / {total_pages}</div>", unsafe_allow_html=True)
        with col_next:
            if current_page < total_pages:
                if st.button("Suivant >", key="tech_next"):
                    st.session_state.tech_page = current_page + 1
                    st.rerun()

def tech_detail_ticket(tid):
    t = get_ticket_full(tid=tid)
    if not t:
        st.error("Ticket non trouve")
        return
    
    # Bouton retour en haut
    col_back, col_title = st.columns([1, 5])
    with col_back:
        if st.button("← Retour", key="tech_close_detail", type="secondary"):
            del st.session_state.tech_selected
            st.rerun()
    with col_title:
        st.markdown(f"### Ticket {t['ticket_code']}")
    
    status_class = get_status_class(t.get('statut', ''))
    st.markdown(f"<span class='status-badge {status_class}' style='font-size:1.1rem;'>{t.get('statut','')}</span>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Infos client
        modèle = f"{t.get('marque','')} {t.get('modele','')}"
        if t.get('modele_autre'): modèle += f" ({t['modele_autre']})"
        panne = t.get('panne', '')
        if t.get('panne_detail'): panne += f" ({t['panne_detail']})"
        
        st.markdown(f"""
        **Client:** {t.get('client_nom','')} {t.get('client_prenom','')}<br>
        **Tel:** {t.get('client_tel','')}<br>
        **Appareil:** {modèle}<br>
        **Problème:** {panne}
        """, unsafe_allow_html=True)
        
        # Sécurité
        st.markdown(f"""
        <div style="background: #fffbeb; border: 1px solid #fbbf24; border-radius: 6px; padding: 0.75rem; margin: 0.5rem 0;">
            <strong>Code PIN:</strong> {t.get('pin') or 'Aucun'}<br>
            <strong>Schéma:</strong> {t.get('pattern') or 'Aucun'}
        </div>
        """, unsafe_allow_html=True)
        
        # Notes
        if t.get('notes_internes'):
            st.markdown("**Notes:**")
            st.text_area("", value=t.get('notes_internes', ''), height=100, disabled=True, key=f"tech_notes_view_{tid}", label_visibility="collapsed")
    
    with col2:
        # Changer statut
        st.markdown("**Changer le statut:**")
        statut_actuel = t.get('statut', STATUTS[0])
        for s in STATUTS:
            btn_type = "primary" if s == "Rendu au client" else "secondary"
            disabled = (s == statut_actuel)
            if st.button(s, key=f"tech_status_{tid}_{s}", use_container_width=True, disabled=disabled, type=btn_type if s == "Rendu au client" else "secondary"):
                changer_statut(tid, s)
                st.success(f"Statut mis a jour: {s}")
                st.rerun()
    
    st.markdown("---")
    
    # Section commentaires technicien
    st.markdown("**Ajouter une note interne:**")
    col_note, col_btn = st.columns([4, 1])
    with col_note:
        note_tech = st.text_input("Note technique", placeholder="Ex: Pièce a commander, problème identifie...", key=f"tech_comment_{tid}", label_visibility="collapsed")
    with col_btn:
        if st.button("Ajouter", key=f"tech_add_comment_{tid}", type="primary"):
            if note_tech:
                ajouter_note(tid, f"[TECH] {note_tech}")
                st.success("Note ajoutee!")
                st.rerun()
    
    # Message pour le client (a transmettre par l'accueil)
    st.markdown("---")
    st.markdown("**Message a transmettre au client (via accueil):**")
    comment_client = st.text_area("", value=t.get('commentaire_client') or "", height=80, 
                                  placeholder="Ex: Écran remplace, test OK. Attention batterie faible...",
                                  key=f"tech_client_comment_{tid}", label_visibility="collapsed")
    if st.button("Enregistrer le message", key=f"tech_save_client_comment_{tid}"):
        update_ticket(tid, commentaire_client=comment_client)
        st.success("Message enregistré pour l'accueil!")
        st.rerun()
    
    st.markdown("---")
    
    # Section réparation supplémentaire
    st.markdown("**Réparation supplémentaire:**")
    col_rep, col_prix = st.columns([3, 1])
    with col_rep:
        rep_supp = st.text_input("Description de la réparation supplémentaire", 
                                 value=t.get('reparation_supp') or "",
                                 placeholder="Ex: Remplacement nappe Face ID, Soudure connecteur...",
                                 key=f"tech_rep_supp_{tid}")
    with col_prix:
        prix_supp = st.number_input("Prix (€)", min_value=0.0, step=5.0,
                                    value=float(t.get('prix_supp') or 0),
                                    key=f"tech_prix_supp_{tid}")
    
    if st.button("Enregistrer réparation supp.", key=f"tech_save_rep_supp_{tid}"):
        update_ticket(tid, reparation_supp=rep_supp, prix_supp=prix_supp)
        st.success("Réparation supplémentaire enregistrée!")
        st.rerun()
    
    st.markdown("---")
    
    # Section messagerie
    st.markdown("**Contacter le client:**")
    tel = t.get('client_tel', '')
    email = t.get('client_email', '')
    
    messages = get_messages_predefs(t)
    type_msg = st.selectbox("Message prédéfini", list(messages.keys()), key=f"tech_msg_type_{tid}")
    
    # Mettre a jour le message quand le type change
    tech_msg_key = f"tech_msg_text_{tid}"
    if f"tech_last_msg_type_{tid}" not in st.session_state:
        st.session_state[f"tech_last_msg_type_{tid}"] = type_msg
    
    if st.session_state[f"tech_last_msg_type_{tid}"] != type_msg:
        st.session_state[f"tech_last_msg_type_{tid}"] = type_msg
        st.session_state[tech_msg_key] = messages[type_msg]
    
    if tech_msg_key not in st.session_state:
        st.session_state[tech_msg_key] = messages[type_msg]
    
    msg_custom = st.text_area("Message", value=st.session_state[tech_msg_key], height=200, key=tech_msg_key)
    
    if msg_custom:
        col_wa, col_sms, col_email = st.columns(3)
        with col_wa:
            if tel:
                st.markdown(f'<a href="{wa_link(tel, msg_custom)}" target="_blank" style="display:block;text-align:center;padding:10px;background:#25D366;color:white;border-radius:8px;text-decoration:none;font-weight:bold;">WhatsApp</a>', unsafe_allow_html=True)
        with col_sms:
            if tel:
                st.markdown(f'<a href="{sms_link(tel, msg_custom)}" target="_blank" style="display:block;text-align:center;padding:10px;background:#3b82f6;color:white;border-radius:8px;text-decoration:none;font-weight:bold;">SMS</a>', unsafe_allow_html=True)
        with col_email:
            if email:
                sujet = f"Réparation {t.get('ticket_code','')} - Klikphone"
                st.markdown(f'<a href="{email_link(email, sujet, msg_custom)}" target="_blank" style="display:block;text-align:center;padding:10px;background:#6b7280;color:white;border-radius:8px;text-decoration:none;font-weight:bold;">Email</a>', unsafe_allow_html=True)

# =============================================================================
# PAGE SUIVI CLIENT
# =============================================================================
def ui_suivi():
    st.markdown("""
    <div class="klik-header">
        <span class="klik-title">Klikphone</span>
    </div>
    <p class="klik-subtitle">Suivi de votre réparation</p>
    """, unsafe_allow_html=True)
    
    params = st.query_params
    code_url = params.get("ticket", "")
    
    col1, col2 = st.columns(2)
    with col1:
        code = st.text_input("N° de ticket", value=code_url, placeholder="KP-000001")
    with col2:
        tel = st.text_input("Votre téléphone", placeholder="06 12 34 56 78")
    
    if st.button("RECHERCHER", type="primary", use_container_width=True):
        if code and tel:
            t = get_ticket_full(code=code)
            tel_clean = "".join(filter(str.isdigit, tel))
            client_tel_clean = "".join(filter(str.isdigit, t.get('client_tel', ''))) if t else ""
            
            if t and tel_clean == client_tel_clean:
                status_class = get_status_class(t.get('statut', ''))
                modèle = f"{t.get('marque','')} {t.get('modele','')}"
                if t.get('modele_autre'): modèle += f" ({t['modele_autre']})"
                
                st.markdown(f"""
                <div style="background:white; padding:1.5rem; border-radius:12px; margin-top:1.5rem; border:1px solid #e5e7eb;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;">
                        <h3 style="margin:0;">{t['ticket_code']}</h3>
                        <span class="status-badge {status_class}">{t.get('statut','')}</span>
                    </div>
                    <p><strong>Appareil:</strong> {modèle}</p>
                    <p><strong>Depose le:</strong> {fmt_date(t.get('date_depot',''))}</p>
                    <p><strong>Derniere mise à jour:</strong> {fmt_date(t.get('date_maj',''))}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Barre de progression
                progress = {"En attente de diagnostic": 25, "En cours de réparation": 50, 
                           "Réparation terminée": 100, "Clôturé": 100}.get(t.get('statut',''), 0)
                st.progress(progress / 100)
            else:
                st.error("Ticket non trouvé ou numéro de téléphone incorrect")
        else:
            st.warning("Veuillez remplir les deux champs")
    
    st.markdown("---")
    if st.button("Retour à l'accueil"):
        st.session_state.mode = None
        st.rerun()

# =============================================================================
# ÉCRAN D'ACCUEIL
# =============================================================================
def ui_home():
    # Logo et en-tete
    st.markdown(f"""
    <div style="text-align:center; padding:2rem 0;">
        <img src="data:image/png;base64,{LOGO_B64}" style="width:80px; height:80px; margin-bottom:1rem;">
        <div style="background: linear-gradient(135deg, #fb923c, #f97316); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3rem; font-weight: 800; letter-spacing: -2px;">KLIKPHONE</div>
        <p style="color:#6b7280; font-size:0.95rem; margin-top:0.5rem;">Spécialiste Apple - 79 Place Saint Léger, Chambéry</p>
        <p style="color:#6b7280; font-size:0.9rem;">04 79 60 89 22</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("CLIENT\n\nDéposer un appareil", key="go_client", use_container_width=True, type="primary"):
            st.session_state.mode = "client"
            st.rerun()
    
    with col2:
        if st.button("ACCUEIL\n\nGestion des demandes", key="go_accueil", use_container_width=True):
            st.session_state.mode = "auth_accueil"
            st.rerun()
    
    with col3:
        if st.button("TECHNICIEN\n\nSuivi réparations", key="go_tech", use_container_width=True):
            st.session_state.mode = "auth_tech"
            st.rerun()
    
    # Style pour les gros boutons
    st.markdown("""
    <style>
    div[data-testid="stHorizontalBlock"] > div > div > div > div > button {
        height: 150px !important;
        font-size: 18px !important;
        font-weight: bold !important;
        border-radius: 16px !important;
        white-space: pre-wrap !important;
    }
    div[data-testid="stHorizontalBlock"] > div:nth-child(1) button {
        background: linear-gradient(135deg, #fb923c, #f97316) !important;
        border: none !important;
    }
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) button {
        background: linear-gradient(135deg, #3b82f6, #2563eb) !important;
        border: none !important;
        color: white !important;
    }
    div[data-testid="stHorizontalBlock"] > div:nth-child(3) button {
        background: linear-gradient(135deg, #10b981, #059669) !important;
        border: none !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_left, col_center, col_right = st.columns([1, 2, 1])
    with col_center:
        if st.button("Suivre ma réparation", use_container_width=True, key="go_suivi"):
            st.session_state.mode = "suivi"
            st.rerun()

def ui_auth(mode):
    titre = "Accès Accueil" if mode == "accueil" else "Accès Technicien"
    pin_key = "PIN_ACCUEIL" if mode == "accueil" else "PIN_TECH"
    target = "accueil" if mode == "accueil" else "tech"
    
    st.markdown(f"""
    <div class="klik-header">
        <span class="klik-title">Klikphone</span>
    </div>
    <p class="klik-subtitle">{titre}</p>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        pin = st.text_input("Code PIN", type="password", placeholder="••••")
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Retour", use_container_width=True):
                st.session_state.mode = None
                st.rerun()
        with col_b:
            if st.button("Valider", type="primary", use_container_width=True):
                if pin == get_param(pin_key):
                    st.session_state.mode = target
                    st.session_state.auth = True
                    st.rerun()
                else:
                    st.error("Code PIN incorrect")

# =============================================================================
# MAIN
# =============================================================================
def main():
    init_db()
    load_css()
    
    if "mode" not in st.session_state: st.session_state.mode = None
    if "auth" not in st.session_state: st.session_state.auth = False
    
    mode = st.session_state.mode
    
    if mode is None: ui_home()
    elif mode == "client": ui_client()
    elif mode == "auth_accueil": ui_auth("accueil")
    elif mode == "auth_tech": ui_auth("tech")
    elif mode == "accueil":
        if st.session_state.auth: ui_accueil()
        else: st.session_state.mode = "auth_accueil"; st.rerun()
    elif mode == "tech":
        if st.session_state.auth: ui_tech()
        else: st.session_state.mode = "auth_tech"; st.rerun()
    elif mode == "suivi": ui_suivi()

if __name__ == "__main__":
    main()
