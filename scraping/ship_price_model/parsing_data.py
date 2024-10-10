import json

def parse_model_data(input_file, output_file):
    with open(input_file, 'r') as file:
        data = json.load(file)

    data_for_model = []
    for sneaker in data:
        sneaker_dict = {
            "sneaker_name": sneaker.get("sneaker_name"),
            "retail_price_eur": sneaker.get("retail_price_eur"),
            "lowest_price_eur": sneaker.get("lowest_price_eur"),
            "instant_ship_lowest_price_eur" : sneaker.get("instant_ship_lowest_price_eur"),
            "gp_lowest_price_eur": sneaker.get("gp_lowest_price_eur"),
            "gp_instant_ship_lowest_price_eur": sneaker.get("gp_instant_ship_lowest_price_eur"),
        }
        data_for_model.append(sneaker_dict)

    with open(output_file, 'w') as file:
        json.dump(data_for_model, file, indent = 4)

def get_training_testing_data(input_file, train_output_file, test_output_file):
    with open(input_file, 'r') as file:
        data = json.load(file)

    training_data = [sneaker for sneaker in data if
                     sneaker.get('instant_ship_lowest_price_eur') is not None and sneaker.get(
                         'gp_instant_ship_lowest_price_eur') is not None]

    print(f"Number of sneakers meeting the condition: {len(training_data)}")

    split_index = int(len(training_data) * 0.75)
    train_data = training_data[:split_index]
    test_data = training_data[split_index:]

    # Save the training data
    with open(train_output_file, 'w') as file:
        json.dump(train_data, file, indent=4)

    # Save the testing data
    with open(test_output_file, 'w') as file:
        json.dump(test_data, file, indent=4)

def get_data_to_predict(input_file, output_file):
    with open(input_file, 'r') as file:
        data = json.load(file)

    predict_data = [sneaker for sneaker in data if
                     sneaker.get('instant_ship_lowest_price_eur') is  None or sneaker.get(
                         'gp_instant_ship_lowest_price_eur') is None]

    print(f"Number of sneakers meeting the condition: {len(predict_data)}")

    with open(output_file, 'w') as file:
        json.dump(predict_data, file, indent = 4)

