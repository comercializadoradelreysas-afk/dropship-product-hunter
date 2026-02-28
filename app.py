import streamlit as st
import pandas as pd
import time
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="OmniSpy AI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── PALETA: Slate Profundo + Verde Salvia + Oro Suave ────────────────────────
# Genera confianza, calma la mente y facilita decisiones claras
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500;600;700&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

:root {
    --bg-primary:    #0E1117;
    --bg-card:       #161C27;
    --bg-hover:      #1C2436;
    --border:        #1E2D40;
    --border-light:  #243347;

    --sage:          #6B9E82;
    --sage-light:    #89B89C;
    --sage-glow:     rgba(107, 158, 130, 0.15);
    --sage-border:   rgba(107, 158, 130, 0.35);

    --gold:          #C8A96E;
    --gold-light:    #D4BA86;
    --gold-glow:     rgba(200, 169, 110, 0.12);

    --text-primary:  #E8E4DC;
    --text-secondary:#9AA3B2;
    --text-muted:    #5C6878;

    --red-soft:      #C47B7B;
    --blue-soft:     #6B91C8;
}

* { font-family: 'DM Sans', sans-serif; }
h1, h2, h3 { font-family: 'Cormorant Garamond', serif; }

.stApp { background-color: var(--bg-primary); color: var(--text-primary); }
.main .block-container { padding: 2rem 2.5rem 4rem 2.5rem; max-width: 1400px; }
[data-testid="stSidebar"] { background: #0A0F18; border-right: 1px solid var(--border); }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

.omnispy-header { padding: 3rem 0 2rem 0; border-bottom: 1px solid var(--border); margin-bottom: 2.5rem; }
.omnispy-header h1 { font-size: 2.8rem; font-weight: 600; color: var(--text-primary); letter-spacing: -0.5px; margin: 0; line-height: 1; }
.omnispy-header .tag { font-family: 'DM Mono', monospace; font-size: 0.7rem; letter-spacing: 3px; text-transform: uppercase; color: var(--sage); background: var(--sage-glow); border: 1px solid var(--sage-border); padding: 3px 10px; border-radius: 4px; }
.omnispy-header .subtitle { font-size: 0.9rem; color: var(--text-muted); margin-top: 8px; font-weight: 300; }
.status-line { display: flex; align-items: center; gap: 8px; margin-top: 14px; font-size: 0.78rem; color: var(--text-muted); font-family: 'DM Mono', monospace; }
.pulse { width: 7px; height: 7px; border-radius: 50%; background: var(--sage); display: inline-block; animation: pulse 2.5s ease-in-out infinite; flex-shrink: 0; }
@keyframes pulse { 0%, 100% { opacity: 1; box-shadow: 0 0 0 0 rgba(107,158,130,0.4); } 50% { opacity: 0.6; box-shadow: 0 0 0 5px rgba(107,158,130,0); } }

.metric-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; margin-bottom: 2rem; }
.metric-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 10px; padding: 20px 18px; transition: all 0.25s ease; position: relative; overflow: hidden; }
.metric-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, var(--sage), transparent); opacity: 0; transition: opacity 0.25s; }
.metric-card:hover { border-color: var(--border-light); background: var(--bg-hover); transform: translateY(-2px); box-shadow: 0 8px 32px rgba(0,0,0,0.3); }
.metric-card:hover::before { opacity: 1; }
.metric-value { font-family: 'Cormorant Garamond', serif; font-size: 2.4rem; font-weight: 600; color: var(--text-primary); line-height: 1; margin-bottom: 6px; }
.metric-value.accent { color: var(--sage-light); }
.metric-value.gold { color: var(--gold); }
.metric-label { font-size: 0.72rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1.5px; font-weight: 500; }
.metric-delta { font-size: 0.75rem; color: var(--sage); margin-top: 4px; font-family: 'DM Mono', monospace; }

.divider { height: 1px; background: var(--border); margin: 1.5rem 0; }
.divider-accent { height: 1px; background: linear-gradient(90deg, var(--sage-border), transparent); margin: 1.5rem 0; }

