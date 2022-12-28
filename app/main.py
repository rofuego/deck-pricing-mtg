import pandas as pd

page = pd.read_html('https://www.mtggoldfish.com/archetype/pioneer-mono-white-humans#paper')

df = page[0]
df.columns = ['#', 'Card', 'Mana', 'Tprice']
df = df.loc[:, ["#","Card","Tprice"]]

search = ["Spells ", "Lands ", "Cards Total", "Planeswalkers ", "Artifacts ", "Enchantments "]
mask = df.apply(lambda x: x.str.contains("|".join(search))).any(axis=1)
df = df.drop(df[mask].index)
df = df.reset_index(drop=True)

mask = df['#'].str.contains('Sideboard')
stop_index = df[mask].index[0]

main = df.iloc[:stop_index].copy()

""" sb = df.iloc[stop_index + 1:].copy() """

main.loc[:, 'Tprice'] = main['Tprice'].str.slice(2)
main['Tprice'] = pd.to_numeric(main['Tprice'])
main['#'] = pd.to_numeric(main['#'], downcast='integer')


def calc_uprice(row):
    return row['Tprice'] / row['#']

main = main.assign(Uprice=main.apply(calc_uprice, axis=1))

data = pd.read_csv('data.csv')
data['#'] = pd.to_numeric(data['#'], downcast='integer')

new = pd.DataFrame(columns=['#Use', '#Have', 'Card', 'Bprice'])

for index, row in main.iterrows():
    match = data.loc[data['Card'] == row['Card']]
    if not match.empty:
        row_index = match.index[0]
        price = row['Uprice'] *  (row["#"] - data.at[row_index, "#"])
        if price <= 0:
            price = 0

        new_row = pd.Series({'#Use': row["#"], '#Have': data.at[row_index, "#"], 'Card': row['Card'], 'Bprice': price})
        new = pd.concat([new, new_row.to_frame().T], ignore_index=True)
    else:
        new_row = pd.Series({'#Use': row["#"], '#Have': 0, 'Card': row['Card'], 'Bprice': row['Tprice']})
        new = pd.concat([new, new_row.to_frame().T], ignore_index=True)


print(data)
print(new)
print('total: ' + str(new['Bprice'].sum()))