import pandas as pd

data = pd.read_csv('data.csv')
data['Quantity'] = pd.to_numeric(data['Quantity'], downcast='integer')

add_cards = pd.read_csv('database/add_cards.csv')
add_cards['Quantity'] = pd.to_numeric(data['Quantity'], downcast='integer')

for index, row in add_cards.iterrows():
    match = data.loc[data['Card'] == row["Card"]]
    if not match.empty:
        row_index_data = match.index[0]
        data.at[row_index_data, "Quantity"] = row["Quantity"] + \
            data.at[row_index_data, "Quantity"]
    else:
        new_row = pd.Series({'Quantity': row['Quantity'], 'Card': row["Card"]})
        data = pd.concat([data, new_row.to_frame().T], ignore_index=True)

data = data.sort_values(by='Card', inplace=False)
print(data)

data.to_csv('data.csv', mode='w', index=False, header=['Quantity', 'Card'])