.badge { display: inline-flex; align-items: center; gap: 4px; padding: 3px 10px; border-radius: 5px; font-size: 0.72rem; font-weight: 500; font-family: 'DM Mono', monospace; letter-spacing: 0.5px; }
.badge-sage { background: var(--sage-glow); color: var(--sage-light); border: 1px solid var(--sage-border); }
.badge-gold { background: var(--gold-glow); color: var(--gold); border: 1px solid rgba(200,169,110,0.3); }
.badge-red  { background: rgba(196,123,123,0.1); color: var(--red-soft); border: 1px solid rgba(196,123,123,0.25); }
.badge-blue { background: rgba(107,145,200,0.1); color: var(--blue-soft); border: 1px solid rgba(107,145,200,0.25); }

.score-number { font-family: 'Cormorant Garamond', serif; font-size: 2.6rem; font-weight: 700; line-height: 1; }
.score-high { color: var(--sage-light); }
.score-mid  { color: var(--gold); }
.score-low  { color: var(--red-soft); }
.score-label { font-size: 0.68rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 2px; margin-top: 3px; }

.data-row { display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid var(--border); }
.data-row:last-child { border-bottom: none; }
.data-key { font-size: 0.8rem; color: var(--text-muted); }
.data-val { font-size: 0.85rem; color: var(--text-primary); font-family: 'DM Mono', monospace; }
.data-val.green { color: var(--sage-light); }
.data-val.gold  { color: var(--gold); }

.sidebar-label { font-family: 'DM Mono', monospace; font-size: 0.65rem; letter-spacing: 2.5px; text-transform: uppercase; color: var(--text-muted); margin-bottom: 10px; padding-bottom: 6px; border-bottom: 1px solid var(--border); }
.api-status { display: flex; align-items: center; gap: 8px; padding: 6px 0; font-size: 0.8rem; color: var(--text-secondary); }
.api-dot { width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; }
.api-dot.on  { background: var(--sage); }
.api-dot.off { background: var(--red-soft); }

.stTabs [data-baseweb="tab-list"] { background: transparent; border-bottom: 1px solid var(--border); gap: 0; padding: 0; }
.stTabs [data-baseweb="tab"] { color: var(--text-muted); font-size: 0.82rem; font-weight: 500; padding: 10px 20px; border-radius: 0; border-bottom: 2px solid transparent; transition: all 0.2s; }
.stTabs [aria-selected="true"] { color: var(--sage-light) !important; border-bottom: 2px solid var(--sage) !important; background: transparent !important; }

.stButton > button { background: transparent !important; color: var(--sage-light) !important; border: 1px solid var(--sage-border) !important; border-radius: 7px !important; font-size: 0.82rem !important; font-weight: 500 !important; padding: 9px 20px !important; transition: all 0.2s !important; }
.stButton > button:hover { background: var(--sage-glow) !important; border-color: var(--sage) !important; box-shadow: 0 0 20px rgba(107,158,130,0.15) !important; }

.trend-up   { color: var(--sage-light); font-family: 'DM Mono', monospace; font-size: 0.8rem; }
.trend-flat { color: var(--gold); font-family: 'DM Mono', monospace; font-size: 0.8rem; }
.trend-down { color: var(--red-soft); font-family: 'DM Mono', monospace; font-size: 0.8rem; }

