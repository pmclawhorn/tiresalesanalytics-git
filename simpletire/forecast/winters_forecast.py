import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')
import pandas as pd

pd.set_option("display.max_columns", 20)
pd.set_option("display.max_rows", 100)
import seaborn as sns;

sns.set()


def main():
    subgroup = input("What subgroup are you interested in? (e.g. \"Trailer\"")
    frequency = input("What is the frequency of your input data? (12 for monthly, 52 for weekly)")


if __name__ == "__main__":
    main()


class WintersForecast:
    pass

    def __init__(self, subgroup, frequency, lookahead):
        self.subgroup = subgroup
        self.frequency = frequency
        self.lookahead = lookahead

    def generate_forecast(self):
        pass

    def plot_forecast(self):
        pass

    def plot_residuals(self):
        pass

    def generate_csv(self):
        pass


# child class for other forecast
class OtherForecast(WintersForecast):
    pass
