"""
    Author: Pierce M. McLawhorn
    This Module fits an exponential smoothing model to time series data generated in the imported module
    data_preprocess.
"""
import warnings
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import SimpleExpSmoothing

warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')
import pandas as pd
pd.set_option("display.max_columns", 20)
pd.set_option("display.max_rows", 100)
import seaborn as sns; sns.set()
from old.trailer_forecast_load import subtype_result_month

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