import warnings
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# from forecast.data_load import historical_data
# from forecast.data_helpers import TopTwenty
from tabulate import tabulate

pdtabulate = lambda df: tabulate(df, headers='keys', tablefmt='psql')
warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')
pd.set_option("display.max_columns", 20)
pd.set_option("display.max_rows", 100)
sns.set()

#price aggregate
orders_with_coupons = pd.read_csv(r'/Users/piercemclawhorn/om597/data/orders_with_coupons.csv')
orders_with_coupons = orders_with_coupons.loc[:, ['name', 'start_date', 'Order_Coupon_Total']]
owc_group = orders_with_coupons.groupby('name').agg({'Order_Coupon_Total': ['sum', 'mean']}).reset_index()
owc_group = owc_group.sort_values([('Order_Coupon_Total', 'sum')], ascending=False)
print('Top Coupons by Total Dollar Amount Redeemed\n')
print(pdtabulate(owc_group.head(20)))


#brand_group = brands.groupby('Brand').agg({'Quantity': ['sum', 'mean']}).reset_index()
#        brand_group = brand_group.sort_values([('Quantity', 'sum')], ascending=False)
#        print("The top 20 Brands for Sub_Type " + se


# amount aggregate
all_coupons = pd.read_csv(r'/Users/piercemclawhorn/om597/data/all_coupons.csv')
all_coupons = all_coupons.loc[:, ['name', 'start_date', 'used_count']]
allcoupons_group = all_coupons.groupby('name').agg({'used_count': ['sum', 'mean']}).reset_index()
allcoupons_group = allcoupons_group.sort_values([('used_count', 'sum')], ascending=False)
print('Top Coupons by Number of Times Redeemed\n')
print(pdtabulate(allcoupons_group.head(20)))
