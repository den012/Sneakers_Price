import json
from platform import release


def get_data_for_model(input_file, output_file):
    with open(input_file, 'r') as file:
        data = json.load(file)

    data_for_model = []
    for sneaker in data:
        release_date = sneaker.get('release_date')
        if release_date is not None:
            release_date = int(release_date)
            year = release_date // 10000
            month  = (release_date % 10000) // 100
            day = release_date % 100
        else:
            year = None
            month = None
            day = None
        sneaker_dict = {
            'sneaker_name' : sneaker.get('sneaker_name'),
            'sneaker_color': sneaker.get('sneaker_color'),
            'release_year' : year,
            'release_month': month,
            'release_day' : day,
        }
        data_for_model.append(sneaker_dict)

    with open(output_file, 'w') as file:
        json.dump(data_for_model, file, indent = 4)

