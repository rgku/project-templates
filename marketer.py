import requests
from config import config

PINTEREST_API = "https://api.pinterest.com/v5"

def create_pin(data: dict, product: dict, image_url: str = None):
    description = data.get("pinterest_description", "")
    description += f"\n\nGrab your copy: {product['url']}"

    pin_data = {
        "pin_name": data.get("seo_title", data["title"])[:100],
        "description": description[:500],
        "board_id": config.pinterest_board_id,
        "media_source": {
            "source_type": "image_url",
            "url": image_url or product.get("preview_url", ""),
        },
    }

    resp = requests.post(
        f"{PINTEREST_API}/pins",
        headers={
            "Authorization": f"Bearer {config.pinterest_access_token}",
            "Content-Type": "application/json",
        },
        json=pin_data,
        timeout=30,
    )

    if resp.status_code == 429:
        return None

    resp.raise_for_status()
    return resp.json().get("id")
