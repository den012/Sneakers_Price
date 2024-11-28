from keras.src.metrics import accuracy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV

brand_map = {
    #Nike
    "Air": "Nike", "Jordan": "Nike", "Air Max": "Nike", "Dunk": "Nike",
    "Blazer": "Nike", "Force": "Nike", "Vapor": "Nike", "React": "Nike",
    "Pegasus": "Nike", "Zoom": "Nike", "Cortez": "Nike", "NikeLab": "Nike",
    "Kobe": "Nike", "Quest": "Nike", "Sabrina": "Nike", "Metcon": "Nike",
    "Clogposite": "Nike", "LeBron": "Nike", "Alpha": "Nike", "Gore-Tex": "Nike",
    "Structure": "Nike", "Infinity Run": "Nike", "Phantom": "Nike", "Presto": "Nike",
    "Flyknit": "Nike", "Huarache": "Nike", "Free": "Nike", "ACG": "Nike",
    "Shox": "Nike", "Air Rift": "Nike", "Hyperdunk": "Nike", "Odyssey": "Nike",
    "Epic": "Nike", "Mercurial": "Nike", "Tiempo": "Nike", "M2K Tekno": "Nike",
    "Daybreak": "Nike", "Waffle": "Nike", "Killshot": "Nike", "FlyEase": "Nike",
    "React Element": "Nike", "Roshe": "Nike", "Crater": "Nike", "SFB": "Nike",
    "Fear of God": "Nike", "Waffle One": "Nike", "ISPA": "Nike", "Court Vision": "Nike",
    "Sb": "Nike", "Lunar": "Nike", "Vandal": "Nike", "NikeCourt": "Nike",
    "JA": "Nike", "KD": "Nike", "Kyrie": "Nike", "PG": "Nike", "Book 1": "Nike",
    "P-600": "Nike", "WMNS": "Nike", "Tanjun": "Nike", "Revolution": "Nike",
    "Stussy": "Nike",

    "Bottega Veneta": "Bottega Veneta",
    "Versace": "Versace",
    "Supreme": "Supreme",
    "Chanel": "Chanel",
    "Rick Owens": "Rick Owens",
    "Alexander McQueen": "Alexander McQueen",
    "Balenciaga": "Balenciaga",
    "Converse": "Converse",
    "Fila": "Fila",
    "Givenchy": "Givenchy",
    "Gucci": "Gucci",
    "Lanvin": "Lanvin",
    "Louis Vuitton": "Louis Vuitton",
    "Maison Margiela": "Maison Margiela",
    "Off-White": "Off-White",
    "Prada": "Prada",

    # Adidas
    "UltraBoost": "Adidas", "Yeezy": "Adidas", "NMD": "Adidas", "Superstar": "Adidas",
    "Stan Smith": "Adidas", "Gazelle": "Adidas", "Samba": "Adidas", "Adizero": "Adidas",
    "Predator": "Adidas", "Copa": "Adidas", "X": "Adidas", "Pharrell": "Adidas",
    "ZX": "Adidas", "Forum": "Adidas", "EQT": "Adidas", "Ozweego": "Adidas",
    "SL": "Adidas", "Terrex": "Adidas", "Torsion": "Adidas", "Tubular": "Adidas",
    "4D": "Adidas", "Alphabounce": "Adidas", "Climacool": "Adidas", "POD": "Adidas",
    "Crazy Explosive": "Adidas", "PureBoost": "Adidas", "Nite Jogger": "Adidas",
    "Prophere": "Adidas", "Falcon": "Adidas", "Iniki": "Adidas", "Raf Simons": "Adidas",

    # Puma
    "Suede": "Puma", "RS-X": "Puma", "Rider": "Puma", "Cali": "Puma",
    "Basket": "Puma", "Cell": "Puma", "Disc": "Puma", "Future Rider": "Puma",
    "Fenty": "Puma", "Ignite": "Puma", "Evoknit": "Puma", "Tsugi": "Puma",
    "Roma": "Puma", "Speedcat": "Puma", "RS Dreamer": "Puma", "Slipstream": "Puma",
    "Blaze": "Puma", "Jamming": "Puma", "Avid": "Puma", "Ralph Sampson": "Puma",
    "LQDCell": "Puma", "Thunder": "Puma", "Wild Rider": "Puma", "Clyde": "Puma",

    # New Balance
    "574": "New Balance", "990": "New Balance", "997": "New Balance",
    "550": "New Balance", "9060": "New Balance", "X-Racer": "New Balance",
    "Hesi Low": "New Balance", "1080": "New Balance", "860": "New Balance",
    "Fresh Foam": "New Balance", "FuelCell": "New Balance", "Kaizen": "New Balance",
    "998": "New Balance", "373": "New Balance", "327": "New Balance",
    "Vision Racer": "New Balance", "2002R": "New Balance", "501": "New Balance",
    "Vongo": "New Balance", "Minimus": "New Balance", "Cush+": "New Balance", "1000": "New Balance",
    "1906A": "New Balance",

    # Skechers
    "D'Lites": "Skechers", "Max Cushioning": "Skechers", "Go Walk": "Skechers",
    "Arch Fit": "Skechers", "Energy": "Skechers", "Skech-Air": "Skechers",
    "GOrun": "Skechers", "Bobs": "Skechers", "Flex Appeal": "Skechers",
    "Gowalk Arch": "Skechers", "Hyper Burst": "Skechers", "Ultra Flex": "Skechers",
    "D'Lux": "Skechers", "You by Skechers": "Skechers", "Skechers Foamies": "Skechers",
    "Twinkle Toes": "Skechers", "Relaxed Fit": "Skechers", "Equalizer": "Skechers",
    "Shuffles": "Skechers", "Treadfit": "Skechers", "Delson": "Skechers",

    # Asics
    "Gel": "Asics", "Kayano": "Asics", "Nimbus": "Asics", "Cumulus": "Asics",
    "Quantum": "Asics", "Lyte": "Asics", "Noosa": "Asics", "GT-2000": "Asics",
    "GT-1000": "Asics", "Trabuco": "Asics", "Metaride": "Asics", "Tarther": "Asics",
    "DS Trainer": "Asics", "Gel-Lyte III": "Asics", "Gel-Venture": "Asics",
    "FujiTrabuco": "Asics", "GlideRide": "Asics", "Court FF": "Asics", "Blast": "Asics",
    "Kihachiro": "Asics"
}

