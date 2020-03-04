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
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from fbprophet.diagnostics import performance_metrics
from fbprophet.plot import plot_cross_validation_metric
from scipy.stats import boxcox
from fbprophet.diagnostics import cross_validation
import plotly.offline as py
py.init_notebook_mode()

pdtabulate = lambda df: tabulate(df, headers='keys', tablefmt='psql')
# warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')
pd.set_option("display.max_columns", 20)
pd.set_option("display.max_rows", 100)
sns.set()


# time_series is an instance of PreProcessData.data (or one of its subclasses),
#  frequency is the number of periods in a season (e.g. 52 for a year),
#  lookahead is the number of periods in the future you want to forecast.
class ProphetForecast:
    def __init__(self, time_series, frequency, lookahead, name):
        self.time_series = time_series
        self.frequency = frequency
        self.lookahead = lookahead
        self.name = name
        self.m = Prophet()

    def generate(self):
        # Add holidays as a component to the forecast
        self.m.add_country_holidays('UnitedStates')

        self.time_series['ds'] = self.time_series.index
        self.time_series['y'] = self.time_series.iloc[:, 0]

#        bc = str(input("Would you like to perform a box-cox transformation on the data to remove noise? (Y/N)"))
#        if bc == "Y":
#            self.time_series['y'] = boxcox(self.time_series['y'], lmbda=0.0)

        print(self.time_series)
        self.m.fit(df=self.time_series)
        future = self.m.make_future_dataframe(periods=int(self.lookahead))
        forecast = self.m.predict(future)

        fig = self.m.plot(forecast, xlabel="Time", ylabel="Tire Sales (units sold)")
        ax = fig.gca()
        ax.set_title(label="2020 Prophet Forecast - " + self.name, fontsize=24)
        plt.show()

        fig2 = self.m.plot_components(forecast)
        ax2 = fig2.gca()
        # ax2.set_title(label="2020 Prophet Forecast - " + self.name + " - Trend Components", fontsize=24)
        plt.show()

    def plot_(self):
        # Plot Forecasts
        pass

    def plot_residuals(self):
        print("CROSS VALIDATION RESULTS")
        df_cv = cross_validation(self.m, initial='365 days', period='365 days', horizon='365 days')
        print(pdtabulate(df_cv))

        print("PERFORMANCE METRICS")
        df_p = performance_metrics(df_cv)
        print(pdtabulate(df_p))
        # Mean absolute percentage error
        fig3 = plot_cross_validation_metric(df_cv, metric='mape')
        ax3 = fig3.gca()
        plt.show()

    def plot_components(self):
        pass

    def output_csv(self):
        df_cv = cross_validation(self.m, initial='365 days', period='365 days', horizon='365 days')
        df_cv.head()
        # df_cv.to_csv(r'/Users/piercemclawhorn/om597/simpletire-git/simpletire/reports/branddemand.csv',
        #                    encoding='utf-8', index=True)


def main():
    obj = preprocess_data()
    print("For your chosen data, there are " + str(obj.frequency) + " periods in a season (365 means daily data)")
    lookahead = str(input("How may periods in the future would you like to forecast? For Prophet, 365 means one year."))

#    forecast = ProphetForecast(obj.data, obj.frequency, lookahead, obj.name)
    # hard code 365
    forecast = ProphetForecast(obj.data, obj.frequency, 365, obj.name)

    print("generating forecast...")
    forecast.generate()

#    do_print = str(input("Would you like to plot the forecast? (Y/N)"))
#    if do_print == "Y":
#        forecast.plot_()

    do_print = str(input("Would you like to plot the residuals?? (Y/N)"))
    if do_print == "Y":
        forecast.plot_residuals()

    do_output = str(input("Would you like to generate a csv of the forecast? (Y/N)"))
    if do_output == "Y":
        forecast.output_csv()
        print(".csv file generated. File may be found in simpletire-git/reports")


if __name__ == "__main__":
    main()
