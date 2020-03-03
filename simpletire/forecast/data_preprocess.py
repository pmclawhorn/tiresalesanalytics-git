"""
    Author: Pierce M. McLawhorn
    This Module pre-processes data for forecast generation, as specified
    by user input when running any of the forecast modules, or when run individually through main().
    Data aggregation is enabled by Subtype, Brand, Line, and Brand within Subtype, for either weekly or monthly
    sampling periods. Additionally, the data is normalized such that any outliers beyond 2 standard deviations
    (at the aggregate level) are normalized with the previous sample period. Code structure loosely follows the
    Adapter design pattern.
"""
import warnings
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from forecast.data_load import historical_data
from forecast.data_helpers import TopTwenty
from tabulate import tabulate

pdtabulate = lambda df: tabulate(df, headers='keys', tablefmt='psql')
warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')
pd.set_option("display.max_columns", 20)
pd.set_option("display.max_rows", 100)
sns.set()


# Hierarchy is Brand -> Subtype -> Line
# The level refers to one of these, the group refers to a group within that level,
#  frequency refers to data frequency.
class PreProcessData:
    def __init__(self, level_one, level_two, group_one, group_two, frequency):
        self.data = pd.DataFrame()
        self.level_one = level_one
        self.level_two = level_two
        self.group_one = group_one
        self.group_two = group_two
        self.frequency = frequency
        if self.level_one == 1:
            self.level_one = "Brand"
        elif self.level_one == 2:
            self.level_one = "Sub_Type"
        elif self.level_one == 3:
            self.level_one = "Line"
        elif self.level_one == 4:
            self.level_one = "Sub_Type"
            self.level_two = "Brand"

    # Aggregate data to proper form
    def aggregate(self):
        # Aggregate Monthly Data
        if self.frequency == 12:
            self.data = historical_data.loc[(historical_data[str(self.level_one)] == str(self.group))]

            # Compute Columns for profit, include shipping cost
            self.data['Net_Profit'] = ((self.data['Ext_Sales'] - self.data['Ext_Cost']) - self.data['Admin_Ship_Est'])

            # Aggregate Data to Monthly
            subtype_demand_month = self.data.loc[:, ['Created', 'Quantity', str(self.level_one)]]
            subtype_demand_month['Created'] = pd.to_datetime(subtype_demand_month['Created'])
            subtype_demand_month = subtype_demand_month.groupby(str(self.level_one)).resample('M', on='Created',
                                                                                              label='right',
                                                                                              closed='right') \
                .sum().reset_index().sort_values(by='Created')

            # Fill data where a subtype may have been ordered 0 times in a week
            subtype_result_month = subtype_demand_month.groupby(['Created', str(self.level_one)])[
                'Quantity'].sum().reset_index(). \
                pivot(index='Created', columns=str(self.level_one), values='Quantity').resample('M', label='right',
                                                                                                closed='right'). \
                asfreq().fillna(0)

            self.data = subtype_result_month
            return self.data
        # Aggregate Weekly Data
        elif self.frequency == 52:
            self.data = historical_data.loc[(historical_data[str(self.level_one)] == str(self.group_one))]

            # Compute Columns for profit, include shipping cost
            self.data['Net_Profit'] = ((self.data['Ext_Sales'] - self.data['Ext_Cost']) - self.data['Admin_Ship_Est'])

            # Aggregate Data to Weekly
            subtype_demand_week = self.data.loc[:, ['Created', 'Quantity', str(self.level_one)]]
            subtype_demand_week['Created'] = pd.to_datetime(subtype_demand_week['Created'])
            subtype_demand_week = subtype_demand_week.groupby(str(self.level_one)).resample('W-Mon', on='Created',
                                                                                            label='left',
                                                                                            closed='left') \
                .sum().reset_index().sort_values(by='Created')

            # Fill data where a subtype may have been ordered 0 times in a week
            subtype_result_week = subtype_demand_week.groupby(['Created', str(self.level_one)])['Quantity'].sum(). \
                reset_index().pivot(index='Created', columns=str(self.level_one), values='Quantity'). \
                resample('W-Mon', label='left', closed='left').asfreq().fillna(0)

            self.data = subtype_result_week
            return self.data

        # If there is a group within group
        #  elif self.level_two:
        #    pass

    # Normalize outliers that lie beyond 2 standard deviations
    def normalize(self):
        # TODO: finish this method
        print("finish normalize function")
        # compute standard deviations and normalize here

    # Displays top 10 weeks in terms of quantity for current instance
    def demand_spikes(self):
        if self.group_two == 0:
            spike_weeks = self.data.sort_values(by=str(self.group_one), ascending=False)
        else:
            spike_weeks = self.data.sort_values(by=str(self.group_two), ascending=False)

        print("Top 10 Highest weeks by Units Sold")
        # spike_weeks['Created'] = (spike_weeks['Created']).date
        print(pdtabulate(spike_weeks.head(10)))

    def generate_report(self):
        pass
        # TODO: This, maybe save as a helper or create in forecasting functions


