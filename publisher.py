import os
import requests
from config import config

GUMROAD_API = "https://api.gumroad.com/v2"


def _upload_file(filepath: str) -> str:
    file_size = os.path.getsize(filepath)
    filename = os.path.basename(filepath)

    presign_resp = requests.post(
        f"{GUMROAD_API}/files/presign",
        data={
            "access_token": config.gumroad_access_token,
            "filename": filename,
            "file_size": file_size,
        },
        timeout=30,
    )
    presign_resp.raise_for_status()
    presign = presign_resp.json()
    if not presign.get("success"):
        raise RuntimeError(f"Presign failed: {presign}")

    upload_id = presign["upload_id"]
    key = presign["key"]
    parts_meta = presign["parts"]

    uploaded_parts = []
    with open(filepath, "rb") as f:
        for part in sorted(parts_meta, key=lambda p: p["part_number"]):
            chunk = f.read(5 * 1024 * 1024)
            put_resp = requests.put(part["presigned_url"], data=chunk, timeout=120)
            put_resp.raise_for_status()
            etag = put_resp.headers.get("ETag", "").strip('"')
            uploaded_parts.append({
                "part_number": part["part_number"],
                "etag": etag,
            })

    complete_resp = requests.post(
        f"{GUMROAD_API}/files/complete",
        json={
            "access_token": config.gumroad_access_token,
            "upload_id": upload_id,
            "key": key,
            "parts": uploaded_parts,
        },
        timeout=30,
    )
    complete_resp.raise_for_status()
    complete = complete_resp.json()
    if not complete.get("success"):
        raise RuntimeError(f"Complete failed: {complete}")

    return complete["file_url"]


def publish(data: dict, filepath: str) -> dict:
    price_cents = int(float(data.get("price", 7.99)) * 100)

    file_url = _upload_file(filepath)

    product_data = [
        ("access_token", config.gumroad_access_token),
        ("name", data["title"]),
        ("description", data.get("description", "")),
        ("price", str(price_cents)),
        ("files[][url]", file_url),
    ]
    for tag in data.get("tags", []):
        product_data.append(("tags[]", tag))
    resp = requests.post(
        f"{GUMROAD_API}/products",
        data=product_data,
        timeout=30,
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
