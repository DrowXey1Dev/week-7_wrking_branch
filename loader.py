'''
Script to load geographical data into a pandas DataFrame, and save it as a CSV file.
'''
#-----IMPORTS-----#
from geopy.geocoders import Nominatim
from geopyexc import GeocoderTimedOut, GeocoderServiceError
import pandas as pd


def get_geolocator(agent='h501-student'):
    """
    Initiate a Nominatim geolocator instance given an `agent`.

    Parameters
    ----------
    agent : str, optional
        Agent name for Nominatim, by default 'h501-student'
    """
    return Nominatim(user_agent=agent)



def fetch_location_data(geolocator, loc):

    #try catch to handle location not being found. Return NaN values instead
    try:
        #the code below catches timeout/service exceptions raised. Imports seem to be broken im not sure if im missing something
        #or if im supposed to fix that. Assuming that the imports were not broken this would catch.
        location = geolocator.geocode(loc)


        #if a network error or service error occurs, return a dictionary with the original
        #location string and NaN values for other fields
    except (GeocoderTimedOut, GeocoderServiceError) as error:
        return {"location": loc, "latitude": float('nan'),
                "longitude": float('nan'), "type": float('nan')}
    
    #handle invalid or unresolvable location
    if location is None:
        return {"location": loc, "latitude": float('nan'),
                "longitude": float('nan'), "type": float('nan')}

    #return entire block of valid info
    return {
        "location": loc,
        "latitude": location.latitude,
        "longitude": location.longitude,
        "type": getattr(location, 'geojson', {}).get('type', 'Unknown')
    }


def build_geo_dataframe(locations):

    #build a panda df from the list of location names
    geolocator = get_geolocator()
    geo_data = [fetch_location_data(geolocator, loc) for loc in locations]
    return pd.DataFrame(geo_data)




#-------------------------------------------------------------------#
#-----MAIN-----#
if __name__ == "__main__":
    #sample list of locations demonstrating valid and invalid entries
    locations = ["Museum of Modern Art", "iuyt8765(*&)", "Alaska", "Franklin's Barbecue", "Burj Khalifa"]
    #build the DataFrame by geocoding each entry
    df = build_geo_dataframe(locations)
    #column from the saved CSV so the file contains only the data columns
    df.to_csv("./geo_data.csv", index=False)
    print(df)