# Subclass for when brand within subtype data is of interest
class BrandWithinSubtype(PreProcessData):
    def double_aggregate(self):
        self.data = historical_data.loc[(historical_data[str(self.level_one)] == str(self.group_one))]
        self.data = self.data.loc[(self.data[str(self.level_two)] == str(self.group_two))]

        # Compute Columns for profit, include shipping cost
        self.data['Net_Profit'] = ((self.data['Ext_Sales'] - self.data['Ext_Cost']) - self.data['Admin_Ship_Est'])

        # Aggregate Data to Weekly
        subtype_demand_week = self.data.loc[:, ['Created', 'Quantity', str(self.level_two)]]
        subtype_demand_week['Created'] = pd.to_datetime(subtype_demand_week['Created'])
        subtype_demand_week = subtype_demand_week.groupby(str(self.level_two)).resample('W-Mon', on='Created',
                                                                                          label='left',
                                                                                          closed='left') \
            .sum().reset_index().sort_values(by='Created')

        # Fill data where a subtype may have been ordered 0 times in a week
        subtype_result_week= subtype_demand_week.groupby(['Created', str(self.level_two)])[
            'Quantity'].sum().reset_index(). \
            pivot(index='Created', columns=str(self.level_two), values='Quantity').resample('W-Mon', label='left',
                                                                                            closed='left'). \
            asfreq().fillna(0)

        self.data = subtype_result_week
        return self.data


# Subclass for when warehouse data is of interest
# Use same initialization parameters as parent class, overrides aggregate function
# SupplierWarehouseName or SupplierWarehouseID
class Warehouse(PreProcessData):
    # double_aggregate for when warehouse and brand is of interest
    def double_aggregate(self, warehouse):
        self.data = historical_data.loc[(historical_data['SupplierWarehouseName'] == str(warehouse))]
        self.data = self.data.loc[(self.data[str(self.level_one)] == str(self.group_one))]
        self.data = self.data.loc[(self.data[str(self.level_two)] == str(self.group_two))]

        # Compute Columns for profit, include shipping cost
        self.data['Net_Profit'] = ((self.data['Ext_Sales'] - self.data['Ext_Cost']) - self.data['Admin_Ship_Est'])

        # Aggregate Data to Weekly
        subtype_demand_week = self.data.loc[:, ['Created', 'Quantity', str(self.level_two)]]
        subtype_demand_week['Created'] = pd.to_datetime(subtype_demand_week['Created'])
        subtype_demand_week = subtype_demand_week.groupby(str(self.level_two)).resample('W-Mon', on='Created',
                                                                                        label='left',
                                                                                        closed='left') \
            .sum().reset_index().sort_values(by='Created')

        # Fill data where a subtype may have been ordered 0 times in a week
        subtype_result_week = subtype_demand_week.groupby(['Created', str(self.level_two)])[
            'Quantity'].sum().reset_index(). \
            pivot(index='Created', columns=str(self.level_two), values='Quantity').resample('W-Mon', label='left',
                                                                                            closed='left'). \
            asfreq().fillna(0)

        self.data = subtype_result_week
        return self.data

    # override aggregate for when warehouse is of interest
    def aggregate(self, warehouse):
        self.data = historical_data.loc[(historical_data['SupplierWarehouseName'] == str(warehouse))]
        self.data = self.data.loc[(self.data[str(self.level_one)] == str(self.group_one))]

        # Compute Columns for profit, include shipping cost
        self.data['Net_Profit'] = ((self.data['Ext_Sales'] - self.data['Ext_Cost']) - self.data['Admin_Ship_Est'])

        # Aggregate Data to Weekly
        subtype_demand_week = self.data.loc[:, ['Created', 'Quantity', str(self.level_one)]]
        subtype_demand_week['Created'] = pd.to_datetime(subtype_demand_week['Created'])
        subtype_demand_week = subtype_demand_week.groupby(str(self.level_one)).resample('W-Mon', on='Created',
                                                                                        label='left',
                                                                                        closed='left') \
            .sum().reset_index().sort_values(by='Created') # FIXME

        # Fill data where a subtype may have been ordered 0 times in a week
        subtype_result_week = subtype_demand_week.groupby(['Created', str(self.level_one)])['Quantity'].sum(). \
            reset_index().pivot(index='Created', columns=str(self.level_one), values='Quantity'). \
            resample('W-Mon', label='left', closed='left').asfreq().fillna(0)

        self.data = subtype_result_week
        return self.data