.info-banner { background: var(--bg-card); border: 1px solid var(--border); border-left: 3px solid var(--sage); border-radius: 0 8px 8px 0; padding: 14px 18px; font-size: 0.84rem; color: var(--text-secondary); margin: 1rem 0; }
.section-title { font-family: 'Cormorant Garamond', serif; font-size: 1.5rem; font-weight: 600; color: var(--text-primary); margin-bottom: 4px; }
.section-sub { font-size: 0.8rem; color: var(--text-muted); margin-bottom: 1.5rem; }
</style>
""", unsafe_allow_html=True)


# ─── DEMO DATA ────────────────────────────────────────────────────────────────
def get_demo_products():
    return [
        {"id": "FB-SAL-001", "name": "Colágeno Marino Hidrolizado", "niche": "Salud", "country": "Colombia", "language": "ES", "platform": "Shopify", "store_url": "vitalife.myshopify.com", "price_sell": 59.99, "price_cost": 5.20, "margin": 91.3, "ad_days": 34, "score": 96, "trend": "Rising", "value_perception": "Muy Alta", "ad_spend": "Alto", "keywords": ["envío gratis", "compra ahora"], "description": "Suplemento antiedad de alta recompra. Audiencia mujeres 35-55. Margen brutal."},
        {"id": "FB-BEL-002", "name": "Rodillo Jade Facial", "niche": "Belleza", "country": "Chile", "language": "ES", "platform": "Shopify", "store_url": "glowco.myshopify.com", "price_sell": 44.99, "price_cost": 3.80, "margin": 91.6, "ad_days": 21, "score": 91, "trend": "Rising", "value_perception": "Alta", "ad_spend": "Alto", "keywords": ["obtenga el suyo", "envío gratis"], "description": "Percepción de lujo extrema. Costo real muy bajo. Mercado bienestar en expansión."},
        {"id": "FB-HOG-003", "name": "Organizador Magnético de Cables", "niche": "Hogar", "country": "México", "language": "EN", "platform": "Shopify", "store_url": "ordenpro.myshopify.com", "price_sell": 29.99, "price_cost": 2.60, "margin": 91.3, "ad_days": 18, "score": 84, "trend": "Rising", "value_perception": "Media-Alta", "ad_spend": "Medio", "keywords": ["free shipping", "buy now"], "description": "Solución para escritorios. Mercado tech y trabajo remoto en crecimiento sostenido."},
        {"id": "FB-LIM-004", "name": "Cepillo Eléctrico Multiusos", "niche": "Limpieza", "country": "España", "language": "IT", "platform": "Shopify", "store_url": "cleanpro.myshopify.com", "price_sell": 39.99, "price_cost": 5.10, "margin": 87.2, "ad_days": 15, "score": 79, "trend": "Stable", "value_perception": "Alta", "ad_spend": "Medio", "keywords": ["50% sconto", "spedizione gratis"], "description": "Limpieza de baños y azulejos sin esfuerzo. Viralidad comprobada en mercado italiano."},
        {"id": "FB-SAL-005", "name": "Parches Detox Pie", "niche": "Salud", "country": "Colombia", "language": "ID", "platform": "Shopify", "store_url": "detoxlife.myshopify.com", "price_sell": 24.99, "price_cost": 1.80, "margin": 92.8, "ad_days": 28, "score": 88, "trend": "Rising", "value_perception": "Alta", "ad_spend": "Alto", "keywords": ["gratis ongkir", "beli sekarang"], "description": "Ticket bajo pero margen brutal. Mercado Indonesia en fase de explosión de demanda."},
    ]


# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:1.5rem 0 1rem 0; border-bottom:1px solid var(--border); margin-bottom:1.2rem;">
        <div style="font-family:'Cormorant Garamond',serif; font-size:1.5rem; font-weight:600; color:var(--text-primary);">OmniSpy</div>
        <div style="font-family:'DM Mono',monospace; font-size:0.65rem; color:var(--sage); letter-spacing:2px; text-transform:uppercase; margin-top:2px;">Product Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-label">Parámetros de búsqueda</div>', unsafe_allow_html=True)
    nichos  = st.multiselect("Nichos", ["Salud", "Hogar", "Belleza", "Limpieza"], default=["Salud", "Belleza"])
    paises  = st.multiselect("Países objetivo", ["Colombia", "Chile", "México", "España", "Argentina"], default=["Colombia", "Chile"])
    idiomas = st.multiselect("Idiomas", ["ES", "EN", "IT", "NO", "ID", "SL"], default=["ES", "EN"])
    min_days  = st.slider("Días mínimos activo", 5, 30, 8)
    min_score = st.slider("Score mínimo", 50, 100, 70)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-label">Estado de conexiones</div>', unsafe_allow_html=True)

    for label, env_key in [("Facebook Ads API", "FACEBOOK_TOKEN"), ("Notion Database", "NOTION_TOKEN"), ("Google Drive", "GOOGLE_DRIVE_FOLDER_ID"), ("OpenAI GPT-4o", "OPENAI_API_KEY")]:
        ok  = bool(os.getenv(env_key))
        dot = "on" if ok else "off"
        txt = "Conectado" if ok else "Sin configurar"
        st.markdown(f'<div class="api-status"><div class="api-dot {dot}"></div>{label} — <span style="color:var(--text-muted)">{txt}</span></div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:0.72rem; color:var(--text-muted); font-family:DM Mono,monospace; line-height:1.6;">Actualizado<br>{datetime.now().strftime("%d %b %Y, %H:%M")}</div>', unsafe_allow_html=True)


# ─── HEADER ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="omnispy-header">
    <div style="display:flex; align-items:center; gap:14px; margin-bottom:6px;">
        <h1>OmniSpy AI</h1>
        <span class="tag">v1.0 · BETA</span>
    </div>
    <div class="subtitle">Motor de inteligencia para detectar productos ganadores en Facebook Ads Library</div>
    <div class="status-line">
        <span class="pulse"></span>
        Sistema activo &nbsp;·&nbsp; {datetime.now().strftime('%d de %B, %Y')} &nbsp;·&nbsp; Última actualización {datetime.now().strftime('%H:%M')}
    </div>
</div>
""", unsafe_allow_html=True)


