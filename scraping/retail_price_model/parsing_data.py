import json

def clean_dataset(input_file, output_file):
    with open(input_file, 'r') as file:
        data = json.load(file)

    cleaned_data = []
    for sneaker in data:
        if sneaker.get('box_condition') is not None and sneaker.get('product_condition') is not None and sneaker.get('lowest_price_eur') is not None and sneaker.get('gp_lowest_price_eur') is not None and sneaker.get('retail_price_eur') is not None:
            cleaned_data.append(sneaker)

    print(f'found {len(cleaned_data)}')
    with open(output_file, 'w') as file:
        json.dump(cleaned_data, file, indent=4)


def get_prediction_data(input_file, output_file):
    with open(input_file, 'r') as file:
        data = json.load(file)

    model_data = []
    for sneaker in data:
        if sneaker.get('retail_price_eur') == 0.0:
            model_data.append({
                'sneaker_name' : sneaker.get('sneaker_name'),
                'collaboration' : sneaker.get('collaboration'),
                'release_year' : sneaker.get('release_year'),
                'lowest_price_eur' : sneaker.get('lowest_price_eur'),
                'retail_price_eur': sneaker.get('retail_price_eur')
            })

    print(f'found {len(model_data)}')
    with open(output_file, 'w') as file:
        json.dump(model_data, file, indent=4)

def get_test_train_data(input_file, train_output_file, test_output_file):
    with open(input_file, 'r') as file:
        data = json.load(file)

    training_data = []
    for sneaker in data:
        if sneaker.get('retail_price_eur') != 0.0:
            training_data.append({
                'sneaker_name': sneaker.get('sneaker_name'),
                'collaboration': sneaker.get('collaboration'),
                'release_year': sneaker.get('release_year'),
                'lowest_price_eur': sneaker.get('lowest_price_eur'),
                'retail_price_eur': sneaker.get('retail_price_eur')
            })

    print(f"Number of sneakers meeting the condition: {len(training_data)}")

    split_index = int(len(training_data) * 0.75)
    train_data = training_data[:split_index]
    test_data = training_data[split_index:]

    with open(train_output_file, 'w') as file:
        json.dump(train_data, file, indent=4)

    with open(test_output_file, 'w') as file:
        json.dump(test_data, file, indent=4)

def merge_predicted_data(original_file, predicted_file, output_file):
    with open(original_file, 'r') as file:
        original_data = json.load(file)

    with open(predicted_file, 'r') as file:
        predicted_data = json.load(file)

    predicted_dict = {sneaker['sneaker_name']: sneaker for sneaker in predicted_data}

    for sneaker in original_data:
        if sneaker['sneaker_name'] in predicted_dict:
            sneaker['retail_price_eur'] = predicted_dict[sneaker['sneaker_name']]['retail_price_eur']

    with open(output_file, 'w') as file:
        json.dump(original_data, file, indent=4)

    print(f'Merged data saved to {output_file}')
