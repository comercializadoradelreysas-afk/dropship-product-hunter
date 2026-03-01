import streamlit as st
import pandas as pd
import time
import os
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="OmniSpy AI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

:root {
    --bg:         #0E1117;
    --card:       #161C27;
    --hover:      #1C2436;
    --border:     #1E2D40;
    --border2:    #243347;
    --sage:       #6B9E82;
    --sage-l:     #89B89C;
    --sage-g:     rgba(107,158,130,0.15);
    --sage-b:     rgba(107,158,130,0.35);
    --gold:       #C8A96E;
    --gold-l:     #D4BA86;
    --gold-g:     rgba(200,169,110,0.12);
    --txt:        #E8E4DC;
    --txt2:       #9AA3B2;
    --muted:      #5C6878;
    --red:        #C47B7B;
    --blue:       #6B91C8;
}
* { font-family: 'DM Sans', sans-serif; }
h1,h2,h3 { font-family: 'Cormorant Garamond', serif; }
code { font-family: 'DM Mono', monospace; }

.stApp { background: var(--bg); color: var(--txt); }
.main .block-container { padding: 1.5rem 2rem 4rem 2rem; max-width: 1500px; }
[data-testid="stSidebar"] { background: #0A0F18; border-right: 1px solid var(--border); }
#MainMenu, footer, header, [data-testid="stToolbar"] { visibility: hidden; display: none; }

/* Header */
.top-header { padding: 2rem 0 1.5rem; border-bottom: 1px solid var(--border); margin-bottom: 2rem; display: flex; justify-content: space-between; align-items: flex-end; }
.top-header h1 { font-size: 2.5rem; font-weight: 600; color: var(--txt); margin: 0; line-height: 1; }
.top-header .sub { font-size: 0.82rem; color: var(--muted); margin-top: 6px; }
.tag { font-family: 'DM Mono', monospace; font-size: 0.65rem; letter-spacing: 3px; text-transform: uppercase; color: var(--sage); background: var(--sage-g); border: 1px solid var(--sage-b); padding: 3px 10px; border-radius: 4px; }
.pulse { width: 7px; height: 7px; border-radius: 50%; background: var(--sage); display: inline-block; animation: pulse 2.5s ease-in-out infinite; margin-right: 6px; }
@keyframes pulse { 0%,100%{opacity:1;box-shadow:0 0 0 0 rgba(107,158,130,0.4);}50%{opacity:.6;box-shadow:0 0 0 5px rgba(107,158,130,0);} }

/* Platform selector */
.platform-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin: 1.2rem 0; }
.plat-card { background: var(--card); border: 2px solid var(--border); border-radius: 12px; padding: 16px 12px; text-align: center; cursor: pointer; transition: all 0.2s; }
.plat-card:hover { border-color: var(--sage-b); background: var(--hover); }
.plat-card.active { border-color: var(--sage); background: var(--sage-g); }
.plat-icon { font-size: 1.8rem; margin-bottom: 6px; }
.plat-name { font-size: 0.8rem; font-weight: 600; color: var(--txt); }
.plat-status { font-size: 0.68rem; color: var(--muted); font-family: 'DM Mono', monospace; margin-top: 2px; }

/* Country pills */
.country-grid { display: flex; gap: 8px; flex-wrap: wrap; margin: 1rem 0; }
.country-pill { padding: 6px 16px; border-radius: 20px; border: 1px solid var(--border2); font-size: 0.8rem; cursor: pointer; transition: all 0.2s; background: var(--card); color: var(--txt2); }
.country-pill.active { background: var(--sage-g); border-color: var(--sage); color: var(--sage-l); font-weight: 600; }
.country-pill.target { background: rgba(200,169,110,0.15); border-color: var(--gold); color: var(--gold); font-weight: 700; }

/* Metrics */
.metric-row { display: grid; grid-template-columns: repeat(6, 1fr); gap: 10px; margin-bottom: 1.5rem; }
.met { background: var(--card); border: 1px solid var(--border); border-radius: 10px; padding: 16px 14px; }
.met-v { font-family: 'Cormorant Garamond', serif; font-size: 2rem; font-weight: 700; color: var(--txt); line-height: 1; }
.met-v.g { color: var(--sage-l); }
.met-v.gold { color: var(--gold); }
.met-l { font-size: 0.68rem; color: var(--muted); text-transform: uppercase; letter-spacing: 1.5px; margin-top: 4px; }
.met-d { font-size: 0.72rem; color: var(--sage); font-family: 'DM Mono', monospace; margin-top: 2px; }

/* Product winner card */
.winner-card { background: var(--card); border: 1px solid var(--border); border-radius: 14px; padding: 0; margin-bottom: 14px; overflow: hidden; transition: all 0.2s; }
.winner-card:hover { border-color: var(--border2); box-shadow: 0 6px 30px rgba(0,0,0,0.3); }
.winner-card-inner { display: grid; grid-template-columns: 180px 1fr 200px 160px; gap: 0; }

.prod-image { width: 180px; height: 180px; object-fit: cover; border-radius: 14px 0 0 14px; }
.prod-image-placeholder { width: 180px; height: 180px; background: var(--hover); border-radius: 14px 0 0 14px; display: flex; align-items: center; justify-content: center; font-size: 3rem; }

.prod-info { padding: 20px; }
.prod-name { font-family: 'Cormorant Garamond', serif; font-size: 1.3rem; font-weight: 600; color: var(--txt); margin-bottom: 4px; }
.prod-id { font-family: 'DM Mono', monospace; font-size: 0.72rem; color: var(--muted); margin-bottom: 10px; }
.prod-desc { font-size: 0.83rem; color: var(--txt2); line-height: 1.6; margin-bottom: 12px; }

