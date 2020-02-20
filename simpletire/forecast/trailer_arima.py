"""
    This Module Runs fits an ARIMA model (SARIMAX) to time series data fed through
    subtype_result into local var trailer_series. Note that trailer_series may be modified
    to be any time series, so long as it is at least 2 years of weekly data (54 entries)
"""

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

# Initialize local variable for time series
trailer_series = subtype_result['Trailer']
print(trailer_series)

# Iterable parameters for seasonality, trend, and noise (kindof, see real definition below)
p = d = q = range(0, 2)
pdq = list(itertools.product(p, d, q))
seasonal_pdq = [(x[0], x[1], x[2], 12) for x in
                list(itertools.product(p, d, q))]
aic_list = []

# Run Seasonal ARIMA model: parameters(p, d, q) = (autocorrelation (actual), timedelta, partial correlation)
#              seasonal_pdq parameters(P, D, Q, s) = same but for seasonal component,
# Iterate through a range of parameters, find optimal fit based on AIC (Akaike Information Criteria)
# Note: For a seasonal ARIMA with 2 years of data, a first order model uses timedelta = d = (xt - 12)

for param in pdq:
    try:
        mod = sm.tsa.statespace.SARIMAX(trailer_series, order=param, trend='c')
    except ValueError:
        print('Parameter error in sm.tsa.statespace.SARIMAX: {} {}'.format(param))
        continue

    results = mod.fit(disp=0)
    aic_list.append(results.aic)
    print('ARIMA{} - AIC:{}'.format(param, results.aic))


# Balance of fit and parsimony (AIC) to select the optimal parameter set
print(min(aic_list))

# for trailer 2018-19, suggested best is SARIMAX(0, 1, 1)x(1, 1, 1, 12) - AIC:1251.6785346603538
# or: SARIMAX(2, 2, 1)x(2, 2, 1, 12) - AIC:892.8377404539615

# Fit the model using optimal parameters
mod = sm.tsa.statespace.SARIMAX(trailer_series, order=(1, 1, 1), trend='c',
                                enforce_stationarity=True, enforce_invertibility=True)
results = mod.fit(disp=False)
print(results.summary())
# print(results.summary(tables[1])) # for concise results

results.plot_diagnostics(figsize=(16, 8))
plt.show()

print(np.std(subtype_result['Trailer']))
