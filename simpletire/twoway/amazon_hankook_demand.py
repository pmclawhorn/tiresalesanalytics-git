import pandas as pd
pd.set_option("display.max_columns", 20)
pd.set_option("display.max_rows", 100)
import statsmodels.api as sm
import matplotlib
from pylab import rcParams
import seaborn as sns; sns.set()


# Filter the Data to Necessary Columns, Remove Extraneous Data
# FIXME if you are not Pierce then this path will need to be changed (lazy i will fix later)
jan26_raw = pd.read_csv(r'/Users/piercemclawhorn/om597/data/OrderItemMargin-01-26.csv')
jan26 = jan26_raw.loc[:, ['Source', 'Created', 'ProductID', 'Quantity', 'Cost', 'Unit_Cost', 'Price', 'Unit_Price',
                          'Ext_Sales', 'Ext_Cost', 'Brand', 'Sub_Type', 'Line', 'Admin_Ship_Est']]
jan26 = jan26.loc[~(jan26['Source'] == "BulkOrders")]  # Remove bulk orders
jan26 = jan26.loc[(jan26['Source'] == "Amazon")]  # Remove bulk orders
jan26 = jan26.loc[(jan26['Brand'] == "Hankook")]


# These Brands are selected from the top 10% of brands as computed in profit/brand.py

# Compute Columns for profit, include shipping cost
jan26['Net_Profit'] = ((jan26['Ext_Sales'] - jan26['Ext_Cost']) - jan26['Admin_Ship_Est'])
brand_demand = jan26.loc[:, ['Source', 'Created', 'Quantity', 'Brand', 'Net_Profit']]



