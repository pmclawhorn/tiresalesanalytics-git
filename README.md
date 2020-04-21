# simpletire-git

## ABOUT:
A Python Data Analysis and Forecasting Suite. Created by Pierce McLawhorn for SimpleTire as part of OM-597: Advanced Analysis in Supply Chain at The University of Alabama.

## INTRODUCTION:
This project is essentially an interactive data manipulation and forecasting tool. Using pandas, numpy, and other data manipulation packages, a user is first prompted on how they want to partition the data, from a comprehensive table of all orders processed by SimpleTire. For the purposes of this project, the data is sourced from .csv files (totalling ~3.5 million rows), however it may be easily modified to utilize live data, by editing forecast/data_load.py. The user is able to partition the data by:

 (1) Brand
 (2) Subtype
 (3) Line
 (4) BrandWithinSubtype
 (5) Source
 (6) SKU

As well as Warehouse Region, and Warehouses themselves, which are top level selections that may be partitioned further into the numbered subcategories. Data may be aggregated by demand (sales quantity), revenue, or profit, on a daily, weekly, or monthly basis.

The result of any of these aggregation selections is a (most often daily) time series. From there, the user has a choice of forecasting based on a naive Holt-Winters forecast, or more notably a forecast enabled by the Facebook Prophet package, which takes daily data as an input and incorporates weekly and yearly seasonality. See documentation at https://facebook.github.io/prophet/docs/quick_start.html#python-api for more information. The program generates a forecast one year in the future, displays a graph (with a 20% shaded confidence interval), and provides the option to display component trends as well as an MAPE error statistic on procedurally generated iterations of the same forecast x number of days in the future. The user is also presented with an option to generate a .csv report of the final forecast.

## HOW TO RUN:
1. Clone the Entire Repository.
2. Open the project in your preferred Python IDE (I recommend PyCharm, but any IDE will do.)
3. To generate a Prophet forecast, run simpletire/forecast/forecast_prophet.py
  3a. The program flows as follows:
      forecast_prophet.py calls data_preprocess.py, which calls_data.load.
      They are named appropriately for their functionalities, data_load loads the data from the specified .csv files.
      Note: any user in the future wishing to modify the data source should edit this file, either to a different file path
      (Necessary on a different machine), or to a live data source.
      data_preprocess provides all of the data shaping and manipulation functionality. Selection by any of the aforementioned
      categories, optional smoothing, and informative output to aid in input selection is provided here.
  3b. data_helpers.py supports information display, like when trying to select a warehouse, it gives you suggestions based on
  the top warehouses so that you do not go in blind.
 4. Similarly to Step 3, run simpletire/forecast/forecast_winters.py to run a simpler, Holt_Winters forecast based on the  chosen data.
5. In the course of running these programs, you will be prompted (Y/N) if you would like to plot the forecast (in an interactive matplotlib window), plot the forecast seasonality components, plot relevant error statistics, or generate a .csv report of the selected forecast.

  