.prod-data { padding: 20px 16px; border-left: 1px solid var(--border); }
.data-item { display: flex; justify-content: space-between; padding: 7px 0; border-bottom: 1px solid var(--border); }
.data-item:last-child { border: none; }
.dk { font-size: 0.75rem; color: var(--muted); }
.dv { font-size: 0.8rem; color: var(--txt); font-family: 'DM Mono', monospace; }
.dv.g { color: var(--sage-l); }
.dv.gold { color: var(--gold); }

.prod-score { padding: 20px 16px; border-left: 1px solid var(--border); display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; }
.score-big { font-family: 'Cormorant Garamond', serif; font-size: 3rem; font-weight: 700; line-height: 1; }
.score-big.hi { color: var(--sage-l); }
.score-big.mid { color: var(--gold); }
.score-big.lo { color: var(--red); }
.score-lbl { font-size: 0.65rem; color: var(--muted); text-transform: uppercase; letter-spacing: 2px; margin-top: 2px; }

/* Badge */
.badge { display: inline-flex; align-items: center; padding: 2px 9px; border-radius: 4px; font-size: 0.68rem; font-weight: 500; font-family: 'DM Mono', monospace; margin-right: 4px; }
.b-sage { background: var(--sage-g); color: var(--sage-l); border: 1px solid var(--sage-b); }
.b-gold { background: var(--gold-g); color: var(--gold); border: 1px solid rgba(200,169,110,0.3); }
.b-red  { background: rgba(196,123,123,0.1); color: var(--red); border: 1px solid rgba(196,123,123,0.25); }
.b-blue { background: rgba(107,145,200,0.1); color: var(--blue); border: 1px solid rgba(107,145,200,0.25); }

/* CTA Box */
.cta-box { background: linear-gradient(135deg, rgba(107,158,130,0.1), rgba(200,169,110,0.08)); border: 1px solid var(--sage-b); border-radius: 10px; padding: 14px 18px; margin-top: 10px; }
.cta-title { font-size: 0.78rem; font-weight: 600; color: var(--sage-l); margin-bottom: 4px; text-transform: uppercase; letter-spacing: 1px; }
.cta-url { font-family: 'DM Mono', monospace; font-size: 0.8rem; color: var(--gold); word-break: break-all; }
.cta-hint { font-size: 0.75rem; color: var(--txt2); margin-top: 6px; line-height: 1.5; }

/* Competition table */
.comp-row { display: grid; grid-template-columns: 40px 1fr 80px 80px 80px 100px; gap: 8px; padding: 10px 14px; border-bottom: 1px solid var(--border); align-items: center; font-size: 0.82rem; }
.comp-header { background: var(--hover); border-radius: 8px 8px 0 0; font-size: 0.7rem; color: var(--muted); text-transform: uppercase; letter-spacing: 1px; }
.comp-rank { font-family: 'DM Mono', monospace; color: var(--muted); font-size: 0.8rem; }

/* Keyword chips */
.kw-grid { display: flex; gap: 6px; flex-wrap: wrap; margin: 0.8rem 0; }
.kw-chip { background: var(--hover); border: 1px solid var(--border2); border-radius: 6px; padding: 4px 12px; font-size: 0.78rem; color: var(--txt2); cursor: pointer; transition: all 0.2s; }
.kw-chip:hover, .kw-chip.active { background: var(--sage-g); border-color: var(--sage-b); color: var(--sage-l); }

/* Dividers */
.div { height: 1px; background: var(--border); margin: 1.2rem 0; }
.div-a { height: 1px; background: linear-gradient(90deg, var(--sage-b), transparent); margin: 1.2rem 0; }

/* Sidebar */
.sb-lbl { font-family: 'DM Mono', monospace; font-size: 0.62rem; letter-spacing: 2.5px; text-transform: uppercase; color: var(--muted); margin-bottom: 8px; padding-bottom: 5px; border-bottom: 1px solid var(--border); }
.api-row { display: flex; align-items: center; gap: 7px; padding: 5px 0; font-size: 0.78rem; color: var(--txt2); }
.dot { width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; }
.dot-on { background: var(--sage); }
.dot-off { background: var(--red); }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { background: transparent; border-bottom: 1px solid var(--border); gap: 0; padding: 0; }
.stTabs [data-baseweb="tab"] { color: var(--muted); font-size: 0.82rem; padding: 10px 20px; border-radius: 0; border-bottom: 2px solid transparent; }
.stTabs [aria-selected="true"] { color: var(--sage-l) !important; border-bottom: 2px solid var(--sage) !important; background: transparent !important; }

/* Buttons */
.stButton > button { background: transparent !important; color: var(--sage-l) !important; border: 1px solid var(--sage-b) !important; border-radius: 7px !important; font-size: 0.82rem !important; padding: 9px 20px !important; transition: all 0.2s !important; }
.stButton > button:hover { background: var(--sage-g) !important; border-color: var(--sage) !important; }

/* Inputs */
.stTextInput > div > div, .stSelectbox > div, .stMultiSelect > div, .stTextArea > div { background: var(--card) !important; border-color: var(--border) !important; border-radius: 7px !important; }

/* Info box */
.info-box { background: var(--card); border: 1px solid var(--border); border-left: 3px solid var(--sage); border-radius: 0 8px 8px 0; padding: 12px 16px; font-size: 0.82rem; color: var(--txt2); margin: 0.8rem 0; }

