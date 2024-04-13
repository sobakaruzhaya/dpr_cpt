import pandas as pd

def detect_price(image):
    pass

def detect_category(image):
    pass


def get_analog_price():
    file = pd.read_excel("C:\\Users\\alexs\\PycharmProjects\\flaskProject\\price.xlsx", engine='openpyxl', nrows=37)
    for rows,columns in file.iterrows():
        if columns.values[1] == detect_category(image):
            print(columns.values[3])

get_analog_price()