def main():
    # See if User is looking for Warehouse specific data
    want_warehouse = str(input("Are you interested in getting down to the warehouse level? (Y/N)"))

    # Get user input for level of interest
    while True:
        try:
            level = int(input("What level of data are you interested in? Please enter the number.\n\
            Options are: (1) Brand, (2) Subtype, (3) Line, (4) BrandWithinSubtype"))
            if level != int(1) and level != int(2) and level != int(3) and level != int(4):
                raise ValueError
            break
        except ValueError:
            print("Invalid Number, Please Try Again")

    # Get user input for data frequency, TODO: weekly works for all, monthly does not yet
    # frequency = int(input("How frequently do you want the data sampled? (12 for monthly, 52 for weekly)"))
    frequency = int(52)

    # For ALL Warehouses Combined
    if want_warehouse == "N":
        if level != int(4):
            level_one = level
            level_two = 0

            # Get user input for subgroup of interest
            subgroup = str(input("What subgroup at this level are you interested in? (e.g. \'Trailer\', \'Hankook\')"))
            group_one = subgroup
            group_two = 0

            # Instantiate PreProcessData Object
            tire_data = PreProcessData(level_one, level_two, group_one, group_two, frequency)
            tire_data.aggregate()
            tire_data.demand_spikes()
            # tire_data.normalize()
            print("Data Aggregation Complete. Showing First 10 Entries in Weekly Aggregate for:")
            print(group_one)
            print(pdtabulate(tire_data.data.head(20)))
            return tire_data.data

        elif level == int(4):
            level_one = "Sub_Type"
            level_two = "Brand"

            # Get user input for subgroup of interest
            group_one = str(input("What Sub_Type are you interested in? (e.g. \'Trailer\')"))
            # Show Top 20 Brands for that Subtype
            top = TopTwenty("Sub_Type", str(group_one))
            top.show_brands()
            group_two = str(input("Which Brand are you interested in?"))

            tire_data = BrandWithinSubtype(level_one, level_two, group_one, group_two, frequency)
            tire_data.double_aggregate()
            tire_data.demand_spikes()
            # tire_data.normalize()
            name = str(group_one) + " - " + str(group_two)
            tire_data.data.rename(columns={str(group_two): name})
            print("Data Aggregation Complete. Showing First 10 Entries in Weekly Aggregate for:")
            print(name)
            print(pdtabulate(tire_data.data.head(20)))
            return tire_data.data

    # For Warehouse Level
    elif want_warehouse == "Y":
        if level != int(4):
            level_one = level
            level_two = 0

            # Get user input for subgroup of interest
            subgroup = str(input("What subgroup at this level are you interested in? (e.g. \'Trailer\', \'Hankook\')"))
            group_one = subgroup
            group_two = 0

            # Show Top 20 Warehouses for that Sub_Type
            top_warehouses = TopTwenty("Sub_Type", str(group_one))
            top_warehouses.show_warehouses()
            warehouse = str(input("Which Warehouse are you interested in? (enter exact name)"))

            # Instantiate PreProcessData Object
            tire_data = Warehouse(level_one, level_two, group_one, group_two, frequency)
            tire_data.aggregate(warehouse)
            tire_data.demand_spikes()
            # tire_data.normalize()
            name = str(group_one) + " - " + str(warehouse)
            tire_data.data.rename(columns={str(group_one): name})
            print("Data Aggregation Complete. Showing First 10 Entries in Weekly Aggregate for:")
            print(name)
            print(pdtabulate(tire_data.data.head(20)))
            return tire_data.data

        elif level == int(4):
            level_one = "Sub_Type"
            level_two = "Brand"

            # Get user input for subgroup of interest
            group_one = str(input("What Sub_Type are you interested in? (e.g. \'Trailer\')"))

            # Show Top 20 Warehouses for that Sub_Type, prompt for selection
            top_warehouses = TopTwenty("Sub_Type", str(group_one))
            top_warehouses.show_warehouses()
            warehouse = str(input("Which Warehouse are you interested in? (enter exact name)"))

            # Show Top 20 Brands for that Sub_Type and Warehouse, prompt for selection
            top_brands = TopTwenty("Sub_Type", str(group_one))
            top_brands.show_brands_in_warehouse(warehouse)
            group_two = str(input("Which Brand are you interested in?"))

            # Instantiate Warehouse Object
            tire_data = Warehouse(level_one, level_two, group_one, group_two, frequency)
            tire_data.double_aggregate(warehouse)
            tire_data.demand_spikes()
            # tire_data.normalize()
            name = str(level_two) + " - " + str(group_two) + " - " + str(warehouse)
            tire_data.data.rename(columns={str(level_two): name})
            print("Data Aggregation Complete. Showing First 10 Entries in Weekly Aggregate for:")
            print(name)
            print(pdtabulate(tire_data.data.head(20)))
            return tire_data.data


