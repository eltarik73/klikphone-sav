"""
Service de scraping Mobilax.fr
Récupère les prix des pièces détachées (écrans, batteries, connecteurs)
pour Samsung, Google, Xiaomi, Huawei, Motorola.
"""

import re
import math
import json
import time
from datetime import datetime
from collections import defaultdict

import httpx

from app.database import get_cursor


# ─── CONFIG ─────────────────────────────────────────────────

MOBILAX_BASE = "https://www.mobilax.fr"
BRANDS_SLUGS = {
    "Samsung": "samsung",
    "Google": "google",
    "Xiaomi": "xiaomi",
    "Huawei": "huawei",
    "Motorola": "motorola",
}

# Modèles haut de gamme (marge 70€ au lieu de 60€)
HAUT_DE_GAMME_PATTERNS = [
    r"Galaxy\s+S2[0-9]", r"Galaxy\s+Note\s*(1[0-9]|2[0-9])",
    r"Galaxy\s+Z\s+Flip", r"Galaxy\s+Z\s+Fold",
    r"Pixel\s+[7-9](?:\s+Pro)?", r"Pixel\s+10",
    r"Xiaomi\s+1[3-9]", r"Xiaomi\s+15",
    r"Huawei\s+P[4-6]0\s+Pro", r"Huawei\s+Mate\s+[4-5]0",
    r"Edge\s+[4-7]0\s+(?:Ultra|Pro)",
    r"Razr\s+[4-6]0",
]

# Modèles pliants (marge 100€)
PLIANT_PATTERNS = [
    r"Galaxy\s+Z\s+Flip", r"Galaxy\s+Z\s+Fold",
    r"Pixel\s+\d+\s+Pro\s+Fold",
    r"Razr\s+\d+",
]


# ─── PRIX ────────────────────────────────────────────────────

def arrondi_9(prix):
    """Arrondi à 9 : dernier chiffre 0-1→9 inf, 2-9→9 sup."""
    p = round(prix)
    if p <= 0:
        return 9
    last = p % 10
    if last == 9:
        return p
    elif last <= 1:
        return p - last - 1
    else:
        return p + (9 - last)


def detect_categorie(model_name):
    """Détecte si un modèle est pliant, haut de gamme, ou standard."""
    for pat in PLIANT_PATTERNS:
        if re.search(pat, model_name, re.IGNORECASE):
            return "pliant"
    for pat in HAUT_DE_GAMME_PATTERNS:
        if re.search(pat, model_name, re.IGNORECASE):
            return "haut_de_gamme"
    return "standard"


def calcul_prix_client(prix_ht, type_piece, categorie="standard"):
    base = prix_ht * 1.2
    if type_piece.lower() in ["ecran", "écran"]:
        if categorie == "pliant":
            marge = 100
        elif categorie == "haut_de_gamme":
            marge = 70
        else:
            marge = 60
    else:
        marge = 60
    return arrondi_9(base + marge)


# ─── CLASSIFICATION ──────────────────────────────────────────

def classify_piece(name):
    """Classifie le type de pièce depuis le nom produit."""
    low = name.lower()
    if any(x in low for x in ["ecran", "écran", "bloc écran", "lcd", "oled", "tactile"]):
        return "Ecran"
    elif "batterie" in low or "battery" in low:
        return "Batterie"
    elif "connecteur de charge" in low or "connecteur charge" in low:
        return "Connecteur de charge"
    elif "camera arriere" in low or "caméra arrière" in low or "appareil photo" in low:
        return "Camera arriere"
    return None


def extract_quality(name):
    """Extrait la qualité d'un écran depuis le nom produit."""
    low = name.lower()
    if "original pulled" in low or "piec" in low:
        return "Original Pulled"
    elif "assembled" in low:
        return "Assembled"
    elif "bloc écran complet" in low and "original" in low:
        return "Original (Bloc)"
    elif "original" in low:
        return "Original"
    elif "soft oled" in low:
        return "Soft OLED"
    elif "hard oled" in low:
        return "Hard OLED"
    elif "oled" in low and "incell" not in low:
        return "OLED"
    elif "incell" in low:
        return "Incell"
    elif "cof" in low:
        return "COF"
    elif "cog" in low:
        return "COG"
    elif "tft" in low:
        return "TFT"
    elif "ips" in low:
        return "IPS"
    elif "lcd" in low:
        return "LCD"
    elif "premium" in low:
        return "Premium"
    elif "oem" in low:
        return "OEM"
    return "Standard"


