import requests
import json

#url = https://ac.cnstrc.com/search/nike?c=ciojs-client-2.51.2&key=key_XT7bjdbvjgECO5d8&i=1037ff49-ad22-480b-a078-980b4d5c4d6c&s=1&page=1&num_results_per_page=24&sort_by=relevance&sort_order=descending&fmt_options%5Bhidden_fields%5D=gp_lowest_price_cents_224&fmt_options%5Bhidden_fields%5D=gp_instant_ship_lowest_price_cents_224&fmt_options%5Bhidden_facets%5D=gp_lowest_price_cents_224&fmt_options%5Bhidden_facets%5D=gp_instant_ship_lowest_price_cents_224&variations_map=%7B%22group_by%22%3A%5B%7B%22name%22%3A%22product_condition%22%2C%22field%22%3A%22data.product_condition%22%7D%2C%7B%22name%22%3A%22box_condition%22%2C%22field%22%3A%22data.box_condition%22%7D%5D%2C%22values%22%3A%7B%22min_regional_price%22%3A%7B%22aggregation%22%3A%22min%22%2C%22field%22%3A%22data.gp_lowest_price_cents_224%22%7D%2C%22min_regional_instant_ship_price%22%3A%7B%22aggregation%22%3A%22min%22%2C%22field%22%3A%22data.gp_instant_ship_lowest_price_cents_224%22%7D%7D%2C%22dtype%22%3A%22object%22%7D&qs=%7B%22features%22%3A%7B%22display_variations%22%3Atrue%7D%2C%22feature_variants%22%3A%7B%22display_variations%22%3A%22matched%22%7D%7D&_dt=1728226205676

#scrape goat.com
def scrape_sneakers(query, output_file = 'sneakers_data.json'):
    all_sneakers = []
    page = 1

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write("[")

        while True:
            url = f'https://ac.cnstrc.com/search/{query}?c=ciojs-client-2.51.2&key=key_XT7bjdbvjgECO5d8&i=1037ff49-ad22-480b-a078-980b4d5c4d6c&s=1&page={page}&num_results_per_page=24&sort_by=relevance&sort_order=descending&fmt_options%5Bhidden_fields%5D=gp_lowest_price_cents_224&fmt_options%5Bhidden_fields%5D=gp_instant_ship_lowest_price_cents_224&fmt_options%5Bhidden_facets%5D=gp_lowest_price_cents_224&fmt_options%5Bhidden_facets%5D=gp_instant_ship_lowest_price_cents_224&variations_map=%7B%22group_by%22%3A%5B%7B%22name%22%3A%22product_condition%22%2C%22field%22%3A%22data.product_condition%22%7D%2C%7B%22name%22%3A%22box_condition%22%2C%22field%22%3A%22data.box_condition%22%7D%5D%2C%22values%22%3A%7B%22min_regional_price%22%3A%7B%22aggregation%22%3A%22min%22%2C%22field%22%3A%22data.gp_lowest_price_cents_224%22%7D%2C%22min_regional_instant_ship_price%22%3A%7B%22aggregation%22%3A%22min%22%2C%22field%22%3A%22data.gp_instant_ship_lowest_price_cents_224%22%7D%7D%2C%22dtype%22%3A%22object%22%7D&qs=%7B%22features%22%3A%7B%22display_variations%22%3Atrue%7D%2C%22feature_variants%22%3A%7B%22display_variations%22%3A%22matched%22%7D%7D&_dt=1728226205676'

            response = requests.get(url)
            if response.status_code != 200:
                print(f"failed to fetch status code = {response.status_code}")
                break

            output = json.loads(response.text)
            results = output.get('response', {}).get('results', [])

            if not results:
                print("No more results")
                break

            for sneaker in results:
                json.dump(sneaker, file, ensure_ascii=False)
                all_sneakers.append(sneaker)
                file.write(",\n")

            print(f"Scraped {page}, found {len(results)}")
            page += 1

        file.seek(file.tell() - 2, 0)
        file.write("]")
    return all_sneakers

scraped_sneakers = scrape_sneakers('sneakers', 'sneakers_data.json')
print(f"Scraped {len(scraped_sneakers)}")




