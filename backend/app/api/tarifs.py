"""
API Tarifs — Gestion des grilles tarifaires de réparation.
"""

import math
import threading
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional

from app.database import get_cursor
from app.models import TarifOut, TarifImportRequest, TarifStats
from app.api.auth import get_current_user

router = APIRouter(prefix="/api/tarifs", tags=["tarifs"])

# ─── TABLE INIT ──────────────────────────────────────────────
INIT_SQL = """
CREATE TABLE IF NOT EXISTS tarifs (
    id SERIAL PRIMARY KEY,
    marque VARCHAR(50) NOT NULL,
    modele VARCHAR(100) NOT NULL,
    type_piece VARCHAR(50) NOT NULL,
    qualite VARCHAR(50) DEFAULT '',
    nom_fournisseur TEXT DEFAULT '',
    prix_fournisseur_ht DECIMAL(10,2),
    prix_client INTEGER NOT NULL,
    categorie VARCHAR(20) DEFAULT 'standard',
    source VARCHAR(50) DEFAULT 'mobilax',
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_tarifs_marque ON tarifs(marque);
CREATE INDEX IF NOT EXISTS idx_tarifs_modele ON tarifs(modele);
CREATE INDEX IF NOT EXISTS idx_tarifs_recherche ON tarifs(marque, modele, type_piece);
"""


def _ensure_table():
    """Crée la table tarifs si elle n'existe pas."""
    try:
        with get_cursor() as cur:
            cur.execute(INIT_SQL)
    except Exception:
        pass  # Table existe déjà


# ─── HELPERS ─────────────────────────────────────────────────

def arrondi_9(prix):
    """Arrondi au 9 : 0-1→9 inf, 2-9→9 sup."""
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


def calcul_prix_client(prix_ht, type_piece, categorie="standard"):
    """
    Règles KLIKPHONE:
    - Écrans standard : prix × 1.2 + 60
    - Écrans haut de gamme : prix × 1.2 + 70
    - Écrans pliants : prix × 1.2 + 100
    - Batteries / Connecteurs / Caméras : prix × 1.2 + 60
    """
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


# ─── ENDPOINTS ───────────────────────────────────────────────

@router.get("", response_model=list[TarifOut])
async def list_tarifs(
    q: Optional[str] = None,
    marque: Optional[str] = None,
    type_piece: Optional[str] = None,
    limit: int = Query(1000, le=5000),
    offset: int = 0,
    user: dict = Depends(get_current_user),
):
    """Liste les tarifs avec filtres optionnels."""
    _ensure_table()

    conditions = []
    params = []

    if q:
        conditions.append("(LOWER(modele) LIKE %s OR LOWER(marque) LIKE %s OR LOWER(nom_fournisseur) LIKE %s)")
        term = f"%{q.lower()}%"
        params.extend([term, term, term])

    if marque:
        conditions.append("LOWER(marque) = %s")
        params.append(marque.lower())

    if type_piece:
        conditions.append("LOWER(type_piece) = %s")
        params.append(type_piece.lower())

    where = "WHERE " + " AND ".join(conditions) if conditions else ""

    with get_cursor() as cur:
        cur.execute(
            f"""SELECT * FROM tarifs {where}
                ORDER BY marque, modele, type_piece, qualite
                LIMIT %s OFFSET %s""",
            params + [limit, offset],
        )
        return cur.fetchall()


@router.get("/stats", response_model=TarifStats)
async def get_stats(user: dict = Depends(get_current_user)):
    """Statistiques sur les tarifs."""
    _ensure_table()

    with get_cursor() as cur:
        cur.execute("""
            SELECT
                COUNT(*) as total_tarifs,
                COUNT(DISTINCT modele) as total_modeles,
                COUNT(DISTINCT marque) as total_marques,
                MIN(prix_client) as prix_min,
                MAX(prix_client) as prix_max,
                MAX(updated_at) as last_update
            FROM tarifs
        """)
        row = cur.fetchone()

        cur.execute("""
            SELECT marque, COUNT(DISTINCT modele) as nb_modeles
            FROM tarifs GROUP BY marque ORDER BY marque
        """)
        par_marque = {r["marque"]: r["nb_modeles"] for r in cur.fetchall()}

    return TarifStats(
        total_tarifs=row["total_tarifs"] or 0,
        total_modeles=row["total_modeles"] or 0,
        total_marques=row["total_marques"] or 0,
        prix_min=row["prix_min"],
        prix_max=row["prix_max"],
        last_update=str(row["last_update"]) if row["last_update"] else None,
        par_marque=par_marque,
    )


@router.post("/import", response_model=dict)
async def import_tarifs(
    data: TarifImportRequest,
    user: dict = Depends(get_current_user),
):
    """Import bulk de tarifs (JSON). Vide et recrée."""
    _ensure_table()

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    count = 0

    with get_cursor() as cur:
        # Vider la table
        cur.execute("DELETE FROM tarifs")

        for t in data.tarifs:
            cur.execute(
                """INSERT INTO tarifs
                   (marque, modele, type_piece, qualite, nom_fournisseur,
                    prix_fournisseur_ht, prix_client, categorie, source, updated_at)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (
                    t.marque, t.modele, t.type_piece, t.qualite,
                    t.nom_fournisseur, t.prix_fournisseur_ht, t.prix_client,
                    t.categorie, t.source, now,
                ),
            )
            count += 1

    return {"ok": True, "imported": count}


@router.post("/update", response_model=dict)
async def update_tarifs(user: dict = Depends(get_current_user)):
    """Lance le scraping Mobilax en background et met à jour la BDD."""
    _ensure_table()

    def _run_scrape():
        try:
            from app.services.scraper_mobilax import scrape_and_update
            scrape_and_update()
        except Exception as e:
            print(f"[SCRAPER] Erreur: {e}")

    thread = threading.Thread(target=_run_scrape, daemon=True)
    thread.start()

    return {"ok": True, "message": "Mise à jour lancée en arrière-plan"}


@router.delete("/clear", response_model=dict)
async def clear_tarifs(user: dict = Depends(get_current_user)):
    """Vide la table tarifs."""
    _ensure_table()

    with get_cursor() as cur:
        cur.execute("DELETE FROM tarifs")
        cur.execute("SELECT COUNT(*) as c FROM tarifs")
        row = cur.fetchone()

    return {"ok": True, "remaining": row["c"]}
