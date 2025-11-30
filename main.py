#main.py
from csv_loading import load_data, data_inspection
#entry point for program to run
def main():
    #TODO need to fix path because this only works on this machine
    #load csv
    df = load_data("data\School_Attendance_dataset.csv")
    #check out and fix data
    dataframe = data_inspection(df)


if __name__ == "__main__":
    main()
