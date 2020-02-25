import warnings
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')
import pandas as pd
pd.set_option("display.max_columns", 20)
pd.set_option("display.max_rows", 100)
import seaborn as sns; sns.set()

# Hierarchy is Brand -> Subtype -> Line

# Filter the Data to Necessary Columns, Remove Extraneous Data
jan26_raw = pd.read_csv(r'/Users/piercemclawhorn/om597/data/OrderItemMargin-01-26.csv')
raw_2018 = pd.read_csv(r'/Users/piercemclawhorn/om597/data/OrderItemMargin_2018.csv')
feb12_raw = pd.concat([jan26_raw, raw_2018], axis=0, sort=False)
feb12 = feb12_raw.loc[:, ['Source', 'Created', 'ProductID', 'Quantity', 'Cost', 'Unit_Cost', 'Price', 'Unit_Price',
                          'Ext_Sales', 'Ext_Cost', 'Brand', 'Sub_Type', 'Line', 'Admin_Ship_Est']]
feb12 = feb12.loc[~(feb12['Source'] == "BulkOrders")]
feb12 = feb12.loc[(feb12['Sub_Type'] == "Trailer")]  # Select only the Trailer Sub_Type

# Compute Columns for profit, include shipping cost
feb12['Net_Profit'] = ((feb12['Ext_Sales'] - feb12['Ext_Cost']) - feb12['Admin_Ship_Est'])
subtype_demand = feb12.loc[:, ['Created', 'Quantity', 'Sub_Type']]

# Aggregate Data to Weekly
subtype_demand['Created'] = pd.to_datetime(subtype_demand['Created'])
subtype_demand = subtype_demand.groupby('Sub_Type').resample('W-Mon', on='Created', label='left', closed='left')\
                                        .sum().reset_index().sort_values(by='Created')

# Aggregate Data to Daily
subtype_demand_day = feb12.loc[:, ['Created', 'Quantity', 'Sub_Type']]
subtype_demand_day['Created'] = pd.to_datetime(subtype_demand['Created'])
subtype_demand_day = subtype_demand_day.groupby('Sub_Type').resample('D', on='Created', label='left', closed='left')\
                                        .sum().reset_index().sort_values(by='Created')

# Aggregate Data to Monthly
subtype_demand_month = feb12.loc[:, ['Created', 'Quantity', 'Sub_Type']]
subtype_demand_month['Created'] = pd.to_datetime(subtype_demand_month['Created'])
subtype_demand_month = subtype_demand_month.groupby('Sub_Type').resample('M', on='Created', label='right', closed='right')\
                                        .sum().reset_index().sort_values(by='Created')

# Fill data where a subtype may have been ordered 0 times in a week
subtype_result = subtype_demand.groupby(['Created', 'Sub_Type'])['Quantity'].sum().reset_index().\
    pivot(index='Created', columns='Sub_Type', values='Quantity').resample('W-Mon', label='left', closed='left').\
    asfreq().fillna(0)

subtype_result_day = subtype_demand_day.groupby(['Created', 'Sub_Type'])['Quantity'].sum().reset_index().\
    pivot(index='Created', columns='Sub_Type', values='Quantity').resample('D', label='left', closed='left').\
    asfreq().fillna(0)

subtype_result_month = subtype_demand_month.groupby(['Created', 'Sub_Type'])['Quantity'].sum().reset_index().\
    pivot(index='Created', columns='Sub_Type', values='Quantity').resample('M', label='right', closed='right').\
    asfreq().fillna(0)

print(subtype_result_month)