.section-t { font-family: 'Cormorant Garamond', serif; font-size: 1.4rem; font-weight: 600; color: var(--txt); margin-bottom: 3px; }
.section-s { font-size: 0.78rem; color: var(--muted); margin-bottom: 1rem; }
</style>
""", unsafe_allow_html=True)


# ─── KEYWORDS POR NICHO ───────────────────────────────────────────────────────
KEYWORDS_BY_NICHE = {
    "Salud & Bienestar": ["colágeno", "suplementos", "vitaminas", "pérdida de peso", "detox", "antiedad", "proteína", "articulaciones", "digestión", "energía"],
    "Belleza & Cuidado": ["rodillo jade", "masajeador facial", "sérum", "antiage", "piel radiante", "crema hidratante", "maquillaje", "cabello", "uñas"],
    "Hogar & Organización": ["organizador", "cocina gadget", "limpieza hogar", "almacenamiento", "decoración", "iluminación LED", "jardín", "herramientas"],
    "Limpieza & Higiene": ["cepillo eléctrico", "limpiador ultrasónico", "spray desinfectante", "trapeador", "aspiradora mini", "quitamanchas"],
    "Tecnología & Gadgets": ["auriculares inalámbricos", "cargador rápido", "soporte celular", "smartwatch", "lámpara LED", "mini proyector"],
    "Mascotas": ["cama mascotas", "juguete perro", "alimentador automático", "collar GPS", "arnés", "cepillo mascotas"],
    "Bebés & Niños": ["monitor bebé", "silla de comer", "juguete educativo", "portabebé", "lámpara nocturna"],
    "Fitness & Deporte": ["banda resistencia", "rueda abdomen", "colchoneta yoga", "mancuernas", "saltarín", "masajeador muscular"],
}

KEYWORDS_GENERAL = [
    "envío gratis", "50% descuento", "compra ahora", "oferta limitada",
    "obtenga el suyo", "agotarse pronto", "free shipping", "50% off",
    "buy now", "spedizione gratis", "gratis ongkir", "envío rápido",
]

COUNTRIES = {
    "🇨🇴 Colombia":  {"code": "CO", "flag": "🇨🇴", "currency": "COP", "multiplier": 4200},
    "🇲🇽 México":    {"code": "MX", "flag": "🇲🇽", "currency": "MXN", "multiplier": 17},
    "🇨🇱 Chile":     {"code": "CL", "flag": "🇨🇱", "currency": "CLP", "multiplier": 950},
    "🇪🇨 Ecuador":   {"code": "EC", "flag": "🇪🇨", "currency": "USD", "multiplier": 1},
    "🇵🇪 Perú":      {"code": "PE", "flag": "🇵🇪", "currency": "PEN", "multiplier": 3.8},
    "🇦🇷 Argentina": {"code": "AR", "flag": "🇦🇷", "currency": "ARS", "multiplier": 900},
    "🇪🇸 España":    {"code": "ES", "flag": "🇪🇸", "currency": "EUR", "multiplier": 0.92},
    "🇺🇸 Global":    {"code": "ALL","flag": "🌎", "currency": "USD", "multiplier": 1},
}

PLATFORMS = [
    {"id": "facebook",  "name": "Facebook Ads",  "icon": "📘", "status": "Activo",    "color": "#1877F2"},
    {"id": "tiktok",    "name": "TikTok Ads",    "icon": "🎵", "status": "Activo",    "color": "#FF0050"},
    {"id": "instagram", "name": "Instagram Ads", "icon": "📸", "status": "Pronto",    "color": "#E1306C"},
    {"id": "pinterest", "name": "Pinterest Ads", "icon": "📌", "status": "Pronto",    "color": "#E60023"},
]

PRODUCT_IMAGES = {
    "Salud & Bienestar":   "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=300&h=300&fit=crop",
    "Belleza & Cuidado":   "https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?w=300&h=300&fit=crop",
    "Hogar & Organización":"https://images.unsplash.com/photo-1484101403633-562f891dc89a?w=300&h=300&fit=crop",
    "Limpieza & Higiene":  "https://images.unsplash.com/photo-1585421514738-01798e348b17?w=300&h=300&fit=crop",
    "Tecnología & Gadgets":"https://images.unsplash.com/photo-1468495244123-6c6c332eeece?w=300&h=300&fit=crop",
    "Mascotas":            "https://images.unsplash.com/photo-1601758125946-6ec2ef64daf8?w=300&h=300&fit=crop",
    "Fitness & Deporte":   "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=300&h=300&fit=crop",
    "Bebés & Niños":       "https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=300&h=300&fit=crop",
}

def get_demo_winners(target_country, search_countries, nichos):
    """Genera productos ganadores detectados en otros países para vender en el target"""
    products = [
        {"id": "FB-240228-7821", "name": "Colágeno Marino Premium 5000mg", "niche": "Salud & Bienestar",
         "origin_country": "🇪🇸 España", "platform": "facebook",
         "store": "vitalife-es.myshopify.com", "store_url": "https://vitalife-es.myshopify.com/products/colageno-marino",
         "ad_id": "6382910475201", "ad_days": 34, "score": 96, "trend": "Rising",
         "price_usd": 39.99, "cost_usd": 3.20, "margin": 92.0,
         "monthly_revenue": 18400, "competition": "Baja",
         "keywords": ["envío gratis", "antiedad"], "value_perception": "Muy Alta",
         "why_winner": "34 días activo con alto presupuesto. Recompra mensual. Margen 92%. Audiencia mujeres 35-55 sin competencia directa en Colombia.",
         "cta_hint": "Busca en la tienda los creativos de video — usan testimonio de cliente real + antes/después. Fácil de replicar para Colombia."},
        {"id": "TK-240227-3341", "name": "Rodillo Jade Gua Sha Set Lujo", "niche": "Belleza & Cuidado",
         "origin_country": "🇺🇸 Global", "platform": "tiktok",
         "store": "glowskin-us.myshopify.com", "store_url": "https://glowskin-us.myshopify.com/products/jade-roller-set",
         "ad_id": "7291038847562", "ad_days": 21, "score": 91, "trend": "Rising",
         "price_usd": 44.99, "cost_usd": 3.80, "margin": 91.6,
         "monthly_revenue": 12800, "competition": "Media",
         "keywords": ["obtenga el suyo", "piel radiante"], "value_perception": "Alta",
         "why_winner": "21 días activo en TikTok con 2.3M views orgánico. Costo real $3.8 USD. En Colombia puede venderse a $180.000 COP con percepción de lujo.",
         "cta_hint": "El video viral muestra el efecto de desinflamación en 60 segundos. Busca UGC creators en Colombia para replicar el contenido."},
        {"id": "FB-240225-9912", "name": "Organizador Magnético Cables USB", "niche": "Hogar & Organización",
         "origin_country": "🇲🇽 México", "platform": "facebook",
         "store": "ordenpro-mx.myshopify.com", "store_url": "https://ordenpro-mx.myshopify.com/products/organizador-cables",
         "ad_id": "6198273645019", "ad_days": 18, "score": 84, "trend": "Rising",
         "price_usd": 19.99, "cost_usd": 1.80, "margin": 91.0,
         "monthly_revenue": 8200, "competition": "Baja",
         "keywords": ["compra ahora", "oferta limitada"], "value_perception": "Media-Alta",
         "why_winner": "Problema universal: cables desordenados. Activo 18 días en México. Fácil de importar. Ticket bajo = impulso de compra alto.",
         "cta_hint": "Anuncia a audiencia de profesionales home office 25-45. El ángulo 'escritorio perfecto' funciona mejor que 'organización'."},
        {"id": "FB-240220-5543", "name": "Cepillo Eléctrico Limpia-Todo 360°", "niche": "Limpieza & Higiene",
         "origin_country": "🇦🇷 Argentina", "platform": "facebook",
         "store": "cleanpro-ar.myshopify.com", "store_url": "https://cleanpro-ar.myshopify.com/products/cepillo-electrico",
         "ad_id": "6847291038475", "ad_days": 15, "score": 79, "trend": "Stable",
         "price_usd": 29.99, "cost_usd": 4.50, "margin": 85.0,
         "monthly_revenue": 6100, "competition": "Media",
         "keywords": ["50% descuento", "envío gratis"], "value_perception": "Alta",
         "why_winner": "Viral en Argentina y España. El ángulo de limpieza de azulejos sin esfuerzo genera alta retención de video. Compra impulsiva.",
         "cta_hint": "Usa ángulo 'baño brillante en 2 minutos'. Audiencia mujeres 28-50. El descuento del 50% en el CTA aumenta 3x el CTR."},
        {"id": "TK-240222-1127", "name": "Parches Detox Bambú Pie", "niche": "Salud & Bienestar",
         "origin_country": "🇨🇱 Chile", "platform": "tiktok",
         "store": "detoxlife-cl.myshopify.com", "store_url": "https://detoxlife-cl.myshopify.com/products/parches-detox",
         "ad_id": "7108394726510", "ad_days": 28, "score": 88, "trend": "Rising",
         "price_usd": 17.99, "cost_usd": 1.20, "margin": 93.3,
         "monthly_revenue": 14200, "competition": "Baja",
         "keywords": ["gratis ongkir", "detox natural"], "value_perception": "Alta",
         "why_winner": "28 días activo. Margen 93%. Ticket bajo = alta conversión. El ángulo de 'toxinas visibles' es psicológicamente poderoso en el mercado latino.",
         "cta_hint": "El creativos debe mostrar el parche después de usarse (color oscuro = toxinas). Genera curiosidad inmediata. Bundle de 30 parches funciona mejor."},
    ]

    filtered = [p for p in products if p["niche"] in nichos] if nichos else products
    return filtered


def get_competition_data(target_country):
    return [
        {"rank": 1, "store": "naturavida-co.com", "niche": "Salud", "products": 12, "est_revenue": "$8,200/mes", "top_product": "Colágeno", "weakness": "Sin reviews"},
        {"rank": 2, "store": "bellezapro.co", "niche": "Belleza", "products": 8, "est_revenue": "$5,100/mes", "top_product": "Sérum Vitamina C", "weakness": "Alto precio"},
        {"rank": 3, "store": "hogarsmart.myshopify.com", "niche": "Hogar", "products": 23, "est_revenue": "$3,800/mes", "top_product": "Organizadores", "weakness": "Fotos malas"},
        {"rank": 4, "store": "fitnesscol.com", "niche": "Fitness", "products": 15, "est_revenue": "$2,900/mes", "top_product": "Bandas", "weakness": "Sin video ads"},
        {"rank": 5, "store": "mascotas360.co", "niche": "Mascotas", "products": 7, "est_revenue": "$2,100/mes", "top_product": "Cama mascotas", "weakness": "Poco tráfico"},
    ]


# ─── SESSION STATE ────────────────────────────────────────────────────────────
if "selected_platforms" not in st.session_state:
    st.session_state.selected_platforms = ["facebook"]
if "target_country" not in st.session_state:
    st.session_state.target_country = "🇨🇴 Colombia"
if "search_countries" not in st.session_state:
    st.session_state.search_countries = ["🇺🇸 Global", "🇲🇽 México", "🇪🇸 España"]
if "selected_nichos" not in st.session_state:
    st.session_state.selected_nichos = ["Salud & Bienestar", "Belleza & Cuidado"]
if "selected_keywords" not in st.session_state:
    st.session_state.selected_keywords = ["envío gratis", "50% descuento", "compra ahora"]
if "scanned" not in st.session_state:
    st.session_state.scanned = False


# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:1.2rem 0 1rem; border-bottom:1px solid var(--border); margin-bottom:1rem;">
        <div style="font-family:'Cormorant Garamond',serif; font-size:1.5rem; font-weight:600; color:var(--txt);">OmniSpy AI</div>
        <div style="font-family:'DM Mono',monospace; font-size:0.62rem; color:var(--sage); letter-spacing:2px;">PRODUCT INTELLIGENCE</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-lbl">🎯 País objetivo (donde vendes)</div>', unsafe_allow_html=True)
    target = st.selectbox("", list(COUNTRIES.keys()), index=0, label_visibility="collapsed")
    st.session_state.target_country = target

    st.markdown('<div class="sb-lbl" style="margin-top:1rem">🌍 Buscar ganadores en</div>', unsafe_allow_html=True)
    search_c = st.multiselect("", [c for c in COUNTRIES.keys() if c != target], default=["🇺🇸 Global", "🇲🇽 México", "🇪🇸 España"], label_visibility="collapsed")
    st.session_state.search_countries = search_c

    st.markdown('<div class="sb-lbl" style="margin-top:1rem">📦 Nichos a buscar</div>', unsafe_allow_html=True)
    nichos = st.multiselect("", list(KEYWORDS_BY_NICHE.keys()), default=["Salud & Bienestar", "Belleza & Cuidado"], label_visibility="collapsed")
    st.session_state.selected_nichos = nichos

    st.markdown('<div class="sb-lbl" style="margin-top:1rem">⏱ Filtros</div>', unsafe_allow_html=True)
    min_days  = st.slider("Días mínimos activo", 5, 30, 8)
    min_score = st.slider("Score mínimo ganador", 50, 100, 70)

    st.markdown('<div class="div"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-lbl">🔌 Conexiones</div>', unsafe_allow_html=True)
    for lbl, key in [("Facebook API","FACEBOOK_TOKEN"),("Notion","NOTION_TOKEN"),("Google Drive","GOOGLE_DRIVE_FOLDER_ID"),("OpenAI","OPENAI_API_KEY")]:
        ok  = bool(os.getenv(key))
        st.markdown(f'<div class="api-row"><div class="dot {"dot-on" if ok else "dot-off"}"></div>{lbl} — <span style="color:var(--muted)">{"OK" if ok else "Pendiente"}</span></div>', unsafe_allow_html=True)

    st.markdown('<div class="div"></div>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:0.7rem; color:var(--muted); font-family:DM Mono,monospace;">{datetime.now().strftime("%d %b %Y · %H:%M")}</div>', unsafe_allow_html=True)


# ─── HEADER ──────────────────────────────────────────────────────────────────
target_info = COUNTRIES.get(st.session_state.target_country, {})
st.markdown(f"""
<div class="top-header">
    <div>
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:4px;">
            <h1>OmniSpy AI</h1>
            <span class="tag">v2.0</span>
        </div>
        <div class="sub">Detecta productos ganadores en otros países para vender en {st.session_state.target_country}</div>
        <div style="margin-top:8px; font-size:0.78rem; color:var(--muted); font-family:'DM Mono',monospace;">
            <span class="pulse"></span>Sistema activo · {datetime.now().strftime('%d %B %Y · %H:%M')}
        </div>
    </div>
    <div style="text-align:right;">
        <div style="font-size:2.5rem;">{target_info.get('flag','🌎')}</div>
        <div style="font-size:0.78rem; color:var(--sage-l); font-family:'DM Mono',monospace; margin-top:4px;">MERCADO OBJETIVO</div>
        <div style="font-size:1rem; color:var(--txt); font-weight:600;">{st.session_state.target_country}</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ─── SELECTOR DE PLATAFORMAS ─────────────────────────────────────────────────
