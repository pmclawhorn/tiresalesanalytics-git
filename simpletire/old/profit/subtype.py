import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

# Filter the Data to Necessary Columns, Remove Extraneous Data
# TODO if you are not Pierce then you will need to change the file path
jan26_raw = pd.read_csv(r'/Users/piercemclawhorn/om597/data/OrderItemMargin-01-26.csv')
raw_2018 = pd.read_csv(r'/Users/piercemclawhorn/om597/data/OrderItemMargin_2018.csv')
feb12_raw = pd.concat([jan26_raw, raw_2018], axis=0, sort=False)

feb12 = feb12_raw.loc[:, ['Source', 'Created', 'ProductID', 'Quantity', 'Cost', 'Unit_Cost', 'Price', 'Unit_Price', 'Ext_Sales', 'Ext_Cost', 'Brand', 'Sub_Type', 'Line', 'Admin_Ship_Est']]
feb12 = feb12.loc[~(feb12['Source'] == "BulkOrders")]

# Compute Column for profit, include shipping cost
feb12['Net_Profit'] = ((feb12['Ext_Sales'] - feb12['Ext_Cost']) - feb12['Admin_Ship_Est'])


# SubType Analysis - Aggregate by SubType and Sort by Profit (sum)
subtype = feb12.loc[:, ['ProductID', 'Quantity', 'Cost', 'Unit_Cost', 'Price', 'Unit_Price', 'Ext_Sales',
                      'Ext_Cost', 'Net_Profit', 'Sub_Type'
                    ]]
subtype = subtype.sort_values(['Ext_Sales'], ascending=[False])
subtype_group = subtype.groupby('Sub_Type').agg({'Net_Profit': ['sum','mean']}).reset_index()
subtype_group = subtype_group.sort_values([('Net_Profit', 'sum')], ascending=False)


print("\nSUBTYPE AGGREGATE\n")
print(subtype_group)

#subtype_group.plot(figsize=(15, 6))
#plt.show()

subtype_group.to_csv(r'/Users/piercemclawhorn/om597/simpletire-git/simpletire/reports/subtypeprofit.csv', encoding='utf-8', index=True)