"""
    Author: Pierce M. McLawhorn
    This Module fits a Holt/Winters (triple exponential smoothing) model to time series data generated in the
    imported module data_preprocess.
"""

import matplotlib.pyplot as plt
import warnings
import pandas as pd
import seaborn as sns
import statistics
import math
from tabulate import tabulate
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from forecast.data_preprocess import PreProcessData
from forecast.data_preprocess import preprocess_data

pdtabulate = lambda df: tabulate(df, headers='keys', tablefmt='psql')
# warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')
pd.set_option("display.max_columns", 20)
pd.set_option("display.max_rows", 100)
sns.set()


# time_series is an instance of PreProcessData.data (or one of its subclasses),
#  frequency is the number of periods in a season (e.g. 52 for a year),
#  lookahead is the number of periods in the future you want to forecast.
class WintersForecast:
    def __init__(self, time_series, frequency, lookahead, name):
        self.time_series = time_series
        self.frequency = frequency
        self.lookahead = lookahead
        self.name = name
        self.fit1 = ExponentialSmoothing(self.time_series, seasonal_periods=52, trend='add', seasonal='add').fit(
            use_boxcox=True)
        self.fit2 = ExponentialSmoothing(self.time_series, seasonal_periods=52, trend='add', seasonal='mul').fit(
            use_boxcox=True)
        self.fit3 = ExponentialSmoothing(self.time_series, seasonal_periods=52, trend='add', seasonal='add',
                                         damped=True).fit(use_boxcox=True)
        self.fit4 = ExponentialSmoothing(self.time_series, seasonal_periods=52, trend='add', seasonal='mul',
                                         damped=True).fit(use_boxcox=True)

    def generate(self):

        results = pd.DataFrame(index=[r"smoothing level - alpha", r"smoothing slope - beta", r"damping slope - phi",
                                      r"seasonal smoothing - gamma", r"initial level", "initial slope", "SSE"])
                                      # "MSE","Log Likelihood"])
        params = ['smoothing_level', 'smoothing_slope', 'damping_slope', 'smoothing_seasonal', 'initial_level',
                  'initial_slope']
        results["Additive"] = [self.fit1.params[p] for p in params] + [self.fit1.sse] # + math.sqrt([self.fit1.sse])
        results["Multiplicative"] = [self.fit2.params[p] for p in params] + [self.fit2.sse]
        results["Additive Dam"] = [self.fit3.params[p] for p in params] + [self.fit3.sse]
        results["Multiplicative Dam"] = [self.fit4.params[p] for p in params] + [self.fit4.sse]
        # results2 = self.fit3.params_formatted
        print(pdtabulate(results))
        #  print(pdtabulate(results2))

    def plot_(self):
        ax = self.time_series.plot(figsize=(18, 10), marker='o', color='black')
        ax.set_title(label="2020 Forecast: Holt-Winters Method - " + self.name, fontsize=24)
        ax.set_ylabel("Tire Sales (units sold)")
        ax.set_xlabel(xlabel="Week")
        self.fit1.fittedvalues.plot(ax=ax, style='--', color='red')
        self.fit2.fittedvalues.plot(ax=ax, style='--', color='green')
        self.fit3.fittedvalues.plot(ax=ax, style='--', color='blue')
        self.fit4.fittedvalues.plot(ax=ax, style='--', color='orange')

        self.fit1.forecast(52).rename('Holt-Winters (additive-trend, add-seasonal)').plot(ax=ax, style='--', marker='o',
                                                                                          color='red', legend=True)
        self.fit2.forecast(52).rename('Holt-Winters (additive-trend, mul-seasonal)').plot(ax=ax, style='--', marker='o',
                                                                                          color='green', legend=True)
        self.fit4.forecast(52).rename('Holt-Winters (add-damped-trend, mul-seasonal)').plot(ax=ax, style='--',
                                                                                            marker='o', color='orange',
                                                                                            legend=True)
        self.fit3.forecast(52).rename('Holt-Winters (add-damped-trend, add-seasonal)').plot(ax=ax, style='--',
                                                                                            marker='o',
                                                                                            color='blue', legend=True)
        # this selects rows
        #df.loc[['Niko', 'Penelope']]
        # Plot Forecasts
        plt.show()

    def plot_residuals(self):
        self.time_series.resid.plt.scatter()
        plt.show()

    def output_csv(self):
        pass


def main():
    obj = preprocess_data()
    print("For your chosen data, there are " + str(obj.frequency) + " periods in a season (e.g. 52 means weekly data)")
    lookahead = str(input("How may periods in the future would you like to forecast?"))

    forecast = WintersForecast(obj.data, obj.frequency, lookahead, obj.name)

    print("generating forecast...")
    forecast.generate()

    do_print = str(input("Would you like to plot the forecast? (Y/N)"))
    if do_print == "Y":
        forecast.plot_()

    do_print = str(input("Would you like to plot the residuals?? (Y/N)"))
    if do_print == "Y":
        forecast.plot_residuals()

    do_output = str(input("Would you like to generate a csv of the forecast? (Y/N)"))
    if do_output == "Y":
        forecast.output_csv()
        print(".csv file generated. File may be found in simpletire-git/reports")


if __name__ == "__main__":
    main()
