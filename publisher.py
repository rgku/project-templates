import requests
from config import config

GUMROAD_API = "https://api.gumroad.com/v2"

def publish(data: dict, filepath: str) -> dict:
    price_cents = int(float(data.get("price", 7.99)) * 100)

    with open(filepath, "rb") as f:
        resp = requests.post(
            f"{GUMROAD_API}/products",
            data={
                "access_token": config.gumroad_access_token,
                "name": data["title"],
                "description": data.get("description", ""),
                "price": price_cents,
                "tags": ",".join(data.get("tags", [])),
            },
            files={"file": f},
            timeout=60,
        )
    resp.raise_for_status()
    result = resp.json()
    if not result.get("success"):
        raise RuntimeError(f"Gumroad error: {result}")

    product = result["product"]
    return {
        "product_id": product["id"],
        "url": product["short_url"],
        "preview_url": product.get("preview_url"),
    }
