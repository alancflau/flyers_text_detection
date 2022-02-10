import pandas as pd
import numpy as np

def clean_up(item_list, price_list):
    df = pd.DataFrame(list(zip(item_list, price_list)),
                      columns=['Item', 'Price'])
    df['Item'].replace('', np.nan, inplace=True)
    df['Price'].replace('', np.nan, inplace=True)
    df.dropna(subset=['Item', 'Price'], inplace=True)

    return df