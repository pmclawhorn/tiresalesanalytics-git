import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

# Filter the Data to Necessary Columns, Remove Extraneous Data
# TODO if you are not Pierce then you will need to change the file path
jan26_raw = pd.read_csv(r'/Users/piercemclawhorn/om597/data/OrderItemMargin-01-26.csv')
jan26 = jan26_raw.loc[:, ['Source', 'Created', 'ProductID', 'Quantity', 'Cost', 'Unit_Cost', 'Price',
                          'Unit_Price', 'Ext_Sales', 'Ext_Cost', 'Brand', 'Sub_Type', 'Line', 'Admin_Ship_Est'
                          ]]
jan26 = jan26.loc[~(jan26['Source'] == "BulkOrders")]  # Remove bulk orders
jan26 = jan26.loc[(jan26['Source'] == "Amazon")]
jan26 = jan26.loc[jan26['Brand'].isin(['Hankook', 'Crosswind', 'Bridgestone', 'Goodyear', 'Toyo', 'Cooper', 'Achilles'])]

# Compute Column for profit, include shipping cost
jan26['Net_Profit'] = ((jan26['Ext_Sales'] - jan26['Ext_Cost']) - jan26['Admin_Ship_Est'])


# Brand Analysis - Aggregate by Brand and Sort by Profit (sum)
brand = jan26.loc[:, ['ProductID', 'Quantity', 'Cost', 'Unit_Cost', 'Price', 'Unit_Price', 'Ext_Sales',
                      'Ext_Cost', 'Net_Profit', 'Brand'
                      ]]
brand = brand.sort_values(['Net_Profit'], ascending=[False])
brand_group = brand.groupby('Brand').agg({'Net_Profit': ['sum']}).reset_index()
brand_group = brand_group.sort_values([('Net_Profit', 'sum')], ascending=False)
print(brand_group)

"""
# Get the top n% of brands
n = 10
brand_group_top = brand_group.head(int(len(brand_group) * (n/100)))
# brand_group_bottom = brand_group.tail(int(len(brand_group) * (n/100)))
print("\nBRAND AGGREGATE\n")
print("Top 10% of Brands by Profit\n")
print(brand_group_top)
# print(brand_group_bottom)
"""

# Output file to simpletire/reports/
brand_group.to_csv(r'/Users/piercemclawhorn/om597/simpletire-git/simpletire/reports/amznhankookprofit.csv', encoding='utf-8', index=True)

#brand_group.plot(figsize =(15, 6))
#plt.show()

# Plot TODO
#brand_plot = pd.DataFrame()
#brand_plot['Profit'] = brand_group_top.loc[:, ('Net_Profit', 'sum')]
#brand_plot['Brand'] = brand_group_top.loc[:, ['Brand']]

#print(brand_plot)
#brand_plot.plot('Brand', 'Profit', figsize=(15, 6))
#plt.show()
# print("Bottom 10% of Brands by Profit\n")
# print(brand_group_bottom)

jan26 = jan26_raw.loc[:, ['Source', 'Created', 'ProductID', 'Quantity', 'Cost', 'Unit_Cost', 'Price',
                          'Unit_Price', 'Ext_Sales', 'Ext_Cost', 'Brand', 'Sub_Type', 'Line', 'Admin_Ship_Est'
                          ]]
jan26 = jan26.loc[~(jan26['Source'] == "BulkOrders")]  # Remove bulk orders
jan26 = jan26.loc[(jan26['Brand'] == "Hankook")]
jan26 = jan26.loc[jan26['Source'].isin(['Amazon', 'WalMart', 'SimpleWebsite', 'eBay'])]

# Compute Column for profit, include shipping cost
jan26['Net_Profit'] = ((jan26['Ext_Sales'] - jan26['Ext_Cost']) - jan26['Admin_Ship_Est'])


# Brand Analysis - Aggregate by Brand and Sort by Profit (sum)
source = jan26.loc[:, ['ProductID', 'Quantity', 'Cost', 'Unit_Cost', 'Price', 'Unit_Price', 'Ext_Sales',
                      'Ext_Cost', 'Net_Profit', 'Brand', 'Source'
                      ]]
source = source.sort_values(['Net_Profit'], ascending=[False])
source_group = source.groupby('Source').agg({'Net_Profit': ['sum']}).reset_index()
source_group = source_group.sort_values([('Net_Profit', 'sum')], ascending=False)
source_group = source_group.reset_index()
print(source_group)

source_group.to_csv(r'/Users/piercemclawhorn/om597/simpletire-git/simpletire/reports/hankookamznprofit.csv', encoding='utf-8', index=True)