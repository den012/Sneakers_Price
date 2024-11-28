from scrape_data.scrape import *
from filter_data.arrange_columns import *
from filter_data.drop_outbounds import *
from filter_data.get_brands import *
from filter_data.get_collaboration import *
from filter_data.days_since_release import *


def main():
    # scrape goat.com
    # sneakers = scrape_sneakers('sneakers', 'sneakers.json')
    # print(f"Successfully scraped {len(sneakers)} sneakers")

    # clear columns
    # clear_columns('sneakers.json', 'sneakers.json')

    #drop outbounds
    filter_outbound_prices('sneakers.json', 'sneakers.json')
    #drop null
    # filter_null('sneakers.json', 'sneakers.json')

    # detect brand
    # get_brand('sneakers.json', 'sneakers.json')

    # detect collaboration
    # count, data = add_collaboration('sneakers.json', 'sneakers.json', celebs)
    # print(f"Number of collaborations found: {count}")

    # #release date
    # filter_release_date('sneakers.json', 'sneakers.json')
    # process_sneaker_data('sneakers.json', 'sneakers.json')

    #box condition
    # filter_box_condition('sneakers.json', 'sneakers.json')





    print("x")

if __name__ == '__main__':
    main()