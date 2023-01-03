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


list = [df_lands, df_creatures, df_spells]
eval = pd.DataFrame(
    columns=['Quantity to buy', 'Card'])

data = pd.read_csv('data.csv')
data['Quantity'] = pd.to_numeric(data['Quantity'], downcast='integer')

for df in list:
    eval = pd.DataFrame(
        columns=['Quantity to buy', 'Card'])
    for index, row in df.iterrows():
        match_data = data.loc[data['Card'] == row['Card']]
        if not match_data.empty:
            row_index_data = match_data.index[0]
            if data.at[row_index_data, "Quantity"] < row["# Played"]:
                quantity = row["# Played"] - \
                    data.at[row_index_data, "Quantity"]
                new_row = pd.Series(
                    {'Quantity to buy': quantity, 'Card': row['Card']})
                eval = pd.concat(
                    [eval, new_row.to_frame().T], ignore_index=True)
        else:
            new_row = pd.Series(
                {'Quantity to buy': row["# Played"], 'Card': row['Card']})
            eval = pd.concat(
                [eval, new_row.to_frame().T], ignore_index=True)
    print(eval)
