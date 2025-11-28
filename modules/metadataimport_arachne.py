#Harvest metadata from Arachne
# 
#Given an entity ID.

local_file = False

#Libraries
import requests
import json

#Parameters for test
test_id = "https://arachne.dainst.org/entity/6945889"
test_id2 = "https://arachne.dainst.org/entity/7120743"

#Constant Values only for this repository
# has language = german
# has_access_rights = BY-NC-ND 3.0
# has_access_policy = https://arachne.dainst.org/info/order

#Retrieves the whole json object and saves it to the variable data

def get_metadata(uri):
    arachne_api = "https://arachne.dainst.org/data/entity/"
    data = {}
    entity_id = uri.split("/")[-1]  # Extract the entity ID from the URI
    url = arachne_api + entity_id
    response = requests.get(url)
    data = response.json()
    return data

#data = get_metadata(test_id2)
#print(data)

#1. has_identifier
#set manually while creating a new dataset

#2. has_title
def get_title(data):
    title = data["title"]
    return title

#title = get_title(data)
#print(title)

#3. has_description
def get_description(data):
   sections = data["sections"][0]['content']
   for dict in sections:
      if 'label' in dict and dict['label'] == 'Beschreibung':
         description = dict['content'][0]['value']
         break
      else:
         description = 'not_defined'
   return description

#description = get_description(data)
#print(description)

#4. was_issued
#set manually
def get_was_issued(data):
    was_issued = 'not_defined'
    return was_issued

#5. was_modified
#set manually
def get_was_modified(data):
    was_modified = 'not_defined'
    return was_modified

#6. has_publisher
#constant value across all metadata
def get_publisher(data):
    has_publisher = "DCH"
    return has_publisher

#7. has_contributor
#constant value across all metadata
def get_contributor(data):
    has_contributor = "FAIR.rdm"
    return has_contributor

#8. has_creator
#set manually
def get_creator(data):
    has_creator = 'not_defined'
    return has_creator

#9. has_owner
#set manually
def get_owner(data):
    has_owner = 'not_defined'
    return has_owner

#10. has_responsible
#set manually
def get_responsible(data):
    has_responsible = 'not_defined'
    return has_responsible

#11. has_original_id
def get_original_id(data):
    has_original_id = data["entityId"]
    return has_original_id

#has_original_id = get_original_id(data)
#print(has_original_id)

#12. has_ARIADNE_subject
#set manually
def get_ariadne_subject(data):
    has_ariadne_subject = 'not_defined'
    return has_ariadne_subject

#13. has_native_subject
#set manually
def get_native_subject(data):
    has_native_subject = 'not_defined'
    return has_native_subject

#14. has_derived_subject_uri
#set manually
def get_derived_subject_uri(data):
    has_derived_subject_uri = 'not_defined'
    return has_derived_subject_uri

#15. has_derived_subject_term
#set manually
def get_derived_subject_term(data):
    has_derived_subject_term = 'not_defined'
    return has_derived_subject_term

#16. has_language
def get_language(data):
    language = "german"
    return language

#has_language = get_language(data)
#print(has_language)

#17. was_created_on
#set manually
def get_was_created_on(data):
    was_created_on = 'not_defined'
    return was_created_on

#18. has_landing_page
#set manually while creating a new dataset

#19. has_access_policy
def get_access_policy(data):
    policy = "https://arachne.dainst.org/info/order"
    return policy

#has_access_policy = get_access_policy(data)
#print(has_access_policy)

#20. has_access_rights
def get_access_rights(data):
    rights = "BY-NC-ND 3.0"
    return rights

#has_access_rights = get_access_rights(data)
#print(has_access_rights)

#21. has_extent
#set manually
def get_extent(data):
    has_extent = 'not_defined'
    return has_extent

#TEMPORAL COVERAGE
#Returns the temporal coverage of the entity

#22. has_periodo_uri
#set manually
def get_periodo_uri(data):
    has_periodo_uri = 'not_defined'
    return has_periodo_uri

#23. has_native_period
def get_native_period(data):
    if 'dates' in data:
        native_period = data["dates"]
        #Check if native period consits of equal items
        if all(item == native_period[0] for item in native_period):
            return native_period[0]
        else:
            period1 = native_period[0]['label']
            period2 = native_period[1]['label']
            native_period = f"{period1} - {period2}"
    else:
        native_period = 'unavailable'
    return native_period

#has_native_period = get_native_period(data)
#print(has_native_period)

#24. has_chronontology_uri
def get_chronontology_uri(data):
   sections = data["sections"][0]['content']
   for dict in sections:
      if 'label' in dict and dict['label'] == 'Datierung':
        dating = dict['content'][0]['value']
        dating = dating.split('"')
        uris = []
        for a in dating:
            if "chronontology" in a:
               uris.append(a)
        if len(uris) > 0:
           period1 = uris[0]
           period2 = uris[1]
           chronontology_uri = f"{period1} - {period2}"
           return chronontology_uri
        else:
           period = uris[0]
           chronontology_uri = period
           return chronontology_uri
      else:
         dating = 'not_defined'
   return dating

#has_chronontology_uri = get_chronontology_uri(data)
#print(has_chronontology_uri)

