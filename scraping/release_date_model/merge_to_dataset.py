import json

def refractor_data(input_file, output_file):
    with open(input_file, 'r') as file:
        data = json.load(file)

        for sneaker in data:
            release_date = sneaker.get('release_date')
            if release_date is not None:
                release_date = int(release_date)
                sneaker['release_year'] = release_date // 10000
                sneaker['release_month'] = (release_date % 10000) // 100
                sneaker['release_day'] = release_date % 100
            else:
                sneaker['release_year'] = None
                sneaker['release_month'] = None
                sneaker['release_day'] = None
            if 'release_date' in sneaker:
                del sneaker['release_date']

        with open(output_file, 'w') as file:
            json.dump(data, file, indent=4)

def update_release_dates(input_file, predicted_data_file, output_file):
    with open(input_file, 'r') as file:
        old_data = json.load(file)


    with open(predicted_data_file, 'r') as file:
        predicted_data = json.load(file)

    predicted_dict = {sneaker['sneaker_name']: sneaker for sneaker in predicted_data}


    for sneaker in old_data:
        if sneaker.get('release_date') is None:
            predicted_sneaker = predicted_dict.get(sneaker['sneaker_name'])
            if predicted_sneaker:
                sneaker['release_year'] = predicted_sneaker.get('release_year')
                sneaker['release_month'] = predicted_sneaker.get('release_month')
                sneaker['release_day'] = predicted_sneaker.get('release_day')
        if 'release_date' in sneaker:
            del sneaker['release_date']
    # Save the updated dataset to a new JSON file
    with open(output_file, 'w') as file:
        json.dump(old_data, file, indent=4)

