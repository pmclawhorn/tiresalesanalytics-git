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

# SUBTYPE ANALYSIS
subtype = dec6_condensed.loc[:, ['ProductID', 'Quantity', 'Cost', 'Unit_Cost', 'Price', 'Unit_Price', 'Ext_Sales', 'Ext_Cost', 'Net_Profit', 'Sub_Type']]
subtype = subtype.sort_values(['Ext_Sales'], ascending=[False])
# Aggregate by Sub_Type
subtype_group = subtype.groupby('Sub_Type').agg({'Net_Profit': ['sum','mean', 'min', 'max']}).reset_index()
# Sort by Quantity (sum)
subtype_group = subtype_group.sort_values([('Net_Profit', 'sum')], ascending=False)

print("\nSUBTYPE AGGREGATE\n")
print(subtype_group)

subtype_group.plot(figsize=(15, 6))
plt.show()

subtype_group.to_csv(r'/Users/piercemclawhorn/om597/simpletire-git/simpletire/reports/subtypeprofit.csv', encoding='utf-8', index=True)