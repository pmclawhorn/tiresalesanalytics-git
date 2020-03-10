"""
    This Module Runs fits Winter's Model to time series data fed through
    subtype_result into local var trailer_series. Note that trailer_series may be modified
    to be any time series, so long as it is at least 2 years of weekly data (54 entries)
"""

import warnings

import matplotlib.pyplot as plt
from pandas import DataFrame
from statsmodels.tsa.holtwinters import ExponentialSmoothing

warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')
import pandas as pd
pd.set_option("display.max_columns", 20)
pd.set_option("display.max_rows", 100)
import seaborn as sns; sns.set()
from old.trailer_forecast_load import subtype_result

# Initialize local variable for time series
trailer_series = subtype_result['Trailer']
# print(trailer_series)

fit1 = ExponentialSmoothing(trailer_series, seasonal_periods=52, trend='add', seasonal='add').fit(use_boxcox=True)
fit2 = ExponentialSmoothing(trailer_series, seasonal_periods=52, trend='add', seasonal='mul').fit(use_boxcox=True)
fit3 = ExponentialSmoothing(trailer_series, seasonal_periods=52, trend='add', seasonal='add', damped=True).fit(use_boxcox=True)
fit4 = ExponentialSmoothing(trailer_series, seasonal_periods=52, trend='add', seasonal='mul', damped=True).fit(use_boxcox=True)
results = pd.DataFrame(index=[r"$\alpha$",r"$\beta$",r"$\phi$",r"$\gamma$",r"$l_0$","$b_0$","SSE"])
params = ['smoothing_level', 'smoothing_slope', 'damping_slope', 'smoothing_seasonal', 'initial_level', 'initial_slope']
results["Additive"] = [fit1.params[p] for p in params] + [fit1.sse]
results["Multiplicative"] = [fit2.params[p] for p in params] + [fit2.sse]
results["Additive Dam"] = [fit3.params[p] for p in params] + [fit3.sse]
results["Multiplicative Dam"] = [fit4.params[p] for p in params] + [fit4.sse]

ax = trailer_series.plot(figsize=(24, 8), marker='o', color='black',
                         title="2020 Forecasts: Holt-Winters' Method (monthly data)")
ax.set_ylabel("Trailer Tires Sales (units sold)")
ax.set_xlabel("Year")
# fit1.fittedvalues.plot(ax=ax, style='--', color='red')
# fit2.fittedvalues.plot(ax=ax, style='--', color='green')
fit3.fittedvalues.plot(ax=ax, style='--', color='blue')
# fit4.fittedvalues.plot(ax=ax, style='--', color='blue')


# fit1.forecast(52).rename('Holt-Winters (additive-trend, add-seasonal)').plot(ax=ax, style='--', marker='o', color='red', legend=True)
# fit2.forecast(52).rename('Holt-Winters (additive-trend, mul-seasonal)').plot(ax=ax, style='--', marker='o', color='green', legend=True)
fit3.forecast(52).rename('Holt-Winters (add-damped-trend, add-seasonal)').plot(ax=ax, style='--', marker='o', color='blue', legend=True)
# fit4.forecast(12).rename('Holt-Winters (add-damped-trend, mul-seasonal)').plot(ax=ax, style='--', marker='o', color='blue', legend=True)

# Plot Forecasts
plt.show()
print("Figure 7.6: Forecasting trailer tires sales using Holt-Winters method with both additive and multiplicative seasonality.")

# Plot Diagnostics
print(results)
print(fit3.fittedvalues)
print(fit3.forecast(52))
trailer_2020forecast = fit3.forecast(52)
trailer_2020forecast.to_csv(r'/Users/piercemclawhorn/om597/simpletire-git/simpletire/reports/trailer_2020Wforecast.csv', encoding='utf-8', index=True)
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
residuals = DataFrame(fit3.resid)
residuals.plot(kind='kde')
plt.title('Holt/Winters Fit Residual Error Density Plot: add-trend, add-seasonal (the blue one)', fontsize='large')
plt.show()


