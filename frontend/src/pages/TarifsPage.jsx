import { useState, useEffect, useCallback, useMemo } from 'react';
import { Search, RefreshCw, ChevronDown, ChevronRight, Tag, Monitor, Battery, Plug, Camera, Info } from 'lucide-react';
import api from '../lib/api';

// ─── COULEURS MARQUES ────────────────────────────────────
const BRAND_COLORS = {
  Samsung:  { bg: 'bg-blue-600',   text: 'text-blue-600',   light: 'bg-blue-50',   ring: 'ring-blue-200' },
  Google:   { bg: 'bg-green-600',  text: 'text-green-600',  light: 'bg-green-50',  ring: 'ring-green-200' },
  Xiaomi:   { bg: 'bg-orange-600', text: 'text-orange-600', light: 'bg-orange-50', ring: 'ring-orange-200' },
  Huawei:   { bg: 'bg-red-600',    text: 'text-red-600',    light: 'bg-red-50',    ring: 'ring-red-200' },
  Motorola: { bg: 'bg-cyan-600',   text: 'text-cyan-600',   light: 'bg-cyan-50',   ring: 'ring-cyan-200' },
};

// ─── COULEURS QUALITÉS ───────────────────────────────────
const QUALITY_STYLES = {
  'Original':         { bg: 'bg-emerald-50',  text: 'text-emerald-700', ring: 'ring-emerald-200' },
  'Original (Bloc)':  { bg: 'bg-emerald-50',  text: 'text-emerald-700', ring: 'ring-emerald-200' },
  'Original Pulled':  { bg: 'bg-teal-50',     text: 'text-teal-700',    ring: 'ring-teal-200' },
  'Assembled':        { bg: 'bg-sky-50',      text: 'text-sky-700',     ring: 'ring-sky-200' },
  'Soft OLED':        { bg: 'bg-violet-50',   text: 'text-violet-700',  ring: 'ring-violet-200' },
  'Hard OLED':        { bg: 'bg-purple-50',   text: 'text-purple-700',  ring: 'ring-purple-200' },
  'OLED':             { bg: 'bg-blue-50',     text: 'text-blue-700',    ring: 'ring-blue-200' },
  'Incell':           { bg: 'bg-amber-50',    text: 'text-amber-700',   ring: 'ring-amber-200' },
  'LCD':              { bg: 'bg-zinc-100',    text: 'text-zinc-700',    ring: 'ring-zinc-300' },
  'COF':              { bg: 'bg-slate-50',    text: 'text-slate-700',   ring: 'ring-slate-200' },
  'COG':              { bg: 'bg-slate-50',    text: 'text-slate-700',   ring: 'ring-slate-200' },
  'TFT':              { bg: 'bg-stone-50',    text: 'text-stone-600',   ring: 'ring-stone-200' },
  'Premium':          { bg: 'bg-indigo-50',   text: 'text-indigo-700',  ring: 'ring-indigo-200' },
  'OEM':              { bg: 'bg-gray-50',     text: 'text-gray-600',    ring: 'ring-gray-200' },
  'Standard':         { bg: 'bg-gray-50',     text: 'text-gray-600',    ring: 'ring-gray-200' },
};

const DEFAULT_QUALITY = { bg: 'bg-gray-50', text: 'text-gray-600', ring: 'ring-gray-200' };

const PIECE_ICONS = {
  'Ecran': Monitor,
  'Batterie': Battery,
  'Connecteur de charge': Plug,
  'Camera arriere': Camera,
};

const ALL_BRANDS = ['Samsung', 'Google', 'Xiaomi', 'Huawei', 'Motorola'];

// ─── COMPOSANT PRINCIPAL ─────────────────────────────────

