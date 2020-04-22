"""
    Author: Pierce M. McLawhorn
    This Module loads raw data from .csv records, such it may be manipulated in data_preprocess.py.
    This type of global variable implementation is used purely for speed and memory efficiency.
    Run this module once (ensuring that you set the correct file paths) and then run one of the *_forecast.py modules.
"""
import warnings
import pandas as pd

warnings.filterwarnings("ignore")
pd.set_option("display.max_columns", 20)
pd.set_option("display.max_rows", 100)

# Global Static Raw Data
raw_2020 = pd.read_csv(r'/Users/piercemclawhorn/om597/data/OrderItemMargin_2020.csv')
jan26_raw = pd.read_csv(r'/Users/piercemclawhorn/om597/data/OrderItemMargin-01-26.csv')
jan26_raw = jan26_raw.loc[(jan26_raw['Created'] < '2020-01-01')]
raw_2018 = pd.read_csv(r'/Users/piercemclawhorn/om597/data/OrderItemMargin_2018.csv')
historical_data_raw = pd.concat([jan26_raw, raw_2018], axis=0, sort=False)
historical_data_raw = pd.concat([historical_data_raw, raw_2020], axis=0, sort=False)
historical_data = historical_data_raw.loc[:, ['Source', 'Created', 'ProductID', 'Quantity', 'Cost', 'Unit_Cost',
                                              'Price', 'Unit_Price', 'Ext_Sales', 'Ext_Cost', 'Brand', 'Sub_Type',
                                              'Line', 'Admin_Ship_Est', 'SupplierWarehouseName',
                                              'SupplierWarehouseID']]
historical_data = historical_data.loc[~(historical_data['Source'] == "BulkOrders")]

select_source = str(input("Would you like to ONLY include data from a specified Source? (Y/N) \n" +
                          "NOTE: If you select this option now , the later Source selection will not work. \n" +
                          "This option exists here to select smaller subcategories within your chosen source. \n"))
if select_source == "Y":
    source = str(input("Which Source would you like? e.g. SimpleWebsite, Amazon \n "))
    historical_data = historical_data.loc[historical_data['Source'] == source]

# Get the Table for Supplier Regions
supplier_regions = pd.read_csv(r'/Users/piercemclawhorn/om597/data/supplier_regions.csv')

# Rename 'name' column to 'SupplierWarehouseName', convert region to int type
supplier_regions.rename(columns={'name': 'SupplierWarehouseName'}, inplace=True)
supplier_regions['region'] = supplier_regions['region'].fillna(0).astype(int)

# TEST print(supplier_regions.head(20))

# Add supplier region column to the rest of the data
historical_data = pd.merge(historical_data, supplier_regions, on='SupplierWarehouseName')
historical_data['ProductID'] = historical_data['ProductID'].fillna(0).astype(str)
# TEST print(historical_data.head(20))


def main():
    print(historical_data.head(20))


if __name__ == "__main__":
    main()
