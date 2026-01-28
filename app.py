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
# CSS DESIGN SYSTEM - SAAS PREMIUM (Notion/Stripe/Linear inspired)
# =============================================================================
def load_css():
    st.markdown("""
<style>
/* ============================================
   KLIKPHONE SAV - DESIGN SYSTEM v2.0
   Inspiration: Notion + Stripe + Linear
   Minimal • Clean • Professional
   ============================================ */

/* === TYPOGRAPHY === */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* === DESIGN TOKENS === */
:root {
    /* Brand */
    --brand-50: #fff7ed;
    --brand-100: #ffedd5;
    --brand-200: #fed7aa;
    --brand-300: #fdba74;
    --brand-400: #fb923c;
    --brand-500: #f97316;
    --brand-600: #ea580c;
    
    /* Neutrals */
    --neutral-0: #ffffff;
    --neutral-50: #fafafa;
    --neutral-100: #f5f5f5;
    --neutral-200: #e5e5e5;
    --neutral-300: #d4d4d4;
    --neutral-400: #a3a3a3;
    --neutral-500: #737373;
    --neutral-600: #525252;
    --neutral-700: #404040;
    --neutral-800: #262626;
    --neutral-900: #171717;
    
    /* Semantic */
    --success-light: #ecfdf5;
    --success: #10b981;
    --success-dark: #059669;
    --warning-light: #fffbeb;
    --warning: #f59e0b;
    --warning-dark: #d97706;
    --error-light: #fef2f2;
    --error: #ef4444;
    --error-dark: #dc2626;
    --info-light: #eff6ff;
    --info: #3b82f6;
    --info-dark: #2563eb;
    
    /* Spacing (4px base) */
    --sp-1: 4px;
    --sp-2: 8px;
    --sp-3: 12px;
    --sp-4: 16px;
    --sp-5: 20px;
    --sp-6: 24px;
    --sp-8: 32px;
    --sp-10: 40px;
    --sp-12: 48px;
    
    /* Radius */
    --r-sm: 6px;
    --r-md: 8px;
    --r-lg: 12px;
    --r-xl: 16px;
    --r-full: 9999px;
    
    /* Shadows */
    --shadow-xs: 0 1px 2px 0 rgb(0 0 0 / 0.05);
    --shadow-sm: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
    --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
    --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
    
    /* Typography */
    --font: 'Inter', -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
    --text-xs: 0.75rem;
    --text-sm: 0.875rem;
    --text-base: 1rem;
    --text-lg: 1.125rem;
    --text-xl: 1.25rem;
    --text-2xl: 1.5rem;
    --text-3xl: 2rem;
}

/* === RESET === */
*, *::before, *::after {
    font-family: var(--font) !important;
    box-sizing: border-box;
}

/* === STREAMLIT OVERRIDES === */
.stApp {
    background: var(--neutral-50) !important;
}

#MainMenu, footer, header, .stDeployButton,
[data-testid="stToolbar"], [data-testid="stDecoration"],
.viewerBadge_container__r5tak { 
    display: none !important; 
}

.main .block-container {
    padding: var(--sp-6) var(--sp-6) !important;
    max-width: 1400px !important;
}

/* === TYPOGRAPHY === */
h1, h2, h3 {
    color: var(--neutral-900) !important;
    font-weight: 600 !important;
    letter-spacing: -0.02em !important;
}

.page-header {
    margin-bottom: var(--sp-6);
}

.page-title {
    font-size: var(--text-2xl);
    font-weight: 700;
    color: var(--neutral-900);
    margin: 0;
    letter-spacing: -0.025em;
}

.page-subtitle {
    font-size: var(--text-sm);
    color: var(--neutral-500);
    margin-top: var(--sp-1);
}

.section-header {
    display: flex;
    align-items: center;
    gap: var(--sp-2);
    font-size: var(--text-base);
    font-weight: 600;
    color: var(--neutral-800);
    margin-bottom: var(--sp-4);
    padding-bottom: var(--sp-3);
    border-bottom: 1px solid var(--neutral-200);
}

/* === CARDS === */
.card {
    background: var(--neutral-0);
    border: 1px solid var(--neutral-200);
    border-radius: var(--r-lg);
    padding: var(--sp-5);
    transition: all 0.15s ease;
}

.card:hover {
    border-color: var(--neutral-300);
    box-shadow: var(--shadow-sm);
}

.card-elevated {
    background: var(--neutral-0);
    border: 1px solid var(--neutral-200);
    border-radius: var(--r-xl);
    padding: var(--sp-6);
    box-shadow: var(--shadow-sm);
}

/* KPI Cards */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: var(--sp-4);
    margin-bottom: var(--sp-6);
}

.kpi-card {
    background: var(--neutral-0);
    border: 1px solid var(--neutral-200);
    border-radius: var(--r-lg);
    padding: var(--sp-5);
    transition: all 0.15s ease;
}

.kpi-card:hover {
    border-color: var(--brand-300);
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}

.kpi-label {
    font-size: var(--text-xs);
    font-weight: 500;
    color: var(--neutral-500);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: var(--sp-2);
}

.kpi-value {
    font-size: var(--text-3xl);
    font-weight: 700;
    color: var(--neutral-900);
    line-height: 1;
}

.kpi-value.brand { color: var(--brand-500); }
.kpi-value.success { color: var(--success); }
.kpi-value.warning { color: var(--warning); }
.kpi-value.info { color: var(--info); }

/* === STATUS BADGES === */
.badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 10px;
    border-radius: var(--r-full);
    font-size: var(--text-xs);
    font-weight: 500;
    white-space: nowrap;
}

.badge::before {
    content: '';
    width: 6px;
    height: 6px;
    border-radius: 50%;
}

.status-diagnostic {
    background: var(--warning-light);
    color: var(--warning-dark);
}
.status-diagnostic::before { background: var(--warning); }

.status-encours {
    background: var(--info-light);
    color: var(--info-dark);
}
.status-encours::before { background: var(--info); }

.status-termine {
    background: var(--success-light);
    color: var(--success-dark);
}
.status-termine::before { background: var(--success); }

.status-rendu {
    background: var(--success);
    color: white;
}
.status-rendu::before { background: rgba(255,255,255,0.6); }

.status-cloture {
    background: var(--neutral-100);
    color: var(--neutral-600);
}
.status-cloture::before { background: var(--neutral-400); }

/* === TICKET LIST === */
.ticket-list {
    display: flex;
    flex-direction: column;
    gap: var(--sp-2);
}

.ticket-row {
    display: flex;
    align-items: center;
    gap: var(--sp-4);
    padding: var(--sp-4);
    background: var(--neutral-0);
    border: 1px solid var(--neutral-200);
    border-radius: var(--r-md);
    transition: all 0.15s ease;
    cursor: pointer;
}

.ticket-row:hover {
    border-color: var(--brand-300);
    background: var(--brand-50);
    transform: translateX(4px);
}

.ticket-code {
    font-family: 'SF Mono', Monaco, 'Courier New', monospace !important;
    font-size: var(--text-sm);
    font-weight: 600;
    color: var(--brand-600);
    min-width: 100px;
}

.ticket-client {
    font-weight: 500;
    color: var(--neutral-900);
    flex: 1;
}

.ticket-device {
    font-size: var(--text-sm);
    color: var(--neutral-500);
    flex: 1;
}

.ticket-date {
    font-size: var(--text-xs);
    color: var(--neutral-400);
    min-width: 80px;
}

.ticket-alert {
    background: var(--error-light);
    color: var(--error-dark);
    padding: 2px 8px;
    border-radius: var(--r-sm);
    font-size: var(--text-xs);
    font-weight: 600;
}

/* === TABLE HEADER === */
.table-header {
    display: flex;
    align-items: center;
    gap: var(--sp-4);
    padding: var(--sp-3) var(--sp-4);
    background: var(--neutral-100);
    border-radius: var(--r-md);
    margin-bottom: var(--sp-2);
    font-size: var(--text-xs);
    font-weight: 600;
    color: var(--neutral-500);
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* === BUTTONS === */
.stButton > button {
    font-family: var(--font) !important;
    font-weight: 500 !important;
    font-size: var(--text-sm) !important;
    padding: 8px 16px !important;
    border-radius: var(--r-md) !important;
    transition: all 0.15s ease !important;
    border: none !important;
}

.stButton > button[kind="primary"],
.stButton > button[data-testid="baseButton-primary"] {
    background: var(--brand-500) !important;
    color: white !important;
}

.stButton > button[kind="primary"]:hover,
.stButton > button[data-testid="baseButton-primary"]:hover {
    background: var(--brand-600) !important;
    transform: translateY(-1px) !important;
    box-shadow: var(--shadow-md) !important;
}

.stButton > button[kind="secondary"],
.stButton > button[data-testid="baseButton-secondary"] {
    background: var(--neutral-0) !important;
    color: var(--neutral-700) !important;
    border: 1px solid var(--neutral-300) !important;
}

.stButton > button[kind="secondary"]:hover,
.stButton > button[data-testid="baseButton-secondary"]:hover {
    background: var(--neutral-50) !important;
    border-color: var(--neutral-400) !important;
}

/* === FORM INPUTS === */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    border: 1px solid var(--neutral-300) !important;
    border-radius: var(--r-md) !important;
    padding: 10px 12px !important;
    font-size: var(--text-sm) !important;
    background: var(--neutral-0) !important;
    transition: all 0.15s ease !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--brand-400) !important;
    box-shadow: 0 0 0 3px var(--brand-100) !important;
    outline: none !important;
}

.stTextInput > div > div > input::placeholder {
    color: var(--neutral-400) !important;
}

.stSelectbox > div > div {
    border: 1px solid var(--neutral-300) !important;
    border-radius: var(--r-md) !important;
    background: var(--neutral-0) !important;
}

.stSelectbox > div > div > div {
    padding: 8px 12px !important;
    font-size: var(--text-sm) !important;
    min-height: 40px !important;
}

.stSelectbox > div > div:focus-within {
    border-color: var(--brand-400) !important;
    box-shadow: 0 0 0 3px var(--brand-100) !important;
}

/* Labels */
.stTextInput > label, .stTextArea > label,
.stSelectbox > label, .stNumberInput > label {
    font-size: var(--text-sm) !important;
    font-weight: 500 !important;
    color: var(--neutral-700) !important;
}

/* === TABS === */
.stTabs [data-baseweb="tab-list"] {
    background: var(--neutral-100) !important;
    padding: 4px !important;
    border-radius: var(--r-lg) !important;
    gap: 4px !important;
}

.stTabs [data-baseweb="tab"] {
    padding: 8px 16px !important;
    font-size: var(--text-sm) !important;
    font-weight: 500 !important;
    color: var(--neutral-600) !important;
    background: transparent !important;
    border-radius: var(--r-md) !important;
    border: none !important;
}

.stTabs [data-baseweb="tab"]:hover {
    color: var(--neutral-900) !important;
    background: var(--neutral-50) !important;
}

.stTabs [aria-selected="true"] {
    background: var(--neutral-0) !important;
    color: var(--neutral-900) !important;
    box-shadow: var(--shadow-sm) !important;
}

.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] {
    display: none !important;
}

/* === EXPANDER === */
.streamlit-expanderHeader {
    font-size: var(--text-sm) !important;
    font-weight: 600 !important;
    color: var(--neutral-700) !important;
    background: var(--neutral-50) !important;
    border-radius: var(--r-md) !important;
    padding: var(--sp-3) var(--sp-4) !important;
    border: 1px solid var(--neutral-200) !important;
}

.streamlit-expanderContent {
    border: 1px solid var(--neutral-200) !important;
    border-top: none !important;
    border-radius: 0 0 var(--r-md) var(--r-md) !important;
    padding: var(--sp-4) !important;
    background: var(--neutral-0) !important;
}

/* === PROGRESS === */
.stProgress > div > div {
    background: var(--neutral-200) !important;
    border-radius: var(--r-full) !important;
    height: 8px !important;
}

.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--brand-400), var(--brand-500)) !important;
    border-radius: var(--r-full) !important;
}

/* === METRICS === */
[data-testid="stMetricValue"] {
    font-size: var(--text-2xl) !important;
    font-weight: 700 !important;
    color: var(--neutral-900) !important;
}

[data-testid="stMetricLabel"] {
    font-size: var(--text-sm) !important;
    font-weight: 500 !important;
    color: var(--neutral-500) !important;
}

/* === ALERTS === */
.stAlert {
    border-radius: var(--r-md) !important;
    border: none !important;
    padding: var(--sp-4) !important;
}

.stSuccess { background: var(--success-light) !important; }
.stWarning { background: var(--warning-light) !important; }
.stError { background: var(--error-light) !important; }
.stInfo { background: var(--info-light) !important; }

/* === DIVIDERS === */
hr {
    border: none !important;
    height: 1px !important;
    background: var(--neutral-200) !important;
    margin: var(--sp-5) 0 !important;
}

/* === FILTER BAR === */
.filter-bar {
    background: var(--neutral-0);
    border: 1px solid var(--neutral-200);
    border-radius: var(--r-lg);
    padding: var(--sp-4);
    margin-bottom: var(--sp-4);
}

/* === NAV HEADER === */
.nav-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--sp-4) var(--sp-5);
    background: var(--neutral-0);
    border-bottom: 1px solid var(--neutral-200);
    margin: calc(-1 * var(--sp-6)) calc(-1 * var(--sp-6)) var(--sp-5);
}

.nav-logo {
    display: flex;
    align-items: center;
    gap: var(--sp-3);
}

.nav-logo-text {
    font-size: var(--text-xl);
    font-weight: 700;
    color: var(--brand-600);
    letter-spacing: -0.02em;
}

.nav-actions {
    display: flex;
    align-items: center;
    gap: var(--sp-2);
}

/* === DETAIL SECTIONS === */
.detail-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: var(--sp-4);
}

.detail-card {
    background: var(--neutral-0);
    border: 1px solid var(--neutral-200);
    border-radius: var(--r-lg);
    padding: var(--sp-5);
}

.detail-card-header {
    font-size: var(--text-sm);
    font-weight: 600;
    color: var(--neutral-800);
    margin-bottom: var(--sp-4);
    padding-bottom: var(--sp-3);
    border-bottom: 1px solid var(--neutral-100);
    display: flex;
    align-items: center;
    gap: var(--sp-2);
}

.detail-row {
    display: flex;
    justify-content: space-between;
    padding: var(--sp-2) 0;
    border-bottom: 1px solid var(--neutral-100);
}

.detail-row:last-child { border-bottom: none; }

.detail-label {
    font-size: var(--text-sm);
    color: var(--neutral-500);
}

.detail-value {
    font-size: var(--text-sm);
    font-weight: 500;
    color: var(--neutral-900);
}

/* === PRICE BOX === */
.price-box {
    background: linear-gradient(135deg, var(--brand-50), var(--neutral-0));
    border: 2px solid var(--brand-200);
    border-radius: var(--r-lg);
    padding: var(--sp-5);
}

.price-total {
    font-size: var(--text-3xl);
    font-weight: 700;
    color: var(--brand-600);
}

.price-label {
    font-size: var(--text-sm);
    color: var(--neutral-500);
}

/* === EMPTY STATE === */
.empty-state {
    text-align: center;
    padding: var(--sp-12) var(--sp-6);
}

.empty-icon {
    font-size: 48px;
    margin-bottom: var(--sp-4);
    opacity: 0.4;
}

.empty-title {
    font-size: var(--text-lg);
    font-weight: 600;
    color: var(--neutral-700);
    margin-bottom: var(--sp-2);
}

.empty-text {
    font-size: var(--text-sm);
    color: var(--neutral-500);
}

/* === RESPONSIVE === */
@media (max-width: 768px) {
    .main .block-container {
        padding: var(--sp-4) !important;
    }
    
    .detail-grid {
        grid-template-columns: 1fr;
    }
    
    .kpi-grid {
        grid-template-columns: repeat(2, 1fr);
    }
    
    .ticket-row {
        flex-wrap: wrap;
    }
    
    .nav-header {
        flex-direction: column;
        gap: var(--sp-3);
    }
}

/* === ANIMATIONS === */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}

.fade-in {
    animation: fadeIn 0.2s ease-out;
}

/* === PRINT === */
@media print {
    .stButton, .nav-header, .stTabs [data-baseweb="tab-list"] {
        display: none !important;
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
        societe TEXT,
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
        commande_piece INTEGER DEFAULT 0,
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
    
    # Table commandes de pièces
    c.execute("""CREATE TABLE IF NOT EXISTS commandes_pieces (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_id INTEGER,
        description TEXT,
        fournisseur TEXT,
        reference TEXT,
        prix REAL,
        statut TEXT DEFAULT 'A commander',
        date_commande TEXT,
        date_reception TEXT,
        notes TEXT,
        date_creation TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (ticket_id) REFERENCES tickets(id))""")
    
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
    
    # Migration: ajouter societe dans clients
    try:
        c.execute("ALTER TABLE clients ADD COLUMN societe TEXT")
    except:
        pass
    
    # Migration: ajouter commande_piece dans tickets
    try:
        c.execute("ALTER TABLE tickets ADD COLUMN commande_piece INTEGER DEFAULT 0")
    except:
        pass
    
    conn.commit()
    
    # Params défaut
    params = {
        "PIN_ACCUEIL": "2626", "PIN_TECH": "2626",
        "TEL_BOUTIQUE": "04 79 60 89 22",
        "ADRESSE_BOUTIQUE": "79 Place Saint Léger, 73000 Chambéry",
        "NOM_BOUTIQUE": "Klikphone",
        "HORAIRES_BOUTIQUE": "Lundi-Samedi 10h-19h",
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
def get_or_create_client(nom, tel, prenom="", email="", societe=""):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT id FROM clients WHERE telephone=?", (tel,))
    r = c.fetchone()
    if r:
        cid = r["id"]
        c.execute("UPDATE clients SET nom=?, prenom=?, email=?, societe=? WHERE id=?", (nom, prenom, email, societe, cid))
    else:
        c.execute("INSERT INTO clients (nom, prenom, telephone, email, societe) VALUES (?,?,?,?,?)", (nom, prenom, tel, email, societe))
        cid = c.lastrowid
    conn.commit()
    conn.close()
    return cid

def get_all_clients():
    """Récupère tous les clients"""
    conn = get_db()
    c = conn.cursor()
    c.execute("""SELECT c.*, COUNT(t.id) as nb_tickets 
                 FROM clients c 
                 LEFT JOIN tickets t ON c.id = t.client_id 
                 GROUP BY c.id 
                 ORDER BY c.nom, c.prenom""")
    clients = [dict(row) for row in c.fetchall()]
    conn.close()
    return clients

def get_client_by_id(client_id):
    """Récupère un client par son ID"""
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM clients WHERE id=?", (client_id,))
    r = c.fetchone()
    conn.close()
    return dict(r) if r else None

def update_client(client_id, nom=None, prenom=None, telephone=None, email=None, societe=None):
    """Met à jour les informations d'un client"""
    conn = get_db()
    c = conn.cursor()
    updates = []
    params = []
    if nom is not None: updates.append("nom=?"); params.append(nom)
    if prenom is not None: updates.append("prenom=?"); params.append(prenom)
    if telephone is not None: updates.append("telephone=?"); params.append(telephone)
    if email is not None: updates.append("email=?"); params.append(email)
    if societe is not None: updates.append("societe=?"); params.append(societe)
    if updates:
        params.append(client_id)
        c.execute(f"UPDATE clients SET {', '.join(updates)} WHERE id=?", params)
        conn.commit()
    conn.close()

def search_clients(query):
    """Recherche des clients par nom, prénom, téléphone ou société"""
    conn = get_db()
    c = conn.cursor()
    q = f"%{query}%"
    c.execute("""SELECT * FROM clients 
                 WHERE nom LIKE ? OR prenom LIKE ? OR telephone LIKE ? OR societe LIKE ?
                 ORDER BY nom, prenom LIMIT 20""", (q, q, q, q))
    clients = [dict(row) for row in c.fetchall()]
    conn.close()
    return clients

# Fonctions commandes de pièces
FOURNISSEURS = ["Utopya", "Piece2mobile", "Amazon", "Mobilax", "Autre"]

def get_commandes_pieces(ticket_id=None, statut=None):
    """Récupère les commandes de pièces"""
    conn = get_db()
    c = conn.cursor()
    q = """SELECT cp.*, t.ticket_code, t.marque, t.modele, 
           c.nom as client_nom, c.prenom as client_prenom
           FROM commandes_pieces cp
           LEFT JOIN tickets t ON cp.ticket_id = t.id
           LEFT JOIN clients c ON t.client_id = c.id
           WHERE 1=1"""
    params = []
    if ticket_id:
        q += " AND cp.ticket_id = ?"
        params.append(ticket_id)
    if statut:
        q += " AND cp.statut = ?"
        params.append(statut)
    q += " ORDER BY cp.date_creation DESC"
    c.execute(q, params)
    commandes = [dict(row) for row in c.fetchall()]
    conn.close()
    return commandes

def ajouter_commande_piece(ticket_id, description, fournisseur, reference="", prix=0, notes=""):
    """Ajoute une commande de pièce"""
    conn = get_db()
    c = conn.cursor()
    c.execute("""INSERT INTO commandes_pieces 
                 (ticket_id, description, fournisseur, reference, prix, notes, statut)
                 VALUES (?, ?, ?, ?, ?, ?, 'A commander')""",
              (ticket_id, description, fournisseur, reference, prix, notes))
    conn.commit()
    conn.close()

def update_commande_piece(commande_id, statut=None, date_commande=None, date_reception=None, notes=None):
    """Met à jour une commande de pièce"""
    conn = get_db()
    c = conn.cursor()
    updates = []
    params = []
    if statut: updates.append("statut=?"); params.append(statut)
    if date_commande: updates.append("date_commande=?"); params.append(date_commande)
    if date_reception: updates.append("date_reception=?"); params.append(date_reception)
    if notes is not None: updates.append("notes=?"); params.append(notes)
    if updates:
        params.append(commande_id)
        c.execute(f"UPDATE commandes_pieces SET {', '.join(updates)} WHERE id=?", params)
        conn.commit()
    conn.close()

def delete_commande_piece(commande_id):
    """Supprime une commande de pièce"""
    conn = get_db()
    c = conn.cursor()
    c.execute("DELETE FROM commandes_pieces WHERE id=?", (commande_id,))
    conn.commit()
    conn.close()

def creer_ticket(client_id, cat, marque, modele, modele_autre, panne, panne_detail, pin, pattern, notes, imei="", commande_piece=0):
    conn = get_db()
    c = conn.cursor()
    c.execute("""INSERT INTO tickets 
        (client_id, categorie, marque, modele, modele_autre, imei, panne, panne_detail, pin, pattern, notes_client, commande_piece, statut) 
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,'En attente de diagnostic')""", 
        (client_id, cat, marque, modele, modele_autre, imei, panne, panne_detail, pin, pattern, notes, commande_piece))
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
        
        # Corps en HTML si fourni (retirer le bouton imprimer)
        if html_content:
            # Retirer le bouton imprimer du HTML envoyé par email
            html_clean = html_content.replace('onclick="window.print()"', 'style="display:none"')
            html_clean = html_clean.replace('IMPRIMER', '')
            msg.attach(MIMEText(html_clean, 'html', 'utf-8'))
        
        # Connexion et envoi
        server = smtplib.SMTP(smtp_host, int(smtp_port or 587))
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_from or smtp_user, destinataire, msg.as_string())
        server.quit()
        
        return True, "Email envoyé avec succès!"
    except Exception as e:
        return False, f"Erreur d'envoi: {str(e)}"

