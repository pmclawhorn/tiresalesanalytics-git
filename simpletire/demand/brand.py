import warnings
import numpy as np
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')
import pandas as pd
pd.set_option("display.max_columns", 20)
pd.set_option("display.max_rows", 100)
# import matplotlib
import seaborn as sns; sns.set()
# import metabase

# Filter the Data to Necessary Columns, Remove Extraneous Data
# if you are not Pierce then this path will need to be changed (lazy i will fix later)
jan26_raw = pd.read_csv(r'/Users/piercemclawhorn/om597/data/OrderItemMargin-01-26.csv')
raw_2018 = pd.read_csv(r'/Users/piercemclawhorn/om597/data/OrderItemMargin_2018.csv')
feb12_raw = pd.concat([jan26_raw, raw_2018], axis=0, sort=False)

feb12 = feb12_raw.loc[:, ['Source', 'Created', 'ProductID', 'Quantity', 'Cost', 'Unit_Cost', 'Price', 'Unit_Price',
                          'Ext_Sales', 'Ext_Cost', 'Brand', 'Sub_Type', 'Line', 'Admin_Ship_Est']]
feb12 = feb12.loc[~(feb12['Source'] == "BulkOrders")]  # Remove bulk orders

# These Brands are selected from the top 10% of brands as computed in profit/brand.py
feb12 = feb12.loc[feb12['Brand'].isin(['Hankook', 'Crosswind', 'Bridgestone', 'Goodyear', 'Toyo', 'Cooper', 'Achilles',
                                       'Sceptor', 'Firestone', 'Nexen', 'Michelin', 'Atturo', 'Kumhho', 'Radar', 'Nitto',
                                       'Falken', 'Federal', 'Westlake'])]

# Compute Columns for profit, include shipping cost
feb12['Net_Profit'] = ((feb12['Ext_Sales'] - feb12['Ext_Cost']) - feb12['Admin_Ship_Est'])
# empty df here
brand_demand = feb12.loc[:, ['Created', 'Quantity', 'Brand']]
print(brand_demand)

# Aggregate Data to Weekly
brand_demand['Created'] = pd.to_datetime(brand_demand['Created'])
brand_demand = brand_demand.groupby('Brand').resample('W-Mon', on='Created', label='left', closed='left').sum().reset_index().sort_values(by='Created')
print(brand_demand)

# Fill data where a subtype may have been ordered 0 times in a week
brand_result = brand_demand.groupby(['Created', 'Brand'])['Quantity'].sum().reset_index().pivot(index='Created', columns='Brand', values='Quantity').resample('W-Mon', label='left', closed='left').asfreq().fillna(0)

# This represents Sales by Week for each subtype
# Plot Subtype
print(brand_result)
brand_result.plot(figsize=(15, 6))
plt.show()

# Plot Variance
print("VARIANCE:\n")
print(brand_result.var())
#subvar = brand_result.var()
#subvar.plot(figsize=(15, 6))
#plt.show()

# Plot StdDev
print("STANDARD DEVIATION:\n")
print(np.std(brand_result))
# print("Test to change")

brand_result.to_csv(r'/Users/piercemclawhorn/om597/simpletire-git/simpletire/reports/branddemand.csv', encoding='utf-8', index=True)
brand_result.var().to_csv(r'/Users/piercemclawhorn/om597/simpletire-git/simpletire/reports/branddemandvar.csv', encoding='utf-8', index=True)
np.std(brand_result).to_csv(r'/Users/piercemclawhorn/om597/simpletire-git/simpletire/reports/branddemandstddev.csv', encoding='utf-8', index=True)