st.markdown('<div class="section-t">Plataformas de búsqueda</div>', unsafe_allow_html=True)
st.markdown('<div class="section-s">Selecciona donde buscar anuncios activos</div>', unsafe_allow_html=True)

cols = st.columns(4)
for i, plat in enumerate(PLATFORMS):
    with cols[i]:
        is_active = plat["id"] in st.session_state.selected_platforms
        is_ready  = plat["status"] == "Activo"
        border_color = "#6B9E82" if is_active else "#1E2D40"
        bg_color = "rgba(107,158,130,0.1)" if is_active else "#161C27"
        opacity = "1" if is_ready else "0.5"

        st.markdown(f"""
        <div style="background:{bg_color}; border:2px solid {border_color}; border-radius:12px; padding:16px 12px; text-align:center; opacity:{opacity}; transition:all 0.2s;">
            <div style="font-size:1.8rem;">{plat['icon']}</div>
            <div style="font-size:0.82rem; font-weight:600; color:var(--txt); margin-top:4px;">{plat['name']}</div>
            <div style="font-size:0.68rem; color:{'var(--sage)' if is_ready else 'var(--muted)'}; font-family:'DM Mono',monospace; margin-top:2px;">{'✓ ' if is_active else ''}{plat['status']}</div>
        </div>
        """, unsafe_allow_html=True)

        if is_ready:
            if st.button(f"{'✓ Activo' if is_active else 'Activar'}", key=f"plat_{plat['id']}"):
                if plat["id"] in st.session_state.selected_platforms:
                    st.session_state.selected_platforms.remove(plat["id"])
                else:
                    st.session_state.selected_platforms.append(plat["id"])
                st.rerun()


