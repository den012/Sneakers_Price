import json

with open('updated_sneaker_data.json', 'r') as file:
    data = json.load(file)

unknown_brand = []
for shoe in data:
    if shoe.get('brand') == "Unknown":
        unknown_brand.append({
            "name": shoe.get("value"),
            "brand": shoe.get("brand")
        })

with open('unknown_brand_shoes', 'w') as file:
    json.dump(unknown_brand, file, indent = 4)

print(f"Found {len(unknown_brand)} shoes")