def envoyer_email_avec_pdf(destinataire, sujet, message, pdf_bytes, filename="document.pdf"):
    """Envoie un email avec une pièce jointe PDF"""
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.mime.application import MIMEApplication
    
    smtp_host = get_param("SMTP_HOST")
    smtp_port = get_param("SMTP_PORT")
    smtp_user = get_param("SMTP_USER")
    smtp_pass = get_param("SMTP_PASS")
    smtp_from = get_param("SMTP_FROM")
    smtp_from_name = get_param("SMTP_FROM_NAME") or "Klikphone"
    
    if not smtp_host or not smtp_user or not smtp_pass:
        return False, "Configuration SMTP incomplète."
    
    try:
        msg = MIMEMultipart()
        msg['From'] = f"{smtp_from_name} <{smtp_from or smtp_user}>"
        msg['To'] = destinataire
        msg['Subject'] = sujet
        
        msg.attach(MIMEText(message, 'plain', 'utf-8'))
        
        # Ajouter le PDF en pièce jointe
        pdf_part = MIMEApplication(pdf_bytes, _subtype='pdf')
        pdf_part.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(pdf_part)
        
        server = smtplib.SMTP(smtp_host, int(smtp_port or 587))
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_from or smtp_user, destinataire, msg.as_string())
        server.quit()
        
        return True, "Email avec PDF envoyé!"
    except Exception as e:
        return False, f"Erreur: {str(e)}"

