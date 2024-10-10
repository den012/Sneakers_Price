import json

def fix_sneaker_discount(input_file, output_file):
    with open(input_file, 'r', encoding = 'utf-8') as file:
        data = json.load(file)
        for sneaker in data:
            if not sneaker.get('discount_tag'):
                try:
                    lowest_price = int(sneaker.get('lowest_price_euros', 0))
                    retail_price = int(sneaker.get('retail_price_euros', 0))
                    if lowest_price < retail_price:
                        sneaker['discount_tag'] = 'under_retail'
                    else:
                        sneaker['discount_tag'] = 'over_retail'
                except:
                    sneaker['discount_tag'] = 'invalid_price'

    with open(output_file, 'w', encoding = 'utf-8') as file:
        json.dump(data, file, indent = 4)

