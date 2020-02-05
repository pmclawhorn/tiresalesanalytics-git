import pandas as pd

jan26_raw = pd.read_csv(r'/Users/piercemclawhorn/om597/data/OrderItemMargin-01-26.csv')
jan26 = jan26_raw.loc[:, ['Source', 'Created', 'ProductID', 'Quantity', 'Cost', 'Unit_Cost', 'Price',
                          'Unit_Price', 'Ext_Sales', 'Ext_Cost', 'Brand', 'Sub_Type', 'Line', 'Admin_Ship_Est'
                          ]]
jan26 = jan26.loc[~(jan26['Source'] == "BulkOrders")]  # Remove bulk orders

subtype = jan26.loc[:, ['ProductID', 'Quantity', 'Cost', 'Unit_Cost', 'Price', 'Unit_Price', 'Ext_Sales',
                      'Ext_Cost', 'Sub_Type'
                    ]]
subtype = subtype.sort_values(['Ext_Sales'], ascending=[False])
subtype_group = subtype.groupby('Sub_Type').agg({'Quantity': ['sum','mean']}).reset_index()
subtype_group = subtype_group.sort_values([('Quantity', 'sum')], ascending=False)

print(subtype_group)