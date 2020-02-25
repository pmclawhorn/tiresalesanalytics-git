"""
    This Module Runs fits an ARIMA model (SARIMAX) to time series data fed through
    subtype_result into local var trailer_series. Note that trailer_series may be modified
    to be any time series, so long as it is at least 2 years of weekly data (54 entries)
"""

import warnings
import itertools
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import SimpleExpSmoothing

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
from forecast.trailer_forecast_load import subtype_result_month

# Initialize local variable for time series
trailer_series = subtype_result_month['Trailer']
# print(trailer_series)

fit1 = SimpleExpSmoothing(trailer_series).fit(smoothing_level=0.2,optimized=False)
fcast1 = fit1.forecast(12).rename(r'$\alpha=0.2$')
fit2 = SimpleExpSmoothing(trailer_series).fit(smoothing_level=0.1,optimized=False)
fcast2 = fit2.forecast(12).rename(r'$\alpha=0.1$')
fit3 = SimpleExpSmoothing(trailer_series).fit()
fcast3 = fit3.forecast(12).rename(r'$\alpha=%s$'%fit3.model.params['smoothing_level'])

# print(fcast2)
#print(fit2.fittedvalues)


ax = trailer_series.plot(marker='o', color='black', figsize=(18, 8))
fcast1.plot(marker='o', ax=ax, color='blue', legend=True)
fit1.fittedvalues.plot(marker='o', ax=ax, color='blue')
fcast2.plot(marker='o', ax=ax, color='red', legend=True)

fit2.fittedvalues.plot(marker='o', ax=ax, color='red')
fcast3.plot(marker='o', ax=ax, color='green', legend=True)
fit3.fittedvalues.plot(marker='o', ax=ax, color='green')
plt.title('Trailer Tires - 2020 Sales Forecast - Simple Exponential Smoothing')
plt.show()

deviations2 = abs(fit2.fittedvalues - subtype_result_month['Trailer'])
print(deviations2)
mad2 = sum(deviations2) / len(deviations2)
print("Mean Absolute Deviation (alpha = 0.1):")
print(mad2)

deviations3 = abs(fit3.fittedvalues - subtype_result_month['Trailer'])
# print(deviations2)
mad3 = sum(deviations3) / len(deviations3)
print("Mean Absolute Deviation (alpha = 1.0):")
print(mad3)



"""

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
"""
