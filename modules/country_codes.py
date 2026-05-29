import geopandas as gpd
from shapely import wkt
import os


def create_wkt_from_point_coordinates(latitude, longitude):
    """
    Create a WKT point string from latitude and longitude coordinates.
    
    Args:
        latitude (float): Latitude coordinate (-90 to 90)
        longitude (float): Longitude coordinate (-180 to 180)
    Returns:
        str: WKT point string representing the coordinates
    """
    
    # Create WKT point string
    longitude = float(longitude[0])  # Convert from array to float
    latitude = float(latitude[0])    # Convert from array to float

    wkt_point = f"POINT ({longitude} {latitude})"
    
    return wkt_point

def create_wkt_from_bbox_coordinates(min_lat, min_lon, max_lat, max_lon):
    """
    Create a WKT polygon string from bounding box coordinates.
    
    Args:
        min_lat (float): Minimum latitude (south)
        min_lon (float): Minimum longitude (west)
        max_lat (float): Maximum latitude (north)
        max_lon (float): Maximum longitude (east)

    Returns:
        str: WKT polygon string representing the bounding box
    """
    min_lat = float(min_lat[0])
    min_lon = float(min_lon[0])
    max_lat = float(max_lat[0])
    max_lon = float(max_lon[0])

    # Create WKT polygon string
    wkt_polygon = f"POLYGON (({min_lon} {min_lat}, {min_lon} {max_lat}, {max_lon} {max_lat}, {max_lon} {min_lat}, {min_lon} {min_lat}))"
    
    return wkt_polygon

def create_wkt_from_polygon_coordinates(wkt_polygon):
    """
    Create a WKT polygon string from provided WKT polygon coordinates.
    
    Args:
        wkt_polygon (str): WKT polygon string representing the area of interest
    Returns:
        str: WKT polygon string representing the area of interest
    """
    return wkt_polygon[0]  # Assuming wkt_polygon is a list with one string element

def countries_from_wkt(wkt_string, module_dir=os.path.dirname(__file__)):
    # WKT in Geometrie umwandeln
    geom = wkt.loads(wkt_string)

    shapefile_path = os.path.join(module_dir, "ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp")

    #Check if file exists
    if not os.path.exists(shapefile_path):
        raise FileNotFoundError("The required shapefile 'ne_110m_admin_0_countries.shp' was not found. Please ensure it is in the correct directory.")
    else:
        print(f"Shapefile found at: {shapefile_path}")
    
    #get directory of this module
    shapefile_path = os.path.join(module_dir, "ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp")

    # Welt-Länder laden (Natural Earth Dataset)
    world = gpd.read_file(shapefile_path)

    # Geometrie als GeoDataFrame
    gdf = gpd.GeoDataFrame(geometry=[geom], crs="EPSG:4326")

    # Länder finden, die sich schneiden
    intersecting = world[world.intersects(geom)]

    #Create set
    code_set = set(intersecting["ISO_A3"])

    #Convert set to string
    code_string = ", ".join(code_set)

    # ISO alpha-3 Codes als Set zurückgeben
    return code_string


# Test with provided coordinates
if __name__ == "__main__":
    # Test point coordinates
    lat = ['7.8']
    long = ['9.4']
    
    codes = countries_from_wkt(create_wkt_from_point_coordinates(lat, long))
    print("point:")
    print(codes)

    # Test WKT polygon
    wkt_polygon = ['MULTIPOLYGON (((15.49693033248794549 14.5842891733467237, 11.90141951793591168 13.85480284196543899, 12.82120135421666518 11.73488917936738929, 16.38883999191170915 11.81674587642149987, 16.61181740676764917 13.20443796150061821, 15.49693033248794549 14.5842891733467237)))']

    wkt_string = ['POLYGON ((7 50, 7 51, 8 51, 8 50, 7 50))']

    codes = countries_from_wkt(wkt_polygon)
    print("polygon:")
    print(codes)

    #Test BBox
    min_lat = ['8.842752']
    min_lon = ['-16.039888']
    max_lat = ['21.967249']
    max_lon = ['39.676250']

    codes = countries_from_wkt(create_wkt_from_bbox_coordinates(min_lat, min_lon, max_lat, max_lon))
    print("bbox:")
    print(codes)







