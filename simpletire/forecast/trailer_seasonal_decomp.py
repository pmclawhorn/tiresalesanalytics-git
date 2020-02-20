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
from trailer_forecast_load import subtype_result

'''
# Hierarchy is Brand -> Subtype -> Line

# Filter the Data to Necessary Columns, Remove Extraneous Data
jan26_raw = pd.read_csv(r'/Users/piercemclawhorn/om597/data/OrderItemMargin-01-26.csv')
raw_2018 = pd.read_csv(r'/Users/piercemclawhorn/om597/data/OrderItemMargin_2018.csv')
feb12_raw = pd.concat([jan26_raw, raw_2018], axis=0, sort=False)
feb12 = feb12_raw.loc[:, ['Source', 'Created', 'ProductID', 'Quantity', 'Cost', 'Unit_Cost', 'Price', 'Unit_Price',
                          'Ext_Sales', 'Ext_Cost', 'Brand', 'Sub_Type', 'Line', 'Admin_Ship_Est']]
feb12 = feb12.loc[~(feb12['Source'] == "BulkOrders")]
feb12 = feb12.loc[(feb12['Sub_Type'] == "Trailer")]  # Select only the Trailer Sub_Type

# Compute Columns for profit, include shipping cost
feb12['Net_Profit'] = ((feb12['Ext_Sales'] - feb12['Ext_Cost']) - feb12['Admin_Ship_Est'])
subtype_demand = feb12.loc[:, ['Created', 'Quantity', 'Sub_Type']]

# Aggregate Data to Weekly
subtype_demand['Created'] = pd.to_datetime(subtype_demand['Created'])
subtype_demand = subtype_demand.groupby('Sub_Type').resample('W-Mon', on='Created', label='left', closed='left')\
                                        .sum().reset_index().sort_values(by='Created')

# Fill data where a subtype may have been ordered 0 times in a week
subtype_result = subtype_demand.groupby(['Created', 'Sub_Type'])['Quantity'].sum().reset_index().\
    pivot(index='Created', columns='Sub_Type', values='Quantity').resample('W-Mon', label='left', closed='left').\
    asfreq().fillna(0)
# subtype_result.to_csv(r'/Users/piercemclawhorn/om597/simpletire-git/simpletire/reports/trailerdemand.csv',\
#                      encoding='utf-8', index=True)
'''
# This represents Sales by Week for each subtype
# Plot Subtype
# print(subtype_result)
# subtype_result.plot(figsize=(30, 6))
    # fig, ax = plt.subplots()
    # ax.plot('Created', 'Trailer', data=subtype_result)
# plt.xlabel('Month')
# plt.ylabel('Quantity Sold')
# plt.title('Number of Trailer Tires Sold by Week: 2018-2019')
    # plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
    # plt.xticks(np.arange(0, 500, 6000))
    # plt.yticks(np.arange(0, 11, 1))
# plt.grid(True)
# plt.show()

# Plot Variance
print("VARIANCE:\n")
print(subtype_result.var())
# subvar = subtype_result.var()
# subvar.plot(figsize = (15, 6))
# plt.show()

# Plot StdDev
print("STANDARD DEVIATION:\n")
print(np.std(subtype_result))

# FORECASTING

# subtype_series = subtype_result.reset_index()
subtype_series = subtype_result
# subtype_series = subtype_series.loc[:, ['Passenger']]
print(subtype_series)

# SEASONAL DECOMPOSITION USING MOVING AVERAGES

# plt.rcParams['lines.linewidth'] = 3.0
plt.rcParams['figure.figsize'] = 18, 8
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.prop_cycle'] = matplotlib.cycler(color=["#ff6832", "#000000", "0.7"])
decomposition = sm.tsa.seasonal_decompose(subtype_series, model='multiplicative')
# print(decomposition)
figure = decomposition.plot()
fig = plt.figure()
# ax = plt.gca()
plt.title('Trailer Tires - Seasonal Decomposition by Quantity Sold - 01/01/18-01-26-20')
plt.grid(True)
plt.show()


