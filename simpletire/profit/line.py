import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import h5py
import numpy as np

# Filter the Data to Necessary Columns, Remove Extraneous Data
# TODO if you are not Pierce then you will need to change the file path
jan26_raw = pd.read_csv(r'/Users/piercemclawhorn/om597/data/OrderItemMargin-01-26.csv')
jan26 = jan26_raw.loc[:, ['Source', 'Created', 'ProductID', 'Quantity', 'Cost', 'Unit_Cost', 'Price',
                          'Unit_Price', 'Ext_Sales', 'Ext_Cost', 'Brand', 'Sub_Type', 'Line', 'Admin_Ship_Est'
                          ]]
jan26 = jan26.loc[~(jan26['Source'] == "BulkOrders")]  # Remove bulk orders


# Compute Column for profit, include shipping cost
jan26['Net_Profit'] = ((jan26['Ext_Sales'] - jan26['Ext_Cost']) - jan26['Admin_Ship_Est'])
jan26['Line'] = jan26['Brand'] + " " + jan26['Line']


# LINE ANALYSIS
line = jan26.loc[:, ['ProductID', 'Quantity', 'Cost', 'Unit_Cost', 'Price', 'Unit_Price', 'Ext_Sales', 'Ext_Cost', 'Net_Profit', 'Line']]
line = line.sort_values(['Ext_Sales'], ascending=[False])
# Aggregate by Brand
line_group = line.groupby('Line').agg({'Net_Profit': ['sum', 'mean']}).reset_index()
# Sort by Profit (sum)
line_group = line_group.sort_values([('Net_Profit', 'sum')], ascending=False)


n = 1
line_group_top = line_group.head(int(len(line_group) * (n/100)))
line_group_bottom = line_group.tail(int(len(line_group) * (n/100)))

print("\nLINE AGGREGATE\n")
print("Top 1% of Lines by Total Profit\n")
print(line_group_top)
#print("Bottom 10% of Lines by Total Profit\n")
print(line_group_bottom)

# Sort by net profit then just grab the head(50) or whatever

#line_group_top.plot(figsize=(15, 6))
#plt.show()

line_group_top.to_csv(r'/Users/piercemclawhorn/om597/simpletire-git/simpletire/reports/lineprofit.csv', encoding='utf-8', index=True)