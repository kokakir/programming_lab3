"""
@author: Kyrychek Mykola Pavlovich, K-11, variant = 89
Main function
"""
import sys
import load_data
import class_information
import class_error
   
def std_input() -> int or str:
    """
    Function check whether right std input was given
    Returns
    -------
    int or str
    If correct, return it. Return 0(error_sign), otherwise.
    """
    res = 0
    if len(sys.argv) == 2:
        res = sys.argv[1]
    return res

def main(settings_file: str):
    """
    The function calls the function of downloading and checking all files
    then the data analysis function
    Parameters
    ----------
    settings_file : str
        The name of the settings file
        which is obtained from the command line
    Returns
    -------
    None.
    """
    class_error.student_info()
    class_error.condition_info()
    class_error.working_out()
    try:
        print('ini ' + settings_file + ' : ', end = "")
        ini = load_data.load_ini(settings_file)
    except OSError:
        raise class_error.SettingsFileError()
    except ValueError:
        raise class_error.SettingsFileError()
    data = class_information.Information()
    load_data.load_file(data, ini[0]['csv'], ini[0]['json'], ini[0]['encoding'])
    data.data_analysis(ini[1]['fname'], ini[1]['encoding'])
    
if __name__ == "__main__":
    try:
        file = std_input()
        if file:
            main(file) 
        else:
            raise class_error.CMDError()
    except class_error.Error as err:
        print('\n', err, '\n', sep = '')
        class_error.program_assistant(err)