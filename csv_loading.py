#csv_loading.py

import pandas as pd

def load_data(path):
    #load csv as dataframe
    df = pd.read_csv(path)
    #fix true/false to 0 or 1
    #df["?"] = df["?"].astype(int)
    return df

def data_inspection(dataframe):
    #TODO REMOVE DEBUG STATMENTS
    print("Dataframe Head:")
    print(dataframe.head())
    print("shape:")
    print(dataframe.shape)
    print("info")
    print(dataframe.info())

    #remove duplicate rows
    initial_rows = dataframe.shape[0]
    dataframe.drop_duplicates(inplace=True)
    final_rows = dataframe.shape[0]
    removed_count = initial_rows - final_rows
    #TODO REMOVE DEBUG STATEMENTS
    print("Dataframe Head:")
    print(dataframe.head())
    print("shape:")
    print(dataframe.shape)
    print("info")
    print(dataframe.info())

    print(initial_rows == final_rows)
    if (initial_rows == final_rows):
        print("No duplicate rows to be removed")
    else:
        print("Duplicate rows removed:")
        print(removed_count)

    return dataframe
