import pandas as pd
import os

def update_row_sheet(path, row, column, new_value):
    df = pd.read_excel("prueba-demo.xlsx", engine="openpyxl")
    df.loc[0, "Columna1"] = "PRUEBA DEMO"
    df.to_excel("prueba-demo.xlsx", index=False)