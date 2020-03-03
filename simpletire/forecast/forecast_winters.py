"""
    Author: Pierce M. McLawhorn
    This Module fits a Holt/Winters (triple exponential smoothing) model to time series data generated in the
    imported module data_preprocess.
"""

import matplotlib.pyplot as plt
import warnings
import pandas as pd
import seaborn as sns
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


# time_series is an instance of PreProcessData (or one of its subclasses),
#  frequency is the number of periods in a season (e.g. 52 for a year),
#  lookahead is the number of periods in the future you want to forecast.
class WintersForecast:
    def __init__(self, time_series, frequency, lookahead):
        self.time_series = time_series
        self.frequency = frequency
        self.lookahead = lookahead
        self.fit1 = 0
        self.fit2 = 0
        self.fit3 = 0
        self.fit4 = 0

    def generate(self):
        self.fit1 = ExponentialSmoothing(self.time_series, seasonal_periods=52, trend='add', seasonal='add').fit(
            use_boxcox=True)
        self.fit2 = ExponentialSmoothing(self.time_series, seasonal_periods=52, trend='add', seasonal='mul').fit(
            use_boxcox=True)
        self.fit3 = ExponentialSmoothing(self.time_series, seasonal_periods=52, trend='add', seasonal='add', damped=True)\
            .fit(use_boxcox=True)
        self.fit4 = ExponentialSmoothing(self.time_series, seasonal_periods=52, trend='add', seasonal='mul', damped=True)\
            .fit(use_boxcox=True)
        results = pd.DataFrame(index=[r"$\alpha$", r"$\beta$", r"$\phi$", r"$\gamma$", r"$l_0$", "$b_0$", "SSE"])
        params = ['smoothing_level', 'smoothing_slope', 'damping_slope', 'smoothing_seasonal', 'initial_level',
                  'initial_slope']
        results["Additive"] = [self.fit1.params[p] for p in params] + [self.fit1.sse]
        results["Multiplicative"] = [self.fit2.params[p] for p in params] + [self.fit2.sse]
        results["Additive Dam"] = [self.fit3.params[p] for p in params] + [self.fit3.sse]
        results["Multiplicative Dam"] = [self.fit4.params[p] for p in params] + [self.fit4.sse]
        print(results)

    def plot_(self):
        ax = self.time_series.plot(figsize=(24, 8), marker='o', color='black',
                                 title="2020 Forecasts: Holt-Winters' Method (monthly data)")
        ax.set_ylabel("Trailer Tires Sales (units sold)")
        ax.set_xlabel("Year")
        self.fit1.fittedvalues.plot(ax=ax, style='--', color='red')
        self.fit2.fittedvalues.plot(ax=ax, style='--', color='green')
        self.fit3.fittedvalues.plot(ax=ax, style='--', color='blue')
        self.fit4.fittedvalues.plot(ax=ax, style='--', color='orange')

        self.fit1.forecast(52).rename('Holt-Winters (additive-trend, add-seasonal)').plot(ax=ax, style='--', marker='o',
                                                                                          color='red', legend=True)
        self.fit2.forecast(52).rename('Holt-Winters (additive-trend, mul-seasonal)').plot(ax=ax, style='--', marker='o',
                                                                                          color='green', legend=True)
        self.fit3.forecast(52).rename('Holt-Winters (add-damped-trend, add-seasonal)').plot(ax=ax, style='--',
                                                                                            marker='o',
                                                                                            color='blue', legend=True)
        self.fit4.forecast(52).rename('Holt-Winters (add-damped-trend, mul-seasonal)').plot(ax=ax, style='--',
                                                                                            marker='o', color='orange',
                                                                                            legend=True)
        # Plot Forecasts
        plt.show()

    def plot_residuals(self):
        pass

    def output_csv(self):
        pass


def main():
    obj = preprocess_data()
    print("For your chosen data, there are " + str(obj.frequency) + " periods in a season (e.g. 52 means weekly data)")
    lookahead = str(input("How may periods in the future would you like to forecast?"))

    forecast = WintersForecast(obj.data, obj.frequency, lookahead)

    print("generating forecast...")
    forecast.generate()

    do_print = str(input("Would you like to plot the forecast? (Y/N)"))
    if do_print == "Y":
        forecast.plot_()

    do_output = str(input("Would you like to generate a csv of the forecast? (Y/N)"))
    if do_output == "Y":
        forecast.output_csv()
        print(".csv file generated. File may be found in simpletire-git/reports")


if __name__ == "__main__":
    main()
