import json
import re

#create a list with celebrities that worked with shoe companies
celebs = ['Supreme', 'Prada', 'Migos', 'Gucci', 'Vetements', 'Maison Margiela', 'Kobe Bryant', 'Cardi B', 'Stüssy',
 'Balenciaga', 'Vivienne Westwood', 'Stone Island', 'Odell Beckham Jr.', "Puma's LaMelo Ball", 'Off-White', 'Versace',
 'One Star', 'Fenty', 'J Balvin', 'Comme des Garçons', 'Marcelo Burlon', 'Chanel', 'Selena Gomez', 'Nigo', 'Fendi',
 'G-Dragon', 'Cactus Jack', 'Bad Bunny', 'Travis Scott', 'Bella Hadid', 'Gigi Hadid', 'Fresh Foam', 'Kanye West',
 'Teyana Taylor', 'Valentino', 'Dolce & Gabbana', 'Michael Jordan', 'Big Sean', 'Yves Saint Laurent', 'Givenchy',
 'Kaitlyn Dever', 'Beyoncé', 'Rick Owens', 'A$AP Rocky', 'Ariana Grande', 'Donald Glover', 'Tinker Hatfield',
 'Justin Timberlake', 'Balmain', 'Sabrina', 'Yeezy', 'Dame D.O.L.L.A.', 'Rihanna', 'Kylie Jenner', 'Burberry',
 'Serena Williams', 'Dior', 'Kendall Jenner', 'Dwayne Johnson', 'Alexander McQueen', 'J Cole', 'Fabolous', 'Lil Nas X',
 'Hermès', 'Tyler the Creator', 'Bape', 'Cactus Plant Flea Market', 'Kendrick Lamar', 'Union', 'Kenzo', 'Drake',
 'Louis Vuitton', 'Kith', 'A-Cold-Wall*', 'Snoop Dogg', 'Moncler', 'Fear of God', 'James Harden', 'Pharrell Williams',
 'Post Malone', 'Acne Studios', 'Thom Browne', 'Tinashe', 'Kaws', 'Kiko Kostadinov', 'Jerry Lorenzo', 'Karl Lagerfeld',
 'Kith x Coca-Cola', 'Kith x Looney Tunes', 'Kith x Power Rangers', 'Kith x Rugrats', 'Kith x Versace', 'Kith x Vogue', 'Kith',
'KD', 'Kyrie', 'LeBron', 'PG', 'Kobe', 'Hello Kitty', 'SpongeBob SquarePants', 'Patrick Star', 'Sandy Cheeks', 'Mr. Krabs',
'Ambush', 'JFS', 'F.C.R.B', 'Union LA', 'GOODENOUGH', 'mita', 'Saquon Barkley', 'Livestrong', 'Kevin Bradley', 'CNCPTS',
'Undercover',
]

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

