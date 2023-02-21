import pandas as pd
from math import ceil

url_creatures = 'https://www.mtggoldfish.com/format-staples/modern/full/creatures'
url_spells = "https://www.mtggoldfish.com/format-staples/modern/full/spells"

page_creatures = pd.read_html(url_creatures)
page_spells = pd.read_html(url_spells)

df_creatures = page_creatures[0]
df_spells = page_spells[0]

df_creatures.columns = ['Quantity', 'Card', 'Cost', "% of Decks", '# Played']
df_spells.columns = ['Quantity', 'Card', 'Cost', "% of Decks", '# Played']

df_creatures['# Played'] = df_creatures['# Played'].apply(ceil)
df_spells['# Played'] = df_spells['# Played'].apply(ceil)


df_list = [df_creatures, df_spells]
df_final = pd.DataFrame(
    columns=['Buy', 'Card'])

data = pd.read_csv('data.csv')
data['Quantity'] = pd.to_numeric(data['Quantity'], downcast='integer')

for df in df_list:
    df_final = pd.DataFrame(
        columns=['Buy', 'Card'])
    for index, row in df.iterrows():
        match_data = data.loc[data['Card'] == row['Card']]
        if not match_data.empty:
            row_index_data = match_data.index[0]
            if data.at[row_index_data, "Quantity"] < row["# Played"]:
                quantity = row["# Played"] - \
                    data.at[row_index_data, "Quantity"]
                new_row = pd.Series(
                    {'Buy': quantity, 'Card': row['Card']})
                df_final = pd.concat(
                    [df_final, new_row.to_frame().T], ignore_index=True)
        else:
            new_row = pd.Series(
                {'Buy': row["# Played"], 'Card': row['Card']})
            df_final = pd.concat(
                [df_final, new_row.to_frame().T], ignore_index=True)
    print("*****")
    print(df_final.to_string(index=False))