# ─── MODEL NORMALIZATION ────────────────────────────────────

def normalize_samsung(name):
    cleaned = re.sub(
        r"\s+(?:Noir|Blanc|Bleu|Rouge|Vert|Rose|Gris|Argent|Or|Violet|Jaune|Orange|"
        r"Cream|Lavande|Graphite|Phantom|Burgundy|Berry|Clair|Nuit|Eclipse|Lime|"
        r"Corail|Lilas|Sauge|Bronze)(?:\s.*)?$", "", name
    )
    cleaned = re.sub(r"\s+(?:GH\d{2}-\d+\w?\s*)+", " ", cleaned)
    cleaned = re.sub(r"\s+SM-\w+", "", cleaned)
    cleaned = re.sub(r"\s+[A-Z]\d{3}[A-Z]?\s*(?:/.*)?$", "", cleaned)
    cleaned = re.sub(r"\s+EB-\w+", "", cleaned)
    cleaned = re.sub(r"\s+HQ-\w+", "", cleaned)

    patterns = [
        r"(Galaxy\s+Z\s+(?:Flip|Fold)\s*\d+\s*(?:5G)?(?:\s+(?:Ultra|FE))?)",
        r"(Galaxy\s+S\d+\s*(?:Ultra|Plus|\+|FE|Lite|5G)*)",
        r"(Galaxy\s+A\d+\s*(?:s|e)?\s*(?:5G|4G)*)",
        r"(Galaxy\s+M\d+\s*(?:s)?)",
        r"(Galaxy\s+Note\s*\d+\s*(?:Ultra|Plus|\+|Lite|5G|FE)*)",
        r"(Galaxy\s+XCover\s*\d+\s*(?:Pro|s)?)",
        r"(Galaxy\s+Tab\s+\w+\s*\d*)",
    ]
    for pat in patterns:
        m = re.search(pat, cleaned, re.IGNORECASE)
        if m:
            return "Samsung " + re.sub(r"\s+", " ", m.group(1).strip())
    return None


def normalize_google(name):
    cleaned = re.sub(r"\s+G\d{3}[\w-]*", "", name)
    cleaned = re.sub(r"\s+\d{10,}\w*", "", cleaned)
    m = re.search(r"(Pixel\s+\d+\s*(?:Pro\s*(?:XL|Fold)?|a\s*(?:5G)?|XL)?)", cleaned, re.IGNORECASE)
    if m:
        return "Google " + m.group(1).strip()
    return None


def normalize_xiaomi(name):
    cleaned = re.sub(r"\s+\d{10,}\w*", "", name)
    cleaned = re.sub(r"\s+BM\w+", "", cleaned)
    cleaned = re.sub(r"\s+BLP\w+", "", cleaned)
    cleaned = re.sub(r"\s+BN\d+\w*", "", cleaned)
    cleaned = re.sub(
        r"\s+(?:Noir|Blanc|Bleu|Rouge|Vert|Rose|Gris|Argent|Or|Violet|Jaune|"
        r"Orange|Azur|Perle|Nuit|Tarnish|Arctic|Global)(?:\s.*)?$", "", cleaned
    )

    patterns = [
        r"(Redmi\s+Note\s+\d+\s*(?:Pro\s*(?:\+|Plus)?|S|T|R)?(?:\s+5G)?)",
        r"(Redmi\s+(?:A\s*)?\d+\s*(?:A|C|Pro|Plus|Note|T)?(?:\s+5G)?)",
        r"(Poco\s+[A-Z]\d+\s*(?:Pro|Plus|GT)?(?:\s+5G)?)",
        r"(Poco\s+(?:M|F|C|X)\d+\s*(?:Pro|Plus|GT)?(?:\s+5G)?)",
        r"(Xiaomi\s+\d+\s*(?:T\s*(?:Pro)?|Lite(?:\s+5G)?|Pro|Ultra|NE|5G)*)",
        r"((?:Xiaomi\s+)?Mi\s+\d+\s*(?:T\s*(?:Pro)?|Lite(?:\s+5G)?|Pro|Ultra|5G|NE)*)",
        r"((?:Xiaomi\s+)?Mi\s+Note\s+\d+\s*(?:Lite|Pro|5G)*)",
        r"((?:Xiaomi\s+)?Mi\s+[A-Z]\d+\s*(?:Lite)?)",
        r"((?:Xiaomi\s+)?Mi\s+Mix\s*\d*(?:\s+5G)?)",
    ]
    for pat in patterns:
        m = re.search(pat, cleaned, re.IGNORECASE)
        if m:
            model = m.group(1).strip()
            if not model.startswith("Xiaomi"):
                model = "Xiaomi " + model
            return model
    return None


