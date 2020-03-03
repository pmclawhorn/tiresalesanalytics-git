import warnings
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from forecast.data_load import historical_data
from tabulate import tabulate

pdtabulate = lambda df: tabulate(df, headers='keys', tablefmt='psql')
warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')
pd.set_option("display.max_columns", 20)
pd.set_option("display.max_rows", 100)
sns.set()


# Helper for Brand Selection
class TopTwenty:
    def __init__(self, level, group):
        self.level = level
        self.group = group

    # Prints and Displays a Table of the 20 Top Selling Brands for a passed-in Subtype
    # Returns a list
    def show_brands(self):
        brands = historical_data.loc[(historical_data['Sub_Type'] == str(self.group))]
        brands['Net_Profit'] = ((brands['Ext_Sales'] - brands['Ext_Cost']) - brands['Admin_Ship_Est'])
        brands = brands.loc[:, ['ProductID', 'Quantity', 'Cost', 'Unit_Cost', 'Price', 'Unit_Price', 'Ext_Sales',
                                'Ext_Cost', 'Net_Profit', 'Brand', 'Subtype', 'SupplierWarehouseName', 'Line']]
        brands = brands.sort_values(['Quantity'], ascending=[False])
        brand_group = brands.groupby('Brand').agg({'Quantity': ['sum', 'mean']}).reset_index()
        brand_group = brand_group.sort_values([('Quantity', 'sum')], ascending=False)
        print("The top 20 Brands for Sub_Type " + self.group + " are: ")
        print(pdtabulate(brand_group.head(20)))
        top20_brands = list(brand_group.head(20)['Brand'])
        return top20_brands

    def show_warehouses(self):
        warehouses = historical_data.loc[(historical_data['Sub_Type'] == str(self.group))]
        warehouses['Net_Profit'] = ((warehouses['Ext_Sales'] - warehouses['Ext_Cost']) - warehouses['Admin_Ship_Est'])
        warehouses = warehouses.loc[:,
                     ['ProductID', 'Quantity', 'Cost', 'Unit_Cost', 'Price', 'Unit_Price', 'Ext_Sales',
                      'Ext_Cost', 'Net_Profit', 'Brand', 'Subtype', 'SupplierWarehouseName', 'Line']]
        warehouses = warehouses.sort_values(['Quantity'], ascending=[False])
        warehouse_group = warehouses.groupby('SupplierWarehouseName').agg({'Quantity': ['sum', 'mean']}).reset_index()
        warehouse_group = warehouse_group.sort_values([('Quantity', 'sum')], ascending=False)
        print("The top 20 Warehouses for Sub_Type " + self.group + " are: ")
        print(pdtabulate(warehouse_group.head(20)))
        top20_warehouses = list(warehouse_group.head(20)['SupplierWarehouseName'])
        return top20_warehouses

    def show_brands_in_warehouse(self, warehouse):
        brands = historical_data.loc[(historical_data['SupplierWarehouseName'] == str(warehouse))]
        brands = brands.loc[(brands['Sub_Type'] == str(self.group))]
        brands['Net_Profit'] = ((brands['Ext_Sales'] - brands['Ext_Cost']) - brands['Admin_Ship_Est'])
        brands = brands.loc[:, ['ProductID', 'Quantity', 'Cost', 'Unit_Cost', 'Price', 'Unit_Price', 'Ext_Sales',
                                'Ext_Cost', 'Net_Profit', 'Brand', 'Subtype', 'SupplierWarehouseName', 'Line']]
        brands = brands.sort_values(['Quantity'], ascending=[False])
        brand_group = brands.groupby('Brand').agg({'Quantity': ['sum', 'mean']}).reset_index()
        brand_group = brand_group.sort_values([('Quantity', 'sum')], ascending=False)
        print("The top 20 Brands for Sub_Type " + self.group + " in Warehouse " + warehouse + " are: ")
        print(pdtabulate(brand_group.head(20)))
        top20_brands = list(brand_group.head(20)['Brand'])
        return top20_brands


def main():
    print("data_helpers.py loaded...")

