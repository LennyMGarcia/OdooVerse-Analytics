import pandas as pd

def convert_numeric_columns(data, ignore=[]):
    for column in data.columns:
        if column not in ignore and not pd.api.types.is_object_dtype(data[column]):
            try:
                data[column] = pd.to_numeric(data[column], errors="coerce")  
            except Exception as e:
                print(f"⚠️ Could not convert '{column}': {e}")

    return data

def fill_numeric_columns(data, ignore=[]):
    for column in data.columns:
        if column not in ignore and not pd.api.types.is_object_dtype(data[column]):
            try:
                #Sales data can easily be filled with 0 if not
                data[column] = data[column].fillna(0) 
            except Exception as e:
                print(f"⚠️ could not be filled '{column}': {e}")

    return data


def convert_object_lowercase(data, ignore=[]):
    for column in data.columns:
        if column not in ignore and pd.api.types.is_object_dtype(data[column]):
            try:
                data[column] =  data[column].fillna("").str.lower().str.strip()
            except Exception as e:
                print(f"⚠️ Could not convert '{column}': {e}")

    return data