#csv_loading.py
import io
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
    final_rows = dataframe.shape[0]
    removed_count = initial_rows - final_rows
    if (initial_rows == final_rows):
        print("No duplicate rows to be removed")
    else:
        print("Duplicate rows removed:")
        print(removed_count)
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

    buffer = io.StringIO()
    dataframe.info(buf=buffer)
    info = buffer.getvalue()
    info_df = pd.DataFrame({"info": info.splitlines()})
    info_df.to_csv("data/dataset_info.csv", index=False)
    head = dataframe.head()
    head.to_csv(f"data/dataset_head.csv", index=False)
    shape = pd.DataFrame({
        "rows": [dataframe.shape[0]],
        "columns": [dataframe.shape[1]]
    })
    shape.to_csv(f"data/dataset_shape.csv", index=False)

    print(initial_rows == final_rows)
    if (initial_rows == final_rows):
        print("No duplicate rows to be removed")
    else:
        print("Duplicate rows removed:")
        print(removed_count)


    dataframe = clean_up(dataframe)
    dataframe.to_csv(f"data/normalized_clean_dataframe.csv", index=False)

    return dataframe

def clean_up(df):

    #combine two columns
    df["Category: Student Group"] = df["Category"].fillna("").str.strip() + ": " + df["Student group"]
    df = df.drop(columns=["Category", "Student group"])
    print("NEW DATAFRAME HEAD:")
    print(df.head())

    return df