def html_to_pdf(html_content):
    """Convertit HTML en PDF (utilise une approche simple avec base64)"""
    try:
        # Nettoyer le HTML - retirer les boutons d'impression
        html_clean = html_content.replace('onclick="window.print()"', 'style="display:none !important"')
        html_clean = html_clean.replace('>IMPRIMER', ' style="display:none !important">IMPRIMER')
        
        # Essayer avec weasyprint si disponible
        try:
            from weasyprint import HTML
            pdf_bytes = HTML(string=html_clean).write_pdf()
            return pdf_bytes
        except ImportError:
            pass
        
        # Essayer avec pdfkit si disponible
        try:
            import pdfkit
            pdf_bytes = pdfkit.from_string(html_clean, False)
            return pdf_bytes
        except ImportError:
            pass
        
        # Fallback: retourner None et envoyer en HTML
        return None
    except Exception as e:
        return None

def export_clients_excel():
    """Exporte la liste des clients en Excel"""
    try:
        import io
        clients = get_all_clients()
        
        # Créer le fichier Excel avec openpyxl
        try:
            from openpyxl import Workbook
            from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
            
            wb = Workbook()
            ws = wb.active
            ws.title = "Clients Klikphone"
            
            # Style header
            header_font = Font(bold=True, color="FFFFFF")
            header_fill = PatternFill(start_color="F97316", end_color="F97316", fill_type="solid")
            header_alignment = Alignment(horizontal="center", vertical="center")
            thin_border = Border(
                left=Side(style='thin'),
                right=Side(style='thin'),
                top=Side(style='thin'),
                bottom=Side(style='thin')
            )
            
            # Headers
            headers = ["Nom", "Prénom", "Société", "Téléphone", "Email", "Date création", "Nb tickets"]
            for col, header in enumerate(headers, 1):
                cell = ws.cell(row=1, column=col, value=header)
                cell.font = header_font
                cell.fill = header_fill
                cell.alignment = header_alignment
                cell.border = thin_border
            
            # Données
            for row_idx, client in enumerate(clients, 2):
                ws.cell(row=row_idx, column=1, value=client.get('nom', '')).border = thin_border
                ws.cell(row=row_idx, column=2, value=client.get('prenom', '')).border = thin_border
                ws.cell(row=row_idx, column=3, value=client.get('societe', '') or '').border = thin_border
                ws.cell(row=row_idx, column=4, value=client.get('telephone', '')).border = thin_border
                ws.cell(row=row_idx, column=5, value=client.get('email', '')).border = thin_border
                ws.cell(row=row_idx, column=6, value=client.get('date_creation', '')[:10] if client.get('date_creation') else '').border = thin_border
                ws.cell(row=row_idx, column=7, value=client.get('nb_tickets', 0)).border = thin_border
            
            # Ajuster largeur colonnes
            ws.column_dimensions['A'].width = 20
            ws.column_dimensions['B'].width = 20
            ws.column_dimensions['C'].width = 25
            ws.column_dimensions['D'].width = 15
            ws.column_dimensions['E'].width = 30
            ws.column_dimensions['F'].width = 15
            ws.column_dimensions['G'].width = 12
            
            # Sauvegarder dans un buffer
            output = io.BytesIO()
            wb.save(output)
            output.seek(0)
            return output.getvalue(), "clients_klikphone.xlsx"
            
        except ImportError:
            # Fallback: créer un CSV
            import csv
            output = io.StringIO()
            writer = csv.writer(output, delimiter=';')
            writer.writerow(["Nom", "Prénom", "Société", "Téléphone", "Email", "Date création", "Nb tickets"])
            for client in clients:
                writer.writerow([
                    client.get('nom', ''),
                    client.get('prenom', ''),
                    client.get('societe', '') or '',
                    client.get('telephone', ''),
                    client.get('email', ''),
                    client.get('date_creation', '')[:10] if client.get('date_creation') else '',
                    client.get('nb_tickets', 0)
                ])
            return output.getvalue().encode('utf-8-sig'), "clients_klikphone.csv"
            
    except Exception as e:
        return None, str(e)

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
    devis = float(t.get('devis_estime') or 0)
    tarif = float(t.get('tarif_final') or 0)
    prix_supp = float(t.get('prix_supp') or 0)
    reparation_supp = t.get('reparation_supp', '')
    
    # Paramètres dynamiques de la boutique
    adresse = get_param("ADRESSE_BOUTIQUE") or "79 Place Saint Léger, 73000 Chambéry"
    horaires = get_param("HORAIRES_BOUTIQUE") or "Lundi-Samedi 10h-19h"
    tel_boutique = get_param("TEL_BOUTIQUE") or "04 79 60 89 22"
    nom_boutique = get_param("NOM_BOUTIQUE") or "Klikphone"
    
    # Calcul du montant TOTAL (inclut réparation supplémentaire)
    total_devis = devis + prix_supp
    total_tarif = tarif + prix_supp if tarif > 0 else 0
    
    # Formater le montant final
    if total_tarif > 0:
        montant = f"{total_tarif:.2f} €"
    elif total_devis > 0:
        montant = f"{total_devis:.2f} €"
    else:
        montant = "Nous consulter"
    
    # Formater le devis (inclut prix_supp)
    devis_txt = f"{total_devis:.2f} €" if total_devis > 0 else "Nous consulter"
    
    # Détail si réparation supplémentaire
    detail_supp = ""
    if reparation_supp and prix_supp > 0:
        detail_supp = f"\n(dont {reparation_supp}: {prix_supp:.2f} €)"
    
    messages = {
        "-- Choisir un message --": "",
        
        "Appareil reçu": f"""Bonjour {prénom},

Nous vous informons que votre appareil {marque} {modèle} a bien été réceptionné à la boutique {nom_boutique}.

Numéro de suivi : {code}

Nous allons procéder au diagnostic et reviendrons vers vous dans les plus brefs délais.

Cordialement,
L'équipe {nom_boutique}
{tel_boutique}""",

        "Diagnostic en cours": f"""Bonjour {prénom},

Nous vous informons que le diagnostic de votre appareil {marque} {modèle} est actuellement en cours à la boutique {nom_boutique}.

Numéro de suivi : {code}

Nous reviendrons vers vous rapidement avec le résultat du diagnostic.

Cordialement,
L'équipe {nom_boutique}
{tel_boutique}""",

        "Devis à valider": f"""Bonjour {prénom},

Le diagnostic de votre appareil {marque} {modèle} est terminé.

Devis de réparation : {devis_txt}{detail_supp}

Merci de nous confirmer votre accord pour procéder à la réparation en répondant à ce message ou en nous appelant.

Cordialement,
L'équipe {nom_boutique}
{tel_boutique}""",

        "En cours de réparation": f"""Bonjour {prénom},

Nous vous informons que votre appareil {marque} {modèle} est actuellement en cours de réparation à la boutique {nom_boutique}.

Numéro de suivi : {code}

Nous vous prévenons dès que la réparation sera terminée.

Cordialement,
L'équipe {nom_boutique}
{tel_boutique}""",

        "Attente de pièce": f"""Bonjour {prénom},

Nous vous informons que nous sommes en attente d'une pièce pour la réparation de votre appareil {marque} {modèle}.

Délai estimé : 2 à 5 jours ouvrables.

Nous vous prévenons dès réception de la pièce.

Cordialement,
L'équipe {nom_boutique}
{tel_boutique}""",

        "Appareil prêt": f"""Bonjour {prénom},

Nous vous informons que votre appareil {marque} {modèle} est prêt à être récupéré à la boutique {nom_boutique}.

Montant à régler : {montant}{detail_supp}

Adresse : {adresse}
Horaires : {horaires}

N'oubliez pas votre pièce d'identité.

Cordialement,
L'équipe {nom_boutique}
{tel_boutique}""",

        "Relance récupération": f"""Bonjour {prénom},

Nous vous rappelons que votre appareil {marque} {modèle} est prêt et vous attend à la boutique {nom_boutique} depuis plusieurs jours.

Merci de venir le récupérer dans les meilleurs délais.

Adresse : {adresse}
Horaires : {horaires}

Cordialement,
L'équipe {nom_boutique}
{tel_boutique}""",

        "Non réparable": f"""Bonjour {prénom},

Après diagnostic approfondi, nous avons le regret de vous informer que votre appareil {marque} {modèle} n'est malheureusement pas réparable.

Vous pouvez venir le récupérer à la boutique. Aucun frais ne vous sera facturé pour le diagnostic.

Nous restons à votre disposition pour toute question.

Cordialement,
L'équipe {nom_boutique}
{tel_boutique}""",

        "Rappel RDV": f"""Bonjour {prénom},

Nous vous rappelons votre rendez-vous à la boutique {nom_boutique} pour votre appareil {marque} {modèle}.

Adresse : {adresse}

À bientôt !

L'équipe {nom_boutique}
{tel_boutique}""",

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
    
    # URL de suivi avec le numéro de ticket
    url_suivi = get_param("URL_SUIVI") or "https://klikphone-sav.streamlit.app"
    ticket_code = t.get('ticket_code', '')
    url_suivi_ticket = f"{url_suivi}?ticket={ticket_code}"
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=100x100&data={urllib.parse.quote(url_suivi_ticket)}"
    
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

def ticket_devis_facture_html(t, doc_type="devis"):
    """Génère un ticket DEVIS ou RÉCAPITULATIF DE PAIEMENT selon le type"""
    modele_txt = t.get("modele", "")
    if t.get("modele_autre"): modele_txt += f" ({t['modele_autre']})"
    
    panne = t.get('panne', '')
    if panne == "Autre" and t.get('panne_detail'):
        panne = t.get('panne_detail')
    elif t.get('panne_detail'):
        panne += f" ({t['panne_detail']})"
    
    # Tarifs
    devis_val = t.get('devis_estime') or 0
    acompte_val = t.get('acompte') or 0
    rep_supp = t.get('reparation_supp') or ""
    prix_supp = t.get('prix_supp') or 0
    
    # Calculs TVA (prix TTC)
    total_ttc = devis_val + prix_supp
    total_ht = total_ttc / 1.20
    tva = total_ttc - total_ht
    reste = max(0, total_ttc - acompte_val)
    
    # Type de document
    is_facture = doc_type == "facture"
    doc_title = "RÉCAPITULATIF DE PAIEMENT" if is_facture else "DEVIS"
    doc_color = "#16a34a" if is_facture else "#3b82f6"
    doc_num = f"R-{t['ticket_code']}" if is_facture else f"D-{t['ticket_code']}"
    
    # Ligne réparation supplémentaire
    rep_supp_line = ""
    if rep_supp:
        rep_supp_line = f"""
        <tr>
            <td style="padding:10px; border-bottom:1px solid #e5e7eb;">Réparation supplémentaire<br><small style="color:#666;">{rep_supp}</small></td>
            <td style="padding:10px; text-align:right; border-bottom:1px solid #e5e7eb;">{prix_supp:.2f} €</td>
        </tr>
        """
    
    # Date du document
    from datetime import datetime
    date_doc = datetime.now().strftime("%d/%m/%Y")
    
    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: 'Segoe UI', Arial, sans-serif; 
            font-size: 12px; 
            padding: 20px;
            background: #f5f5f5;
        }}
        .document {{ 
            max-width: 400px; 
            margin: 0 auto; 
            background: linear-gradient(180deg, #ffffff 0%, #fafafa 100%);
            border-radius: 16px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.15);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, {doc_color} 0%, {doc_color}dd 100%);
            color: white;
            padding: 20px;
            text-align: center;
        }}
        .header img {{ width: 50px; height: 50px; margin-bottom: 10px; }}
        .header h1 {{ font-size: 24px; font-weight: 800; margin: 5px 0; letter-spacing: 2px; }}
        .header .doc-num {{ font-size: 14px; opacity: 0.9; margin-top: 5px; }}
        .header .date {{ font-size: 11px; opacity: 0.8; margin-top: 5px; }}
        
        .company-info {{
            background: #f8f9fa;
            padding: 15px;
            text-align: center;
            font-size: 11px;
            color: #666;
            border-bottom: 1px solid #e5e7eb;
        }}
        
        .client-section {{
            padding: 15px 20px;
            border-bottom: 1px solid #e5e7eb;
        }}
        .client-section h3 {{
            font-size: 11px;
            text-transform: uppercase;
            color: #999;
            margin-bottom: 8px;
            letter-spacing: 1px;
        }}
        .client-section p {{ margin: 3px 0; color: #333; }}
        
        .details-section {{
            padding: 15px 20px;
        }}
        .details-section h3 {{
            font-size: 11px;
            text-transform: uppercase;
            color: #999;
            margin-bottom: 10px;
            letter-spacing: 1px;
        }}
        
        .items-table {{
            width: 100%;
            border-collapse: collapse;
        }}
        .items-table th {{
            background: #f3f4f6;
            padding: 10px;
            text-align: left;
            font-size: 10px;
            text-transform: uppercase;
            color: #666;
            letter-spacing: 0.5px;
        }}
        .items-table th:last-child {{ text-align: right; }}
        
        .totals {{
            background: linear-gradient(180deg, #f8f9fa 0%, #f3f4f6 100%);
            padding: 15px 20px;
            margin-top: 10px;
        }}
        .total-line {{
            display: flex;
            justify-content: space-between;
            padding: 5px 0;
            font-size: 12px;
        }}
        .total-line.small {{ color: #666; font-size: 11px; }}
        .total-line.main {{
            font-size: 16px;
            font-weight: 700;
            border-top: 2px solid {doc_color};
            padding-top: 10px;
            margin-top: 5px;
        }}
        .total-line.reste {{
            font-size: 18px;
            font-weight: 800;
            color: #dc2626;
            border-top: 2px dashed #dc2626;
            padding-top: 10px;
            margin-top: 10px;
        }}
        
        .footer {{
            background: #1f2937;
            color: white;
            padding: 15px;
            text-align: center;
            font-size: 10px;
        }}
        .footer p {{ margin: 3px 0; opacity: 0.8; }}
        
        .print-btn {{
            display: block;
            width: calc(100% - 40px);
            margin: 20px;
            padding: 12px;
            background: linear-gradient(135deg, {doc_color} 0%, {doc_color}dd 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
        }}
        .print-btn:hover {{ opacity: 0.9; }}
        
        @media print {{
            .print-btn {{ display: none; }}
            body {{ padding: 0; background: white; }}
            .document {{ box-shadow: none; max-width: 100%; }}
        }}
    </style>
</head>
<body>
    <div class="document">
        <div class="header">
            <img src="data:image/png;base64,{LOGO_B64}" alt="Klikphone">
            <h1>{doc_title}</h1>
            <div class="doc-num">{doc_num}</div>
            <div class="date">Date: {date_doc}</div>
        </div>
        
        <div class="company-info">
            <strong>KLIKPHONE</strong> - Spécialiste Apple<br>
            79 Place Saint Léger, 73000 Chambéry<br>
            Tél: 04 79 60 89 22 | SIRET: XXX XXX XXX XXXXX
        </div>
        
        <div class="client-section">
            <h3>Client</h3>
            <p><strong>{t.get('client_nom','')} {t.get('client_prenom','')}</strong></p>
            <p>Tél: {t.get('client_tel','')}</p>
            {f"<p>Email: {t.get('client_email')}</p>" if t.get('client_email') else ""}
        </div>
        
        <div class="client-section">
            <h3>Appareil</h3>
            <p><strong>{t.get('marque','')} {modele_txt}</strong></p>
            {f"<p>IMEI: {t.get('imei')}</p>" if t.get('imei') else ""}
        </div>
        
        <div class="details-section">
            <h3>Prestations</h3>
            <table class="items-table">
                <thead>
                    <tr>
                        <th>Description</th>
                        <th>Prix TTC</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="padding:10px; border-bottom:1px solid #e5e7eb;">{panne}</td>
                        <td style="padding:10px; text-align:right; border-bottom:1px solid #e5e7eb;">{devis_val:.2f} €</td>
                    </tr>
                    {rep_supp_line}
                </tbody>
            </table>
        </div>
        
        <div class="totals">
            <div class="total-line main">
                <span>Total TTC</span>
                <span>{total_ttc:.2f} €</span>
            </div>
            <div class="total-line small">
                <span>dont HT</span>
                <span>{total_ht:.2f} €</span>
            </div>
            <div class="total-line small">
                <span>dont TVA (20%)</span>
                <span>{tva:.2f} €</span>
            </div>
            <div class="total-line">
                <span>Acompte versé</span>
                <span style="color:#16a34a;">- {acompte_val:.2f} €</span>
            </div>
            <div class="total-line reste">
                <span>RESTE À PAYER</span>
                <span>{reste:.2f} €</span>
            </div>
        </div>
        
        <div class="footer">
            <p>{"Ce devis est valable 30 jours." if not is_facture else "Merci pour votre confiance !"}</p>
            <p>{"Devis non contractuel - Prix susceptibles de modification après diagnostic." if not is_facture else ""}</p>
            <p style="margin-top:8px; font-weight:bold; color:#dc2626;">{"" if not is_facture else "⚠️ Ce ticket ne fait pas office de facture."}</p>
        </div>
        
        <button class="print-btn" onclick="window.print()">IMPRIMER {doc_title}</button>
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
    
    # Société (facultatif)
    societe = st.text_input("Société (facultatif)", placeholder="Nom de l'entreprise si professionnel")
    
    notes = st.text_area("Remarques", placeholder="Accessoires laisses, precisions sur le problème...")
    
    # Option commande de pièce
    commande_piece = st.checkbox("⚙️ Pièce à commander pour cette réparation", help="Cochez si une pièce doit être commandée")
    
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
            cid = get_or_create_client(nom, telephone, prenom, email, societe)
            code = creer_ticket(cid, d.get("cat",""), d.get("marque",""), d.get("modele",""),
                               d.get("modele_autre",""), d.get("panne",""), d.get("panne_detail",""),
                               d.get("pin",""), d.get("pattern",""), notes, "", 1 if commande_piece else 0)
            
            # Si commande pièce cochée, créer une entrée dans commandes_pieces
            if commande_piece:
                # Récupérer le ticket pour avoir l'ID
                t = get_ticket(code=code)
                if t:
                    modele_txt = f"{d.get('marque','')} {d.get('modele','')}"
                    if d.get('modele_autre'): modele_txt += f" ({d['modele_autre']})"
                    panne_txt = d.get('panne', '') or d.get('panne_detail', '') or 'Pièce à préciser'
                    ajouter_commande_piece(t['id'], f"Pièce pour {panne_txt} - {modele_txt}", "A définir", "", 0, "Commande créée depuis totem client")
            
            st.session_state.done = code
            st.rerun()

# =============================================================================
# INTERFACE STAFF (ACCUEIL) - STYLE PORTAIL STAFF
# =============================================================================
def ui_accueil():
    # === HEADER NAV ===
    st.markdown(f"""
    <div class="nav-header">
        <div class="nav-logo">
            <img src="data:image/png;base64,{LOGO_B64}" style="width:36px;height:36px;">
            <span class="nav-logo-text">KLIKPHONE</span>
            <span style="color:var(--neutral-400);font-size:var(--text-sm);margin-left:8px;">SAV Manager</span>
        </div>
        <div class="nav-actions" id="nav-btns"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Boutons navigation
    col_spacer, col_tech, col_logout = st.columns([8, 1, 1])
    with col_tech:
        if st.button("🔧 Tech", key="goto_tech", type="secondary", use_container_width=True):
            st.session_state.mode = "tech"
            st.rerun()
    with col_logout:
        if st.button("Sortir", key="logout_acc", type="secondary", use_container_width=True):
            st.session_state.mode = None
            st.session_state.auth = False
            st.rerun()
    
    # === KPI CARDS ===
    all_tickets = chercher_tickets()
    commandes_attente = get_commandes_pieces(statut="A commander")
    nb_total = len(all_tickets)
    nb_attente = len([t for t in all_tickets if t.get('statut') == "En attente de diagnostic"])
    nb_encours = len([t for t in all_tickets if t.get('statut') == "En cours de réparation"])
    nb_commandes = len(commandes_attente)
    
    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-label">Total tickets</div>
            <div class="kpi-value">{nb_total}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">En attente</div>
            <div class="kpi-value warning">{nb_attente}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">En réparation</div>
            <div class="kpi-value info">{nb_encours}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Pièces à commander</div>
            <div class="kpi-value" style="color:{'var(--error)' if nb_commandes > 0 else 'var(--success)'};">{nb_commandes}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # === TABS ===
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📋 Demandes", "➕ Nouvelle", "👥 Clients", "📦 Commandes", "📄 Attestation", "⚙️ Config"])
    
    with tab1:
        staff_liste_demandes()
    with tab2:
        staff_nouvelle_demande()
    with tab3:
        staff_gestion_clients()
    with tab4:
        staff_commandes_pieces()
    with tab5:
        staff_attestation()
    with tab6:
        staff_config()
    
    # Footer
    st.markdown("""
    <div style="text-align:center;padding:20px 0;margin-top:40px;border-top:1px solid var(--neutral-200);color:var(--neutral-400);font-size:12px;">
        Créé par <strong>TkConcept26</strong>
    </div>
    """, unsafe_allow_html=True)

def staff_liste_demandes():
    # Si un ticket est sélectionné, afficher directement le traitement
    if st.session_state.get("edit_id"):
        staff_traiter_demande(st.session_state.edit_id)
        return
    
    # === FILTER BAR ===
    st.markdown('<div class="filter-bar">', unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns([2, 1.5, 1.5, 1.5, 1.5])
    with col1:
        f_statut = st.selectbox("Filtrer par statut", ["Tous"] + STATUTS, key="f_statut", label_visibility="collapsed")
    with col2:
        f_code = st.text_input("N° Ticket", key="f_code", placeholder="🔍 KP-...", label_visibility="collapsed")
    with col3:
        f_tel = st.text_input("Téléphone", key="f_tel", placeholder="📞 06...", label_visibility="collapsed")
    with col4:
        f_nom = st.text_input("Nom", key="f_nom", placeholder="👤 Nom client", label_visibility="collapsed")
    with col5:
        tri = st.selectbox("Tri", ["📅 Récent", "📅 Ancien", "🏷️ Statut"], key="f_tri", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Recherche avec les filtres
    tickets = chercher_tickets(
        statut=f_statut if f_statut != "Tous" else None,
        code=f_code.strip() if f_code and f_code.strip() else None, 
        tel=f_tel.strip() if f_tel and f_tel.strip() else None, 
        nom=f_nom.strip() if f_nom and f_nom.strip() else None
    )
    
    # Appliquer le tri
    if "Ancien" in tri:
        tickets = sorted(tickets, key=lambda x: x.get('date_depot', ''))
    elif "Statut" in tri:
        ordre_statut = {s: i for i, s in enumerate(STATUTS)}
        tickets = sorted(tickets, key=lambda x: ordre_statut.get(x.get('statut', ''), 99))
    
    # Pagination
    ITEMS_PER_PAGE = 8
    total_pages = max(1, (len(tickets) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE)
    
    if "accueil_page" not in st.session_state:
        st.session_state.accueil_page = 1
    
    current_page = st.session_state.accueil_page
    start_idx = (current_page - 1) * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    tickets_page = tickets[start_idx:end_idx]
    
    # Header avec compteur
    st.markdown(f"""
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
        <span style="font-size:var(--text-sm);color:var(--neutral-500);">{len(tickets)} ticket(s) trouvé(s)</span>
        <span style="font-size:var(--text-sm);color:var(--neutral-400);">Page {current_page}/{total_pages}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Table header
    st.markdown("""
    <div class="table-header">
        <div style="min-width:90px;">Ticket</div>
        <div style="flex:1;">Client</div>
        <div style="flex:1;">Appareil</div>
        <div style="min-width:80px;">Date</div>
        <div style="min-width:140px;">Statut</div>
        <div style="min-width:100px;">Note</div>
        <div style="min-width:70px;">Action</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Liste des tickets
    if not tickets_page:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">📭</div>
            <div class="empty-title">Aucun ticket trouvé</div>
            <div class="empty-text">Modifiez vos filtres ou créez un nouveau ticket</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for t in tickets_page:
            status_class = get_status_class(t.get('statut', ''))
            modele = f"{t.get('marque','')} {t.get('modele','')}"
            if t.get('modele_autre'): modele += f" ({t['modele_autre']})"
            modele = modele[:25] + "..." if len(modele) > 25 else modele
            
            client_nom = f"{t.get('client_nom','')} {t.get('client_prenom','')}"
            client_nom = client_nom[:20] + "..." if len(client_nom) > 20 else client_nom
            
            has_message = t.get('commentaire_client')
            date_short = fmt_date(t.get('date_depot',''))[:10]
            
            col1, col2, col3, col4, col5, col6, col7 = st.columns([1.2, 1.5, 1.5, 1, 1.8, 1.2, 0.8])
            with col1:
                st.markdown(f"<span class='ticket-code'>{t['ticket_code']}</span>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<span class='ticket-client'>{client_nom}</span>", unsafe_allow_html=True)
            with col3:
                st.markdown(f"<span class='ticket-device'>{modele}</span>", unsafe_allow_html=True)
            with col4:
                st.markdown(f"<span class='ticket-date'>{date_short}</span>", unsafe_allow_html=True)
            with col5:
                st.markdown(f"<span class='badge {status_class}'>{t.get('statut','')}</span>", unsafe_allow_html=True)
            with col6:
                if has_message:
                    st.markdown("<span class='ticket-alert'>📢 Message</span>", unsafe_allow_html=True)
                else:
                    st.markdown("<span style='color:var(--neutral-300);'>—</span>", unsafe_allow_html=True)
            with col7:
                if st.button("Ouvrir", key=f"process_{t['id']}", type="primary", use_container_width=True):
                    st.session_state.edit_id = t['id']
                    st.rerun()
            
            st.markdown("<div style='height:1px;background:var(--neutral-100);margin:8px 0;'></div>", unsafe_allow_html=True)
    
    # Navigation pagination
    if total_pages > 1:
        st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
        col_prev, col_pages, col_next = st.columns([1, 3, 1])
        with col_prev:
            if current_page > 1:
                if st.button("← Précédent", key="accueil_prev", type="secondary", use_container_width=True):
                    st.session_state.accueil_page = current_page - 1
                    st.rerun()
        with col_pages:
            # Indicateurs de pages
            pages_html = " ".join([
                f"<span style='display:inline-block;width:8px;height:8px;border-radius:50%;background:{'var(--brand-500)' if i+1 == current_page else 'var(--neutral-300)'};margin:0 3px;'></span>"
                for i in range(min(total_pages, 10))
            ])
            st.markdown(f"<div style='text-align:center;padding:8px 0;'>{pages_html}</div>", unsafe_allow_html=True)
        with col_next:
            if current_page < total_pages:
                if st.button("Suivant →", key="accueil_next", type="secondary", use_container_width=True):
                    st.session_state.accueil_page = current_page + 1
                    st.rerun()

def staff_traiter_demande(tid):
    t = get_ticket_full(tid=tid)
    if not t:
        st.error("Demande non trouvée")
        return
    
    # === HEADER ===
    status_class = get_status_class(t.get('statut', ''))
    modele_txt = f"{t.get('marque','')} {t.get('modele','')}"
    if t.get('modele_autre'): modele_txt += f" ({t['modele_autre']})"
    
    col_back, col_info = st.columns([1, 6])
    with col_back:
        if st.button("← Retour", key="close_process", type="secondary", use_container_width=True):
            st.session_state.edit_id = None
            st.rerun()
    
    st.markdown(f"""
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:24px;">
        <div>
            <span style="font-size:var(--text-2xl);font-weight:700;color:var(--neutral-900);">{t['ticket_code']}</span>
            <span style="margin-left:16px;font-size:var(--text-base);color:var(--neutral-500);">{t.get('client_nom','')} {t.get('client_prenom','')}</span>
        </div>
        <span class="badge {status_class}" style="font-size:var(--text-sm);padding:8px 16px;">{t.get('statut','')}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # === GRID LAYOUT ===
    col1, col2 = st.columns([1, 1], gap="large")
    
    # === COLONNE GAUCHE: Infos ===
    with col1:
        # Card Client
        st.markdown("""<div class="detail-card-header">👤 Informations Client</div>""", unsafe_allow_html=True)
        panne = t.get('panne', '')
        if t.get('panne_detail'): panne += f" ({t['panne_detail']})"
        
        st.markdown(f"""
        <div class="detail-card">
            <div class="detail-row">
                <span class="detail-label">Nom complet</span>
                <span class="detail-value">{t.get('client_nom','')} {t.get('client_prenom','')}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Téléphone</span>
                <span class="detail-value" style="font-family:monospace;">{t.get('client_tel','')}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Email</span>
                <span class="detail-value">{t.get('client_email') or '—'}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Appareil</span>
                <span class="detail-value">{modele_txt}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Motif</span>
                <span class="detail-value">{panne}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Déposé le</span>
                <span class="detail-value">{fmt_date(t.get('date_depot',''))}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Sécurité (si présent)
        if t.get('pin') or t.get('pattern'):
            st.markdown(f"""
            <div style="background:var(--warning-light);border:1px solid var(--warning);border-radius:var(--r-md);padding:16px;margin:16px 0;">
                <div style="font-weight:600;color:var(--warning-dark);margin-bottom:8px;">🔐 Codes de sécurité</div>
                <div style="font-size:var(--text-sm);">Code PIN: <strong>{t.get('pin') or 'Aucun'}</strong></div>
                <div style="font-size:var(--text-sm);">Schéma: <strong>{t.get('pattern') or 'Aucun'}</strong></div>
            </div>
            """, unsafe_allow_html=True)
        
        # Message technicien
        if t.get('commentaire_client'):
            st.markdown(f"""
            <div style="background:var(--error-light);border:2px solid var(--error);border-radius:var(--r-md);padding:16px;margin:16px 0;">
                <div style="font-weight:600;color:var(--error-dark);margin-bottom:8px;">⚠️ Message du technicien à transmettre</div>
                <div style="font-style:italic;color:var(--neutral-700);">{t.get('commentaire_client')}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Notes internes
        st.markdown("""<div style="height:16px;"></div>""", unsafe_allow_html=True)
        st.markdown("""<div class="detail-card-header">📝 Notes internes</div>""", unsafe_allow_html=True)
        st.text_area("", value=t.get('notes_internes') or "Aucune note", disabled=True, height=80, key=f"notes_view_{tid}", label_visibility="collapsed")
        
        col_note, col_add = st.columns([4, 1])
        with col_note:
            note = st.text_input("", placeholder="Ajouter une note...", key=f"new_note_{tid}", label_visibility="collapsed")
        with col_add:
            if st.button("Ajouter", key=f"add_note_{tid}", type="secondary", use_container_width=True):
                if note:
                    ajouter_note(tid, note)
                    st.success("Note ajoutée!")
                    st.rerun()
    
    # === COLONNE DROITE: Actions ===
    with col2:
        st.markdown("""<div class="detail-card-header">⚙️ Gestion de la réparation</div>""", unsafe_allow_html=True)
        
        # Type de réparation
        panne_actuelle = t.get('panne', PANNES[0])
        idx_panne = PANNES.index(panne_actuelle) if panne_actuelle in PANNES else 0
        new_panne = st.selectbox("Type de réparation", PANNES, index=idx_panne, key=f"rep_type_{tid}")
        
        panne_detail = ""
        if new_panne in ["Autre", "Diagnostic"]:
            panne_detail = st.text_input("Précisez la réparation", 
                                         value=t.get('panne_detail') or "",
                                         placeholder="Ex: Remplacement connecteur...",
                                         key=f"panne_detail_{tid}")
        
        personne = st.text_input("Personne en charge", value=t.get('personne_charge') or "", key=f"personne_{tid}")
        comment = st.text_area("Commentaire interne", placeholder="Ajouter un commentaire...", height=60, key=f"comment_{tid}")
        
        # Tarifs avec design amélioré
        st.markdown("""<div style="height:8px;"></div>""", unsafe_allow_html=True)
        st.markdown("""<div class="detail-card-header">💰 Tarification</div>""", unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        with col_a:
            devis = st.number_input("Devis TTC (€)", value=float(t.get('devis_estime') or 0), min_value=0.0, step=5.0, key=f"devis_{tid}")
        with col_b:
            acompte = st.number_input("Acompte (€)", value=float(t.get('acompte') or 0), min_value=0.0, step=5.0, key=f"acompte_{tid}")
        
        # Statut
        st.markdown("""<div style="height:8px;"></div>""", unsafe_allow_html=True)
        statut_actuel = t.get('statut', STATUTS[0])
        idx_statut = STATUTS.index(statut_actuel) if statut_actuel in STATUTS else 0
        new_statut = st.selectbox("Statut", STATUTS, index=idx_statut, key=f"statut_{tid}")
        
        # Bouton principal
        st.markdown("""<div style="height:16px;"></div>""", unsafe_allow_html=True)
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("💾 ENREGISTRER", type="primary", use_container_width=True, key=f"save_{tid}"):
                update_ticket(tid, panne=new_panne, panne_detail=panne_detail, personne_charge=personne, 
                             devis_estime=devis, acompte=acompte)
                if comment:
                    ajouter_note(tid, comment)
                if new_statut != statut_actuel:
                    changer_statut(tid, new_statut)
                st.success("Demande mise à jour !")
                st.rerun()
        with col_btn2:
            if st.button("🎫 Ticket Client", use_container_width=True, key=f"print_client_{tid}"):
                st.session_state[f"show_ticket_{tid}"] = "client"
                st.rerun()
        
        # Ligne boutons tickets avec envoi par email
        st.markdown("##### 📄 Documents")
        col_t1, col_t2, col_t3, col_t4 = st.columns(4)
        with col_t1:
            if st.button("📋 Ticket Staff", use_container_width=True, key=f"print_staff_{tid}"):
                st.session_state[f"show_ticket_{tid}"] = "staff"
                st.rerun()
        with col_t2:
            if st.button("📝 DEVIS", use_container_width=True, key=f"print_devis_{tid}", type="secondary"):
                st.session_state[f"show_ticket_{tid}"] = "devis"
                st.rerun()
        with col_t3:
            if st.button("🧾 RÉCAPITULATIF", use_container_width=True, key=f"print_facture_{tid}", type="primary"):
                st.session_state[f"show_ticket_{tid}"] = "facture"
                st.rerun()
        with col_t4:
            pass  # Espace réservé
        
        # Boutons envoi par email
        email_client = t.get('client_email', '')
        if email_client and get_param("SMTP_HOST"):
            st.markdown("##### 📧 Envoyer par email")
            col_e1, col_e2, col_e3 = st.columns(3)
            with col_e1:
                if st.button("📧 Envoyer Ticket", use_container_width=True, key=f"email_client_{tid}"):
                    sujet = f"Ticket {t.get('ticket_code','')} - Klikphone"
                    html = ticket_client_html(t)
                    msg = f"Bonjour,\n\nVeuillez trouver ci-joint votre ticket de dépôt.\n\nCordialement,\nKlikphone"
                    success, result = envoyer_email(email_client, sujet, msg, html)
                    if success:
                        st.success("✅ Ticket envoyé par email!")
                        ajouter_note(tid, f"[EMAIL] Ticket envoyé à {email_client}")
                    else:
                        st.error(f"Erreur: {result}")
            with col_e2:
                if st.button("📧 Envoyer Devis", use_container_width=True, key=f"email_devis_{tid}"):
                    sujet = f"Devis D-{t.get('ticket_code','')} - Klikphone"
                    html = ticket_devis_facture_html(t, "devis")
                    msg = f"Bonjour,\n\nVeuillez trouver ci-joint votre devis.\n\nCordialement,\nKlikphone"
                    success, result = envoyer_email(email_client, sujet, msg, html)
                    if success:
                        st.success("✅ Devis envoyé par email!")
                        ajouter_note(tid, f"[EMAIL] Devis envoyé à {email_client}")
                    else:
                        st.error(f"Erreur: {result}")
            with col_e3:
                if st.button("📧 Envoyer Récap.", use_container_width=True, key=f"email_recap_{tid}"):
                    sujet = f"Récapitulatif R-{t.get('ticket_code','')} - Klikphone"
                    html = ticket_devis_facture_html(t, "facture")
                    msg = f"Bonjour,\n\nVeuillez trouver ci-joint votre récapitulatif de paiement.\n\nCordialement,\nKlikphone"
                    success, result = envoyer_email(email_client, sujet, msg, html)
                    if success:
                        st.success("✅ Récapitulatif envoyé par email!")
                        ajouter_note(tid, f"[EMAIL] Récapitulatif envoyé à {email_client}")
                    else:
                        st.error(f"Erreur: {result}")
        elif not email_client:
            st.info("💡 Ajoutez l'email du client pour envoyer les documents par email")
    
    # === SECTION RÉCAPITULATIF DE PAIEMENT ===
    st.markdown("---")
    st.markdown("### 💰 RÉCAPITULATIF DE PAIEMENT")
    
    devis_val = t.get('devis_estime') or 0
    acompte_val = t.get('acompte') or 0
    rep_supp = t.get('reparation_supp') or ""
    prix_supp = t.get('prix_supp') or 0
    panne_detail_accueil = t.get('panne_detail') or ""
    
    col_fact1, col_fact2 = st.columns(2)
    
    with col_fact1:
        st.markdown("""
        <div style="background:linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); border:1px solid #e2e8f0; border-radius:12px; padding:1rem; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
            <strong style="color:#374151;">📦 Détail des prestations</strong>
        </div>
        """, unsafe_allow_html=True)
        
        # Réparation principale (seulement si "Autre" on affiche le détail)
        panne_affichee = t.get('panne','')
        if panne_affichee == "Autre" and panne_detail_accueil:
            panne_affichee = panne_detail_accueil
        
        st.markdown(f"""
        <table style="width:100%; margin-top:0.5rem;">
            <tr style="border-bottom:1px solid #e2e8f0;">
                <td style="padding:8px;"><strong>Réparation principale</strong><br><span style="color:#666; font-size:0.9rem;">{panne_affichee}</span></td>
                <td style="text-align:right; padding:8px;">{devis_val:.2f} €</td>
            </tr>
        </table>
        """, unsafe_allow_html=True)
        
        # Réparation supplémentaire (ajoutée par technicien)
        if rep_supp:
            st.markdown(f"""
            <table style="width:100%;">
                <tr style="border-bottom:1px solid #e2e8f0; background:#fff7ed;">
                    <td style="padding:8px;"><strong>Réparation supplémentaire</strong><br><span style="color:#666; font-size:0.9rem;">{rep_supp}</span></td>
                    <td style="text-align:right; padding:8px;">{prix_supp:.2f} €</td>
                </tr>
            </table>
            """, unsafe_allow_html=True)
        else:
            st.info("Aucune réparation supplémentaire ajoutée par le technicien")
    
    with col_fact2:
        # Calcul des totaux - Prix TTC (TVA incluse)
        total_ttc = devis_val + prix_supp
        # Calcul inverse : HT = TTC / 1.20
        total_ht = total_ttc / 1.20
        tva = total_ttc - total_ht
        reste = max(0, total_ttc - acompte_val)
        
        st.markdown(f"""
        <div style="background:#f0fdf4; border:2px solid #22c55e; border-radius:8px; padding:1rem;">
            <strong style="color:#16a34a; font-size:1.1rem;">RÉCAPITULATIF</strong>
            <hr style="margin:10px 0; border-color:#22c55e;">
            <table style="width:100%;">
                <tr style="font-weight:bold; font-size:1.1rem;">
                    <td style="padding:5px;">Total TTC</td>
                    <td style="text-align:right; padding:5px;">{total_ttc:.2f} €</td>
                </tr>
                <tr style="color:#666; font-size:0.9rem;">
                    <td style="padding:5px;">dont HT</td>
                    <td style="text-align:right; padding:5px;">{total_ht:.2f} €</td>
                </tr>
                <tr style="color:#666; font-size:0.9rem;">
                    <td style="padding:5px;">dont TVA (20%)</td>
                    <td style="text-align:right; padding:5px;">{tva:.2f} €</td>
                </tr>
                <tr style="border-top:2px solid #22c55e;">
                    <td style="padding:5px;">Acompte versé</td>
                    <td style="text-align:right; padding:5px; color:#16a34a;">- {acompte_val:.2f} €</td>
                </tr>
                <tr style="font-weight:bold; font-size:1.2rem; color:#dc2626;">
                    <td style="padding:10px 5px;">RESTE À PAYER</td>
                    <td style="text-align:right; padding:10px 5px;">{reste:.2f} €</td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
        
        # Bouton pour mettre à jour le tarif final
        if st.button("Mettre à jour le tarif final", key=f"update_tarif_{tid}", type="primary", use_container_width=True):
            update_ticket(tid, tarif_final=total_ttc)
            st.success(f"Tarif final mis à jour: {total_ttc:.2f} €")
            st.rerun()
    
    # Section Messagerie
    st.markdown("---")
    st.markdown("**Contacter le client**")
    
    tel = t.get('client_tel', '')
    email = t.get('client_email', '')
    
    # Messages prédéfinis
    messages = get_messages_predefs(t)
    
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
    msg_custom = st.text_area("Message à envoyer", value=st.session_state[msg_key], height=200, key=msg_key)
    
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
                        st.success("Email envoyé!")
                        ajouter_note(tid, f"[EMAIL] Message envoyé à {email}")
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
        <div style="background: linear-gradient(135deg, rgba(251,146,60,0.2), rgba(249,115,22,0.1)); padding: 15px; border-radius: 12px; margin-bottom: 10px; border-left: 4px solid #fb923c;">
            <strong>🎫 TICKET CLIENT</strong> - Cliquez sur "IMPRIMER" dans le ticket ci-dessous
        </div>
        """, unsafe_allow_html=True)
        st.components.v1.html(ticket_client_html(t), height=700, scrolling=True)
        if st.button("Fermer", key=f"close_ticket_client_{tid}", type="primary", use_container_width=True):
            del st.session_state[f"show_ticket_{tid}"]
            st.rerun()
    
    if st.session_state.get(f"show_ticket_{tid}") == "staff":
        st.markdown("---")
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(107,114,128,0.2), rgba(75,85,99,0.1)); padding: 15px; border-radius: 12px; margin-bottom: 10px; border-left: 4px solid #6b7280;">
            <strong>📋 TICKET STAFF</strong> - Cliquez sur "IMPRIMER" dans le ticket ci-dessous
        </div>
        """, unsafe_allow_html=True)
        st.components.v1.html(ticket_staff_html(t), height=800, scrolling=True)
        if st.button("Fermer", key=f"close_ticket_staff_{tid}", type="primary", use_container_width=True):
            del st.session_state[f"show_ticket_{tid}"]
            st.rerun()
    
    if st.session_state.get(f"show_ticket_{tid}") == "devis":
        st.markdown("---")
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(59,130,246,0.2), rgba(37,99,235,0.1)); padding: 15px; border-radius: 12px; margin-bottom: 10px; border-left: 4px solid #3b82f6;">
            <strong>📝 DEVIS</strong> - Cliquez sur "IMPRIMER" dans le document ci-dessous
        </div>
        """, unsafe_allow_html=True)
        st.components.v1.html(ticket_devis_facture_html(t, "devis"), height=800, scrolling=True)
        if st.button("Fermer", key=f"close_ticket_devis_{tid}", type="primary", use_container_width=True):
            del st.session_state[f"show_ticket_{tid}"]
            st.rerun()
    
    if st.session_state.get(f"show_ticket_{tid}") == "facture":
        st.markdown("---")
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(22,163,74,0.2), rgba(21,128,61,0.1)); padding: 15px; border-radius: 12px; margin-bottom: 10px; border-left: 4px solid #16a34a;">
            <strong>🧾 RÉCAPITULATIF DE PAIEMENT</strong> - Cliquez sur "IMPRIMER" dans le document ci-dessous
        </div>
        """, unsafe_allow_html=True)
        st.components.v1.html(ticket_devis_facture_html(t, "facture"), height=800, scrolling=True)
        st.warning("⚠️ Ce ticket ne fait pas office de facture.")
        if st.button("Fermer", key=f"close_ticket_facture_{tid}", type="primary", use_container_width=True):
            del st.session_state[f"show_ticket_{tid}"]
            st.rerun()

def staff_gestion_clients():
    """Gestion des clients - Liste, modification, export"""
    
    # Header avec export
    col_title, col_export = st.columns([4, 1])
    with col_title:
        st.markdown("""<div class="detail-card-header">👥 Gestion des Clients</div>""", unsafe_allow_html=True)
    with col_export:
        data, filename = export_clients_excel()
        if data:
            st.download_button(
                label="📥 Excel",
                data=data,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" if filename.endswith('.xlsx') else "text/csv",
                key="download_clients",
                type="primary",
                use_container_width=True
            )
    
    st.markdown("---")
    
    # Mode édition client
    if st.session_state.get("edit_client_id"):
        client_id = st.session_state.edit_client_id
        client = get_client_by_id(client_id)
        
        if client:
            st.markdown(f"### ✏️ Modifier le client #{client_id}")
            
            col1, col2 = st.columns(2)
            with col1:
                edit_nom = st.text_input("Nom *", value=client.get('nom', ''), key="edit_client_nom")
                edit_prenom = st.text_input("Prénom", value=client.get('prenom', ''), key="edit_client_prenom")
                edit_societe = st.text_input("Société (facultatif)", value=client.get('societe', '') or '', key="edit_client_societe")
            with col2:
                edit_tel = st.text_input("Téléphone *", value=client.get('telephone', ''), key="edit_client_tel")
                edit_email = st.text_input("Email", value=client.get('email', ''), key="edit_client_email")
            
            col_save, col_cancel = st.columns(2)
            with col_save:
                if st.button("💾 Enregistrer", type="primary", use_container_width=True, key="save_client"):
                    if edit_nom and edit_tel:
                        update_client(client_id, nom=edit_nom, prenom=edit_prenom, telephone=edit_tel, email=edit_email, societe=edit_societe)
                        st.success("✅ Client mis à jour!")
                        st.session_state.edit_client_id = None
                        st.rerun()
                    else:
                        st.error("Nom et téléphone obligatoires")
            with col_cancel:
                if st.button("❌ Annuler", type="secondary", use_container_width=True, key="cancel_edit_client"):
                    st.session_state.edit_client_id = None
                    st.rerun()
            
            st.markdown("---")
        else:
            st.session_state.edit_client_id = None
            st.rerun()
    
    # Recherche
    search = st.text_input("🔍 Rechercher un client", placeholder="Nom, prénom, téléphone ou société...", key="search_clients")
    
    # Liste des clients
    if search and len(search) >= 2:
        clients = search_clients(search)
    else:
        clients = get_all_clients()
    
    st.markdown(f"**{len(clients)} client(s)**")
    
    # Table header
    st.markdown("""
    <div class="table-header">
        <div style="flex:1;">Nom</div>
        <div style="flex:1;">Prénom</div>
        <div style="flex:0.8;">Société</div>
        <div style="flex:1;">Téléphone</div>
        <div style="flex:1.2;">Email</div>
        <div style="min-width:60px;">Tickets</div>
        <div style="min-width:60px;">Action</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Pagination
    ITEMS_PER_PAGE = 15
    total_pages = max(1, (len(clients) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE)
    
    if "clients_page" not in st.session_state:
        st.session_state.clients_page = 1
    
    current_page = st.session_state.clients_page
    start_idx = (current_page - 1) * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    clients_page = clients[start_idx:end_idx]
    
    for client in clients_page:
        col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 1, 0.8, 1, 1.2, 0.4, 0.5])
        with col1:
            st.markdown(f"**{client.get('nom', '')}**")
        with col2:
            st.write(client.get('prenom', ''))
        with col3:
            societe = client.get('societe', '')
            st.write(societe[:12] if societe else "—")
        with col4:
            st.write(client.get('telephone', ''))
        with col5:
            email = client.get('email', '')
            st.write(email[:20] if email else "—")
        with col6:
            st.write(f"{client.get('nb_tickets', 0)}")
        with col7:
            if st.button("✏️", key=f"edit_client_{client['id']}", help="Modifier"):
                st.session_state.edit_client_id = client['id']
                st.rerun()
        
        st.markdown("<div style='height:1px;background:var(--neutral-100);margin:4px 0;'></div>", unsafe_allow_html=True)
    
    # Pagination
    if total_pages > 1:
        st.markdown("---")
        col_prev, col_info, col_next = st.columns([1, 2, 1])
        with col_prev:
            if current_page > 1:
                if st.button("← Précédent", key="clients_prev"):
                    st.session_state.clients_page = current_page - 1
                    st.rerun()
        with col_info:
            st.markdown(f"<div style='text-align:center;'>Page {current_page}/{total_pages}</div>", unsafe_allow_html=True)
        with col_next:
            if current_page < total_pages:
                if st.button("Suivant →", key="clients_next"):
                    st.session_state.clients_page = current_page + 1
                    st.rerun()

def staff_commandes_pieces():
    """Gestion des commandes de pièces"""
    st.markdown("""<div class="detail-card-header">📦 Commandes de Pièces</div>""", unsafe_allow_html=True)
    
    # Onglets
    sub_tab1, sub_tab2, sub_tab3 = st.tabs(["🔴 À commander", "🟡 Commandées", "➕ Nouvelle commande"])
    
    with sub_tab1:
        # Pièces à commander
        commandes = get_commandes_pieces(statut="A commander")
        
        if not commandes:
            st.info("✅ Aucune pièce à commander")
        else:
            st.markdown(f"**{len(commandes)} pièce(s) à commander**")
            
            for cmd in commandes:
                with st.container():
                    col1, col2, col3, col4 = st.columns([2, 1.5, 1, 1])
                    with col1:
                        ticket_info = f"{cmd.get('ticket_code', 'N/A')} - {cmd.get('client_nom', '')} {cmd.get('client_prenom', '')}"
                        st.markdown(f"**{cmd['description']}**")
                        st.caption(f"📋 {ticket_info}")
                        if cmd.get('marque') and cmd.get('modele'):
                            st.caption(f"📱 {cmd['marque']} {cmd['modele']}")
                    with col2:
                        st.write(f"🏪 {cmd.get('fournisseur', 'N/A')}")
                        if cmd.get('reference'):
                            st.caption(f"Réf: {cmd['reference']}")
                    with col3:
                        if cmd.get('prix') and cmd['prix'] > 0:
                            st.write(f"💰 {cmd['prix']:.2f} €")
                    with col4:
                        if st.button("✅ Commandée", key=f"cmd_done_{cmd['id']}", type="primary"):
                            from datetime import datetime
                            update_commande_piece(cmd['id'], statut="Commandée", date_commande=datetime.now().strftime("%Y-%m-%d %H:%M"))
                            st.rerun()
                        if st.button("🗑️", key=f"cmd_del_{cmd['id']}", help="Supprimer"):
                            delete_commande_piece(cmd['id'])
                            st.rerun()
                    
                    st.markdown("<hr style='margin:10px 0;border-color:#eee;'>", unsafe_allow_html=True)
    
    with sub_tab2:
        # Pièces commandées (en attente de réception)
        commandes = get_commandes_pieces(statut="Commandée")
        
        if not commandes:
            st.info("Aucune commande en cours")
        else:
            st.markdown(f"**{len(commandes)} commande(s) en cours**")
            
            for cmd in commandes:
                with st.container():
                    col1, col2, col3, col4 = st.columns([2, 1.5, 1, 1])
                    with col1:
                        ticket_info = f"{cmd.get('ticket_code', 'N/A')} - {cmd.get('client_nom', '')} {cmd.get('client_prenom', '')}"
                        st.markdown(f"**{cmd['description']}**")
                        st.caption(f"📋 {ticket_info}")
                    with col2:
                        st.write(f"🏪 {cmd.get('fournisseur', 'N/A')}")
                        if cmd.get('date_commande'):
                            st.caption(f"Commandé le {cmd['date_commande'][:10]}")
                    with col3:
                        if cmd.get('prix') and cmd['prix'] > 0:
                            st.write(f"💰 {cmd['prix']:.2f} €")
                    with col4:
                        if st.button("📦 Reçue", key=f"cmd_recv_{cmd['id']}", type="primary"):
                            from datetime import datetime
                            update_commande_piece(cmd['id'], statut="Reçue", date_reception=datetime.now().strftime("%Y-%m-%d %H:%M"))
                            st.rerun()
                    
                    st.markdown("<hr style='margin:10px 0;border-color:#eee;'>", unsafe_allow_html=True)
    
    with sub_tab3:
        # Ajouter une nouvelle commande
        st.markdown("##### Ajouter une commande de pièce")
        
        # Sélection du ticket (optionnel)
        tickets_ouverts = [t for t in chercher_tickets() if t.get('statut') not in ['Clôturé', 'Rendu au client']]
        ticket_options = ["-- Sans ticket --"] + [f"{t['ticket_code']} - {t.get('client_nom', '')} ({t.get('marque', '')} {t.get('modele', '')})" for t in tickets_ouverts]
        
        selected_ticket = st.selectbox("Associer à un ticket (optionnel)", ticket_options, key="cmd_ticket")
        
        ticket_id = None
        if selected_ticket != "-- Sans ticket --":
            idx = ticket_options.index(selected_ticket) - 1
            ticket_id = tickets_ouverts[idx]['id']
        
        col1, col2 = st.columns(2)
        with col1:
            cmd_description = st.text_input("Description de la pièce *", placeholder="Ex: Écran iPhone 11", key="cmd_desc")
            cmd_fournisseur = st.selectbox("Fournisseur", FOURNISSEURS, key="cmd_fournisseur")
            if cmd_fournisseur == "Autre":
                cmd_fournisseur = st.text_input("Précisez le fournisseur", key="cmd_fournisseur_autre")
        with col2:
            cmd_reference = st.text_input("Référence (optionnel)", placeholder="Réf. fournisseur", key="cmd_ref")
            cmd_prix = st.number_input("Prix (€)", min_value=0.0, step=1.0, key="cmd_prix")
        
        cmd_notes = st.text_area("Notes", placeholder="Informations complémentaires...", height=80, key="cmd_notes")
        
        if st.button("➕ Ajouter la commande", type="primary", use_container_width=True):
            if cmd_description:
                ajouter_commande_piece(ticket_id, cmd_description, cmd_fournisseur, cmd_reference, cmd_prix, cmd_notes)
                st.success("✅ Commande ajoutée!")
                st.rerun()
            else:
                st.error("La description est obligatoire")

def staff_attestation():
    """Générer une attestation de non-reparabilite"""
    st.markdown("""<div class="detail-card-header">📄 Attestation de Non-Réparabilité</div>""", unsafe_allow_html=True)
    st.markdown("Générez une attestation pour les appareils économiquement irréparables (utile pour les assurances).")
    
    st.markdown("---")
    
    # Option pour sélectionner un client existant
    st.markdown("##### 👤 Informations client")
    
    use_existing = st.checkbox("Rechercher un client existant", key="att_use_existing")
    
    if use_existing:
        search_query = st.text_input("🔍 Rechercher par nom, prénom ou téléphone", key="att_search", placeholder="Tapez pour rechercher...")
        
        if search_query and len(search_query) >= 2:
            clients_found = search_clients(search_query)
            if clients_found:
                options = ["-- Sélectionnez --"] + [f"{c['nom']} {c['prenom']} - {c['telephone']}" for c in clients_found]
                selected = st.selectbox("Clients trouvés", options, key="att_client_select")
                
                if selected != "-- Sélectionnez --":
                    # Trouver le client sélectionné
                    idx = options.index(selected) - 1
                    client = clients_found[idx]
                    
                    # Pré-remplir les champs
                    st.session_state.att_nom_val = client['nom']
                    st.session_state.att_prenom_val = client['prenom']
                    st.session_state.att_email_val = client.get('email', '')
                    st.success(f"✅ Client sélectionné: {client['nom']} {client['prenom']}")
            else:
                st.info("Aucun client trouvé")
    
    # Champs client (modifiables)
    col1, col2 = st.columns(2)
    with col1:
        att_nom = st.text_input("Nom du client *", 
                                value=st.session_state.get('att_nom_val', ''),
                                key="att_nom")
        att_prenom = st.text_input("Prénom du client *", 
                                   value=st.session_state.get('att_prenom_val', ''),
                                   key="att_prenom")
        att_adresse = st.text_input("Adresse du client", key="att_adresse", placeholder="73000 Chambéry")
    with col2:
        att_email = st.text_input("Email du client", 
                                  value=st.session_state.get('att_email_val', ''),
                                  key="att_email", placeholder="client@email.com")
        att_marque = st.selectbox("Marque *", ["Apple", "Samsung", "Xiaomi", "Huawei", "Autre"], key="att_marque")
        att_modele = st.text_input("Modèle *", key="att_modele", placeholder="iPhone 11 Pro")
    
    att_imei = st.text_input("Numéro IMEI / Série *", key="att_imei", placeholder="353833102642466")
    
    st.markdown("---")
    st.markdown("##### 📝 Détails techniques")
    
    att_etat = st.text_area("État de l'appareil au moment du dépôt", key="att_etat", 
                           placeholder="Ex: Chassis arrière endommagé et écran fissuré", height=80)
    att_motif = st.text_area("Motif du dépôt", key="att_motif",
                            placeholder="Ex: iPhone ayant subi un choc violent", height=80)
    att_compte_rendu = st.text_area("Compte rendu du technicien *", key="att_cr",
                                   placeholder="Ex:\n- Afficheur endommagé entraînant la perte d'affichage\n- Chassis endommagé\n- Carte mère trop endommagée", height=120)
    
    st.markdown("---")
    
    if st.button("📄 GÉNÉRER L'ATTESTATION", type="primary", use_container_width=True):
        if not att_nom or not att_prenom or not att_modele or not att_imei or not att_compte_rendu:
            st.error("Veuillez remplir tous les champs obligatoires (*)")
        else:
            from datetime import datetime
            date_jour = datetime.now().strftime("%d/%m/%Y")
            
            # HTML de l'attestation (version pour affichage avec bouton imprimer)
            attestation_html = generate_attestation_html(
                att_nom, att_prenom, att_adresse, att_marque, att_modele, 
                att_imei, att_etat, att_motif, att_compte_rendu, date_jour, 
                include_print_btn=True
            )
            
            st.session_state.attestation_html = attestation_html
            st.session_state.attestation_email = att_email
            st.session_state.attestation_data = {
                'nom': att_nom, 'prenom': att_prenom, 'adresse': att_adresse,
                'marque': att_marque, 'modele': att_modele, 'imei': att_imei,
                'etat': att_etat, 'motif': att_motif, 'compte_rendu': att_compte_rendu,
                'date': date_jour
            }
            st.success("Attestation générée!")
            st.rerun()
    
    # Afficher l'attestation si générée
    if st.session_state.get("attestation_html"):
        st.markdown("---")
        st.markdown("### 📋 Aperçu de l'attestation")
        st.components.v1.html(st.session_state.attestation_html, height=800, scrolling=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔄 Nouvelle attestation", key="new_attestation", type="secondary", use_container_width=True):
                for key in ['attestation_html', 'attestation_email', 'attestation_data', 
                           'att_nom_val', 'att_prenom_val', 'att_email_val']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
        with col2:
            att_email_saved = st.session_state.get("attestation_email", "")
            if att_email_saved and get_param("SMTP_HOST"):
                if st.button("📧 Envoyer par email", key="send_attestation_email", type="primary", use_container_width=True):
                    # Générer le PDF
                    data = st.session_state.get("attestation_data", {})
                    html_for_email = generate_attestation_html(
                        data.get('nom',''), data.get('prenom',''), data.get('adresse',''),
                        data.get('marque',''), data.get('modele',''), data.get('imei',''),
                        data.get('etat',''), data.get('motif',''), data.get('compte_rendu',''),
                        data.get('date',''), include_print_btn=False
                    )
                    
                    sujet = "Attestation de non-réparabilité - Klikphone"
                    message = "Bonjour,\n\nVeuillez trouver ci-jointe votre attestation de non-réparabilité.\n\nCordialement,\nL'équipe Klikphone\n04 79 60 89 22"
                    
                    # Convertir HTML en PDF
                    pdf_bytes = html_to_pdf(html_for_email)
                    if pdf_bytes:
                        success, result = envoyer_email_avec_pdf(att_email_saved, sujet, message, pdf_bytes, "attestation_non_reparabilite.pdf")
                    else:
                        # Fallback: envoyer en HTML
                        success, result = envoyer_email(att_email_saved, sujet, message, html_for_email)
                    
                    if success:
                        st.success(f"✅ Email envoyé à {att_email_saved}!")
                    else:
                        st.error(result)
            elif att_email_saved:
                st.info("💡 Configurez SMTP dans Config > Email")

def generate_attestation_html(nom, prenom, adresse, marque, modele, imei, etat, motif, compte_rendu, date_jour, include_print_btn=True):
    """Génère le HTML de l'attestation"""
    print_btn = '<button class="print-btn" onclick="window.print()">IMPRIMER L\'ATTESTATION</button>' if include_print_btn else ''
    
    return f"""
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
        @media print {{ .print-btn {{ display: none; }} }}
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
        <u>Attestation délivrée à :</u><br>
        <strong>M. {nom.upper()} {prenom.upper()}</strong><br>
        {adresse or "73000 Chambéry"}
    </div>
    
    <div class="titre">COMPTE RENDU TECHNICIEN</div>
    
    <div class="section">
        <p>La société <strong>Klikphone</strong>, spécialiste en réparation de smartphones et tablettes, basée au 79 Place Saint Léger à Chambéry;</p>
        
        <p>Atteste que l'appareil <strong>{marque} {modele}</strong> comportant le numéro IMEI/Série suivant: <strong>{imei}</strong> a bien été déposé à notre atelier pour réparation.</p>
    </div>
    
    <div class="section">
        <div class="section-title">État de l'appareil au moment du dépôt :</div>
        <p>{etat or "Non précisé"}</p>
    </div>
    
    <div class="section">
        <div class="section-title">Motif du dépôt :</div>
        <p>{motif or "Diagnostic demandé"}</p>
    </div>
    
    <div class="section">
        <div class="section-title">Compte rendu du technicien :</div>
        <ul>
            {"".join([f"<li>{line.strip()}</li>" for line in compte_rendu.split(chr(10)) if line.strip()])}
        </ul>
    </div>
    
    <div class="section">
        <div class="section-title">Estimation des réparations :</div>
        <p><strong>Après expertise, nous attestons que cet appareil est économiquement irréparable.</strong></p>
    </div>
    
    <div class="section">
        <div class="section-title">Valeur de l'appareil :</div>
        <p>Se référer à la facture d'achat / devis de remplacement</p>
    </div>
    
    <div class="footer">
        <p>Cette attestation fait office de justificatif pour votre assurance.</p>
        <p>Tous nos diagnostics et nos réparations sont garantis et réalisés par un technicien certifié.</p>
    </div>
    
    <div class="signature">
        Fait à Chambéry, le {date_jour}
    </div>
    
    {print_btn}
</body>
</html>
"""

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
    col1, col2, col3 = st.columns([5, 1, 1])
    with col1:
        st.markdown("<h1 class='page-title'>Espace Technicien</h1>", unsafe_allow_html=True)
    with col2:
        if st.button("🏠 Accueil", key="goto_accueil", type="secondary"):
            st.session_state.mode = "accueil"
            st.rerun()
    with col3:
        if st.button("🚪 Déconnexion", key="logout_tech"):
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
        modele_txt = f"{t.get('marque','')} {t.get('modele','')}"
        if t.get('modele_autre'): modele_txt += f" ({t['modele_autre']})"
        panne = t.get('panne', '')
        if t.get('panne_detail'): panne += f" ({t['panne_detail']})"
        
        st.markdown(f"""
        **Client:** {t.get('client_nom','')} {t.get('client_prenom','')}<br>
        **Tél:** {t.get('client_tel','')}<br>
        **Appareil:** {modele_txt}<br>
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
        # Afficher la tarification définie par l'accueil
        devis = t.get('devis_estime') or 0
        acompte = t.get('acompte') or 0
        rep_supp = t.get('reparation_supp') or ""
        prix_supp = t.get('prix_supp') or 0
        panne_detail = t.get('panne_detail') or ""
        
        # Afficher la réparation à effectuer
        panne_affichee = t.get('panne', '')
        if panne_affichee == "Autre" and panne_detail:
            panne_affichee = panne_detail
        
        st.markdown(f"""
        <div style="background: #dbeafe; border: 1px solid #3b82f6; border-radius: 6px; padding: 0.75rem; margin: 0.5rem 0;">
            <strong style="color:#1d4ed8;">🔧 RÉPARATION À EFFECTUER</strong><br>
            <span style="font-size:1.1rem;">{panne_affichee}</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: #f0fdf4; border: 1px solid #22c55e; border-radius: 6px; padding: 0.75rem; margin: 0.5rem 0;">
            <strong style="color:#16a34a;">💰 TARIFICATION</strong>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        **Devis initial (accueil):** {devis:.2f} €<br>
        **Acompte versé:** {acompte:.2f} €
        """, unsafe_allow_html=True)
        
        if rep_supp:
            st.markdown(f"**Réparation supp.:** {rep_supp} - {prix_supp:.2f} €")
        
        # Calcul total - Prix TTC (TVA incluse)
        total_ttc = devis + prix_supp
        total_ht = total_ttc / 1.20
        tva = total_ttc - total_ht
        reste = max(0, total_ttc - acompte)
        
        st.markdown(f"""
        <div style="background: #fff7ed; border: 1px solid #f97316; border-radius: 6px; padding: 0.75rem; margin: 0.5rem 0;">
            <strong>Total TTC:</strong> {total_ttc:.2f} €<br>
            <span style="color:#666; font-size:0.9rem;">dont HT: {total_ht:.2f} € | TVA: {tva:.2f} €</span><br>
            <hr style="margin:5px 0;">
            <strong style="color:#dc2626;">Reste à payer: {reste:.2f} €</strong>
        </div>
        """, unsafe_allow_html=True)
        
        # Changer statut
        st.markdown("**Changer le statut:**")
        statut_actuel = t.get('statut', STATUTS[0])
        for s in STATUTS:
            btn_type = "primary" if s == "Rendu au client" else "secondary"
            disabled = (s == statut_actuel)
            if st.button(s, key=f"tech_status_{tid}_{s}", use_container_width=True, disabled=disabled, type=btn_type if s == "Rendu au client" else "secondary"):
                changer_statut(tid, s)
                st.success(f"Statut mis à jour: {s}")
                st.rerun()
    
    st.markdown("---")
    
    # Section commentaires technicien
    st.markdown("**Ajouter une note interne:**")
    col_note, col_btn = st.columns([4, 1])
    with col_note:
        note_tech = st.text_input("Note technique", placeholder="Ex: Pièce à commander, problème identifié...", key=f"tech_comment_{tid}", label_visibility="collapsed")
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
                # Envoi direct si SMTP configuré
                if get_param("SMTP_HOST"):
                    if st.button("📧 Email", key=f"tech_send_email_{tid}", type="primary", use_container_width=True):
                        sujet = f"Réparation {t.get('ticket_code','')} - {get_param('NOM_BOUTIQUE') or 'Klikphone'}"
                        success, result = envoyer_email(email, sujet, msg_custom)
                        if success:
                            st.success(f"✅ Email envoyé à {email}!")
                        else:
                            st.error(result)
                else:
                    sujet = f"Réparation {t.get('ticket_code','')} - Klikphone"
                    st.markdown(f'<a href="{email_link(email, sujet, msg_custom)}" target="_blank" style="display:block;text-align:center;padding:10px;background:#6b7280;color:white;border-radius:8px;text-decoration:none;font-weight:bold;">Email</a>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div style="text-align:center;padding:20px 0;margin-top:40px;border-top:1px solid var(--neutral-200);color:var(--neutral-400);font-size:12px;">
        Créé par <strong>TkConcept26</strong>
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# PAGE SUIVI CLIENT
# =============================================================================
def ui_suivi():
    st.markdown(f"""
    <div style="text-align:center; padding:1.5rem 0; background:white; border-radius:16px; margin-bottom:1rem; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
        <img src="data:image/png;base64,{LOGO_B64}" style="width:60px; height:60px; margin-bottom:0.5rem;">
        <div style="color:#f97316; font-size: 1.8rem; font-weight: 800;">KLIKPHONE</div>
        <p style="color:#6b7280; font-size:0.9rem; margin:0;">Suivi de votre réparation</p>
    </div>
    """, unsafe_allow_html=True)
    
    params = st.query_params
    code_url = params.get("ticket", "")
    
    # Formulaire de recherche
    col1, col2 = st.columns(2)
    with col1:
        code = st.text_input("N° de ticket", value=code_url, placeholder="KP-000001")
    with col2:
        tel = st.text_input("Votre téléphone", placeholder="06 12 34 56 78")
    
    rechercher = st.button("🔍 RECHERCHER MA RÉPARATION", type="primary", use_container_width=True)
    
    # Recherche
    if rechercher or (code_url and tel):
        if code and tel:
            t = get_ticket_full(code=code)
            tel_clean = "".join(filter(str.isdigit, tel))
            client_tel_clean = "".join(filter(str.isdigit, t.get('client_tel', ''))) if t else ""
            
            if t and tel_clean == client_tel_clean:
                # Données
                status_class = get_status_class(t.get('statut', ''))
                modele_txt = f"{t.get('marque','')} {t.get('modele','')}"
                if t.get('modele_autre'): modele_txt += f" ({t['modele_autre']})"
                
                panne = t.get('panne', '')
                if t.get('panne_detail'): panne = t.get('panne_detail')
                
                devis = t.get('devis_estime') or 0
                prix_supp = t.get('prix_supp') or 0
                acompte = t.get('acompte') or 0
                total_ttc = devis + prix_supp
                reste = max(0, total_ttc - acompte)
                
                statut = t.get('statut', '')
                progress_map = {
                    "En attente de diagnostic": 20, 
                    "En cours de réparation": 50,
                    "Réparation terminée": 80,
                    "Rendu au client": 100, 
                    "Clôturé": 100
                }
                progress = progress_map.get(statut, 10)
                
                # Affichage avec Streamlit natif
                st.markdown("---")
                
                # En-tête ticket
                col_code, col_statut = st.columns([2, 1])
                with col_code:
                    st.markdown(f"### 🎫 {t['ticket_code']}")
                with col_statut:
                    st.markdown(f"<span class='status-badge {status_class}'>{statut}</span>", unsafe_allow_html=True)
                
                # Infos client et appareil
                st.markdown(f"""
                **👤 Client:** {t.get('client_nom','')} {t.get('client_prenom','')}  
                **📱 Appareil:** {modele_txt}  
                **🔧 Réparation:** {panne}
                """)
                
                # Dates
                col_dates, col_prix = st.columns(2)
                with col_dates:
                    st.markdown(f"""
                    **Déposé le:** {fmt_date(t.get('date_depot',''))}  
                    **Mise à jour:** {fmt_date(t.get('date_maj',''))}
                    """)
                with col_prix:
                    if total_ttc > 0:
                        st.metric("Total TTC", f"{total_ttc:.2f} €")
                        if acompte > 0:
                            st.caption(f"Acompte: -{acompte:.2f} €")
                        st.markdown(f"**Reste à payer: {reste:.2f} €**")
                
                # Progression
                st.markdown("---")
                st.markdown(f"**Progression: {progress}%**")
                st.progress(progress / 100)
                
                # Étapes visuelles
                cols = st.columns(5)
                etapes = ["📥 Déposé", "🔍 Diagnostic", "🔧 Réparation", "✅ Terminé", "🤝 Récupéré"]
                etapes_done = {
                    "En attente de diagnostic": 1,
                    "En cours de réparation": 2,
                    "Réparation terminée": 3,
                    "Rendu au client": 5,
                    "Clôturé": 5
                }
                done_count = etapes_done.get(statut, 0)
                
                for i, (col, etape) in enumerate(zip(cols, etapes)):
                    with col:
                        if i < done_count:
                            st.markdown(f"<div style='text-align:center;color:#16a34a;font-size:0.8rem;'>{etape}</div>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"<div style='text-align:center;color:#9ca3af;font-size:0.8rem;'>{etape}</div>", unsafe_allow_html=True)
                
            else:
                st.error("❌ Ticket non trouvé ou numéro de téléphone incorrect")
        else:
            st.warning("⚠️ Veuillez remplir les deux champs")
    
    st.markdown("---")
    if st.button("← Retour à l'accueil"):
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
    target = "accueil" if mode == "accueil" else "tech"
    
    st.markdown(f"""
    <div style="text-align:center; padding:2rem 0;">
        <img src="data:image/png;base64,{LOGO_B64}" style="width:60px; height:60px; margin-bottom:0.5rem;">
        <div style="color:#f97316; font-size: 1.8rem; font-weight: 800;">KLIKPHONE</div>
        <p style="color:#6b7280; font-size:1rem; margin-top:0.5rem;">{titre}</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        pin = st.text_input("Code PIN", type="password", placeholder="••••", key="auth_pin_input")
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("← Retour", use_container_width=True):
                st.session_state.mode = None
                st.rerun()
        with col_b:
            if st.button("Valider", type="primary", use_container_width=True):
                # PIN unique 2626 pour accueil et technicien
                if pin == "2626":
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
    
    # Si l'URL contient un ticket, aller directement vers le suivi
    params = st.query_params
    if params.get("ticket") and st.session_state.mode is None:
        st.session_state.mode = "suivi"
    
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
