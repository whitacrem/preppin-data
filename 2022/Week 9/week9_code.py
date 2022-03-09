import pandas as pd
import numpy as np

# Import data
original = pd.read_csv('orders.csv', parse_dates=['Order Date', 'Ship Date'])
orders = original
orders = orders[['Row ID', 'Order Date', 'Customer ID']]

# Aggregate the date to the years each customer made an order
# Calculate the year each customer made their first purchase
orders['Year'] = orders['Order Date'].dt.year
orders['First Purchase'] = orders.groupby(['Customer ID'])['Year'].transform('min')

# Scaffold the dataset so that there is a row for each year after a customer's First Purchase, 
# even if they did not make an order
temp_df = orders[['Customer ID','First Purchase']]
temp_df = temp_df.drop_duplicates(subset='Customer ID')

temp_df2 = orders.groupby('Customer ID')['Year'].apply(list)

for key, value in temp_df.iterrows():
    for year in range(value['First Purchase'], 2022):
        if year not in temp_df2[value['Customer ID']]:
            orders = orders.append({'Year': year, 'Customer ID': value['Customer ID'], 'First Purchase': value['First Purchase']}, ignore_index=True)

# Create a field to flag these new rows, making it clear whether a customer placed an order in that year or not
orders['Order?'] = np.where(orders['Order Date'].isna(), 0, 1)

orders = orders.sort_values(by=['Customer ID', 'Year']).reset_index()

# Create a field which flags whether or not a customer placed an order in the previous year
for i in range(1, len(orders)):
    if orders.loc[i-1, 'Order?'] == 0 and orders.loc[i-1, 'Customer ID'] == orders.loc[i, 'Customer ID']:
        orders.loc[i, 'Prev Year?'] = 0
    elif orders.loc[i-1, 'Order?'] == 1 and orders.loc[i-1, 'Customer ID'] == orders.loc[i, 'Customer ID']:
        orders.loc[i, 'Prev Year?'] = 1
    else:
        orders.loc[i, 'Prev Year?'] = np.nan

# Create the Customer Classification using the below definitions:
# New = this is the first year the customer has ordered
# Consistent = the customer ordered this year and last year
# Sleeping = the customer has ordered in the past, but not this year
# Returning = the customer did not order last year, but has ordered this year}

for i in range(0, len(orders)):
    if pd.isna(orders.loc[i, 'Prev Year?']):
        orders.loc[i, 'Customer Classification'] = 'New'
    elif orders.loc[i, 'Prev Year?'] == 1 and orders.loc[i, 'Order?'] == 1:
        orders.loc[i, 'Customer Classification'] = 'Consistent'
    elif orders.loc[i, 'Prev Year?'] == 0 and orders.loc[i, 'Order?'] == 1:
        orders.loc[i, 'Customer Classification'] = 'Returning'
    elif orders.loc[i, 'Prev Year?'] == 1 and orders.loc[i, 'Order?'] == 0:
        orders.loc[i, 'Customer Classification'] = 'Sleeping'

# Calculate the Year on Year difference in the number of customers from each Cohort in each year
orders['YoY Difference'] = orders.groupby(['Year', 'First Purchase'])['Customer ID'].transform('count').diff()

# Join back to the original input data
orders.merge(original, how='left', on='Customer ID')

# Output the data
orders.to_csv('week9_output.csv')