def normalize_huawei(name):
    cleaned = re.sub(r"\s+02\d{3}\w+", "", name)
    cleaned = re.sub(r"\s+\d{10,}\w*", "", cleaned)
    cleaned = re.sub(r"\s+HB\d+\w*", "", cleaned)
    cleaned = re.sub(
        r"\s+(?:Noir|Blanc|Bleu|Rouge|Vert|Rose|Gris|Argent|Or|Violet|Jaune|"
        r"Orange|Star|Twilight|Aurora|Breathing|Midnight|Sakura|Phantom|Emerald)(?:\s.*)?$",
        "", cleaned,
    )
    patterns = [
        r"((?:Huawei\s+)?P\s*\d+\s*(?:Pro\s*(?:\+|Plus)?|Lite)?)",
        r"(Huawei\s+P\s+Smart\s*(?:\+|Plus|Z|S|2019|2020|2021)?)",
        r"(Huawei\s+Mate\s+\d+\s*(?:Pro\s*(?:\+)?|Lite|X\s*(?:4G|5G)?|S|RS)?)",
        r"(Huawei\s+Nova\s+\d+\s*(?:i|SE|T|Pro|Lite)?)",
        r"(Huawei\s+Y\d+\s*(?:p|s|a|Prime|Pro)?(?:\s+\d{4})?)",
        r"(Honor\s+\d+\s*(?:X|A|s|Lite|Pro)?)",
        r"(Honor\s+(?:Magic|View|Play|X)\s*\d+\s*(?:Pro|Lite|5G|4G)?)",
    ]
    for pat in patterns:
        m = re.search(pat, cleaned, re.IGNORECASE)
        if m:
            model = m.group(1).strip()
            if model.startswith("P") and not model.startswith(("Poco", "Pixel")):
                model = "Huawei " + model
            return model
    return None


def normalize_motorola(name):
    cleaned = re.sub(r"\s+5[DP]\d{2}C\w*", "", name)
    cleaned = re.sub(r"\s+XT\d+\w*", "", cleaned)
    cleaned = re.sub(r"\s+SB\d+\w*", "", cleaned)
    cleaned = re.sub(r"\s+\(\w+\)", "", cleaned)
    cleaned = re.sub(
        r"\s+(?:KG\d|JE\d|JK\d|KR\d|KS\d|KT\d|MT\d|ND\d|NE\d|NF\d|NG\d|"
        r"NP\d|NQ\d|NR\d|NS\d|NT\d|PC\d|PG\d)\w*", "", cleaned
    )
    cleaned = re.sub(
        r"\s+(?:Noir|Blanc|Bleu|Rouge|Vert|Rose|Gris|Argent|Or|Violet|Jaune|"
        r"Orange|Eclipse|Lunaire|Indigo|Mystic|Titanium|Nebula|Charcoal)(?:\s.*)?$",
        "", cleaned,
    )
    patterns = [
        r"((?:Motorola\s+)?Edge\s+\d+\s*(?:Ultra|Pro|Neo|Lite|Fusion|Plus|5G)?)",
        r"((?:Motorola\s+)?Razr\s+\d+\s*(?:Ultra|Plus)?)",
        r"((?:Motorola\s+)?Moto\s+G\d+\s*(?:Plus|Play|Power|Fast|Stylus|Force|Pro|5G)?)",
        r"((?:Motorola\s+)?Moto\s+G\s+(?:5G|Power|Play|Stylus|Fast|Pure|Pro)\s*\d*)",
        r"((?:Motorola\s+)?Moto\s+E\d+\s*(?:i|s|Play|Plus|Power)?)",
        r"((?:Motorola\s+)?Moto\s+(?:X|Z|One)\s*\d*\s*(?:Vision|Action|Macro|Zoom|Fusion|Hyper|Power|Play|Force|5G)?)",
        r"((?:Motorola\s+)?(?:One|Defy|ThinkPhone)(?:\s+(?:Vision|Action|Macro|Zoom|Fusion|Hyper|Power|5G))?)",
    ]
    for pat in patterns:
        m = re.search(pat, cleaned, re.IGNORECASE)
        if m:
            model = m.group(1).strip()
            if not model.startswith("Motorola"):
                model = "Motorola " + model
            return model
    return None