export default function TarifsPage() {
  const [tarifs, setTarifs] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [updating, setUpdating] = useState(false);
  const [search, setSearch] = useState('');
  const [brandFilter, setBrandFilter] = useState('');
  const [expandedModels, setExpandedModels] = useState(new Set());

  // ─── CHARGEMENT DONNÉES ────────────────────────────────
  const loadData = useCallback(async () => {
    setLoading(true);
    try {
      const params = {};
      if (search) params.q = search;
      if (brandFilter) params.marque = brandFilter;

      const [tarifsData, statsData] = await Promise.all([
        api.getTarifs(params),
        api.getTarifsStats(),
      ]);
      setTarifs(tarifsData);
      setStats(statsData);
    } catch (err) {
      console.error('Erreur chargement tarifs:', err);
    } finally {
      setLoading(false);
    }
  }, [search, brandFilter]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  // ─── MISE À JOUR ──────────────────────────────────────
  const handleUpdate = async () => {
    if (updating) return;
    setUpdating(true);
    try {
      await api.updateTarifs();
      // Attendre un peu puis recharger
      setTimeout(async () => {
        await loadData();
        setUpdating(false);
      }, 3000);
    } catch (err) {
      console.error('Erreur mise à jour:', err);
      setUpdating(false);
    }
  };

  // ─── TOGGLE ACCORDÉON ─────────────────────────────────
  const toggleModel = (key) => {
    setExpandedModels(prev => {
      const next = new Set(prev);
      if (next.has(key)) next.delete(key);
      else next.add(key);
      return next;
    });
  };

  // ─── STRUCTURE DES DONNÉES ─────────────────────────────
  const structured = useMemo(() => {
    // Grouper par marque → modèle
    const byBrand = {};

    for (const t of tarifs) {
      if (!byBrand[t.marque]) byBrand[t.marque] = {};
      if (!byBrand[t.marque][t.modele]) {
        byBrand[t.marque][t.modele] = { ecrans: [], batterie: null, connecteur: null, camera: null };
      }

      const model = byBrand[t.marque][t.modele];
      const piece = t.type_piece?.toLowerCase();

      if (piece === 'ecran') {
        model.ecrans.push(t);
      } else if (piece === 'batterie') {
        if (!model.batterie || t.prix_client < model.batterie.prix_client) {
          model.batterie = t;
        }
      } else if (piece === 'connecteur de charge') {
        if (!model.connecteur || t.prix_client < model.connecteur.prix_client) {
          model.connecteur = t;
        }
      } else if (piece === 'camera arriere') {
        if (!model.camera || t.prix_client < model.camera.prix_client) {
          model.camera = t;
        }
      }
    }

    // Trier les écrans par prix
    for (const brand of Object.values(byBrand)) {
      for (const model of Object.values(brand)) {
        model.ecrans.sort((a, b) => a.prix_client - b.prix_client);
      }
    }

    return byBrand;
  }, [tarifs]);

  // ─── COMPTEURS ─────────────────────────────────────────
  const totalModels = useMemo(() => {
    let count = 0;
    for (const brand of Object.values(structured)) {
      count += Object.keys(brand).length;
    }
    return count;
  }, [structured]);

  // ─── RENDER ────────────────────────────────────────────
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-6 space-y-5">

      {/* ─── HEADER ─────────────────────────────────── */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <div>
          <div className="flex items-center gap-2 text-sm text-gray-400 mb-1">
            <Tag className="w-4 h-4" />
            <span>Grille tarifaire</span>
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-gray-900">
            Tarifs réparation
          </h1>
        </div>
        <button
          onClick={handleUpdate}
          disabled={updating}
          className="btn bg-violet-600 text-white hover:bg-violet-700 active:bg-violet-800 shadow-sm disabled:opacity-50"
        >
          <RefreshCw className={`w-4 h-4 ${updating ? 'animate-spin' : ''}`} />
          {updating ? 'Mise à jour...' : 'Mettre à jour les tarifs'}
        </button>
      </div>

      {/* ─── STATS CARDS ────────────────────────────── */}
      {stats && stats.total_tarifs > 0 && (
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <div className="card px-4 py-3">
            <p className="text-2xl font-bold text-gray-900">{stats.total_modeles}</p>
            <p className="text-xs text-gray-500 font-medium">Modèles</p>
          </div>
          <div className="card px-4 py-3">
            <p className="text-2xl font-bold text-gray-900">{stats.total_marques}</p>
            <p className="text-xs text-gray-500 font-medium">Marques</p>
          </div>
          <div className="card px-4 py-3">
            <p className="text-2xl font-bold text-violet-600">{stats.prix_min}€ – {stats.prix_max}€</p>
            <p className="text-xs text-gray-500 font-medium">Fourchette prix</p>
          </div>
          <div className="card px-4 py-3">
            <p className="text-2xl font-bold text-gray-900">{stats.total_tarifs}</p>
            <p className="text-xs text-gray-500 font-medium">Lignes tarifs</p>
          </div>
        </div>
      )}

      {/* ─── RECHERCHE + FILTRES ────────────────────── */}
      <div className="card px-4 py-4 space-y-3">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Rechercher un modèle (ex: Galaxy S24, Pixel 9, Redmi Note 13...)"
            className="input pl-10"
          />
        </div>
        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => setBrandFilter('')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              !brandFilter
                ? 'bg-gray-900 text-white'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            Toutes
          </button>
          {ALL_BRANDS.map(b => {
            const colors = BRAND_COLORS[b];
            const active = brandFilter.toLowerCase() === b.toLowerCase();
            return (
              <button
                key={b}
                onClick={() => setBrandFilter(active ? '' : b)}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                  active
                    ? `${colors.bg} text-white`
                    : `${colors.light} ${colors.text} hover:opacity-80`
                }`}
              >
                {b}
                {stats?.par_marque?.[b] && (
                  <span className="ml-1 opacity-70">({stats.par_marque[b]})</span>
                )}
              </button>
            );
          })}
        </div>
      </div>

      {/* ─── CONTENU ────────────────────────────────── */}
      {loading ? (
        <div className="card p-12 text-center">
          <div className="animate-spin w-8 h-8 border-2 border-violet-500 border-t-transparent rounded-full mx-auto mb-3" />
          <p className="text-sm text-gray-500">Chargement des tarifs...</p>
        </div>
      ) : tarifs.length === 0 ? (
        <div className="card p-12 text-center">
          <Tag className="w-12 h-12 text-gray-300 mx-auto mb-3" />
          <p className="text-lg font-semibold text-gray-900 mb-1">Aucun tarif</p>
          <p className="text-sm text-gray-500 mb-4">
            {search || brandFilter
              ? "Aucun résultat pour cette recherche."
              : "Cliquez sur \"Mettre à jour les tarifs\" pour importer les prix depuis Mobilax."}
          </p>
          {!search && !brandFilter && (
            <button onClick={handleUpdate} disabled={updating} className="btn bg-violet-600 text-white hover:bg-violet-700">
              <RefreshCw className={`w-4 h-4 ${updating ? 'animate-spin' : ''}`} />
              Importer les tarifs
            </button>
          )}
        </div>
      ) : (
        <div className="space-y-4">
          {ALL_BRANDS.filter(b => structured[b] && Object.keys(structured[b]).length > 0).map(brand => (
            <BrandSection
              key={brand}
              brand={brand}
              models={structured[brand]}
              expandedModels={expandedModels}
              toggleModel={toggleModel}
            />
          ))}
        </div>
      )}

      {/* ─── FOOTER ─────────────────────────────────── */}
      {tarifs.length > 0 && (
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 text-xs text-gray-400 px-1">
          <p>{totalModels} modèles · {tarifs.length} lignes tarifs</p>
          <div className="flex items-center gap-1">
            <Info className="w-3 h-3" />
            <p>Source: Mobilax · Formule: (HT × 1.2) + marge → arrondi au 9</p>
          </div>
          {stats?.last_update && (
            <p>Dernière MAJ: {new Date(stats.last_update).toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' })}</p>
          )}
        </div>
      )}
    </div>
  );
}


// ─── SECTION MARQUE ──────────────────────────────────────

function BrandSection({ brand, models, expandedModels, toggleModel }) {
  const colors = BRAND_COLORS[brand] || BRAND_COLORS.Samsung;
  const sortedModels = Object.entries(models).sort((a, b) => a[0].localeCompare(b[0]));
  const modelCount = sortedModels.length;

  return (
    <div className="card overflow-hidden">
      {/* Brand header */}
      <div className={`${colors.bg} px-5 py-3 flex items-center justify-between`}>
        <h2 className="text-white font-bold text-sm tracking-wide uppercase">
          {brand}
        </h2>
        <span className="text-white/70 text-xs font-medium">{modelCount} modèles</span>
      </div>

      {/* Models list */}
      <div className="divide-y divide-gray-50">
        {sortedModels.map(([modelName, data], i) => (
          <ModelRow
            key={modelName}
            brand={brand}
            modelName={modelName}
            data={data}
            expanded={expandedModels.has(`${brand}::${modelName}`)}
            toggle={() => toggleModel(`${brand}::${modelName}`)}
            index={i}
          />
        ))}
      </div>
    </div>
  );
}


// ─── LIGNE MODÈLE (ACCORDÉON) ───────────────────────────

function ModelRow({ brand, modelName, data, expanded, toggle, index }) {
  const { ecrans, batterie, connecteur, camera } = data;
  const colors = BRAND_COLORS[brand] || BRAND_COLORS.Samsung;

  // Nom du modèle sans la marque
  const displayName = modelName
    .replace(/^Samsung\s+/i, '')
    .replace(/^Google\s+/i, '')
    .replace(/^Xiaomi\s+/i, '')
    .replace(/^Huawei\s+/i, '')
    .replace(/^Motorola\s+/i, '')
    .replace(/^Honor\s+/i, '');

  // Prix écrans range
  const ecranMin = ecrans.length > 0 ? ecrans[0].prix_client : null;
  const ecranMax = ecrans.length > 0 ? ecrans[ecrans.length - 1].prix_client : null;

  return (
    <div>
      {/* Ligne principale cliquable */}
      <div
        onClick={toggle}
        className={`flex items-center gap-3 px-5 py-3.5 cursor-pointer transition-colors
          ${expanded ? `${colors.light}` : index % 2 === 0 ? 'bg-white' : 'bg-gray-50/50'}
          hover:${colors.light}`}
      >
        {/* Chevron */}
        <div className={`${colors.text} transition-transform ${expanded ? 'rotate-0' : ''}`}>
          {expanded
            ? <ChevronDown className="w-4 h-4" />
            : <ChevronRight className="w-4 h-4" />
          }
        </div>

        {/* Nom modèle */}
        <div className="flex-1 min-w-0">
          <p className="font-semibold text-sm text-gray-900 truncate">{displayName}</p>
          {ecrans.length > 1 && (
            <span className="text-[10px] text-gray-400 font-medium">
              {ecrans.length} qualité{ecrans.length > 1 ? 's' : ''} écran
            </span>
          )}
        </div>

        {/* Prix résumé */}
        <div className="hidden sm:grid sm:grid-cols-4 gap-3 text-center shrink-0" style={{ width: '400px' }}>
          <PriceCell
            icon={Monitor}
            value={ecranMin}
            valueMax={ecranMax}
            label="Écran"
            color="text-violet-600"
          />
          <PriceCell
            icon={Battery}
            value={batterie?.prix_client}
            label="Batterie"
            color="text-emerald-600"
          />
          <PriceCell
            icon={Plug}
            value={connecteur?.prix_client}
            label="Connecteur"
            color="text-blue-600"
          />
          <PriceCell
            icon={Camera}
            value={camera?.prix_client}
            label="Caméra"
            color="text-amber-600"
          />
        </div>

        {/* Prix mobile */}
        <div className="sm:hidden text-right">
          {ecranMin && (
            <p className="text-sm font-bold text-violet-600">
              {ecranMin === ecranMax ? `${ecranMin}€` : `${ecranMin}–${ecranMax}€`}
            </p>
          )}
        </div>
      </div>

      {/* Accordéon déplié */}
      {expanded && (
        <div className={`px-5 py-4 ${colors.light} border-t border-gray-100`}>
          {/* Écrans */}
          {ecrans.length > 0 && (
            <div className="mb-4">
              <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
                Écrans ({ecrans.length} qualité{ecrans.length > 1 ? 's' : ''})
              </p>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
                {ecrans.map((e, i) => (
                  <QualityCard key={i} tarif={e} />
                ))}
              </div>
            </div>
          )}

          {/* Autres pièces */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
            {batterie && (
              <PieceCard label="Batterie" icon={Battery} tarif={batterie} color="emerald" />
            )}
            {connecteur && (
              <PieceCard label="Connecteur de charge" icon={Plug} tarif={connecteur} color="blue" />
            )}
            {camera && (
              <PieceCard label="Caméra arrière" icon={Camera} tarif={camera} color="amber" />
            )}
          </div>

          {/* Détail prix mobile */}
          <div className="sm:hidden mt-3 grid grid-cols-3 gap-2">
            {batterie && (
              <div className="text-center">
                <p className="text-xs text-gray-400">Batterie</p>
                <p className="text-sm font-bold text-emerald-600">{batterie.prix_client}€</p>
              </div>
            )}
            {connecteur && (
              <div className="text-center">
                <p className="text-xs text-gray-400">Connecteur</p>
                <p className="text-sm font-bold text-blue-600">{connecteur.prix_client}€</p>
              </div>
            )}
            {camera && (
              <div className="text-center">
                <p className="text-xs text-gray-400">Caméra</p>
                <p className="text-sm font-bold text-amber-600">{camera.prix_client}€</p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}


// ─── CELLULE PRIX (RÉSUMÉ) ──────────────────────────────

function PriceCell({ icon: Icon, value, valueMax, label, color }) {
  if (!value) return (
    <div className="text-center">
      <p className="text-xs text-gray-300">—</p>
    </div>
  );

  const display = valueMax && valueMax !== value
    ? `${value}–${valueMax}€`
    : `${value}€`;

  return (
    <div className="text-center">
      <p className={`text-sm font-bold ${color}`}>{display}</p>
      <p className="text-[10px] text-gray-400">{label}</p>
    </div>
  );
}


// ─── CARTE QUALITÉ ÉCRAN ────────────────────────────────

function QualityCard({ tarif }) {
  const style = QUALITY_STYLES[tarif.qualite] || DEFAULT_QUALITY;

  return (
    <div className={`rounded-xl px-4 py-3 ring-1 ${style.bg} ${style.ring} flex items-center justify-between gap-3`}>
      <div className="min-w-0">
        <span className={`inline-block px-2 py-0.5 rounded-md text-[11px] font-bold ${style.bg} ${style.text} ring-1 ${style.ring}`}>
          {tarif.qualite || 'Standard'}
        </span>
        <p className="text-[10px] text-gray-400 mt-1 truncate">{tarif.prix_fournisseur_ht?.toFixed(2)}€ HT</p>
      </div>
      <p className="text-xl font-bold text-gray-900 shrink-0">{tarif.prix_client}€</p>
    </div>
  );
}


// ─── CARTE PIÈCE (BATTERIE, CONNECTEUR, CAMÉRA) ────────

function PieceCard({ label, icon: Icon, tarif, color }) {
  return (
    <div className="hidden sm:flex items-center gap-3 bg-white rounded-xl px-4 py-3 ring-1 ring-gray-100">
      <div className={`w-8 h-8 rounded-lg bg-${color}-50 flex items-center justify-center`}>
        <Icon className={`w-4 h-4 text-${color}-600`} />
      </div>
      <div className="flex-1 min-w-0">
        <p className="text-xs font-medium text-gray-600">{label}</p>
        <p className="text-[10px] text-gray-400">{tarif.prix_fournisseur_ht?.toFixed(2)}€ HT</p>
      </div>
      <p className={`text-lg font-bold text-${color}-600`}>{tarif.prix_client}€</p>
    </div>
  );
}
