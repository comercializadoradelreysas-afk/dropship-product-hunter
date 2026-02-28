"""
integrations.py — Módulo de automatización
OmniSpy AI — Notion + Google Drive
"""

import os
import json
import time
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# ─── NOTION ──────────────────────────────────────────────────────────────────
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
NOTION_HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}


def save_product_to_notion(product: dict) -> dict:
    """
    Guarda un producto ganador en la base de datos de Notion
    Retorna la respuesta de la API
    """
    if not NOTION_TOKEN or not NOTION_DATABASE_ID:
        return {"error": "Notion no configurado"}

    score = product.get("score", 0)
    score_emoji = "🔥" if score >= 85 else "⭐" if score >= 70 else "📌"

    payload = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "Nombre": {
                "title": [{"text": {"content": f"{score_emoji} {product.get('name', 'Producto sin nombre')}"}}]
            },
            "ID Anuncio": {
                "rich_text": [{"text": {"content": product.get("id", "")}}]
            },
            "URL Tienda": {
                "url": product.get("store_url", "") or None
            },
            "Nicho": {
                "select": {"name": product.get("niche", "General")}
            },
            "País": {
                "select": {"name": product.get("country", "Global")}
            },
            "Plataforma": {
                "select": {"name": product.get("platform", "Desconocida")}
            },
            "Score Ganador": {
                "number": product.get("score", 0)
            },
            "Días Activo": {
                "number": product.get("ad_days", 0)
            },
            "Precio Venta": {
                "number": product.get("price_sell", 0)
            },
            "Costo": {
                "number": product.get("price_cost", 0)
            },
            "Margen %": {
                "number": product.get("margin", 0)
            },
            "Tendencia": {
                "select": {"name": product.get("trend", "Stable")}
            },
            "Idioma": {
                "select": {"name": product.get("language", "ES")}
            },
            "Fecha Encontrado": {
                "date": {"start": datetime.now().isoformat()}
            },
        }
    }

    try:
        response = requests.post(
            "https://api.notion.com/v1/pages",
            headers=NOTION_HEADERS,
            json=payload,
            timeout=15
        )
        response.raise_for_status()
        result = response.json()
        print(f"✅ Notion: Producto guardado — {product.get('name')}")
        return result

    except requests.exceptions.HTTPError as e:
        print(f"❌ Notion HTTP Error: {e.response.text}")
        return {"error": str(e)}
    except Exception as e:
        print(f"❌ Notion Error: {e}")
        return {"error": str(e)}


def save_products_batch(products: list) -> dict:
    """Guarda múltiples productos en Notion"""
    results = {"success": 0, "errors": 0, "ids": []}

    for product in products:
        result = save_product_to_notion(product)
        if "error" not in result:
            results["success"] += 1
            results["ids"].append(result.get("id", ""))
        else:
            results["errors"] += 1
        time.sleep(0.4)  # Respetar rate limit de Notion

    print(f"📋 Notion batch: {results['success']} guardados, {results['errors']} errores")
    return results


def get_products_from_notion(limit: int = 50) -> list:
    """Obtiene productos desde Notion para mostrar en dashboard"""
    if not NOTION_TOKEN or not NOTION_DATABASE_ID:
        return []

    payload = {
        "sorts": [{"property": "Score Ganador", "direction": "descending"}],
        "page_size": limit,
    }

    try:
        response = requests.post(
            f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query",
            headers=NOTION_HEADERS,
            json=payload,
            timeout=15
        )
        response.raise_for_status()
        data = response.json()

        products = []
        for page in data.get("results", []):
            props = page.get("properties", {})

            def get_text(prop_name):
                prop = props.get(prop_name, {})
                if prop.get("type") == "title":
                    items = prop.get("title", [])
                elif prop.get("type") == "rich_text":
                    items = prop.get("rich_text", [])
                else:
                    return ""
                return items[0]["text"]["content"] if items else ""

            def get_select(prop_name):
                prop = props.get(prop_name, {})
                sel = prop.get("select")
                return sel["name"] if sel else ""

            def get_number(prop_name):
                return props.get(prop_name, {}).get("number", 0)

            def get_url(prop_name):
                return props.get(prop_name, {}).get("url", "")

            products.append({
                "id": get_text("ID Anuncio"),
                "name": get_text("Nombre"),
                "niche": get_select("Nicho"),
                "country": get_select("País"),
                "platform": get_select("Plataforma"),
                "store_url": get_url("URL Tienda"),
                "score": get_number("Score Ganador"),
                "ad_days": get_number("Días Activo"),
                "price_sell": get_number("Precio Venta"),
                "price_cost": get_number("Costo"),
                "margin": get_number("Margen %"),
                "trend": get_select("Tendencia"),
                "language": get_select("Idioma"),
            })

        return products

    except Exception as e:
        print(f"❌ Error obteniendo productos de Notion: {e}")
        return []


