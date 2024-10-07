from scraper import scrape_sneakers
from functions.remove_rename_add_columns import remove_rename_add_data_cols
from functions.detect_brand import detect_brands
from functions.detect_collab import celebs, add_collaboration
from functions.detect_sneaker_dicount_tag import fix_sneaker_discount


# scraped_sneakers = scrape_sneakers('sneakers', 'testing_steps/sneakers_data.json')
# print(f"Scraped {len(scraped_sneakers)}")

# remove_rename_add_data_cols('testing_steps/sneakers_data.json')

# detect_brands('testing_steps/sneakers_data.json', 'testing_steps/sneakers_data.json')

# number, sneakers_with_collab = add_collaboration('testing_steps/sneakers_data.json', 'testing_steps/sneakers_data.json')
# print(number)
# print(f"Processed {len(sneakers_with_collab)}")

# fix_sneaker_discount('testing_steps/sneakers_data.json', 'testing_steps/sneakers_data.json')