#25. from
#set manually
def get_from(data):
    has_from = 'not_defined'
    return has_from

#26. until
#set manually
def get_until(data):
    until = 'not_defined'
    return until

#SPATIAL COVERAGE
#Bounding Box

#27. bb_has_place_name
#set manually
def get_bb_place_name(data):
    has_bb_place_name = 'not_defined'
    return has_bb_place_name

#28. bb_has_coordinate system
#set manually
def get_bb_coordinate_system(data):
    has_bb_coordinate_system = 'not_defined'
    return has_bb_coordinate_system

#29. bb_country_code
#set manually
def get_bb_country_code(data):
    has_bb_country_code = 'not_defined'
    return has_bb_country_code

#30. bb_place_uri
#set manually
def get_bb_place_uri(data):
    has_bb_place_uri = 'not_defined'
    return has_bb_place_uri

#31. has_bounding_box_min_lat
#set manually
def get_bb_min_lat(data):
    has_bb_min_lat = 'not_defined'
    return has_bb_min_lat

#32. has_bounding_box_min_lon
#set manually
def get_bb_min_lon(data):
    has_bb_min_lon = 'not_defined'
    return has_bb_min_lon

#33. has_bounding_box_max_lat
#set manually
def get_bb_max_lat(data):
    has_bb_max_lat = 'not_defined'
    return has_bb_max_lat

#34. has_bounding_box_max_lon
#set manually
def get_bb_max_lon(data):
    has_bb_max_lon = 'not_defined'
    return has_bb_max_lon

#Point

#if has_point
def has_point(data):
    if "places" in data:
        gazid = data["places"][0]["gazetteerId"]
        gazuri = f'https://gazetteer.dainst.org/place/{gazid}.json'
        #get gazetteer data
        response = requests.get(gazuri)
        if response.status_code == 200:
            gaz_data = response.json()
            gaz_data = gaz_data['prefLocation']['coordinates']
            if len(gaz_data) == 2:
                value = 'is_point'
            else:
                value = 'is_not_point'
            return value
    else:
        value = 'unavailable'
        return value
    
#point = has_point(data)
#print(point)

#35. point_has_place_name
def point_get_place_name(data):
    gazid = data["places"][0]["gazetteerId"]
    gazuri = f'https://gazetteer.dainst.org/place/{gazid}.json'
    response = requests.get(gazuri)
    if response.status_code == 200:
        gaz_data = response.json()
        place_name = gaz_data['prefName']['title']
    return place_name

#has_place_name = point_get_place_name(data)
#print(has_place_name)

#36. point_has_coordinate_system
#set manually
def point_get_coordinate_system(data):
    has_coordinate_system = 'not_defined'
    return has_coordinate_system

#37. point_has_country_code
#set manually
def point_get_country_code(data):
    has_country_code = 'not_defined'
    return has_country_code

#38. point_has_place_uri
#set manually
def point_get_place_uri(data):
    has_place_uri = 'not_defined'
    return has_place_uri

#39. has_latitude
def get_lat(data):
    if has_point(data) == 'is_point':
        gazid = data["places"][0]["gazetteerId"]
        gazuri = f'https://gazetteer.dainst.org/place/{gazid}.json'
        #get gazetteer data
        response = requests.get(gazuri)
        if response.status_code == 200:
            gaz_data = response.json()
            lat = gaz_data['prefLocation']['coordinates'][1]
            return lat
    else:
        lat = 'unavailable'
        return lat

#point_lat = get_lat(data)
#print(point_lat)

#40. has_longitude
def get_lon(data):
    if has_point(data) == 'is_point':
        gazid = data["places"][0]["gazetteerId"]
        gazuri = f'https://gazetteer.dainst.org/place/{gazid}.json'
        #get gazetteer data
        response = requests.get(gazuri)
        if response.status_code == 200:
            gaz_data = response.json()
            lon = gaz_data['prefLocation']['coordinates'][0]
            return lon
    else:
        lon = 'unavailable'
        return lon

#point_lon = get_lon(data)
#print(point_lon)

#Polygon

#41. polygon_has_place_name
#set manually
def polygon_has_place_name(data):
    has_polygon_place_name = 'not_defined'
    return has_polygon_place_name

#42. polygon_has_coordinate_system
#set manually
def polygon_has_coordinate_system(data):
    has_polygon_coordinate_system = 'not_defined'
    return has_polygon_coordinate_system

#43. polygon_has_country_code
#set manually
def polygon_has_country_code(data):
    has_polygon_country_code = 'not_defined'
    return has_polygon_country_code

#44. polygon_has_place_uri
#set manually
def polygon_has_place_uri(data):
    has_polygon_place_uri = 'not_defined'
    return has_polygon_place_uri

#45. has_polygonal_representation
#set manually
def get_polygonal_representation(data):
    has_polygonal_representation = 'not_defined'
    return has_polygonal_representation

#46. has_visual_component
#set manually
def get_visual_component(data):
    has_visual_component = 'not_defined'
    return has_visual_component

#47. has_part
#set manually
def get_has_part(data):
    has_part = 'not_defined'
    return has_part

#48. is_part_of
#set manually
def get_is_part_of(data):
    is_part_of = 'not_defined'
    return is_part_of