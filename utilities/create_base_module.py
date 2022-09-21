import os
import numpy as np
import pandas as pd

def create_base_df(directory_path, base_column_names):
    """
    Creates a base pandas dataframe from a given directory with *.txt files

    Parameters:
    directory_path (str): path to the directory where *.txt files are found

    Returns:
    DataFrame
    """
    if os.path.isdir(directory_path):
        files = [file for file in os.listdir(directory_path) if file.endswith('.txt')]
        df = pd.DataFrame()
        
        for file in files:
            file_name = file.split('.')[0][4:]
            tmp_df = pd.read_csv(f'{directory_path}/{file}',
                                 header=None,
                                 sep=' ', 
                                 names=base_column_names)
            tmp_df['file_name'] = file_name
            tmp_df['id'] = file_name+'_'+tmp_df['time'].astype(str) 
    
            df = pd.concat([df, tmp_df], ignore_index=True)
        
        # Order df by id and time
        df = df.sort_values(['id', 'time']).reset_index(drop=True)    
        return df
        
    else:
        print('Please add a valid directory path')
        return