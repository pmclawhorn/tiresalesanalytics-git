"""
    This Module Runs fits a seasonal ARIMA model (SARIMAX) to time series data fed through
    subtype_result into local var trailer_series. Note that trailer_series may be modified
    to be any time series, so long as it is at least 2 years of weekly data with a seasonality
    component.
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
# trailer_series = subtype_result['Trailer'].resample('MS').mean()
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
"""
for param in pdq:
    for param_seasonal in seasonal_pdq:
        try:
            mod = sm.tsa.statespace.SARIMAX(trailer_series, order=param, seasonal_order=param_seasonal, trend='c',
                                            enforce_stationarity=True, enforce_invertibility=True)
        except ValueError:
            print('Parameter error in sm.tsa.statespace.SARIMAX: {} {}'.format(param, param_seasonal))
            continue

        results = mod.fit(disp=0)

        aic_list.append(results.aic)
        # print(aic_list)
        # print(results.aic)

        print('SARIMAX{}x{} - AIC:{}'.format(param, param_seasonal, results.aic))

        # if results.aic < min(aic_list):
        #    print("Current Best Fit is: SARIMAX{}x{}12 - AIC:{}".format(param, param_seasonal, results.aic))

"""

# Balance of fit and parsimony (AIC) to select the optimal parameter set
# print(min(aic_list))

# for trailer 2018-19, suggested best is SARIMAX(0, 1, 1)x(1, 1, 1, 12) - AIC:1251.6785346603538
# or: SARIMAX(2, 2, 1)x(2, 2, 1, 12) - AIC:892.8377404539615

mod = sm.tsa.statespace.SARIMAX(trailer_series, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12), trend='c',
                                 concentrate_scale=True)

results = mod.fit(disp=False)
print(results.summary())
# print(results.summary(tables[1])) # for concise results

# results.plot_diagnostics(figsize=(16, 8))
# plt.title('Sarimax-1, Monthly Average Sample, Quarterly Fit')
# plt.show()


pred = results.get_prediction(start=pd.to_datetime('2019-01-07'), dynamic=True)
pred_ci = pred.conf_int()
ax = trailer_series.plot(label='observed')
pred.predicted_mean.plot(ax=ax, label='One-step ahead Forecast', alpha=.7, figsize=(18, 6))

"""
ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.2)
"""

trailer_forecasted = pred.predicted_mean
trailer_truth = trailer_series
mse = ((trailer_forecasted - trailer_truth) ** 2).mean()
print('The Mean Squared Error is {}'.format(round(mse, 2)))
print('The Root Mean Squared Error is {}'.format(round(np.sqrt(mse), 2)))

plt.text(42, 5300, "Root Mean Square Error=%.3f" % np.sqrt(mse))
ax.set_xlabel('Date')
ax.set_ylabel('Trailer Tire Sales')
plt.title('Trailer Tires - SARIMAX Forecast', fontsize='large')

plt.legend()
plt.show()


"""
pred_uc = results.get_forecast(steps=100)
pred_ci = pred_uc.conf_int()
ax = trailer_series.plot(label='observed', figsize=(14, 7))
pred_uc.predicted_mean.plot(ax=ax, label='Forecast')
ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.25)
ax.set_xlabel('Date')
ax.set_ylabel('Tire Sales')
"""

#plt.legend()
#plt.show()












