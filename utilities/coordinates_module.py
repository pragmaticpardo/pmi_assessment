import numpy as np
import pandas as pd
import gc

def append_origin_destination_coordinates(
    df,
    col_time,
    col_event,
    col_latitude,
    col_longitude):
    """
    Function that accepts a pandas dataframe with time, event, latitude
    and longitude features and appens the origin and destination 
    coordinates based on the time and event values

    Parameters:
    df (pandas.DataFrame): Dataframe containing the required features
    col_time (str): name of time feature
    col_event (str): name of event feature
    col_latitude (str): name of latitude feature
    col_longitude (str): name of longitude feature

    Returns:
    pandas.DataFrame
    """
    # order by time and group by event
    grouped_by_event = df.sort_values([col_time]).groupby(by=[col_event])
    
    # find origin coordinates
    origin_latitude = (grouped_by_event[col_latitude].first()).reset_index().rename(
        columns={col_latitude: 'origin_latitude'})
    origin_longitude = (grouped_by_event[col_longitude].first()).reset_index().rename(
        columns={col_longitude: 'origin_longitude'})
    
    # find destination coordinates
    destination_latitude = (grouped_by_event[col_latitude].last()).reset_index().rename(
        columns={col_latitude: 'destination_latitude'})
    destination_longitude = (grouped_by_event[col_longitude].last()).reset_index().rename(
        columns={col_longitude: 'destination_longitude'})
    
    # merge the arrays
    df = df.merge(origin_latitude, on=col_event)
    df = df.merge(destination_latitude, on=col_event)
    df = df.merge(origin_longitude, on=col_event)
    df = df.merge(destination_longitude, on=col_event)
    
    # make RAM happy
    del grouped_by_event, origin_latitude, origin_longitude, destination_latitude, destination_longitude
    gc.collect()
    
    return df
    
    