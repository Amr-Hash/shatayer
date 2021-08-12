import pandas as pd
import demjson
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

def get_cities_from_json(file_path):
    with open(file_path, encoding='utf-8') as f:
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

def get_cities():
    english_citites = get_cities_from_json('data/en-lookups.json')
    english_citites.set_index('uuid', inplace=True)
    english_citites['name_en'] = english_citites.name
    
    arabic_citites = get_cities_from_json('data/ar-lookups.json')
    arabic_citites.set_index('uuid', inplace=True)
    arabic_citites.rename(columns={'name': 'name_ar'}, inplace=True)
    arabic_citites.drop('country_id', 1, inplace=True)

    return pd.concat([english_citites, arabic_citites], axis=1)

def get_areas_from_json(file_path):
    with open(file_path, encoding='utf-8') as f:
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

def get_areas():
    english_areas = get_areas_from_json('data/en-lookups.json')
    english_areas.set_index('uuid', inplace=True)
    english_areas['name_en'] = english_areas.name
    
    arabic_areas = get_areas_from_json('data/ar-lookups.json')
    arabic_areas.set_index('uuid', inplace=True)
    arabic_areas.rename(columns={'name': 'name_ar'}, inplace=True)
    arabic_areas.drop('city_id', 1, inplace=True)
    arabic_areas.drop('lon', 1, inplace=True)
    arabic_areas.drop('lat', 1, inplace=True)
    
    return pd.concat([english_areas, arabic_areas], axis=1)


def get_zones_from_json(file_path):
    with open(file_path, encoding='utf-8') as f:
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

def get_zones():
    english_zones = get_zones_from_json('data/en-lookups.json')
    english_zones.set_index('uuid', inplace=True)
    english_zones['name_en'] = english_zones.name
    
    arabic_zones = get_zones_from_json('data/ar-lookups.json')
    arabic_zones.set_index('uuid', inplace=True)
    arabic_zones.rename(columns={'name': 'name_ar'}, inplace=True)
    arabic_zones.drop('area_id', 1, inplace=True)
    arabic_zones.drop('lon', 1, inplace=True)
    arabic_zones.drop('lat', 1, inplace=True)
    
    return pd.concat([english_zones, arabic_zones], axis=1)

def insert_into_table(table_name, df):
    db = os.environ.get('POSTGRES_DB', 'x')
    user = os.environ.get('POSTGRES_USER', 'x')
    password =  os.environ.get('POSTGRES_PASSWORD', 'x')
    host = os.environ.get('POSTGRES_HOST', 'x')

    engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}/{db}", echo=False)
    df.to_sql(table_name, con=engine, if_exists='append')

def main():
    # insert_into_table('location_city', get_cities())
    # insert_into_table('location_area', get_areas())
    # insert_into_table('location_zone', get_zones())
    pass
    
if __name__ == "__main__":
    main()
    