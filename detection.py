import pandas as pd

def detect_price(image):
    pass

def detect_category(image):
    pass


def get_analog_price(d):
    file = pd.read_excel("price.xlsx", nrows=37)
    for rows,columns in file.iterrows():
        if columns.values[1] == d:
            return columns.values[3]

get_analog_price()