# ─── MÉTRICAS ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="metric-grid">
    <div class="metric-card"><div class="metric-value accent">1,247</div><div class="metric-label">Anuncios escaneados</div><div class="metric-delta">↑ +182 hoy</div></div>
    <div class="metric-card"><div class="metric-value">94</div><div class="metric-label">Filtrados (+8 días)</div><div class="metric-delta">↑ +12 hoy</div></div>
    <div class="metric-card"><div class="metric-value accent">23</div><div class="metric-label">Ganadores detectados</div><div class="metric-delta">↑ +5 nuevos</div></div>
    <div class="metric-card"><div class="metric-value gold">91.2%</div><div class="metric-label">Margen promedio</div><div class="metric-delta">↑ Estable</div></div>
    <div class="metric-card"><div class="metric-value">6</div><div class="metric-label">Países activos</div><div class="metric-delta">ES · EN · IT · NO · ID · SL</div></div>
</div>
""", unsafe_allow_html=True)


# ─── ACCIONES ─────────────────────────────────────────────────────────────────
c1, c2, c3, _ = st.columns([1, 1, 1, 4])
with c1: iniciar  = st.button("▶  Iniciar escaneo")
with c2: sync_n   = st.button("◈  Sync Notion")
with c3: dl_pack  = st.button("↓  Pack de anuncios")

if iniciar:
    with st.spinner("Escaneando Facebook Ads Library..."):
        pasos = ["Conectando con FB Ads Library...", "Aplicando filtro +8 días activos...", "Detectando tiendas Shopify...", "Analizando percepción de valor...", "Cruzando con Glimpse & Reddit Trends...", "Calculando scores ganadores..."]
        bar = st.progress(0)
        for i, paso in enumerate(pasos):
            time.sleep(0.5); bar.progress(int((i+1)/len(pasos)*100)); st.toast(paso)
    st.success("Escaneo completado — 5 nuevos productos ganadores encontrados")

if sync_n:
    st.warning("Configura NOTION_TOKEN en el archivo .env") if not os.getenv("NOTION_TOKEN") else st.success("Notion actualizado correctamente")

if dl_pack:
    st.warning("Configura GOOGLE_DRIVE_FOLDER_ID en el archivo .env") if not os.getenv("GOOGLE_DRIVE_FOLDER_ID") else st.success("Descargando creativos a Google Drive...")

st.markdown('<div class="divider-accent"></div>', unsafe_allow_html=True)


# ─── TABS ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["  Productos ganadores  ", "  Tendencias  ", "  Base de datos  ", "  Configuración  "])

products = get_demo_products()
filtered = [p for p in products if (not nichos or p["niche"] in nichos) and (not paises or p["country"] in paises) and p["ad_days"] >= min_days and p["score"] >= min_score]


# ══ TAB 1 ════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div style="height:1.2rem"></div>', unsafe_allow_html=True)
    if not filtered:
        st.markdown('<div class="info-banner">No hay productos con los filtros actuales. Ajusta los parámetros en la barra lateral.</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="section-sub">{len(filtered)} productos encontrados con los filtros actuales</div>', unsafe_allow_html=True)
        for p in filtered:
            score_cls = "score-high" if p["score"] >= 85 else "score-mid" if p["score"] >= 70 else "score-low"
            trend_sym = "↑ Rising" if p["trend"] == "Rising" else "→ Stable" if p["trend"] == "Stable" else "↓ Falling"
            trend_cls = "trend-up" if p["trend"] == "Rising" else "trend-flat" if p["trend"] == "Stable" else "trend-down"
            badge_map = {"Salud": "badge-sage", "Belleza": "badge-blue", "Hogar": "badge-gold", "Limpieza": "badge-red"}
            badge_n   = badge_map.get(p["niche"], "badge-sage")

            with st.expander(f"{p['name']}  —  {p['niche']}  ·  {p['country']}  ·  Score {p['score']}/100"):
                col1, col2, col3 = st.columns([3, 1.4, 1.2])

                with col1:
                    kw_badges = "".join(f'<span class="badge badge-gold">{kw}</span>' for kw in p["keywords"])
                    shopify_b = '<span class="badge badge-sage">Shopify ✓</span>' if p["platform"] == "Shopify" else ""
                    st.markdown(f"""
                    <div style="font-family:'Cormorant Garamond',serif; font-size:1.35rem; font-weight:600; color:var(--text-primary); margin-bottom:4px;">{p['name']}</div>
                    <div style="font-size:0.78rem; color:var(--text-muted); font-family:'DM Mono',monospace; margin-bottom:14px;">{p['id']} · {p['platform']} · {p['country']}</div>
                    <div style="display:flex; gap:6px; flex-wrap:wrap; margin-bottom:14px;">
                        <span class="badge {badge_n}">{p['niche']}</span>
                        <span class="badge badge-blue">{p['language']}</span>
                        {shopify_b}{kw_badges}
                    </div>
                    <div style="font-size:0.85rem; color:var(--text-secondary); line-height:1.6; margin-bottom:12px;">{p['description']}</div>
                    <div style="font-family:'DM Mono',monospace; font-size:0.75rem; color:var(--text-muted);">🔗 {p['store_url']}</div>
                    """, unsafe_allow_html=True)

                with col2:
                    st.markdown(f"""
                    <div style="background:var(--bg-primary); border:1px solid var(--border); border-radius:8px; padding:16px;">
                        <div class="data-row"><span class="data-key">Precio venta</span><span class="data-val green">${p['price_sell']}</span></div>
                        <div class="data-row"><span class="data-key">Costo producto</span><span class="data-val">${p['price_cost']}</span></div>
                        <div class="data-row"><span class="data-key">Margen</span><span class="data-val gold">{p['margin']}%</span></div>
                        <div class="data-row"><span class="data-key">Percepción</span><span class="data-val">{p['value_perception']}</span></div>
                        <div class="data-row"><span class="data-key">Ad Spend</span><span class="data-val">{p['ad_spend']}</span></div>
                    </div>
                    """, unsafe_allow_html=True)

                with col3:
                    st.markdown(f"""
                    <div style="background:var(--bg-primary); border:1px solid var(--border); border-radius:8px; padding:16px; text-align:center;">
                        <div class="score-number {score_cls}">{p['score']}</div>
                        <div class="score-label">Score ganador</div>
                        <div class="divider" style="margin:14px 0 10px 0;"></div>
                        <div style="font-family:'DM Mono',monospace; font-size:1.4rem; font-weight:600; color:var(--text-primary);">{p['ad_days']}</div>
                        <div class="score-label">días activo</div>
                        <div class="divider" style="margin:10px 0;"></div>
                        <div class="{trend_cls}">{trend_sym}</div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)
                b1, b2, b3 = st.columns(3)
                with b1: st.button("↓ Descargar videos", key=f"dl_{p['id']}")
                with b2: st.button("◈ Guardar Notion",   key=f"no_{p['id']}")
                with b3: st.button("↗ Ver anuncio FB",   key=f"fb_{p['id']}")


