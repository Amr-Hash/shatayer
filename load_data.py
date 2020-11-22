import pandas as pd
import demjson
from sqlalchemy import create_engine

def cities_dataframe():
    with open('data/ar-lookups.json', encoding='utf-8') as f:
        data = demjson.decode(f.read())
        cities = pd.DataFrame(data['lookups']['cities'])
        
        cities['uuid'] = cities['uuid'].str.strip()
        cities['uuid'] = cities['uuid'].str.replace("-","")

        cities = cities.merge(pd.DataFrame(cities['ref'].apply(pd.Series)), right_index=True, left_index=True)
        cities.rename(columns={'countryUUID': 'country_id'}, inplace=True)
        cities['country_id'] = cities['country_id'].str.strip()
        cities['country_id'] = cities['country_id'].str.replace("-","")
        cities = cities.drop('ref',1)
        
        cities = cities.merge(pd.DataFrame(cities['data'].apply(pd.Series)), right_index=True, left_index=True)
        cities = cities.drop('data',1)
        
        return cities

def areas_dataframe():
    with open('data/ar-lookups.json', encoding='utf-8') as f:
        data = demjson.decode(f.read())
        areas = pd.DataFrame(data['lookups']['areas'])
        
        areas['uuid'] = areas['uuid'].str.strip()
        areas['uuid'] = areas['uuid'].str.replace("-","")

        areas = areas.merge(pd.DataFrame(areas['ref'].apply(pd.Series)), right_index=True, left_index=True)
        areas.rename(columns={'cityUUID': 'city_id'}, inplace=True)
        areas['city_id'] = areas['city_id'].str.strip()
        areas['city_id'] = areas['city_id'].str.replace("-","")
        areas = areas.drop('ref',1)
        
        areas = areas.merge(pd.DataFrame(areas['data'].apply(pd.Series)), right_index=True, left_index=True)
        areas = areas.drop('data',1)
        
        areas = areas.merge(pd.DataFrame(areas['centerLocation'].apply(pd.Series)), right_index=True, left_index=True)
        areas = areas.drop('centerLocation',1)
        
        areas['lat'] = areas['lat'].astype(float)
        areas['lon'] = areas['lon'].astype(float)
        
        areas = areas[['uuid', 'name', 'city_id', 'lat', 'lon']]    
        
        return areas

def zones_dataframe():
    with open('data/ar-lookups.json', encoding='utf-8') as f:
        data = demjson.decode(f.read())
        zones = pd.DataFrame(data['lookups']['zones'])
        
        zones['uuid'] = zones['uuid'].str.strip()
        zones['uuid'] = zones['uuid'].str.replace("-","")

        zones = zones.merge(pd.DataFrame(zones['ref'].apply(pd.Series)), right_index=True, left_index=True)
        zones.rename(columns={'areaUUID': 'area_id'}, inplace=True)
        zones['area_id'] = zones['area_id'].str.strip()
        zones['area_id'] = zones['area_id'].str.replace("-","")
        zones = zones.drop('ref',1)
        
        zones = zones.merge(pd.DataFrame(zones['data'].apply(pd.Series)), right_index=True, left_index=True)
        zones = zones.drop('data',1)
        
        zones = zones.merge(pd.DataFrame(zones['centerLocation'].apply(pd.Series)), right_index=True, left_index=True)
        zones = zones.drop('centerLocation',1)
        
        zones['lat'] = zones['lat'].astype(float)
        zones['lon'] = zones['lon'].astype(float)
        
        zones = zones[['uuid', 'name', 'area_id', 'lat', 'lon']]    
        
        return zones

def insert_into_table(table_name, df):
    engine = create_engine('sqlite:///db.sqlite3', echo=False)
    df.to_sql(table_name, con=engine, if_exists='append', index=False)

def main():
    # insert_into_table('menus_city', cities_dataframe())
    # insert_into_table('menus_area', areas_dataframe())
    insert_into_table('menus_zone', zones_dataframe())
    
if __name__ == "__main__":
    main()
    