st.markdown('<div class="div-a"></div>', unsafe_allow_html=True)

# ─── PALABRAS CLAVE ───────────────────────────────────────────────────────────
st.markdown('<div class="section-t">Palabras clave de búsqueda</div>', unsafe_allow_html=True)
st.markdown('<div class="section-s">Selecciona las que usará la IA para detectar anuncios ganadores</div>', unsafe_allow_html=True)

all_kw = KEYWORDS_GENERAL.copy()
for nicho in st.session_state.selected_nichos:
    all_kw.extend(KEYWORDS_BY_NICHE.get(nicho, [])[:4])
all_kw = list(dict.fromkeys(all_kw))

kw_html = ""
for kw in all_kw[:20]:
    active = kw in st.session_state.selected_keywords
    cls = "kw-chip active" if active else "kw-chip"
    kw_html += f'<span class="{cls}">{kw}</span>'

st.markdown(f'<div class="kw-grid">{kw_html}</div>', unsafe_allow_html=True)

custom_kw = st.text_input("➕ Agregar palabra clave personalizada", placeholder="Ej: masajeador facial, suero vitamina C...")
if custom_kw and custom_kw not in st.session_state.selected_keywords:
    if st.button("Agregar"):
        st.session_state.selected_keywords.append(custom_kw)
        st.rerun()


