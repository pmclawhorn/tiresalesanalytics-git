"""
    Author: Pierce M. McLawhorn
    This Module loads data for forecast generation, as specified
    by user input when running any of winters_forecast.py,
"""
import warnings
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from forecast.load_data import historical_data

warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')
pd.set_option("display.max_columns", 20)
pd.set_option("display.max_rows", 100)
sns.set()


# Hierarchy is Brand -> Subtype -> Line
# The level refers to one of these, the group refers to a group within that level,
#  frequency refers to data frequency.
class PreProcessData:
    def __init__(self, level, group, frequency):
        self.data = pd.DataFrame()
        self.level = level
        self.group = group
        self.frequency = frequency
        if self.level == 1:
            self.level_one = "Brand"
        elif self.level == 2:
            self.level_one = "Sub_Type"
        elif self.level == 3:
            self.level_one = "Line"
        elif self.level == 4:
            self.level_one = "Sub_Type"
            self.level_two = "Brand"

    # Aggregate data to proper form
    def aggregate(self):

        if self.frequency == 12:
            self.data = historical_data.loc[(historical_data[str(self.level_one)] == str(self.group))]

            # Compute Columns for profit, include shipping cost
            self.data['Net_Profit'] = ((self.data['Ext_Sales'] - self.data['Ext_Cost']) - self.data['Admin_Ship_Est'])

            # Aggregate Data to Monthly
            subtype_demand_month = self.data.loc[:, ['Created', 'Quantity', str(self.level_one)]]
            subtype_demand_month['Created'] = pd.to_datetime(subtype_demand_month['Created'])
            subtype_demand_month = subtype_demand_month.groupby(str(self.level_one)).resample('M', on='Created', label='right',
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

        elif self.frequency == 52:
            self.data = historical_data.loc[(historical_data[str(self.level_one)] == str(self.group))]

            # Compute Columns for profit, include shipping cost
            self.data['Net_Profit'] = ((self.data['Ext_Sales'] - self.data['Ext_Cost']) - self.data['Admin_Ship_Est'])

            # Aggregate Data to Monthly
            subtype_demand_week = self.data.loc[:, ['Created', 'Quantity', str(self.level_one)]]
            subtype_demand_week['Created'] = pd.to_datetime(subtype_demand_week['Created'])
            subtype_demand_week = subtype_demand_week.groupby(str(self.level_one)).resample('W-Mon', on='Created', label='left',
                                                                                   closed='left') \
                .sum().reset_index().sort_values(by='Created')

            # Fill data where a subtype may have been ordered 0 times in a week
            subtype_result_week = subtype_demand_week.groupby(['Created', str(self.level_one)])['Quantity'].sum().reset_index().\
                pivot(index='Created', columns=str(self.level_one), values='Quantity').resample('W-Mon', label='left',
                                                                                       closed='left'). \
                asfreq().fillna(0)

            self.data = subtype_result_week
            return self.data

        # If there is a group within group
        #  elif self.level_two:
        #    pass

    # Normalize outliers that lie beyond 2 standard deviations
    def normalize(self):
        print("finish normalize function")


# Subclass for when warehouse data is of interest
# Use same initialization parameters as parent class
# SupplierWarehouseName or SupplierWarehouseID
class Warehouse(PreProcessData):
    pass

    # override load for when warehouse is of interest
    def aggregate(self, warehouse):
        pass


def main():
    # Get user input for level of interest
    while True:
        try:
            level = int(input("What level of data are you interested in? Please enter the number.\n\
                      Options are: (1) Brand, (2) Subtype, (3) Line, or (4) BrandWithinSubtype"))
            if level != int(1) and level != int(2) and level != int(3) and level != int(4):
                raise ValueError
            break
        except ValueError:
            print("Invalid Number, Please Try Again")

    # Get user input for subgroup of interest
    subgroup = str(input("What subgroup are you interested in? (e.g. \'Trailer\', \'Hankook\')"))

    # Get user input for data frequency
    frequency = int(input("How frequently do you want the data sampled? (12 for monthly, 52 for weekly)"))

    # Instantiate PreProcessData Object
    tire_data = PreProcessData(level, subgroup, frequency)
    result = tire_data.aggregate()
    # tire_data.normalize()
    print(result.head(20))
    return tire_data.data


def load_data():
    # Get user input for level of interest
    while True:
        try:
            level = int(input("What level of data are you interested in? Please enter the number.\n\
                          Options are: (1) Brand, (2) Subtype, (3) Line, or (4) BrandWithinSubtype"))
            if level != int(1) and level != int(2) and level != int(3) and level != int(4):
                raise ValueError
            break
        except ValueError:
            print("Invalid Number, Please Try Again")


    # Get user input for subgroup of interest
    subgroup = str(input("What subgroup are you interested in? (e.g. \'Trailer\', \'Hankook\')"))

    # Get user input for data frequency
    frequency = int(input("How frequently do you want the data sampled? (12 for monthly, 52 for weekly)"))

    # Instantiate PreProcessData Object
    tire_data = PreProcessData(level, subgroup, frequency)
    result = tire_data.aggregate()
    # tire_data.normalize()
    print(result.head(20))
    return tire_data.data


if __name__ == "__main__":
    main()

if __name__ == "preprocess_data":
    load_data()
