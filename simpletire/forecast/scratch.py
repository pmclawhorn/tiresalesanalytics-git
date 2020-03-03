import warnings
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from forecast.data_load import historical_data

warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')
pd.set_option("display.max_columns", 20)
pd.set_option("display.max_rows", 100)
sns.set()


# Compute Top 20 Trailer Brands
brandagg = historical_data.loc[(historical_data['Sub_Type'] == "Trailer")]
brandagg['Net_Profit'] = ((brandagg['Ext_Sales'] - brandagg['Ext_Cost']) - brandagg['Admin_Ship_Est'])
brandagg = brandagg.loc[:, ['ProductID', 'Quantity', 'Cost', 'Unit_Cost', 'Price', 'Unit_Price', 'Ext_Sales',
                      'Ext_Cost', 'Net_Profit', 'Brand']]
brandagg = brandagg.sort_values(['Quantity'], ascending=[False])
brand_group = brandagg.groupby('Brand').agg({'Quantity': ['sum', 'mean']}).reset_index()
brand_group = brand_group.sort_values([('Quantity', 'sum')], ascending=False)
print("The top 20 brands at this level are:\n")
print(brand_group.head(20))
top20_brands = list(brand_group.head(20)['Brand'])
# print(top20_brands)

"""
# Aggregate Data to Monthly
subtype_demand_week = brandagg.loc[:, ['Created', 'Quantity', 'Brand']]
subtype_demand_week['Created'] = pd.to_datetime(subtype_demand_week['Created'])
subtype_demand_week = subtype_demand_week.groupby('Brand').resample('W-Mon', on='Created', label='left',
                                                                                closed='left') \
    .sum().reset_index().sort_values(by='Created')

# Fill data where a subtype may have been ordered 0 times in a week
subtype_result_week = subtype_demand_week.groupby(['Created', 'Brand'])['Quantity'].sum().reset_index(). \
    pivot(index='Created', columns='Brand', values='Quantity').resample('W-Mon', label='left',
                                                                                    closed='left'). \
    asfreq().fillna(0)
"""