# ─── BOTÓN PRINCIPAL ─────────────────────────────────────────────────────────
st.markdown('<div class="div-a"></div>', unsafe_allow_html=True)
col_scan, col_notion, col_drive, col_space = st.columns([1.2, 1, 1, 4])

with col_scan:
    scan = st.button("🔍 Iniciar escaneo IA")
with col_notion:
    sync_n = st.button("◈ Sync Notion")
with col_drive:
    dl = st.button("↓ Descargar pack")

if scan:
    plats = ", ".join(st.session_state.selected_platforms)
    paises_busq = ", ".join(st.session_state.search_countries[:3])
    with st.spinner(f"Escaneando {plats} en {paises_busq}..."):
        steps = [
            f"Conectando con {plats.upper()} Ads Library...",
            f"Buscando en: {paises_busq}...",
            "Filtrando anuncios activos +8 días...",
            "Detectando tiendas Shopify/WooCommerce...",
            f"Analizando competencia en {st.session_state.target_country}...",
            "Procesando imágenes de productos con IA...",
            "Calculando scores y oportunidades...",
        ]
        bar = st.progress(0)
        for i, step in enumerate(steps):
            time.sleep(0.5)
            bar.progress(int((i+1)/len(steps)*100))
            st.toast(step)
        st.session_state.scanned = True
    st.success(f"✅ Escaneo completado — 5 productos ganadores detectados para vender en {st.session_state.target_country}")


# ─── MÉTRICAS ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="metric-row">
    <div class="met"><div class="met-v g">1,847</div><div class="met-l">Anuncios escaneados</div><div class="met-d">↑ +234 hoy</div></div>
    <div class="met"><div class="met-v">127</div><div class="met-l">Filtrados +8 días</div><div class="met-d">↑ +18 hoy</div></div>
    <div class="met"><div class="met-v g">5</div><div class="met-l">Ganadores detectados</div><div class="met-d">↑ Hoy</div></div>
    <div class="met"><div class="met-v gold">91.8%</div><div class="met-l">Margen promedio</div><div class="met-d">↑ Estable</div></div>
    <div class="met"><div class="met-v">4</div><div class="met-l">Países analizados</div><div class="met-d">MX · ES · US · CL</div></div>
    <div class="met"><div class="met-v g">$47K</div><div class="met-l">Revenue estimado/mes</div><div class="met-d">Top 5 productos</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="div-a"></div>', unsafe_allow_html=True)


# ─── TABS ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    f"  🏆 Productos Ganadores para {target_info.get('flag','')} {st.session_state.target_country.split()[-1]}  ",
    "  📊 Análisis de Competencia  ",
    "  📋 Base de Datos  ",
    "  ⚙️ Configuración  ",
])