# ══ TAB 2 ════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Tendencias por nicho y país</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Datos cruzados con Glimpse, Reddit y Alibaba Trends</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        df1 = pd.DataFrame({"Nicho": ["Salud","Belleza","Hogar","Limpieza"], "Score": [94,88,76,71], "Anuncios": [340,280,190,145], "Ganadores": [12,8,5,3]})
        st.dataframe(df1, use_container_width=True, hide_index=True)
        st.bar_chart(df1.set_index("Nicho")["Score"])
    with c2:
        df2 = pd.DataFrame({"País": ["Colombia","México","Chile","España","Argentina"], "Anuncios": [420,380,290,260,180], "Ganadores": [23,19,15,12,8]})
        st.dataframe(df2, use_container_width=True, hide_index=True)
        st.bar_chart(df2.set_index("País")["Ganadores"])

    st.markdown('<div class="divider-accent"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Actividad — Últimos 7 días</div>', unsafe_allow_html=True)
    chart = pd.DataFrame({"Escaneados": [180,220,195,310,280,340,290], "Ganadores": [8,11,9,18,15,23,16]}, index=pd.date_range(end=datetime.now(), periods=7, freq="D").strftime("%d/%m"))
    st.line_chart(chart)


# ══ TAB 3 ════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Registro de productos</div>', unsafe_allow_html=True)
    df = pd.DataFrame([{"ID": p["id"], "Producto": p["name"], "Nicho": p["niche"], "País": p["country"], "Plataforma": p["platform"], "Precio": f"${p['price_sell']}", "Margen": f"{p['margin']}%", "Días": p["ad_days"], "Tendencia": p["trend"], "Score": p["score"]} for p in products])

    c1, c2 = st.columns([3, 1])
    with c1: search = st.text_input("Buscar", placeholder="Colágeno, jade, cables...")
    with c2:
        st.markdown('<div style="height:1.6rem"></div>', unsafe_allow_html=True)
        export = st.button("↓ Exportar CSV")

    if search: df = df[df["Producto"].str.contains(search, case=False)]
    st.dataframe(df, use_container_width=True, hide_index=True)
    if export:
        st.download_button("Descargar CSV", df.to_csv(index=False), "omnispy_productos.csv", "text/csv")


