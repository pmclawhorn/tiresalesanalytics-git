import matplotlib.pyplot as plt
from pandas import DataFrame
from statsmodels.tsa.holtwinters import SimpleExpSmoothing, Holt, ExponentialSmoothing
import warnings
warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')
import pandas as pd
pd.set_option("display.max_columns", 20)
pd.set_option("display.max_rows", 100)
import seaborn as sns; sns.set()
from forecast.trailer_forecast_load import subtype_result
from forecast.trailer_forecast_load import subtype_result_month


class WintersForecast:
    pass

    def __init__(self, subgroup, frequency, lookahead):
        self.subgroup = subgroup
        self.frequency = frequency
        self.lookahead = lookahead

    

