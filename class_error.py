"""
@author: Kyrychek Mykola Pavlovich, K-11, variant = 89
Class for inheritance of errors, info of student and condition help-assistant
"""

class Error(Exception):
    def __str__(self):
        """
        Returns
        -------
        str
            Class for inheritance of errors
        """
        return ''

class CMDError(Error):
    def __str__(self):
        """
        Returns
        -------
        str
            If std input was wrong
        """
        return '***** program aborted *****\n***** command line error *****'

class SettingsFileError(Error):
    def __str__(self):
        """
        Returns
        -------
        str
            If settings file has wrong data
        """
        return '***** program aborted *****\n***** init file error *****'

class OpenCsvError(Error):
    def __str__(self):
        """
        Returns
        -------
        str
            If some problems happened with opening of main file
        """
        return '***** program aborted *****\n***** can not read input csv-file *****'

class OpenJsonError(Error):
    def __str__(self):
        """
        Returns
        -------
        str
            If some problems happened with opening of additional file
        """
        return '***** program aborted *****\n***** can not read input json-file *****'

class CsvError(Error):
    def __str__(self):
        """
        Returns
        -------
        str
            If some problems happened with reading main file
        """
        return '***** program aborted *****\n***** incorrect input csv-file *****'

class JsonError(Error):
    def __str__(self):
        """
        Returns
        -------
        str
            If some problems happened with reading additional file
        """
        return '***** program aborted *****\n***** incorrect input json-file *****'

class ComplianceCsvJsonError(Error):
    def __str__(self):
        """
        Returns
        -------
        str
            If the data of the main and additional files do not match
        """
        return '***** program aborted *****\n***** inconsistent information *****'
    
class OutputError(Error):
    def __str__(self):
        """
        Returns
        -------
        str
            If result can not be written in output file
        """
        return '***** program aborted *****\n***** can not write output file *****'

def working_out():
    """
    When function in process
    Returns
    -------
    None.
    """
    print("*****")

def student_info():
    """
    Displays information about author of programm
    Returns
    -------
    None.
    """
    print("Author: Kyrychek Mykola Pavlovich, K-11, variant = 89\n")
    
def condition_info():
    """
    Displays information about the task, what you need to output to the file/console
    Returns
    -------
    None.
    """
    print("Знайти 8 дат, по яких фіксувалася найменша максимальна денна температура. \
Вивести по кожній з них інформацію, на першому рядку:\n\
1) відношення кількості опадів до вологості\n\
2) місяць\n\
3) день\n\
4) рік\n\
5) середня максимальна температура\n\
На наступних рядках вивести для дати спостереження метеостанції, \
де сила вітру була принаймні тричі більша за вологість:\n\
1) середня денна температура\n\
2) максимальна денна температура\n\
3) мінімальна денна температура\n\
4) сила вітру\n\
5) вологість\n\
6) метеостанція")

def help_ini_error():
    """
    Help information about ini
    Returns
    -------
    None.
    """
    print("Перевірте файл з налаштуваннями. Він повинен мати в собі поля з назвами output, \
input, fname, csv, json, encoding.")
    
def help_cmd_error():
    """
    Help information about input in cmd
    Returns
    -------
    None.
    """
    print("Для того щоб программа правильно спрацювала, потрібно при її виклику вказати \
<ім'я файлу>.json/.ini який має в собі назви додвткового та основного файлів, \
кодування та, якщо потрібно, назву вихідного файлу.")
    help_ini_error()
    
def help_data_csv_error():
    """
    Help information about data in csv error
    Returns
    -------
    None.
    """
    print("Основний файл повинен мати в собі поля з назвами('yyyy', 'rain', 'avgt', \
'mm', 'dd', 'hum', 'maxt', 'wind', 'mint', 'meteo'), у правильному вигляді \
та типи даних повинні відповідати заданим типам.")
    
def help_open_csv_error():
    """
    Help information about open csv error
    Returns
    -------
    None.
    """
    print('В папці із кодом немає файла з назвою яка була дана в файлі з налаштуваннями. \
Потрібно вказати правильну назву файла, перевірити кодування та правильність основного файлу.')
    help_data_csv_error()
    
def help_data_json_error():
    """
    Help information about data in json error
    Returns
    -------
    None.
    """
    print('Додатковий файл повинен мати в собі поля з назвами та дані \
які є статистикою за основним файлом, у правильному вигляді \
та типи даних повинні відповідати заданим типам.')
    
def help_open_json_error():
    """
    Help information about open json error
    Returns
    -------
    None.
    """
    print('В папці із кодом немає файла з назвою яка була дана в файлі з налаштуваннями. \
Потрібно вказати правильну назву файла, перевірити кодування та правильність додаткового файлу.')
    help_data_json_error()

def help_csv_to_json_error():
    """
    Help information about data match in csv and json error
    Returns
    -------
    None.
    """
    print('Дані з основного файлу та додаткового не співпали, потрібно перевірити корекність даних.')    
    
def help_output_error():
    """
    Help information about writting in output file error
    Returns
    -------
    None.
    """
    print('Перевірте правильність назви, розширення та кодування вихідного файлу. \
Программа не може записати дані до цього файлу.')
    
def program_assistant(error):   
    if str(error) == '***** program aborted *****\n***** command line error *****':
        help_cmd_error()
    elif str(error) == '***** program aborted *****\n***** init file error *****':
        help_ini_error()
    elif str(error) == '***** program aborted *****\n***** can not read input csv-file *****':
        help_open_csv_error()
    elif str(error) == '***** program aborted *****\n***** can not read input json-file *****':
        help_open_json_error()
    elif str(error) == '***** program aborted *****\n***** incorrect input csv-file *****':
        help_data_csv_error()
    elif str(error) == '***** program aborted *****\n***** incorrect input json-file *****':
        help_data_json_error()
    elif str(error) == '***** program aborted *****\n***** inconsistent information *****':
        help_csv_to_json_error()
    elif str(error) == '***** program aborted *****\n***** can not write output file *****':
        help_output_error()