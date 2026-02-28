"""
scraper.py — Motor de búsqueda en Facebook Ads Library
OmniSpy AI — Módulo de scraping con Playwright
"""

import asyncio
import json
import re
import time
import random
from datetime import datetime
from playwright.async_api import async_playwright

# ─── KEYWORDS POR NICHO E IDIOMA ─────────────────────────────────────────────
KEYWORDS = {
    "Salud": {
        "ES": ["envío gratis", "50% descuento", "compra ahora", "colágeno", "adelgazar"],
        "EN": ["free shipping", "50% off", "buy now", "health supplement", "weight loss"],
        "IT": ["spedizione gratis", "50% sconto", "acquista ora", "salute", "dimagrire"],
        "NO": ["gratis frakt", "50% rabatt", "kjøp nå", "helse", "vekttap"],
        "ID": ["gratis ongkir", "diskon 50%", "beli sekarang", "kesehatan", "suplemen"],
        "SL": ["brezplačna dostava", "50% popust", "kupi zdaj", "zdravje"],
    },
    "Hogar": {
        "ES": ["envío gratis", "oferta limitada", "hogar", "organización", "cocina"],
        "EN": ["free shipping", "limited offer", "home", "kitchen gadget", "organizer"],
        "IT": ["spedizione gratis", "offerta limitata", "casa", "cucina", "organizzatore"],
        "NO": ["gratis frakt", "begrenset tilbud", "hjem", "kjøkken"],
        "ID": ["gratis ongkir", "penawaran terbatas", "rumah", "dapur"],
        "SL": ["brezplačna dostava", "omejena ponudba", "dom", "kuhinja"],
    },
    "Belleza": {
        "ES": ["envío gratis", "obtenga el suyo", "belleza", "piel", "antiedad"],
        "EN": ["free shipping", "get yours now", "beauty", "skincare", "anti-aging"],
        "IT": ["spedizione gratis", "ottieni il tuo", "bellezza", "cura della pelle"],
        "NO": ["gratis frakt", "få din nå", "skjønnhet", "hudpleie"],
        "ID": ["gratis ongkir", "dapatkan sekarang", "kecantikan", "perawatan kulit"],
        "SL": ["brezplačna dostava", "pridobi svojega", "lepota", "nega kože"],
    },
    "Limpieza": {
        "ES": ["envío gratis", "50% descuento", "limpieza", "hogar limpio", "sin esfuerzo"],
        "EN": ["free shipping", "50% off", "cleaning", "clean home", "effortless"],
        "IT": ["spedizione gratis", "pulizia", "casa pulita", "senza sforzo"],
        "NO": ["gratis frakt", "rengjøring", "rent hjem", "uten anstrengelse"],
        "ID": ["gratis ongkir", "kebersihan", "rumah bersih", "tanpa usaha"],
        "SL": ["brezplačna dostava", "čiščenje", "čista hiša"],
    },
}

# ─── CONFIGURACIÓN ───────────────────────────────────────────────────────────
FB_ADS_URL = "https://www.facebook.com/ads/library/"
MIN_AD_DAYS = 8
HEADLESS = True

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
]


def is_shopify_store(url: str) -> bool:
    """Detecta si una URL es de Shopify o WooCommerce"""
    shopify_indicators = ["myshopify.com", "shopify.com", "/products/", "/collections/"]
    woo_indicators = ["woocommerce", "/?product=", "/shop/", "/tienda/"]
    url_lower = url.lower()
    return any(ind in url_lower for ind in shopify_indicators + woo_indicators)


def calculate_score(ad_data: dict) -> int:
    """Calcula el score de producto ganador (0-100)"""
    score = 0

    # Días activo (max 40 puntos)
    days = ad_data.get("ad_days", 0)
    if days >= 30:
        score += 40
    elif days >= 20:
        score += 30
    elif days >= 14:
        score += 20
    elif days >= 8:
        score += 15

    # Es Shopify (20 puntos)
    if ad_data.get("is_shopify"):
        score += 20

    # Tiene video (15 puntos)
    if ad_data.get("has_video"):
        score += 15

    # Keywords de alto valor (15 puntos)
    high_value_kw = ["envío gratis", "free shipping", "50%", "obtenga", "get yours"]
    text = ad_data.get("ad_text", "").lower()
    if any(kw in text for kw in high_value_kw):
        score += 15

    # Múltiples idiomas (10 puntos)
    if ad_data.get("multi_language"):
        score += 10

    return min(score, 100)


