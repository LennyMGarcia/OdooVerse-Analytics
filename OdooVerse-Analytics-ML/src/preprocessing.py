import pandas as pd
import sys
import os

module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)

from src.utils import log_error

def convert_numeric_columns(data, ignore=[]):
    for column in data.columns:
        if column not in ignore and not pd.api.types.is_object_dtype(data[column]):
            try:
                data[column] = pd.to_numeric(data[column], errors="coerce")  
            except Exception as e:
                log_error(f" Could not convert: {str(e)}")

    return data

def fill_numeric_columns(data, ignore=[]):
    for column in data.columns:
        if column not in ignore and not pd.api.types.is_object_dtype(data[column]):
            try:
                #Sales data can easily be filled with 0 if not
                data[column] = data[column].fillna(0) 
            except Exception as e:
                log_error(f" Could be filled: {str(e)}")

    return data


def convert_object_lowercase(data, ignore=[]):
    for column in data.columns:
        if column not in ignore and pd.api.types.is_object_dtype(data[column]):
            try:
                data[column] =  data[column].fillna("").str.lower().str.strip()
            except Exception as e:
                log_error(f" Could not convert: {str(e)}")

    return data