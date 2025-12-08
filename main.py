#main.py
from csv_loading import load_data, data_inspection
from normalize import normalize
#entry point for program to run
def main():
    #load csv
    df = load_data("data\School_Attendance_dataset.csv")
    #check out and fix data
    clean_dataframe = data_inspection(df)
    #normalize data
    normalized_dataframe = normalize(clean_dataframe)

    #TODO CLEAN UP DEBUG CODE
    print("printing normalized df head")
    print(normalized_dataframe.head())
    print("printing normalized df info")
    print(normalized_dataframe.info())
    print("printing normalized df shape")
    print(normalized_dataframe.shape)


if __name__ == "__main__":
    main()
