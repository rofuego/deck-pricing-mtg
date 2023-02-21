import pandas as pd
import requests
from bs4 import BeautifulSoup

url = 'https://www.mtggoldfish.com/archetype/modern-yawgmoth-9bd3dc9a-1da1-442e-9b88-6ef2a027e80b#paper'
page = pd.read_html(url)
response = requests.get(url)
bs = BeautifulSoup(response.text, "html.parser")

deck_title = bs.find(class_="title").text.split("\n")[1]
deck_format = bs.find(class_="deck-container-information").text.split("\n")[1]

df = page[0]
df.columns = ['Quantity', 'Card', 'Mana', 'TotalPrice']
df = df.loc[:, ["Quantity", "Card", "TotalPrice"]]

search = ["Spells ", "Lands ", "Cards Total",
          "Planeswalkers ", "Artifacts ", "Enchantments "]
mask = df.apply(lambda x: x.str.contains("|".join(search))).any(axis=1)
df = df.drop(df[mask].index)
df = df.reset_index(drop=True)

mask = df['Quantity'].str.contains('Sideboard')
stop_index = df[mask].index[0]

main = df.iloc[:stop_index].copy()
main = main.reset_index(drop=True)
sb = df.iloc[stop_index + 1:].copy()
sb = sb.reset_index(drop=True)

main.loc[:, 'TotalPrice'] = main['TotalPrice'].str.slice(2)
main['TotalPrice'] = pd.to_numeric(main['TotalPrice'])
main['Quantity'] = pd.to_numeric(main['Quantity'], downcast='integer')

sb.loc[:, 'TotalPrice'] = sb['TotalPrice'].str.slice(2)
sb['TotalPrice'] = pd.to_numeric(sb['TotalPrice'])
sb['Quantity'] = pd.to_numeric(sb['Quantity'], downcast='integer')


def calc_uprice(row):
    return row['TotalPrice'] / row['Quantity']


main = main.assign(SinglePrice=main.apply(calc_uprice, axis=1))
sb = sb.assign(SinglePrice=sb.apply(calc_uprice, axis=1))

data = pd.read_csv('data.csv')
data['Quantity'] = pd.to_numeric(data['Quantity'], downcast='integer')

""" eval = pd.DataFrame(
    columns=['Card', 'QMain', 'QSb', 'QData', 'SinglePrice', 'TotalPrice'])
 """

eval_main = pd.DataFrame(
    columns=['QuantityInMain', 'QuantityHave', 'Card', 'BuyingPrice'])

eval_sb = pd.DataFrame(
    columns=['QuantityInSb', 'QuantityHave', 'QuantityInMain', 'Card', 'BuyingPrice'])

for index, row in main.iterrows():
    match_data = data.loc[data['Card'] == row['Card']]
    if not match_data.empty:
        row_index_data = match_data.index[0]
        if (row["Quantity"] <= data.at[row_index_data, "Quantity"]):
            price = 0
        else:
            price = row['SinglePrice'] * \
                (row["Quantity"] - data.at[row_index_data, "Quantity"])
        new_row = pd.Series(
            {'QuantityInMain': row["Quantity"], 'QuantityHave': data.at[row_index_data, "Quantity"], 'Card': row['Card'], 'BuyingPrice': price})
        eval_main = pd.concat(
            [eval_main, new_row.to_frame().T], ignore_index=True)
    else:
        new_row = pd.Series(
            {'QuantityInMain': row["Quantity"], 'QuantityHave': 0, 'Card': row['Card'], 'BuyingPrice': row['TotalPrice']})
        eval_main = pd.concat(
            [eval_main, new_row.to_frame().T], ignore_index=True)

for index, row in sb.iterrows():
    match_data = data.loc[data['Card'] == row['Card']]
    if not match_data.empty:
        match_main = main.loc[main['Card'] == row['Card']]
        if not match_main.empty:
            row_index_data = match_data.index[0]
            row_index_main = match_main.index[0]
            if data.at[row_index_data, "Quantity"] >= 4:
                price = 0
                new_row = pd.Series({'QuantityInSb': row["Quantity"], 'QuantityHave': data.at[row_index_data, "Quantity"],
                                     'QuantityInMain': main.at[row_index_main, "Quantity"], 'Card': row['Card'], 'BuyingPrice': price})
            else:
                price = row['SinglePrice'] * ((row["Quantity"] + main.at[row_index_main,
                                              "Quantity"]) - data.at[row_index_data, "Quantity"])
                new_row = pd.Series({'QuantityInSb': row["Quantity"], 'QuantityHave': data.at[row_index_data, "Quantity"],
                                     'QuantityInMain': main.at[row_index_main, "Quantity"], 'Card': row['Card'], 'BuyingPrice': price})
            eval_sb = pd.concat(
                [eval_sb, new_row.to_frame().T], ignore_index=True)
        else:
            row_index_data = match_data.index[0]
            price = row['SinglePrice'] * \
                (row["Quantity"] - data.at[row_index_data, "Quantity"])
            if price <= 0:
                price = 0
            new_row = pd.Series(
                {'QuantityInSb': row["Quantity"], 'QuantityHave': data.at[row_index_data, "Quantity"], 'QuantityInMain': 0, 'Card': row['Card'], 'BuyingPrice': price})
            eval_sb = pd.concat(
                [eval_sb, new_row.to_frame().T], ignore_index=True)
    else:
        match_main = main.loc[main['Card'] == row['Card']]
        if not match_main.empty:
            row_index_main = match_main.index[0]
            quantity_in_main = main.at[row_index_main, "Quantity"]
        else:
            quantity_in_main = 0
        new_row = pd.Series({'QuantityInSb': row["Quantity"], 'QuantityHave': 0,
                            'QuantityInMain': quantity_in_main, 'Card': row['Card'], 'BuyingPrice': row['TotalPrice']})
        eval_sb = pd.concat(
            [eval_sb, new_row.to_frame().T], ignore_index=True)

print("Deck: " + deck_title)
print(deck_format)
print("***** MainDeck *****")
print(eval_main.to_string(index=False))
print("***** Sb *****")
print(eval_sb.to_string(index=False))
print(f"Subtotal pricing main deck: {eval_main['BuyingPrice'].sum():.2f}")
print(f"Subtotal pricing sb: {eval_sb['BuyingPrice'].sum():.2f}")
print(
    f"Total pricing complete deck: {eval_sb['BuyingPrice'].sum() + eval_main['BuyingPrice'].sum():.2f}")
