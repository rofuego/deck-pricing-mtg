import csv

csv_writer = csv.writer(open('data.csv', 'w', newline=''))
rows = [
    ['#', 'Card'],
    [4, 'Goblin Guide'],
    ['4', 'Monastery Swiftspear'],
    ['4', 'Lava Spike'],
    ['4', 'Lightning Bolt'],
    ['4', 'Boros Charm'],
    ['4', 'Lightning Helix'],
    ['4', 'Searing Blaze'],
    ['4', 'Skullcrack'],
    ['4', 'Rift Bolt'],
    ['4', 'Skewer the Critics'],
    ['4', 'Arid Mesa'],
    ['4', 'Bloodstained Mire'],
    ['4', 'Fiery Islet'],
    ['4', 'Inspiring Vantage'],
    ['4', 'Mountain'],
    ['4', 'Sacred Foundry'],
    ['4', 'Scalding Tarn'],
    ['4', 'Sunbaked Canyon'],
    ['4', 'Wooded Foothills'],
    ['4', "Thalia's Lieutenant"],
    ['4', 'Thalia, Guardian of Thraben'],
    ['4', 'Brutal Cathar'],
    ['4', 'Skyclave Apparition'],
    ['4', 'Castle Ardenvale'],
    ['4', 'Eiganjo, Seat of the Empire'],
    ['4', 'Mutavault'],
    ['20', 'Plains'],
]

csv_writer.writerows(rows)