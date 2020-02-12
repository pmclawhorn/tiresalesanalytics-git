import warnings
import itertools
import numpy as np
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')
import pandas as pd
pd.set_option("display.max_columns", 20)
pd.set_option("display.max_rows", 100)
import statsmodels.api as sm
import matplotlib
from pylab import rcParams
import seaborn as sns; sns.set()

# Hierarchy is Brand -> Subtype -> Line
# Filter the Data to Necessary Columns, Remove Extraneous Data
# if you are not Pierce then this path will need to be changed (lazy i will fix later)
jan26_raw = pd.read_csv(r'/Users/piercemclawhorn/om597/data/OrderItemMargin-01-26.csv')
raw_2018 = pd.read_csv(r'/Users/piercemclawhorn/om597/data/OrderItemMargin_2018.csv')
feb12_raw = pd.concat([jan26_raw, raw_2018], axis=0, sort=False)

feb12 = feb12_raw.loc[:, ['Source', 'Created', 'ProductID', 'Quantity', 'Cost', 'Unit_Cost', 'Price', 'Unit_Price', 'Ext_Sales', 'Ext_Cost', 'Brand', 'Sub_Type', 'Line', 'Admin_Ship_Est']]
feb12 = feb12.loc[~(feb12['Source'] == "BulkOrders")]  # Remove bulk orders

# Compute Columns for profit, include shipping cost
feb12['Net_Profit'] = ((feb12['Ext_Sales'] - feb12['Ext_Cost']) - feb12['Admin_Ship_Est'])
line_demand = feb12.loc[:, ['Created', 'Quantity', 'Line']]

# Get the vector for top 1% of lines
n = 1
line = feb12.loc[:, ['ProductID', 'Quantity', 'Cost', 'Unit_Cost', 'Price', 'Unit_Price', 'Ext_Sales', 'Ext_Cost', 'Net_Profit', 'Line']]
line = line.sort_values(['Ext_Sales'], ascending=[False])
line_group = line.groupby('Line').agg({'Net_Profit': ['sum', 'mean']}).reset_index()
line_group = line_group.sort_values([('Net_Profit', 'sum')], ascending=False)
line_group_top = line_group.head(int(len(line_group) * (n/100)))
top_lines = line_group_top['Line']
line_demand = line_demand.loc[line_demand['Line'].isin(top_lines)]

# Aggregate Data to Weekly
line_demand['Created'] = pd.to_datetime(line_demand['Created'])
line_demand = line_demand.groupby('Line').resample('W-Mon', on='Created', label='left', closed='left').sum().reset_index().sort_values(by='Created')

# Fill data where a subtype may have been ordered 0 times in a week
line_result = line_demand.groupby(['Created', 'Line'])['Quantity'].sum().reset_index().pivot(index='Created', columns='Line', values='Quantity').resample('W-Mon', label='left', closed='left').asfreq().fillna(0)

# This represents Sales by Week for each subtype
# Plot Line
print(line_result)
line_result.plot(figsize=(15, 6))
plt.show()

# Plot Variance
print("VARIANCE:\n")
print(line_result.var())
#subvar = subtype_result.var()
#subvar.plot(figsize=(15, 6))
#plt.show()

# Plot StdDev
print("STANDARD DEVIATION:\n")
print(np.std(line_result))

line_result.to_csv(r'/Users/piercemclawhorn/om597/simpletire-git/simpletire/reports/linedemand.csv', encoding='utf-8', index=True)
line_result.var().to_csv(r'/Users/piercemclawhorn/om597/simpletire-git/simpletire/reports/linedemandvar.csv', encoding='utf-8', index=True)
np.std(line_result).to_csv(r'/Users/piercemclawhorn/om597/simpletire-git/simpletire/reports/linedemandstddev.csv', encoding='utf-8', index=True)