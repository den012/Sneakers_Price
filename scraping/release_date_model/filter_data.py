import json
from platform import release


def get_data_for_model(input_file, output_file):
    with open(input_file, 'r') as file:
        data = json.load(file)

    data_for_model = []
    for sneaker in data:
        sneaker_dict = {
            'sneaker_name' : sneaker.get('sneaker_name'),
            'sneaker_color': sneaker.get('sneaker_color'),
            'release_year' : sneaker.get('release_year'),
            'release_month': sneaker.get('release_month'),
            'release_day' : sneaker.get('release_day'),
        }
        data_for_model.append(sneaker_dict)

    with open(output_file, 'w') as file:
        json.dump(data_for_model, file, indent = 4)

def get_training_and_testing_data(input_file, train_output_file):
    with open(input_file, 'r') as file:
        data = json.load(file)

    # Filter out sneakers with non-null release_year
    training_data = [sneaker for sneaker in data if sneaker.get('release_year') is not None]

    # Save the training data
    with open(train_output_file, 'w') as file:
        json.dump(training_data, file, indent=4)

def get_data_to_predict(input_file, output_file):
    with open(input_file, 'r') as file:
        data = json.load(file)

    testing_data = []
    for sneaker in data:
        if sneaker.get('release_year') is None:
            sneaker_dict = {
                'sneaker_name': sneaker.get('sneaker_name'),
                'sneaker_color': sneaker.get('sneaker_color'),
                'release_year': sneaker.get('release_year'),
                'release_month': sneaker.get('release_month'),
                'release_day': sneaker.get('release_day'),
            }
            testing_data.append(sneaker_dict)

    with open(output_file, 'w') as file:
        json.dump(testing_data, file, indent = 4)

