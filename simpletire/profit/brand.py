import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import h5py
import numpy as np

# Hierarchy is Brand -> Subtype -> Line

# Filter the Data to Necessary Columns, Remove Extraneous Data

# FIXME if you are not Pierce then this path will need to be changed (lazy i will fix later)
jan26_raw = pd.read_csv(r'/Users/piercemclawhorn/om597/simpletire-git/simpletire/OrderItemMargin-01-26.csv')
jan26 = jan26_raw.loc[:, ['Source', 'Created', 'ProductID', 'Quantity', 'Cost', 'Unit_Cost', 'Price', 'Unit_Price', 'Ext_Sales', 'Ext_Cost', 'Brand', 'Sub_Type', 'Line', 'Admin_Ship_Est']]
jan26 = jan26.loc[~(jan26['Source'] == "BulkOrders")]  # Remove bulk orders

# Compute Columns for profit, include shipping cost
jan26['Net_Profit'] = ((jan26['Ext_Sales'] - jan26['Ext_Cost']) - jan26['Admin_Ship_Est'])

n = 10

# Hierarchy: Brand -> Subtype -> Line -> SKU

# BRAND ANALYSIS
brand = jan26.loc[:, ['ProductID', 'Quantity', 'Cost', 'Unit_Cost', 'Price', 'Unit_Price', 'Ext_Sales', 'Ext_Cost', 'Net_Profit', 'Brand']]
brand = brand.sort_values(['Net_Profit'], ascending=[False])
# Aggregate by Brand
brand_group = brand.groupby('Brand').agg({'Net_Profit': ['sum','mean', 'min', 'max']}).reset_index()
# Sort by Profit (sum)
brand_group = brand_group.sort_values([('Net_Profit', 'sum')], ascending=False)

brand_group_top = brand_group.head(int(len(brand_group) * (n/100)))
brand_group_bottom = brand_group.tail(int(len(brand_group) * (n/100)))

print("\nBRAND AGGREGATE\n")
print("Top 10% of Brands by Profit\n")
print(brand_group_top)
# print("Bottom 10% of Brands by Profit\n")
# print(brand_group_bottom)

