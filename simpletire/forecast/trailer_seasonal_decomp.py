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
from forecast.trailer_forecast_load import subtype_result

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