NORMALIZERS = {
    "Samsung": normalize_samsung,
    "Google": normalize_google,
    "Xiaomi": normalize_xiaomi,
    "Huawei": normalize_huawei,
    "Motorola": normalize_motorola,
}


def is_too_old(model, brand):
    """Filtre les modèles trop anciens (S6 et en-dessous)."""
    low = model.lower()

    if brand == "Samsung":
        m = re.search(r"galaxy\s+s(\d+)", low)
        if m and int(m.group(1)) <= 6:
            return True
        if re.search(r"galaxy\s+j\d", low):
            return True
        m = re.search(r"galaxy\s+note\s*(\d+)", low)
        if m and int(m.group(1)) <= 5:
            return True

    elif brand == "Google":
        m = re.search(r"pixel\s+(\d+)", low)
        if m and int(m.group(1)) <= 2:
            return True

    elif brand == "Xiaomi":
        m = re.search(r"(?:^|\s)mi\s+(\d+)\b", low)
        if m and int(m.group(1)) <= 5 and "note" not in low and "mix" not in low:
            return True
        m = re.search(r"redmi\s+note\s+(\d+)", low)
        if m and int(m.group(1)) <= 4:
            return True

    elif brand == "Huawei":
        m = re.search(r"\bp(\d+)\b", low)
        if m and int(m.group(1)) <= 8 and "smart" not in low:
            return True
        m = re.search(r"mate\s+(\d+)", low)
        if m and int(m.group(1)) <= 8:
            return True

    elif brand == "Motorola":
        m = re.search(r"moto\s+g(\d+)", low)
        if m and int(m.group(1)) <= 4:
            return True
        if re.search(r"moto\s+[xz]", low):
            return True

    return False


# ─── SCRAPING ────────────────────────────────────────────────

def _fetch_mobilax_brand(client, brand_slug, page=1):
    """Fetch une page de résultats Mobilax pour une marque."""
    url = f"{MOBILAX_BASE}/marques/{brand_slug}?page={page}"
    resp = client.get(url, timeout=30.0)
    return resp.text


def _extract_products_rsc(text):
    """Extrait les produits depuis le flux RSC Next.js."""
    products = []
    # Pattern pour extraire id, name, price depuis le RSC stream
    pattern = re.compile(
        r'\\"id\\":(\d+),\\"name\\":\\"((?:[^\\"\\\\]|\\\\.)*)\\",\\"suffix.*?'
        r'\\"prices\\":\[\{\\"id\\":1,\\"name\\":\\"Bronze\\",\\"rate\\":[\d.]+,\\"price\\":([\d.]+)'
    )
    for match in pattern.finditer(text):
        pid = int(match.group(1))
        name = match.group(2).replace('\\"', '"').replace("\\\\", "\\")
        price = float(match.group(3))
        products.append({"id": pid, "name": name, "price_ht": price})
    return products


