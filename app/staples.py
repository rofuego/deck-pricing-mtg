import pandas as pd
from math import ceil

url_creatures = 'https://www.mtggoldfish.com/format-staples/modern/full/creatures'
url_lands = "https://www.mtggoldfish.com/format-staples/modern/full/lands"
url_spells = "https://www.mtggoldfish.com/format-staples/modern/full/spells"

page_lands = pd.read_html(url_lands)
page_creatures = pd.read_html(url_creatures)
page_spells = pd.read_html(url_spells)

df_creatures = page_creatures[0]
df_lands = page_lands[0]
df_spells = page_spells[0]

df_lands.columns = ['Quantity', 'Card', "% of Decks", '# Played']
df_creatures.columns = ['Quantity', 'Card', 'Cost', "% of Decks", '# Played']
df_spells.columns = ['Quantity', 'Card', 'Cost', "% of Decks", '# Played']

df_lands['# Played'] = df_lands['# Played'].apply(ceil)
df_creatures['# Played'] = df_creatures['# Played'].apply(ceil)
df_spells['# Played'] = df_spells['# Played'].apply(ceil)

print(df_lands)
