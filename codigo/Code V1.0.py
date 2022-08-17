import geopandas as gpd
import pandas as pd
from shapely import wkt

city = pd.read_csv('poligono_de_medellin.csv',sep=';')
city['geometry'] = city['geometry'].apply(wkt.loads)    # Deletes bad geometries
city = gpd.GeoDataFrame(city)

data = pd.read_csv("calles_de_medellin_con_acoso.csv",sep=';')
data['geometry'] = data['geometry'].apply(wkt.loads)
edges = gpd.GeoDataFrame(data)

# The data is saved as a Pandas DataFrame :)
# You must download the .csv file from 
# https://raw.githubusercontent.com/mauriciotoro/ST0245-Eafit/master/proyecto/Datasets/poligono_de_medellin.csv
