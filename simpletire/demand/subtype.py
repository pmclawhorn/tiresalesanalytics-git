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

# FIXME if you are not Pierce then this path will need to be changed (lazy i will fix later)
jan26_raw = pd.read_csv(r'/Users/piercemclawhorn/om597/data/OrderItemMargin-01-26.csv')
jan26 = jan26_raw.loc[:, ['Source', 'Created', 'ProductID', 'Quantity', 'Cost', 'Unit_Cost', 'Price', 'Unit_Price', 'Ext_Sales', 'Ext_Cost', 'Brand', 'Sub_Type', 'Line', 'Admin_Ship_Est']]
jan26 = jan26.loc[~(jan26['Source'] == "BulkOrders")]  # Remove bulk orders
# jan26 = jan26.loc[jan26['Sub_Type'].isin(['ATV/UTV', 'Commercial', 'Farm', 'Golf', 'Lawn & Garden', 'Industrial',  'Passenger', 'Light Truck', 'Trailer'])]

# Compute Columns for profit, include shipping cost
jan26['Net_Profit'] = ((jan26['Ext_Sales'] - jan26['Ext_Cost']) - jan26['Admin_Ship_Est'])
subtype_demand = jan26.loc[:, ['Created', 'Quantity', 'Sub_Type']]

# Aggregate Data to Weekly
subtype_demand['Created'] = pd.to_datetime(subtype_demand['Created'])
subtype_demand = subtype_demand.groupby('Sub_Type').resample('W-Mon', on='Created', label='left', closed='left').sum().reset_index().sort_values(by='Created')

# Fill data where a subtype may have been ordered 0 times in a week
subtype_result = subtype_demand.groupby(['Created', 'Sub_Type'])['Quantity'].sum().reset_index().pivot(index='Created', columns='Sub_Type', values='Quantity').resample('W-Mon', label='left', closed='left').asfreq().fillna(0)

# This represents Sales by Week for each subtype
# Plot Subtype
print(subtype_result)
subtype_result.plot(figsize=(15, 6))
plt.show()

# Plot Variance
print("VARIANCE:\n")
print(subtype_result.var())
#subvar = subtype_result.var()
#subvar.plot(figsize=(15, 6))
#plt.show()

# Plot StdDev
print("STANDARD DEVIATION:\n")
print(np.std(subtype_result))

subtype_result.to_csv(r'/Users/piercemclawhorn/om597/simpletire-git/simpletire/reports/subtypedemand.csv', encoding='utf-8', index=True)
subtype_result.var().to_csv(r'/Users/piercemclawhorn/om597/simpletire-git/simpletire/reports/subtypedemandvar.csv', encoding='utf-8', index=True)
np.std(subtype_result).to_csv(r'/Users/piercemclawhorn/om597/simpletire-git/simpletire/reports/subtypedemandstddev.csv', encoding='utf-8', index=True)