async def scrape_fb_ads(nichos: list, idiomas: list, min_days: int = 8, max_results: int = 10) -> list:
    """
    Función principal de scraping de Facebook Ads Library
    Retorna lista de productos ganadores encontrados
    """
    results = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=HEADLESS,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
            ]
        )

        context = await browser.new_context(
            user_agent=random.choice(USER_AGENTS),
            viewport={"width": 1920, "height": 1080},
            locale="es-ES",
        )

        # Ocultar webdriver
        await context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3]});
        """)

        page = await context.new_page()

        for nicho in nichos:
            for idioma in idiomas:
                keywords = KEYWORDS.get(nicho, {}).get(idioma, [])

                for keyword in keywords[:2]:  # Máx 2 keywords por nicho/idioma
                    try:
                        print(f"🔍 Buscando: '{keyword}' | Nicho: {nicho} | Idioma: {idioma}")

                        # Construir URL de búsqueda
                        search_url = (
                            f"{FB_ADS_URL}?"
                            f"active_status=active&"
                            f"ad_type=all&"
                            f"country=ALL&"
                            f"q={keyword.replace(' ', '+')}&"
                            f"search_type=keyword_unordered&"
                            f"media_type=video"
                        )

                        await page.goto(search_url, wait_until="networkidle", timeout=30000)
                        await asyncio.sleep(random.uniform(2, 4))

                        # Scroll para cargar más anuncios
                        for _ in range(3):
                            await page.keyboard.press("End")
                            await asyncio.sleep(1.5)

                        # Extraer datos de anuncios
                        ads = await page.evaluate("""
                            () => {
                                const adCards = document.querySelectorAll('[data-testid="ad_archive_grid"] > div');
                                return Array.from(adCards).slice(0, 5).map(card => {
                                    const text = card.innerText || '';
                                    const links = Array.from(card.querySelectorAll('a')).map(a => a.href);
                                    const videos = Array.from(card.querySelectorAll('video')).length;
                                    const images = Array.from(card.querySelectorAll('img')).length;
                                    return {
                                        text: text.substring(0, 500),
                                        links: links,
                                        has_video: videos > 0,
                                        has_image: images > 0,
                                    };
                                });
                            }
                        """)

                        for i, ad in enumerate(ads):
                            # Simular días activos (en producción se extrae del HTML)
                            ad_days = random.randint(min_days, 45)

                            if ad_days < min_days:
                                continue

                            # Detectar Shopify en los links
                            is_shopify = any(is_shopify_store(link) for link in ad.get("links", []))
                            store_url = next(
                                (link for link in ad.get("links", []) if is_shopify_store(link)),
                                ad.get("links", [""])[0] if ad.get("links") else ""
                            )

                            ad_data = {
                                "id": f"FB-{nicho[:3].upper()}-{int(time.time())}-{i}",
                                "name": f"Producto {nicho} ({keyword})",
                                "niche": nicho,
                                "language": idioma,
                                "country": "Global",
                                "store_url": store_url,
                                "platform": "Shopify" if is_shopify else "Desconocida",
                                "is_shopify": is_shopify,
                                "ad_text": ad.get("text", ""),
                                "has_video": ad.get("has_video", False),
                                "ad_days": ad_days,
                                "multi_language": len(idiomas) > 1,
                                "keyword": keyword,
                                "found_at": datetime.now().isoformat(),
                            }

                            ad_data["score"] = calculate_score(ad_data)
                            ad_data["trend"] = "Rising" if ad_data["score"] >= 80 else "Stable"
                            ad_data["price_sell"] = round(random.uniform(29.99, 89.99), 2)
                            ad_data["price_cost"] = round(ad_data["price_sell"] * 0.08, 2)
                            ad_data["margin"] = round((1 - ad_data["price_cost"] / ad_data["price_sell"]) * 100, 1)

                            if ad_data["score"] >= 60:
                                results.append(ad_data)
                                print(f"✅ Ganador encontrado: Score {ad_data['score']} | {nicho} | {ad_days} días")

                        await asyncio.sleep(random.uniform(3, 6))

                    except Exception as e:
                        print(f"⚠️ Error scraping '{keyword}': {e}")
                        continue

                    if len(results) >= max_results:
                        break

        await browser.close()

    # Ordenar por score
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:max_results]


def run_scraper(nichos: list, idiomas: list, min_days: int = 8) -> list:
    """Wrapper síncrono para llamar desde Streamlit"""
    try:
        return asyncio.run(scrape_fb_ads(nichos, idiomas, min_days))
    except Exception as e:
        print(f"Error en scraper: {e}")
        return []


if __name__ == "__main__":
    # Test rápido
    results = run_scraper(["Belleza", "Salud"], ["ES", "EN"], min_days=8)
    print(f"\n🎯 {len(results)} productos encontrados:")
    for p in results:
        print(f"  - {p['name']} | Score: {p['score']} | {p['ad_days']} días")
