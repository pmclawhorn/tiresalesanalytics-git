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
import matplotlib.patches as mpatches
from fbprophet.diagnostics import performance_metrics
from fbprophet.plot import plot_cross_validation_metric
from scipy.stats import boxcox
from fbprophet.diagnostics import cross_validation
import plotly.offline as py
py.init_notebook_mode()

pdtabulate = lambda df: tabulate(df, headers='keys', tablefmt='psql')
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
        self.m = Prophet(yearly_seasonality=True)
        self.out_table = time_series  # placeholder for real forecast

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

        # Plot the Components
        plot_bool = str(input("Would you like to plot the forecast?? (Y/N)"))
        if plot_bool == "Y":
            fig = self.m.plot(forecast, figsize=(13.33, 7.5))  # TODO: color='#fe6223')
            ax = fig.gca()
            ax.set_title(label="2020 Prophet Forecast - " + self.name, fontsize=24)
            ax.set_xlabel(xlabel="Month", fontsize=16)
            ax.set_ylabel(ylabel="Tire Sales (units sold)", fontsize=16)
            ax.set_autoscale_on(b=True)
            # ax.subplots_adjust(top=0.93)
            plt.show()

        # Plot the Components
        plot_bool = str(input("Would you like to plot the forecast components?? (Y/N)"))
        if plot_bool == "Y":
            fig2 = self.m.plot_components(forecast)  # , figsize=(10.5, 6))
            ax2 = fig2.gca()
            # FIXME title is on bottom for some reason
            #  ax2.set_title(label="2020 Prophet Forecast - " + self.name + " - Trend Components", fontsize=14)
            plt.show()

    def plot_(self):
        # Plot Forecasts
        pass

    def plot_residuals(self):

        print("CROSS VALIDATION RESULTS")
        df_cv = cross_validation(self.m, initial='365.25 days', period='365.25 days', horizon='365.25 days')
       # df_cv = cross_validation(self.m, initial='180 days', period='180 days', horizon='180 days')
        self.out_table = df_cv
        print(pdtabulate(df_cv))

        print("PERFORMANCE METRICS")
        df_p = performance_metrics(df_cv)
        print(pdtabulate(df_p))

        # Mean absolute percentage error
        fig3 = plot_cross_validation_metric(df_cv, metric='mape', figsize=(11, 6))
        ax3 = fig3.gca()
        blue_patch = mpatches.Patch(color='#5F86BC', label='Accuracy ~= ((1 - MAPE) * 100) %')
        plt.legend(handles=[blue_patch])
        # ax3.legend("Accuracy ~= ((1 - MAPE) * 100) %")
        ax3.set_title(label="Prophet Forecast - Mean Absolute Percentage Error - " + self.name, fontsize=24)
        ax3.set_xlabel(xlabel="Forecast Horizon (days)", fontsize=16)
        ax3.set_ylabel(ylabel="MAPE", fontsize=16)
        ax3.set_ylim([0.0, 0.8])
        plt.show()

    def plot_components(self):
        pass

    def output_csv(self):
        self.out_table.to_csv(r'/Users/piercemclawhorn/om597/simpletire-git/simpletire/reports/prophet-' + self.name +
                              '.csv', encoding='utf-8', index=True)


def main():
    obj = preprocess_data()
    print("For your chosen data, there are " + str(obj.frequency) + " periods in a season (365 means daily data)")
    lookahead = str(input("How may periods in the future would you like to forecast? For Prophet, 365 means one year."))

#    forecast = ProphetForecast(obj.data, obj.frequency, lookahead, obj.name)
    # hard code 365
    forecast = ProphetForecast(obj.data, obj.frequency, lookahead, obj.name)

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
