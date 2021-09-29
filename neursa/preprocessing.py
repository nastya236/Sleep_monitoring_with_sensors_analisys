import pandas as pd
import numpy as np
from datetime import datetime


def get_labels(path):
    '''
    path: global path to csv file with sleeping stages
    '''
    stages = pd.read_csv(path)
    labels = stages[['Wonambi v6.17']].iloc[:, 0].values[1:]
    set_labels = set(labels)
    set_labels = sorted(list(set_labels))
    dict_labels = dict(zip(list(set_labels), np.arange(len(set_labels))))
    result_labels = np.array([dict_labels[i] for i in labels])

    return result_labels


def get_time_for_labels(path, date):
    '''
    path: global path to csv file with sleeping stages
    '''
    
    stages = pd.read_csv(path)
    time_array = stages[['Wonambi v6.17']].iloc[:, 0].index[1:]
    
    time_labels = [i[0] for i in time_array]
    size = len(time_labels)
    start_time = date + ' ' + time_labels[0]
    start_time = datetime.strptime(start_time, "%d.%m.%y %H:%M:%S")
    step = pd.to_timedelta('00:00:30')
    end_time = step * (size - 1) + start_time
    time = np.arange(start_time, 
                     end_time+step, step).astype('datetime64[ms]')
    return time

def time_preprocessing(time):
    new_time = []
    for i in time:
        h, m = i.split('h')
        h = h.strip(' ')
        m = m.strip(' ')
        new_time.append(f'{h}:{m}')
    return new_time

def parse_table_info(path_table = '/Users/anastasiafilippova/Downloads/SleepSensor_Recordings list.xlsx'):

    table = pd.read_excel(path_table)
    headers = table.iloc[3:4, 3:].values[0]
    values = table.iloc[4:, 3:]
    values.columns = headers
    ids = values['Code'].values
    date = values['Date enregistrement (soir)'].values
    start_time = values['L.off'].values
    start_time = time_preprocessing(start_time)
    end_time = values['L.on'].values
    end_time = time_preprocessing(end_time)
    delta = pd.to_datetime(end_time) - pd.to_datetime(start_time)
    delta = np.array([pd.to_timedelta(str(i)[-8:]) for i in delta])
    index = np.arange(len(start_time))
    date = [i[:6]+i.split('.')[-1][-2:] for i in date]
    start = [date[i]+' '+start_time[i] for i in index]
    start = np.array([datetime.strptime(start[i], "%d.%m.%y %H:%M") for i in index])
    end = start+delta
    info = pd.DataFrame({'start': start.astype('datetime64[ns]'),
                         'end': end.astype('datetime64[ns]'), 
                         'date': date})
    info.index = ids
    
    return info

def get_time_sensors(dataset):
    time = dataset.start_time+pd.to_timedelta(dataset.time[0], 's')
    return np.array(time).astype('datetime64[ns]')