def preprocess_data():
    # See if User is looking for Warehouse specific data
    want_warehouse = str(input("Are you interested in getting down to the warehouse level? (Y/N)"))

    # Get user input for level of interest
    while True:
        try:
            level = int(input("What level of data are you interested in? Please enter the number.\n\
                Options are: (1) Brand, (2) Subtype, (3) Line, (4) BrandWithinSubtype"))
            if level != int(1) and level != int(2) and level != int(3) and level != int(4):
                raise ValueError
            break
        except ValueError:
            print("Invalid Number, Please Try Again")

    # Get user input for data frequency, TODO: weekly works for all, monthly does not yet
    # frequency = int(input("How frequently do you want the data sampled? (12 for monthly, 52 for weekly)"))
    frequency = int(52)

    # For ALL Warehouses Combined
    if want_warehouse == "N":
        if level != int(4):
            level_one = level
            level_two = 0

            # Get user input for subgroup of interest
            subgroup = str(input("What subgroup at this level are you interested in? (e.g. \'Trailer\', \'Hankook\')"))
            group_one = subgroup
            group_two = 0

            # Instantiate PreProcessData Object
            tire_data = PreProcessData(level_one, level_two, group_one, group_two, frequency)
            tire_data.aggregate()
            tire_data.demand_spikes()
            # tire_data.normalize()
            print("Data Aggregation Complete. Showing First 10 Entries in Weekly Aggregate for:")
            print(group_one)
            print(pdtabulate(tire_data.data.head(20)))
            return tire_data

        elif level == int(4):
            level_one = "Sub_Type"
            level_two = "Brand"

            # Get user input for subgroup of interest
            group_one = str(input("What Sub_Type are you interested in? (e.g. \'Trailer\')"))
            # Show Top 20 Brands for that Subtype
            top = TopTwenty("Sub_Type", str(group_one))
            top.show_brands()
            group_two = str(input("Which Brand are you interested in?"))

            tire_data = BrandWithinSubtype(level_one, level_two, group_one, group_two, frequency)
            tire_data.double_aggregate()
            tire_data.demand_spikes()
            # tire_data.normalize()
            name = str(group_one) + " - " + str(group_two)
            tire_data.data.rename(columns={str(group_two): name})
            print("Data Aggregation Complete. Showing First 10 Entries in Weekly Aggregate for:")
            print(name)
            print(pdtabulate(tire_data.data.head(20)))
            return tire_data

    # For Warehouse Level
    elif want_warehouse == "Y":
        if level != int(4):
            level_one = level
            level_two = 0

            # Get user input for subgroup of interest
            subgroup = str(input("What subgroup at this level are you interested in? (e.g. \'Trailer\', \'Hankook\')"))
            group_one = subgroup
            group_two = 0

            # Show Top 20 Warehouses for that Sub_Type
            top_warehouses = TopTwenty("Sub_Type", str(group_one))
            top_warehouses.show_warehouses()
            warehouse = str(input("Which Warehouse are you interested in? (enter exact name)"))

            # Instantiate PreProcessData Object
            tire_data = Warehouse(level_one, level_two, group_one, group_two, frequency)
            tire_data.aggregate(warehouse)
            tire_data.demand_spikes()
            # tire_data.normalize()
            name = str(group_one) + " - " + str(warehouse)
            tire_data.data.rename(columns={str(group_one): name})
            print("Data Aggregation Complete. Showing First 10 Entries in Weekly Aggregate for:")
            print(name)
            print(pdtabulate(tire_data.data.head(20)))
            return tire_data

        elif level == int(4):
            level_one = "Sub_Type"
            level_two = "Brand"

            # Get user input for subgroup of interest
            group_one = str(input("What Sub_Type are you interested in? (e.g. \'Trailer\')"))

            # Show Top 20 Warehouses for that Sub_Type, prompt for selection
            top_warehouses = TopTwenty("Sub_Type", str(group_one))
            top_warehouses.show_warehouses()
            warehouse = str(input("Which Warehouse are you interested in? (enter exact name)"))

            # Show Top 20 Brands for that Sub_Type and Warehouse, prompt for selection
            top_brands = TopTwenty("Sub_Type", str(group_one))
            top_brands.show_brands_in_warehouse(warehouse)
            group_two = str(input("Which Brand are you interested in?"))

            # Instantiate Warehouse Object
            tire_data = Warehouse(level_one, level_two, group_one, group_two, frequency)
            tire_data.double_aggregate(warehouse)
            tire_data.demand_spikes()
            # tire_data.normalize()
            name = str(level_two) + " - " + str(group_two) + " - " + str(warehouse)
            tire_data.data.rename(columns={str(level_two): name})
            print("Data Aggregation Complete. Showing First 10 Entries in Weekly Aggregate for:")
            print(name)
            print(pdtabulate(tire_data.data.head(20)))
            return tire_data


if __name__ == "__main__":
    main()

if __name__ == "data_preprocess":
    preprocess_data()