# ══ TAB 4 ════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Configuración de APIs</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-banner">Las credenciales se guardan en el archivo <code>.env</code> en la raíz del proyecto. Nunca las subas a GitHub.</div>', unsafe_allow_html=True)

    with st.form("config"):
        st.markdown("**Facebook Ads Library**")
        fb_token = st.text_input("FACEBOOK_TOKEN", type="password", placeholder="EAA...")
        st.markdown("**Notion**")
        co1, co2 = st.columns(2)
        with co1: n_token = st.text_input("NOTION_TOKEN", type="password", placeholder="ntn_...")
        with co2: n_db    = st.text_input("NOTION_DATABASE_ID", placeholder="xxxxxxxx-xxxx-...")
        st.markdown("**Google Drive**")
        co3, co4 = st.columns(2)
        with co3: gd_folder = st.text_input("GOOGLE_DRIVE_FOLDER_ID", placeholder="1BxiMVs0...")
        with co4: gd_json   = st.text_input("GOOGLE_CREDENTIALS_JSON", placeholder="credentials.json")
        st.markdown("**OpenAI**")
        oa_key = st.text_input("OPENAI_API_KEY", type="password", placeholder="sk-proj-...")

        if st.form_submit_button("Guardar configuración"):
            st.success("Configuración guardada. Reinicia la app para aplicar los cambios.")
            st.code(f"FACEBOOK_TOKEN={fb_token or 'tu_token'}\nNOTION_TOKEN={n_token or 'tu_token'}\nNOTION_DATABASE_ID={n_db or 'tu_id'}\nGOOGLE_DRIVE_FOLDER_ID={gd_folder or 'tu_folder'}\nGOOGLE_CREDENTIALS_JSON={gd_json or 'credentials.json'}\nOPENAI_API_KEY={oa_key or 'tu_key'}", language="bash")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Guía rápida</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.85rem; color:var(--text-secondary); line-height:2.2;">
    1. &nbsp;<strong style="color:var(--text-primary)">Notion</strong> → notion.so/my-integrations → Crear integración → Copiar token<br>
    2. &nbsp;<strong style="color:var(--text-primary)">Google Drive</strong> → console.cloud.google.com → API Drive → Cuenta servicio → JSON<br>
    3. &nbsp;<strong style="color:var(--text-primary)">OpenAI</strong> → platform.openai.com/api-keys → Crear clave nueva<br>
    4. &nbsp;<strong style="color:var(--text-primary)">Facebook</strong> → developers.facebook.com → Token de acceso<br>
    5. &nbsp;Crear archivo <code>.env</code> en la raíz con todas las variables<br>
    6. &nbsp;Ejecutar con <code>streamlit run app.py</code>
    </div>
    """, unsafe_allow_html=True)
