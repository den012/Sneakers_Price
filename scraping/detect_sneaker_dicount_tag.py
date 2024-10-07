import json

def fix_sneaker_discount(input_file, output_file):
    with open(input_file, 'r', encoding = 'utf-8') as file:
        data = json.load(file)
        for sneaker in data:
            if sneaker['sneaker_discount_tag'] == "":
                if sneaker.get('lowest_price_euros') <= sneaker.get('retail_price_euros'):
                    sneaker['sneaker_discount_tag'] = 'under_retail'
                else:
                    sneaker['sneaker_discount_tag'] = 'over_retail'

    with open(output_file, 'w', encoding = 'utf-8') as file:
        json.dump(data, file, indent = 4)

fix_sneaker_discount('data/sneaker_collab_brand.json', 'sneaker_collab_brand_fixed_discount.json')