def scrape_brand(client, brand, brand_slug):
    """Scrape tous les produits d'une marque sur Mobilax."""
    print(f"[SCRAPER] Scraping {brand}...")
    all_products = []

    # Page 1
    text = _fetch_mobilax_brand(client, brand_slug, 1)
    prods = _extract_products_rsc(text)
    all_products.extend(prods)

    # Détecter le nombre total de pages
    total_match = re.search(r'\\"total\\":(\d+)', text)
    if total_match:
        total = int(total_match.group(1))
        per_page = 50
        total_pages = math.ceil(total / per_page)
        print(f"[SCRAPER] {brand}: {total} produits, {total_pages} pages")

        for page in range(2, total_pages + 1):
            try:
                text = _fetch_mobilax_brand(client, brand_slug, page)
                prods = _extract_products_rsc(text)
                all_products.extend(prods)
                if page % 20 == 0:
                    print(f"[SCRAPER] {brand}: page {page}/{total_pages}")
            except Exception as e:
                print(f"[SCRAPER] Erreur page {page}: {e}")
                continue

    print(f"[SCRAPER] {brand}: {len(all_products)} produits récupérés")
    return all_products


def process_products(brand, raw_products):
    """Classifie, normalise et calcule les prix pour les produits d'une marque."""
    normalizer = NORMALIZERS.get(brand)
    if not normalizer:
        return []

    results = []
    grouped = defaultdict(list)

    for p in raw_products:
        name = p["name"]
        if name in ["Bronze", "Silver", "Gold", "Diamond", "Platinum", "Mobilax Repair"]:
            continue

        piece_type = classify_piece(name)
        if not piece_type:
            continue

        model = normalizer(name)
        if not model:
            continue

        if is_too_old(model, brand):
            continue

        quality = extract_quality(name) if piece_type == "Ecran" else ""
        key = (model, piece_type, quality)
        grouped[key].append(p)

    for (model, piece_type, quality), products in grouped.items():
        min_price = min(p["price_ht"] for p in products)
        best_name = min(products, key=lambda p: p["price_ht"])["name"]
        categorie = detect_categorie(model)
        prix_client = calcul_prix_client(min_price, piece_type, categorie)

        results.append({
            "marque": brand,
            "modele": model,
            "type_piece": piece_type,
            "qualite": quality,
            "nom_fournisseur": best_name,
            "prix_fournisseur_ht": min_price,
            "prix_client": prix_client,
            "categorie": categorie,
        })

    return results


# ─── MAIN ENTRY POINT ───────────────────────────────────────

def scrape_and_update():
    """Scrape Mobilax et met à jour la table tarifs."""
    print("[SCRAPER] Démarrage du scraping Mobilax...")
    start = time.time()

    client = httpx.Client(
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        },
        follow_redirects=True,
        timeout=30.0,
    )

    all_tarifs = []

    for brand, slug in BRANDS_SLUGS.items():
        try:
            raw = scrape_brand(client, brand, slug)
            processed = process_products(brand, raw)
            all_tarifs.extend(processed)
            print(f"[SCRAPER] {brand}: {len(processed)} tarifs générés")
        except Exception as e:
            print(f"[SCRAPER] Erreur {brand}: {e}")
            continue

    client.close()

    if not all_tarifs:
        print("[SCRAPER] Aucun tarif récupéré, abandon.")
        return

    # Insérer en BDD
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_cursor() as cur:
        cur.execute("DELETE FROM tarifs")

        for t in all_tarifs:
            cur.execute(
                """INSERT INTO tarifs
                   (marque, modele, type_piece, qualite, nom_fournisseur,
                    prix_fournisseur_ht, prix_client, categorie, source, updated_at)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (
                    t["marque"], t["modele"], t["type_piece"], t["qualite"],
                    t["nom_fournisseur"], t["prix_fournisseur_ht"], t["prix_client"],
                    t["categorie"], "mobilax", now,
                ),
            )

    elapsed = time.time() - start
    print(f"[SCRAPER] Terminé: {len(all_tarifs)} tarifs insérés en {elapsed:.1f}s")
