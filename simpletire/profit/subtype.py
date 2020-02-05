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


# Compute Column for profit, include shipping cost
jan26['Net_Profit'] = ((jan26['Ext_Sales'] - jan26['Ext_Cost']) - jan26['Admin_Ship_Est'])


# SubType Analysis - Aggregate by SubType and Sort by Profit (sum)
subtype = jan26.loc[:, ['ProductID', 'Quantity', 'Cost', 'Unit_Cost', 'Price', 'Unit_Price', 'Ext_Sales',
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