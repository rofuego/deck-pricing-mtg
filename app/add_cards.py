import pandas as pd

data = pd.read_csv('data.csv')
data['Quantity'] = data['Quantity'].astype('int32')

add_cards = pd.read_csv('new_cards.csv')
add_cards['Quantity'] = add_cards['Quantity'].astype('int32')

merged_data = pd.concat([data, add_cards], ignore_index=True, sort=False)
merged_data = merged_data.groupby(['Card'], as_index=False).sum()
merged_data = merged_data.sort_values(by='Card')

print(merged_data)

merged_data.to_csv('data.csv', index=False, header=['Card', 'Quantity'])
