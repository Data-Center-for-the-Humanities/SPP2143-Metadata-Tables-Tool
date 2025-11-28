#Harvest metadata from repo
# 
#Given an name ID.

local_file = False

#Libraries
import requests
import json

#Parameters for test
test_id = "https://repo.dainst.org/dataset/spielende-krieger-katalog"

#Constant Values only for this repository
#None

#Retrieves the whole json object and saves it to the variable data

def get_metadata(uri):
    arachne_api = "https://repo.dainst.org/api/3/action/package_show?id="
    data = {}
    entity_id = uri.split("/")[-1]  # Extract the entity ID from the URI
    url = arachne_api + entity_id
    response = requests.get(url)
    data = response.json()
    data = data["result"]
    return data

data = get_metadata(test_id)
#print(data)

#1. has_identifier
#set manually while creating a new dataset

#2. has_title
def get_title(data):
    maintitle = data["title"]
    subtitle = data["subtitle"]
    if subtitle:
        title = f"{maintitle}: {subtitle}"
    else:
        title = maintitle
    return title

title = get_title(data)
print(title)

#3. has_description
def get_description(data):
    description = data['notes']
    return description

description = get_description(data)
print(description)

#4. was_issued
def get_was_issued(data):
    was_issued = data['doi_date_published']
    return was_issued

was_issued = get_was_issued(data)
print(was_issued)

#5. was_modified
def get_was_modified(data):
    was_modified = data['metadata_modified']
    was_modified = was_modified.split("T")[0]
    return was_modified

was_modified = get_was_modified(data)
print(was_modified)

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
    author_string = data['author']
    author_list = author_string.split(' ')
    first_name = author_list[0]
    last_name = author_list[1]
    has_creator = f"{first_name} {last_name}"
    return has_creator

has_creator = get_creator(data)
print(has_creator)

#9. has_owner
#set manually
def get_owner(data):
    has_owner = get_creator(data)
    return has_owner

#10. has_responsible
#set manually
def get_responsible(data):
    has_responsible = 'not_defined'
    return has_responsible

#11. has_original_id
def get_original_id(data):
    has_original_id = data["doi"]
    return has_original_id

has_original_id = get_original_id(data)
print(has_original_id)

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
    language = data['in_language']
    return language

has_language = get_language(data)
print(has_language)

#17. was_created_on
def get_was_created_on(data):
    was_created_on = data['metadata_created']
    was_created_on = was_created_on.split("T")[0]
    return was_created_on

was_created_on = get_was_created_on(data)
print(was_created_on)

#18. has_landing_page
#set manually while creating a new dataset

#19. has_access_policy
def get_access_policy(data):
    policy = data['license_url']
    return policy

has_access_policy = get_access_policy(data)
print(has_access_policy)

#20. has_access_rights
def get_access_rights(data):
    rights = data['license_id']
    return rights

has_access_rights = get_access_rights(data)
print(has_access_rights)

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
    native_period = 'unavailable'
    return native_period

#has_native_period = get_native_period(data)
#print(has_native_period)

#24. has_chronontology_uri
def get_chronontology_uri(data):
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
    value = 'unavailable'
    return value

#35. point_has_place_name
def point_get_place_name(data):
    place_name = 'not_defined'
    return place_name


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
    lat = 'unavailable'
    return lat

#40. has_longitude
def get_lon(data):
    lon = 'unavailable'
    return lon

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