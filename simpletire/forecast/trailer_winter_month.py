"""
    This Module Runs fits an ARIMA model (SARIMAX) to time series data fed through
    subtype_result into local var trailer_series. Note that trailer_series may be modified
    to be any time series, so long as it is at least 2 years of weekly data (54 entries)
"""

import warnings
import itertools
import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame
from statsmodels.tsa.holtwinters import SimpleExpSmoothing, Holt, ExponentialSmoothing

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

fit1 = ExponentialSmoothing(trailer_series, seasonal_periods=12, trend='add', seasonal='add').fit(use_boxcox=True)
fit2 = ExponentialSmoothing(trailer_series, seasonal_periods=12, trend='add', seasonal='mul').fit(use_boxcox=True)
fit3 = ExponentialSmoothing(trailer_series, seasonal_periods=12, trend='add', seasonal='add', damped=True).fit(use_boxcox=True)
fit4 = ExponentialSmoothing(trailer_series, seasonal_periods=12, trend='add', seasonal='mul', damped=True).fit(use_boxcox=True)
results = pd.DataFrame(index=[r"$\alpha$",r"$\beta$",r"$\phi$",r"$\gamma$",r"$l_0$","$b_0$","SSE"])
params = ['smoothing_level', 'smoothing_slope', 'damping_slope', 'smoothing_seasonal', 'initial_level', 'initial_slope']
results["Additive"] = [fit1.params[p] for p in params] + [fit1.sse]
results["Multiplicative"] = [fit2.params[p] for p in params] + [fit2.sse]
results["Additive Dam"] = [fit3.params[p] for p in params] + [fit3.sse]
results["Multiplicative Dam"] = [fit4.params[p] for p in params] + [fit4.sse]

ax = trailer_series.plot(figsize=(16, 8), marker='o', color='black', title="2020 Forecasts: Holt-Winters' Method (monthly data)")
ax.set_ylabel("Trailer Tires Sales (units sold)")
ax.set_xlabel("Year")
fit1.fittedvalues.plot(ax=ax, style='--', color='red')
fit2.fittedvalues.plot(ax=ax, style='--', color='green')
fit3.fittedvalues.plot(ax=ax, style='--', color='blue')
# fit4.fittedvalues.plot(ax=ax, style='--', color='blue')


fit1.forecast(12).rename('Holt-Winters (additive-trend, add-seasonal)').plot(ax=ax, style='--', marker='o', color='red', legend=True)
fit2.forecast(12).rename('Holt-Winters (additive-trend, mul-seasonal)').plot(ax=ax, style='--', marker='o', color='green', legend=True)
fit3.forecast(12).rename('Holt-Winters (add-damped-trend, add-seasonal)').plot(ax=ax, style='--', marker='o', color='blue', legend=True)
# fit4.forecast(12).rename('Holt-Winters (add-damped-trend, mul-seasonal)').plot(ax=ax, style='--', marker='o', color='blue', legend=True)


trailer_2020forecast = fit3.forecast(52)
trailer_2020forecast.to_csv(r'/Users/piercemclawhorn/om597/simpletire-git/simpletire/reports/trailer_2020Mforecast.csv', encoding='utf-8', index=True)

# Plot Forecasts
plt.show()
print("Figure 7.6: Forecasting trailer tires sales using Holt-Winters method with both additive and multiplicative seasonality.")

# Plot Diagnostics
# print(results)
# results.plot_diagnostics(figsize=(16, 8))

# Plot levels, slopes, trends, and seasonal components
#states1 = pd.DataFrame(np.c_[fit1.level, fit1.slope, fit1.season], columns=['level','slope','seasonal'], index=trailer_series.index)
#states2 = pd.DataFrame(np.c_[fit2.level, fit2.slope, fit2.season], columns=['level','slope','seasonal'], index=trailer_series.index)
#fig, [[ax1, ax4],[ax2, ax5], [ax3, ax6]] = plt.subplots(3, 2, figsize=(16,8))
#states1[['level']].plot(ax=ax1)
#states1[['slope']].plot(ax=ax2)
#states1[['seasonal']].plot(ax=ax3)
#states2[['level']].plot(ax=ax4)
#states2[['slope']].plot(ax=ax5)
#states2[['seasonal']].plot(ax=ax6)
#plt.show()

# Plot Residuals about 0
residuals = DataFrame(fit1.resid)
residuals.plot(kind='kde')
plt.title('Holt/Winters Fit Residual Error Density Plot', fontsize='large')
plt.show()







"""
fit1 = SimpleExpSmoothing(trailer_series).fit()
fcast1 = fit1.forecast(9).rename("SES")
fit2 = Holt(trailer_series).fit()
fcast2 = fit2.forecast(9).rename("Holt's")
fit3 = Holt(trailer_series, exponential=True).fit()
fcast3 = fit3.forecast(9).rename("Exponential")
fit4 = Holt(trailer_series, damped=True).fit(damping_slope=0.98)
fcast4 = fit4.forecast(9).rename("Additive Damped")
fit5 = Holt(trailer_series, exponential=True, damped=True).fit()
fcast5 = fit5.forecast(9).rename("Multiplicative Damped")

ax = trailer_series.plot(color="black", marker="o", figsize=(16,8))
fcast1.plot(ax=ax, color='red', legend=True)
fcast2.plot(ax=ax, color='green', legend=True)
fcast3.plot(ax=ax, color='blue', legend=True)
fcast4.plot(ax=ax, color='cyan', legend=True)
fcast5.plot(ax=ax, color='magenta', legend=True)
ax.set_ylabel('Trailer Tire Sales - Quantity Sold')
plt.title('Simple Exponential Smoothing and Various Holt\'s Methods')
plt.show()
"""

"""
fit1 = Holt(trailer_series).fit(smoothing_level=0.8, smoothing_slope=0.2, optimized=False)
fcast1 = fit1.forecast(12).rename("Holt's linear trend")
fit2 = Holt(trailer_series, exponential=True).fit(smoothing_level=0.8, smoothing_slope=0.2, optimized=False)
fcast2 = fit2.forecast(12).rename("Exponential trend")
fit3 = Holt(trailer_series, damped=True).fit(smoothing_level=0.8, smoothing_slope=0.2)
fcast3 = fit3.forecast(12).rename("Additive damped trend")

ax = trailer_series.plot(color="black", marker="o", figsize=(18,8))
fit1.fittedvalues.plot(ax=ax, color='blue')
fcast1.plot(ax=ax, color='blue', marker="o", legend=True)
fit2.fittedvalues.plot(ax=ax, color='red')
fcast2.plot(ax=ax, color='red', marker="o", legend=True)
fit3.fittedvalues.plot(ax=ax, color='green')
fcast3.plot(ax=ax, color='green', marker="o", legend=True)
plt.title('Holt\'s Method: Exponential, Linear, and Additive Damped Trends')
plt.show()
"""