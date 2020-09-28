"""
@author: Kyrychek Mykola Pavlovich, K-11, variant = 89
The Information class 
    - saves the data of the main file
    - analyzes this data
    - displays data
"""
import pandas as pd
from pathlib import Path
import class_error

class Information():
    def __init__(self):
        """
        The Information class 
        Returns
        -------
        None.
        """
        self.data = ''
    
    def clear(self):
        """
        Function clears a variable in a class
        Returns
        -------
        None.
        """
        self.data = ''
    
    def _output(self, output_file_name: str or bool, encoding: str, output_data: pd.core.frame.DataFrame):
        """
        The function groups the data frame by keys and 
        prints the required values to the console or writes to a file
        Parameters
        ----------
        output_file_name : str or bool
            The name of the exit file to open, or bool operator
        encoding : str
            The encoding in which the files will be opened
        group_data : pd.core.frame.DataFrame
            Sorted dataFrame with the required data for output
        Returns
        -------
        None.
        """
        if output_file_name:
            with open(Path(output_file_name), encoding = encoding, mode = 'w') as file:
                for label, g in output_data.groupby(['mm', 'dd', 'yyyy'], sort = False):
                    file.write(str(g['ratio'][0]) + '\t')
                    file.write(str(label[0]) + '\t')
                    file.write(str(label[1]) + '\t')
                    file.write(str(label[2]) + '\t')
                    file.write(str( g['mean_maxt'][0]) + '\n')
                    if g['kind'][0] == 1:
                        for i, j in g.sort_values(['wind', 'meteo']).iterrows():
                            file.write('\t' + str(j['avgt']) + ' ')  
                            file.write(str(j['maxt']) + ' ')
                            file.write(str(j['mint']) + ' ')
                            file.write(str(j['wind']) + ' ')
                            file.write(str(j['hum']) + ' ')
                            file.write(str(j['meteo']) + '\n')
            print('OK')
        else:
            for label, g in output_data.groupby(['mm', 'dd', 'yyyy'], sort = False):
                print(g['ratio'][0], *label[0:3], g['mean_maxt'][0], sep = '\t')
                if g['kind'][0] == 1:
                    for i, j in g.sort_values(['wind', 'meteo']).iterrows():
                        print('\t',j['avgt'],
                              j['maxt'],
                              j['mint'],
                              j['wind'],
                              j['hum'],
                              j['meteo'], sep = ' ') 
            
                    
    def set_info(self, data: pd.DataFrame):
        """
        The function writes information (data from the main file) 
        to a variable in the class
        Parameters
        ----------
        data : pd.DataFrame
            Data from the main file
        Returns
        -------
        None.
        """
        self.data = data
        
    def data_analysis(self, output_file_name: str, encoding: str):
        """
        The function analyzes the data, sorts the data
        and then calls the information output function
        Parameters
        ----------
        output_file_name : str
            The name of the exit file to open
        encoding : str
            The encoding in which the files will be opened
        Returns
        -------
        None.
        """
        self.data.reset_index(inplace = True)
        self.data['mean_maxt'] = round(self.data.groupby(['yyyy', 'mm', 'dd'])['maxt'].transform('mean'), 2)
        self.data['ratio'] = round(self.data.groupby(['yyyy', 'mm', 'dd'])['rain'].transform('mean') /\
                                   self.data.groupby(['yyyy', 'mm', 'dd'])['hum'].transform('mean'), 3)
        self.data['kind'] = 0                  
        self.data.loc[(self.data['wind'] >= 3*self.data['hum']),'kind'] = 1
        low = self.data.groupby(['mm', 'dd', 'yyyy', 'meteo'])['maxt'].agg('min').nsmallest(n = 8, keep='all').rename('min_maxt') 
        output_data = pd.merge(low, self.data.set_index(['dd', 'mm', 'yyyy', 'meteo']), how='outer', left_index=True,
                                 right_index=True).dropna().drop(columns=['min_maxt']).sort_values(by=['ratio', 'mm', 'dd', 'yyyy'],\
                                 ascending=[False,True,True,True]).reset_index().set_index(['mm', 'dd', 'yyyy'])
        if len(output_file_name) == 0:
            print('output stdout:')
            self._output(False, encoding, output_data)
        else:
            try:
                print('output ' + output_file_name + ' : ', end = "")
                self._output(output_file_name, encoding, output_data)
            except Exception:
                print('UPS')
                raise class_error.OutputError()
            except LookupError:
                raise class_error.OutputError()