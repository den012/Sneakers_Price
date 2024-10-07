import json
import re

#create a list with celebrities that worked with shoe companies
celebs = ["Sabrina", "Cardi B", "Pharrell Williams", "Kendrick Lamar", "Fenty", "Michael Jordan", "Travis Scott",
          "Donald Glover", "Bad Bunny", "Selena Gomez", "Big Sean", "Vivienne Westwood", "Serena Williams", "Gigi Hadid",
          "Kanye West", "One Star", "Justin Timberlake", "Rihanna", "Lil Nas X", "A$AP Rocky", "J Balvin", "Post Malone",
          "Nigo", "Tinker Hatfield", "Teyana Taylor", "Odell Beckham Jr.", "Dame D.O.L.L.A.", "Migos", "Fabolous",
          "Kylie Jenner", "Bella Hadid", "Puma's LaMelo Ball", "Beyoncé", "Snoop Dogg", "Drake", "J Cole", "Ariana Grande",
          "Tyler the Creator", "Kendall Jenner", "Dwayne Johnson", "Kobe Bryant", "G-Dragon", "James Harden", "Kaitlyn Dever",
          "Tinashe", "Fresh Foam"]

#check if there is a collaboration in the sneaker name
def extract_collaboration(sneaker_name):
    colabs = []
    if ' x ' in sneaker_name:
        match = re.match(r'^(.*) [xX] (.*)', sneaker_name, re.IGNORECASE)
        if match:
            colabs.append(match.group(1).strip())
    elif 'Kobe' in sneaker_name:
        colabs.append('Kobe Bryant')
    else:
        for celeb in celebs:
            if celeb[:6].lower() in sneaker_name.lower():
                colabs.append(celeb)
    return ', '.join(colabs)

#create a column fro collaborations
def add_collaboration(input_file = 'sneakers_data.json', output_file = 'sneaker_data_v1.json'):
    count = 0
    with open(input_file, 'r', encoding = 'utf-8') as file:
        sneakers_data = json.load(file)

    for sneaker in sneakers_data:
        name = sneaker.get('sneaker_name')
        if name:
            collaboration = extract_collaboration(name)
            if collaboration:
                count += 1
                print(collaboration)
                sneaker['collaboration'] = 1
                sneaker['collaboration_name'] = collaboration
            else:
                sneaker['collaboration'] = 0
                sneaker['collaboration_name'] = 'No'
    with open(output_file, 'w', encoding = 'utf-8') as file:
        json.dump(sneakers_data, file, ensure_ascii = False, indent= 4)
    return count, sneakers_data

