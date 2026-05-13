from config import config
from state import state
from generator import generate
from builder import build
from publisher import publish
from marketer import create_pin

def main():
    config.validate()
    niche = state.get_next_niche()
    print(f"[{niche}] Generating...")

    data = generate(niche)
    prompts_count = sum(len(c["prompts"]) for c in data["prompts"])
    print(f"  Title: {data['title']}")
    print(f"  Prompts: {prompts_count}")

    filepath = build(data)
    print(f"  PDF: {filepath}")

    product = publish(data, str(filepath))
    print(f"  Gumroad: {product['url']}")

    try:
        pin_id = create_pin(data, product)
        print(f"  Pinterest Pin: {pin_id}")
    except Exception as e:
        print(f"  Pinterest failed (auth pending): {e}")
        pin_id = None

    state.record_template(
        title=data["title"],
        niche=niche,
        prompts_count=prompts_count,
        gumroad_id=product["product_id"],
        gumroad_url=product["url"],
        pinterest_pin_id=pin_id,
    )
    state.mark_niche_used(niche)

    print("Done!")

if __name__ == "__main__":
    main()
