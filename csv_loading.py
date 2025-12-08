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
    dataframe.to_csv(f"data/clean_dataframe.csv", index=False)

    return dataframe

def clean_up(df):

    #dropping rows that add confusion later and can be computed from the other columns
    # Drop rows where student group is 'All Students'
    df = df[df['Student group'] != 'All Students']
    #reset the index
    df = df.reset_index(drop=True)
    print(df.head())

    #combine columns
    df["Category: Student Group"] = df["Category"].fillna("").str.strip() + ": " + df["Student group"]
    df = df.drop(columns=["Category", "Student group"])
    print("NEW DATAFRAME HEAD:")
    print(df.head())

    df["District code: District name"] = df["District code"] + ": " + df["District name"]
    df = df.drop(columns=["District code", "District name"])
    print("NEW DATAFRAME HEAD:")
    print(df.head())

    #dropping columns that don't add value, all rows the same
    df = df.drop(columns=["Date update", "Reporting period"])
    print("NEW DATAFRAME HEAD:")
    print(df.head())


    return df


