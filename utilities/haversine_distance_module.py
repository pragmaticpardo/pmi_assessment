import numpy as np
import pandas as pd
import gc
import geopy.distance

def append_haversine_distance(
    df,
    identifier_feature,
    origin_latitude,
    origin_longitude,
    destination_latitude,
    destination_longitude):
    """
    Function that accepts a pandas dataframe with origin and destination
    features for latitude and longitud geopositional points and returns
    the haversine distance value between origin and destination coordinates
    in km

    Parameters:
    df (pandas.DataFrame): Dataframe containing the geopositional points
    origin_latitude (str): name of latitude origin point feature
    origin_longitude (str): name of longitude origin point feature
    destination_latitude (str): name of latitude destination point feature
    destination_longitude (str): name of longitude destination point feature

    Returns:
    haversine_distance (float)
    """
    def haversine_lambda(df):
        origin_coordinates = (df[origin_latitude], df[origin_longitude])
        destination_coordinates = (df[destination_latitude], df[destination_longitude])
        haversine_distance = (geopy
                              .distance
                              .distance(
                                  origin_coordinates,
                                  destination_coordinates)
                              .kilometers)
        return haversine_distance
    
    travelled_distance_array = (df.groupby(identifier_feature)
                                [[origin_latitude,
                                 origin_longitude,
                                 destination_latitude,
                                 destination_longitude
                                ]]).first().apply(haversine_lambda,axis=1)
    travelled_distance_array = travelled_distance_array.to_frame()
    travelled_distance_array.columns = ['travelled_distance_km']
    df = df.merge(travelled_distance_array, on=identifier_feature)
    
    del travelled_distance_array
    gc.collect()
    
    return df