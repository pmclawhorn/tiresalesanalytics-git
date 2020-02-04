import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import h5py
import numpy as np

pd.set_option("display.max_columns", 999)
pd.set_option("display.max_rows", 999)

dec6_raw = pd.read_csv("OrderItemMargin.csv")
#print(dec6_raw.head())

dec6_condensed = dec6_raw.loc[:, ['Source', 'Created', 'ProductID', 'Quantity', 'Cost', 'Unit_Cost', 'Price', 'Unit_Price', 'Ext_Sales', 'Ext_Cost', 'Brand', 'Sub_Type', 'Line', 'Admin_Ship_Est']]
dec6_condensed['Net_Profit'] = dec6_condensed['Ext_Sales'] - dec6_condensed['Ext_Cost']
#print(dec6_condensed.head())

n = 10

# Hierarchy: Brand -> Subtype -> Line -> SKU
# LINE ANALYSIS
line = dec6_condensed.loc[:, ['ProductID', 'Quantity', 'Cost', 'Unit_Cost', 'Price', 'Unit_Price', 'Ext_Sales', 'Ext_Cost', 'Net_Profit', 'Line']]
line = line.sort_values(['Ext_Sales'], ascending=[False])
# Aggregate by Brand
line_group = line.groupby('Line').agg({'Net_Profit': ['sum','mean', 'min', 'max']}).reset_index()
# Sort by Profit (sum)
line_group = line_group.sort_values([('Net_Profit', 'sum')], ascending=False)

line_group_top = line_group.head(int(len(line_group) * (n/100)))
line_group_bottom = line_group.tail(int(len(line_group) * (n/100)))

print("\nLINE AGGREGATE\n")
print("Top 10% of Lines by Total Profit\n")
print(line_group_top)
print("Bottom 10% of Lines by Total Profit\n")
print(line_group_bottom)