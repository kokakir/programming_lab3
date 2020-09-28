"""
@author: Kyrychek Mykola Pavlovich, K-11, variant = 89
All load- and check- functions
"""
from pathlib import Path
import pandas as pd
import numpy as np
import class_information
import class_error

def check_correctness_ini(inf: pd.core.frame.DataFrame) -> bool:
    """
    The function checks the correctness of the data of the settings file
    Parameters
    ----------
    inf : pd.core.frame.DataFrame
        DataFrame with information from an settings file
    Returns
    -------
    bool
        Returns the success of this operation
    """
    res = False
    if 'encoding' in tuple(inf.axes[0]) and 'fname' in tuple(inf.axes[0]) and\
            'csv' in tuple(inf.axes[0]) and 'json' in tuple(inf.axes[0]) and\
                "output" in tuple(inf.axes[1]) and "input" in tuple(inf.axes[1]):
        res = True
    return res
    
def check_correctness_json(json: pd.core.frame.DataFrame) -> bool:
    """
    The function checks the correctness of the data of the additional file 
    Parameters
    ----------
    json : pandas.core.frame.DataFrame
        DataFrame with information from an additional file
    Returns
    -------
    bool
        Returns the success of this operation 
    """
    return len(json)==3 and all(isinstance(i[0], (np.int64, np.float64)) for i in json.values)

def check_correctness_csv(data: class_information.Information) -> bool:
    """
    The function checks the correctness of the data of the main file
    Parameters
    ----------
    data : class_information.Information
        Object of class Information
    Returns
    -------
    bool
        Returns the success of this operation
    """
    res = False
    if tuple(data.data.axes[1]) == ('yyyy', 'rain', 'avgt', 'mm', 'dd', 'hum', 'maxt', 'wind', 'mint', 'meteo'):
        met_param = data.data[np.logical_not((data.data.meteo.str.len()>=3) &\
                                             (data.data.meteo.str.len()<=11))].empty
        yyyy_param = data.data[data.data.yyyy.str.len()!=4].empty
        data.data['avgt'] = round(data.data['avgt'], 1)
        data.data['maxt'] = round(data.data['maxt'], 1)
        data.data['mint'] = round(data.data['mint'], 1)
        data.data['hum'] = round(data.data['hum'], 1)
        data.data['wind'] = round(data.data['wind'], 2)
        res = met_param and yyyy_param
    else:
        res = False
    return res

def check_compliance_csv_to_json(data: class_information.Information, json: tuple) -> bool:
    """
    The function checks the coincidence of data in the main and additional files
    Parameters
    ----------
    data : class_information.Information
        Object of class Information
    json : tuple
        A tuple of three elements that are present in an additional file 
    Returns
    -------
    bool
        Returns the success of this operation
    """
    data.data = data.data.set_index(['yyyy', 'mm'])
    data.data = data.data.sort_index()
    wind_csv = round(sum(data.data['wind']) / data.data.shape[0], 13)
    year_csv = data.data.index[data.data.shape[0] - 1][0]
    month_csv = data.data.index[data.data.shape[0] - 1][1]
    return int(year_csv) == json[0] and month_csv == json[1] and wind_csv == json[2]
    
def load_ini(file_name: str) -> tuple:
    """
    The function opens a settings file
    checks it for correct data.
    Parameters
    ----------
    file_name : str
        The name of the settings file to open
    Returns
    -------
    tuple
        Returns a tuple which consists of two parts: 
            - the first part is all information for input
            - the second part is all information for output
    """
    file_path = Path(file_name)
    pandas_inf_ini = pd.read_json(file_path, encoding="utf-8")
    if check_correctness_ini(pandas_inf_ini):
        print('OK')
        return (pandas_inf_ini['input'], pandas_inf_ini['output'])
    else:
        raise class_error.SettingsFileError()
    
def load_data(data: object, csv_file_name: str, encoding: str):
    """
    The function opens a main file checks it for correct data. 
    Writes data from the main file to an object variable of the Information class.
    Parameters
    ----------
    data : object
        Object of class Information, for writing the main file
    csv_file_name : str
        The name of the main file to open
    encoding : str
        The encoding in which the files will be opened
    Returns
    -------
    None.
    """
    data.clear()
    file_path = Path(csv_file_name)
    data.set_info(pd.read_csv(file_path, encoding= encoding, sep=';', decimal=".", \
                              dtype={'yyyy': 'object', 'rain': 'int64', 'avgt': 'float64', \
    'hum': 'float64', 'maxt': 'float64', 'wind': 'float64', \
    'mint': 'float64', 'mm': 'int64', 'dd': 'int64'}))
    if check_correctness_csv(data):
        print('OK')
    else:
        raise class_error.CsvError()
    

def load_stat(json_file_name: str, encoding: str) -> tuple:
    """
    The function opens an additional file
    checks it for correct data.
    Parameters
    ----------
    json_file_name : str
        The name of the additional file to open
    encoding : str
        The encoding in which the files will be opened
    Returns
    -------
    tuple
        A tuple of three elements that are present in an additional file 
        (for checking data with the main file)
    """
    file_path = Path(json_file_name)
    json = pd.read_json(file_path, encoding = encoding, orient = 'index')
    if check_correctness_json(json):
        print('OK')
        year, month, wind = json.index
        year_js = json.loc[year][0]
        month_js = json.loc[month][0]
        wind_js = json.loc[wind][0]
        return (year_js, month_js, wind_js)
    else:
        raise class_error.JsonError()
    
    
def load_file(data: class_information.Information, csv_file_name: str, json_file_name: str, encoding: str):
    """
    The function calls 3 sub-functions:
        - loads the main file
        - loads an additional file
        - checks the coincidence of the data of the primary and secondary files
    Parameters
    ----------
    data : class_information.Information
        Object of class Information, for writing the main file
    csv_file_name : str
        The name of the main file to open
    json_file_name : str
        The name of the additional file to open
    encoding : str
        The encoding in which the files will be opened
    Returns
    -------
    None.
    """
    try:
        print('input-csv ' + csv_file_name + ' : ', end = "")
        load_data(data, csv_file_name, encoding)
    except OSError:
        raise class_error.OpenCsvError()
    except LookupError:
        raise class_error.OpenCsvError()
    try:
        print('input-json ' + json_file_name + ' : ', end = "")
        json = load_stat(json_file_name, encoding)
    except OSError:
        raise class_error.OpenJsonError()
    print("json?=csv: ", end = "")
    if check_compliance_csv_to_json(data, json):            
         print("OK")
    else:
        raise class_error.ComplianceCsvJsonError()