# ══ TAB 1: PRODUCTOS GANADORES ════════════════════════════════════════════════
with tab1:
    st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)

    winners = get_demo_winners(
        st.session_state.target_country,
        st.session_state.search_countries,
        st.session_state.selected_nichos
    )
    filtered = [w for w in winners if w["ad_days"] >= min_days and w["score"] >= min_score]

    if not filtered:
        st.markdown('<div class="info-box">No hay productos con los filtros actuales. Ajusta los parámetros en la barra lateral.</div>', unsafe_allow_html=True)
    else:
        st.markdown(
            f'<div class="section-s">{len(filtered)} productos ganadores detectados en otros países — '
            f'Oportunidad para vender en <strong style="color:var(--sage-l)">{st.session_state.target_country}</strong></div>',
            unsafe_allow_html=True
        )

        for p in filtered:
            score_cls = "hi" if p["score"] >= 85 else "mid" if p["score"] >= 70 else "lo"
            trend_sym = "📈 Rising" if p["trend"] == "Rising" else "➡️ Stable"
            niche_color = {"Salud & Bienestar": "b-sage", "Belleza & Cuidado": "b-blue", "Hogar & Organización": "b-gold", "Limpieza & Higiene": "b-red"}.get(p["niche"], "b-sage")
            img_url = PRODUCT_IMAGES.get(p["niche"], "")
            plat_icon = next((pl["icon"] for pl in PLATFORMS if pl["id"] == p["platform"]), "📢")

            # Precio en moneda local
            mult = COUNTRIES.get(st.session_state.target_country, {}).get("multiplier", 1)
            curr = COUNTRIES.get(st.session_state.target_country, {}).get("currency", "USD")
            price_local = int(p["price_usd"] * mult)
            cost_local  = int(p["cost_usd"] * mult)

            with st.expander(f"{plat_icon} [{p['id']}]  {p['name']}  —  {p['niche']}  ·  Detectado en {p['origin_country']}  ·  Score {p['score']}/100  ·  {p['ad_days']} días activo"):

                c_img, c_info, c_data, c_score = st.columns([1.2, 2.5, 1.5, 1.2])

                with c_img:
                    if img_url:
                        st.image(img_url, width=170, caption=p["niche"])
                    else:
                        st.markdown('<div style="width:160px;height:160px;background:var(--hover);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:2.5rem;">📦</div>', unsafe_allow_html=True)

                    st.markdown(f"""
                    <div style="margin-top:8px;">
                        <div style="font-family:'DM Mono',monospace; font-size:0.7rem; color:var(--muted);">AD ID</div>
                        <div style="font-family:'DM Mono',monospace; font-size:0.82rem; color:var(--gold); font-weight:500;">{p['ad_id']}</div>
                    </div>
                    <div style="margin-top:6px;">
                        <div style="font-size:0.7rem; color:var(--muted);">Detectado en</div>
                        <div style="font-size:0.85rem; color:var(--txt);">{p['origin_country']}</div>
                    </div>
                    """, unsafe_allow_html=True)

                with c_info:
                    st.markdown(f"""
                    <div style="font-family:'Cormorant Garamond',serif; font-size:1.3rem; font-weight:600; color:var(--txt); margin-bottom:6px;">{p['name']}</div>
                    <div style="display:flex; gap:5px; flex-wrap:wrap; margin-bottom:12px;">
                        <span class="badge {niche_color}">{p['niche']}</span>
                        <span class="badge b-blue">{plat_icon} {p['platform'].title()}</span>
                        <span class="badge b-sage">Shopify ✓</span>
                        {''.join(f'<span class="badge b-gold">{kw}</span>' for kw in p['keywords'])}
                    </div>
                    <div style="font-size:0.85rem; color:var(--sage-l); font-weight:600; margin-bottom:4px;">¿Por qué es ganador?</div>
                    <div style="font-size:0.83rem; color:var(--txt2); line-height:1.6; margin-bottom:14px;">{p['why_winner']}</div>
                    """, unsafe_allow_html=True)

                    # CTA box
                    st.markdown(f"""
                    <div class="cta-box">
                        <div class="cta-title">🎯 Cómo aprovechar este producto</div>
                        <div class="cta-hint">{p['cta_hint']}</div>
                        <div style="margin-top:10px; font-size:0.72rem; color:var(--muted);">Ver tienda ganadora →</div>
                        <div class="cta-url">{p['store_url']}</div>
                    </div>
                    """, unsafe_allow_html=True)

                with c_data:
                    st.markdown(f"""
                    <div style="background:var(--bg); border:1px solid var(--border); border-radius:10px; padding:14px; margin-top:4px;">
                        <div class="data-item"><span class="dk">Precio sugerido ({curr})</span><span class="dv g">{price_local:,}</span></div>
                        <div class="data-item"><span class="dk">Costo producto</span><span class="dv">{cost_local:,} {curr}</span></div>
                        <div class="data-item"><span class="dk">Margen neto</span><span class="dv gold">{p['margin']}%</span></div>
                        <div class="data-item"><span class="dk">Revenue/mes estimado</span><span class="dv g">${p['monthly_revenue']:,}</span></div>
                        <div class="data-item"><span class="dk">Competencia local</span><span class="dv">{p['competition']}</span></div>
                        <div class="data-item"><span class="dk">Percepción valor</span><span class="dv">{p['value_perception']}</span></div>
                        <div class="data-item"><span class="dk">Días activo</span><span class="dv g">{p['ad_days']} días</span></div>
                        <div class="data-item"><span class="dk">Tendencia</span><span class="dv">{trend_sym}</span></div>
                    </div>
                    """, unsafe_allow_html=True)

                with c_score:
                    st.markdown(f"""
                    <div style="background:var(--bg); border:1px solid var(--border); border-radius:10px; padding:16px; text-align:center; margin-top:4px;">
                        <div class="score-big {score_cls}">{p['score']}</div>
                        <div class="score-lbl">Score ganador</div>
                        <div class="div" style="margin:12px 0 10px;"></div>
                        <div style="font-size:0.72rem; color:var(--muted); text-transform:uppercase; letter-spacing:1px; margin-bottom:3px;">Plataforma</div>
                        <div style="font-size:1.4rem;">{plat_icon}</div>
                        <div class="div" style="margin:10px 0;"></div>
                        <div style="font-size:0.72rem; color:var(--muted); text-transform:uppercase; letter-spacing:1px; margin-bottom:3px;">Origen</div>
                        <div style="font-size:1.1rem;">{p['origin_country'].split()[0]}</div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
                b1, b2, b3, b4 = st.columns(4)
                with b1:
                    st.button("📷 Ver tienda Shopify",  key=f"shop_{p['id']}")
                with b2:
                    st.button("📥 Descargar creativos", key=f"dl_{p['id']}")
                with b3:
                    st.button("◈ Guardar en Notion",    key=f"no_{p['id']}")
                with b4:
                    st.button(f"📢 Ver anuncio {plat_icon}", key=f"ad_{p['id']}")


# ══ TAB 2: COMPETENCIA ════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-t">Competencia en {st.session_state.target_country}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-s">Tiendas activas analizadas en tu mercado objetivo</div>', unsafe_allow_html=True)

    comp = get_competition_data(st.session_state.target_country)

    st.markdown("""
    <div style="background:var(--card); border:1px solid var(--border); border-radius:10px; overflow:hidden;">
        <div class="comp-row comp-header">
            <div>#</div><div>Tienda</div><div>Nicho</div><div>Productos</div><div>Revenue est.</div><div>Debilidad</div>
        </div>
    """, unsafe_allow_html=True)

    for c in comp:
        st.markdown(f"""
        <div class="comp-row">
            <div class="comp-rank">#{c['rank']}</div>
            <div>
                <div style="font-size:0.83rem; color:var(--txt); font-weight:500;">{c['store']}</div>
                <div style="font-size:0.72rem; color:var(--muted);">Top: {c['top_product']}</div>
            </div>
            <div><span class="badge b-sage">{c['niche']}</span></div>
            <div style="font-family:'DM Mono',monospace; font-size:0.8rem; color:var(--txt2);">{c['products']}</div>
            <div style="font-family:'DM Mono',monospace; font-size:0.8rem; color:var(--gold);">{c['est_revenue']}</div>
            <div style="font-size:0.78rem; color:var(--red);">⚠ {c['weakness']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="div-a"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-t">Tendencias de nicho</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        df1 = pd.DataFrame({"Nicho": ["Salud","Belleza","Hogar","Limpieza","Fitness"], "Score": [94,88,76,71,82], "Competencia": ["Baja","Media","Baja","Baja","Media"]})
        st.dataframe(df1, use_container_width=True, hide_index=True)
        st.bar_chart(df1.set_index("Nicho")["Score"])
    with c2:
        st.markdown("""
        <div class="info-box" style="border-left-color:var(--gold);">
            <strong style="color:var(--gold)">💡 Oportunidades detectadas en tu mercado</strong><br><br>
            🟢 <strong>Salud & Bienestar:</strong> Competencia baja, alta demanda post-pandemia. Score 94.<br><br>
            🟢 <strong>Hogar & Organización:</strong> Mercado sin saturar. Score 76 con tendencia al alza.<br><br>
            🟡 <strong>Belleza:</strong> Competencia media pero margen muy alto (91%). Vale la pena.<br><br>
            🔴 <strong>Tecnología:</strong> Saturado con competidores de precio bajo. Evitar por ahora.
        </div>
        """, unsafe_allow_html=True)


# ══ TAB 3: BASE DE DATOS ═════════════════════════════════════════════════════
with tab3:
    st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-t">Registro completo de productos</div>', unsafe_allow_html=True)

    winners_all = get_demo_winners(st.session_state.target_country, [], [])
    df = pd.DataFrame([{
        "ID Anuncio": p["id"],
        "Producto": p["name"],
        "Nicho": p["niche"],
        "Plataforma": p["platform"].title(),
        "Detectado en": p["origin_country"],
        "Precio USD": f"${p['price_usd']}",
        "Margen": f"{p['margin']}%",
        "Días Activo": p["ad_days"],
        "Revenue/mes": f"${p['monthly_revenue']:,}",
        "Competencia": p["competition"],
        "Score": p["score"],
    } for p in winners_all])

    c1, c2 = st.columns([3, 1])
    with c1:
        search = st.text_input("🔍 Buscar", placeholder="Colágeno, jade, organizador...")
    with c2:
        st.markdown('<div style="height:1.5rem"></div>', unsafe_allow_html=True)
        export_btn = st.button("↓ Exportar CSV")

    if search:
        df = df[df["Producto"].str.contains(search, case=False)]

    st.dataframe(df, use_container_width=True, hide_index=True)

    if export_btn:
        st.download_button("Descargar CSV", df.to_csv(index=False), "omnispy_ganadores.csv", "text/csv")


# ══ TAB 4: CONFIGURACIÓN ═════════════════════════════════════════════════════
with tab4:
    st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-t">Configuración de APIs</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-box">Guarda las credenciales en el archivo <code>.env</code> o en Streamlit Secrets. Nunca las subas a GitHub.</div>', unsafe_allow_html=True)

    with st.form("config_form"):
        st.markdown("**📘 Facebook Ads Library**")
        fb = st.text_input("FACEBOOK_TOKEN", type="password", placeholder="EAA...")

        st.markdown("**◈ Notion**")
        n1, n2 = st.columns(2)
        with n1: nt = st.text_input("NOTION_TOKEN", type="password", placeholder="ntn_...")
        with n2: nd = st.text_input("NOTION_DATABASE_ID", placeholder="xxxxxxxx-xxxx-...")

        st.markdown("**☁️ Google Drive**")
        g1, g2 = st.columns(2)
        with g1: gf = st.text_input("GOOGLE_DRIVE_FOLDER_ID", placeholder="1BxiMVs0...")
        with g2: gj = st.text_input("GOOGLE_CREDENTIALS_JSON", placeholder="credentials.json")

        st.markdown("**🤖 OpenAI GPT-4o**")
        oa = st.text_input("OPENAI_API_KEY", type="password", placeholder="sk-proj-...")

        if st.form_submit_button("💾 Guardar configuración"):
            st.success("Configuración guardada. Reinicia la app para aplicar cambios.")

    st.markdown('<div class="div"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-t">Streamlit Secrets (recomendado)</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-s">Pega esto en Settings → Secrets de tu app en Streamlit Cloud</div>', unsafe_allow_html=True)
    st.code("""FACEBOOK_TOKEN = "tu_token_aqui"
NOTION_TOKEN = "ntn_..."
NOTION_DATABASE_ID = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
OPENAI_API_KEY = "sk-proj-..."
GOOGLE_DRIVE_FOLDER_ID = "1m3A7O5RHW7V82MsqLVGxcC4G-3UzLDtN"

[gcp_service_account]
type = "service_account"
project_id = "omnispy-ai"
private_key_id = "tu_key_id"
private_key = "-----BEGIN PRIVATE KEY-----\\ntu_llave_privada\\n-----END PRIVATE KEY-----\\n"
client_email = "omnispy-bot@omnispy-ai.iam.gserviceaccount.com"
client_id = "111550579817412025832"
""", language="toml")