# ─── GOOGLE DRIVE ────────────────────────────────────────────────────────────
def get_drive_service():
    """Inicializa el servicio de Google Drive"""
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build

        credentials_file = os.getenv("GOOGLE_CREDENTIALS_JSON", "credentials.json")

        if not os.path.exists(credentials_file):
            print("⚠️ Archivo credentials.json no encontrado")
            return None

        SCOPES = ["https://www.googleapis.com/auth/drive"]
        credentials = service_account.Credentials.from_service_account_file(
            credentials_file, scopes=SCOPES
        )
        service = build("drive", "v3", credentials=credentials)
        return service

    except Exception as e:
        print(f"❌ Error inicializando Google Drive: {e}")
        return None


def create_product_folder(product_name: str, parent_folder_id: str) -> str:
    """Crea una carpeta en Google Drive para el producto"""
    service = get_drive_service()
    if not service:
        return ""

    folder_metadata = {
        "name": f"📦 {product_name} — {datetime.now().strftime('%Y-%m-%d')}",
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [parent_folder_id],
    }

    try:
        folder = service.files().create(body=folder_metadata, fields="id").execute()
        folder_id = folder.get("id", "")
        print(f"📁 Carpeta creada en Drive: {product_name} ({folder_id})")
        return folder_id

    except Exception as e:
        print(f"❌ Error creando carpeta en Drive: {e}")
        return ""


def download_ad_videos(product: dict, video_urls: list, folder_id: str) -> int:
    """
    Descarga videos creativos del anuncio y los sube a Google Drive
    Retorna el número de videos descargados exitosamente
    """
    service = get_drive_service()
    if not service or not folder_id:
        return 0

    from googleapiclient.http import MediaFileUpload
    import tempfile

    downloaded = 0
    product_name = product.get("name", "producto")

    for i, url in enumerate(video_urls[:5]):  # Máximo 5 videos
        try:
            # Descargar el video
            response = requests.get(url, timeout=30, stream=True)
            response.raise_for_status()

            # Guardar temporalmente
            with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
                for chunk in response.iter_content(chunk_size=8192):
                    tmp.write(chunk)
                tmp_path = tmp.name

            # Subir a Drive
            file_metadata = {
                "name": f"creativo_{i+1}_{product_name[:30]}.mp4",
                "parents": [folder_id],
            }
            media = MediaFileUpload(tmp_path, mimetype="video/mp4", resumable=True)
            service.files().create(
                body=file_metadata,
                media_body=media,
                fields="id"
            ).execute()

            downloaded += 1
            print(f"✅ Video {i+1} subido a Drive")
            os.unlink(tmp_path)  # Limpiar archivo temporal

        except Exception as e:
            print(f"⚠️ Error descargando video {i+1}: {e}")

    return downloaded


def save_product_to_drive(product: dict, video_urls: list = None) -> str:
    """
    Flujo completo: crea carpeta en Drive y descarga videos
    Retorna el link de la carpeta creada
    """
    parent_folder_id = os.getenv("GOOGLE_DRIVE_FOLDER_ID", "")
    if not parent_folder_id:
        print("⚠️ GOOGLE_DRIVE_FOLDER_ID no configurado")
        return ""

    # Crear carpeta del producto
    product_name = product.get("name", "Producto")
    folder_id = create_product_folder(product_name, parent_folder_id)

    if not folder_id:
        return ""

    # Descargar videos si los hay
    if video_urls:
        count = download_ad_videos(product, video_urls, folder_id)
        print(f"📥 {count} videos descargados para: {product_name}")

    folder_link = f"https://drive.google.com/drive/folders/{folder_id}"
    return folder_link


# ─── AUTOMATIZACIÓN 24H ──────────────────────────────────────────────────────
def run_daily_automation(nichos: list, idiomas: list, min_days: int = 8):
    """
    Automatización completa de 24 horas:
    1. Scraping de FB Ads
    2. Guardar en Notion
    3. Crear carpetas en Drive
    """
    from scraper import run_scraper

    print(f"\n🤖 Iniciando automatización diaria — {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    # 1. Scraping
    print("🔍 Fase 1: Scraping Facebook Ads Library...")
    products = run_scraper(nichos, idiomas, min_days)
    print(f"✅ {len(products)} productos encontrados")

    # 2. Guardar en Notion
    print("\n📋 Fase 2: Guardando en Notion...")
    notion_results = save_products_batch(products)
    print(f"✅ {notion_results['success']} productos en Notion")

    # 3. Google Drive
    print("\n📁 Fase 3: Creando carpetas en Google Drive...")
    for product in products[:5]:  # Top 5 productos
        drive_link = save_product_to_drive(product)
        if drive_link:
            product["drive_link"] = drive_link
        time.sleep(1)

    print(f"\n🎯 Automatización completada — {datetime.now().strftime('%H:%M:%S')}")
    return products


if __name__ == "__main__":
    # Test de conexión Notion
    print("🧪 Probando conexión con Notion...")
    test_product = {
        "id": "TEST-001",
        "name": "Producto de Prueba",
        "niche": "Salud",
        "country": "Colombia",
        "platform": "Shopify",
        "store_url": "https://test.myshopify.com",
        "score": 88,
        "ad_days": 15,
        "price_sell": 49.99,
        "price_cost": 4.50,
        "margin": 91.0,
        "trend": "Rising",
        "language": "ES",
    }
    result = save_product_to_notion(test_product)
    print(f"Resultado: {result.get('id', result.get('error', 'Error'))}")
