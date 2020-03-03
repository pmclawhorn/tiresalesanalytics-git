"""
    Author: Pierce M. McLawhorn
    This Module loads raw data from .csv records, such it may be manipulated in preprocess_data.py.
    This type of global variable implementation is used purely for speed and memory efficiency.
    Run this module once (ensuring that you set the correct file paths) and then run one of the *_forecast.py modules.
"""
import warnings
import pandas as pd

warnings.filterwarnings("ignore")
pd.set_option("display.max_columns", 20)
pd.set_option("display.max_rows", 100)

# Global Static Raw Data
jan26_raw = pd.read_csv(r'/Users/piercemclawhorn/om597/data/OrderItemMargin-01-26.csv')
raw_2018 = pd.read_csv(r'/Users/piercemclawhorn/om597/data/OrderItemMargin_2018.csv')
historical_data_raw = pd.concat([jan26_raw, raw_2018], axis=0, sort=False)
historical_data = historical_data_raw.loc[:, ['Source', 'Created', 'ProductID', 'Quantity', 'Cost', 'Unit_Cost',
                                              'Price', 'Unit_Price', 'Ext_Sales', 'Ext_Cost', 'Brand', 'Sub_Type',
                                              'Line', 'Admin_Ship_Est', 'SupplierWarehouseName',
                                              'SupplierWarehouseID']]
historical_data = historical_data.loc[~(historical_data['Source'] == "BulkOrders")]


def main():
    print(historical_data.head(20))


if __name__ == "__main__":
    main()