# Function to detect brand using brand_map
def detect_brand(name):
    for keyword, brand in brand_map.items():
        if keyword.lower() in name.lower():
            return brand
    return "Other"

def get_brand(input_file, output_file):
    data = pd.read_json(input_file)

    data['brand'] = data['slug'].apply(detect_brand)

    # Filter out rows with 'Other' brand
    filtered_data = data[data['brand'] != 'Other']

    # Write the filtered DataFrame to a new JSON file
    filtered_data.to_json(output_file, orient='records', indent=4)


# def predict_with_model(input_file, output_file):
#     data = pd.read_json(input_file)
#
#     data['brand'] = data['slug'].apply(detect_brand)
#
#     # Filter out rows with 'Other' brand
#     data = data[data['brand'] != 'Other']
#
#     # Prepare data for model training
#     X = data['slug']
#     y = data['brand']
#
#     tfidf = TfidfVectorizer()
#     X_tfidf = tfidf.fit_transform(X)
#
#     X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y, test_size=0.2, random_state=42)
#
#     # Train the model
#     model = LogisticRegression()
#     model.fit(X_train, y_train)
#
#     param_grid = {
#         'C': [0.01, 0.1, 1, 10, 100],
#         'solver': ['liblinear', 'lbfgs']
#     }
#
#     # Perform grid search with cross-validation
#     grid_search = GridSearchCV(LogisticRegression(max_iter=1000), param_grid, cv=3, scoring='accuracy')
#     grid_search.fit(X_tfidf, y)
#
#     print(f"Best Parameters: {grid_search.best_params_}")
#     print(f"Best Cross-Validation Accuracy: {grid_search.best_score_:.4f}")
#
#     # Predict the brand for each sneaker in the dataset
#     data['predicted_brand'] = model.predict(tfidf.transform(data['slug']))
#
#     # Filter the DataFrame based on the predicted brand
#     filtered_data = data[data['predicted_brand'] != 'Other']
#
#     # Write the filtered DataFrame to a new JSON file
#     filtered_data.to_json(output_file, orient='records', indent=4)
#
#     # Print the accuracy of the model
#     y_pred = model.predict(X_test)
#     accuracy = accuracy_score(y_test, y_pred)
#     print(f"Accuracy: {accuracy}")
#
#     cv_scores = cross_val_score(model, X_tfidf, y, cv=5, scoring='accuracy')
#     print(f"Cross-Validation Accuracy: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")