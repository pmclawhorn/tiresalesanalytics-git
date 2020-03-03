import warnings
import matplotlib.pyplot as plt
from pandas import DataFrame

warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')
import pandas as pd
pd.set_option("display.max_columns", 20)
pd.set_option("display.max_rows", 100)
import seaborn as sns; sns.set()
from old.trailer_forecast_load import subtype_result
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
from math import sqrt

# Initialize local variable for time series
trailer_series = subtype_result['Trailer']
# trailer_series = subtype_result_day['Trailer']

# trailer_series = subtype_result['Trailer'].resample('MS').sum()

X = trailer_series.values
train, test = X[0:-52], X[-52:]
history = [x for x in train]
# print(history)
predictions = list()

for t in range(len(test)):
    # fit model
    model = ARIMA(history, order=(4, 1, 0))
    model_fit = model.fit(disp=False, trend='c')
    # single step forecast
    yhat = model_fit.forecast()[0]
    predictions.append(yhat)
    history.append(test[t])

# evaluate forecasts
rmse = sqrt(mean_squared_error(test, predictions))
print('Test RMSE: %.3f' % rmse)

print(model_fit.summary())
# model_fit.plot_diagnostics(figsize=(16, 8))

# Plot The Forecast
plt.plot(test, color='#ff6832')
plt.plot(predictions, color='red')
plt.rcParams['figure.figsize'] = 18, 8
# plt.rcParams['figure.facecolor'] = 'white'
# plt.rcParams['axes.prop_cycle'] = matplotlib.cycler(color=["#ff6832", "#000000"])
plt.xlabel('Week Number (2019)')
plt.ylabel('Quantity Sold')
plt.title('Trailer Tires -- ARIMA Forward Walk Model: Predicted vs. Actual', fontsize='large')
plt.text(42, 5300, "Root Mean Square Error=%.3f" % rmse)
plt.xticks(range(0, 52))
plt.grid(True)
plt.legend(["Actual", "Predicted"])
# plt.yticks(np.arange(0, 11, 1))
plt.show()

residuals = DataFrame(model_fit.resid)

#residuals.plot()
#plt.title('AIRMA Fit Residual Line Error Plot', fontsize = 'large')
#plt.show()

residuals.plot(kind='kde')
plt.title('AIRMA Fit Residual Error Density Plot', fontsize = 'large')
plt.show()










