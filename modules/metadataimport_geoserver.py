#Harvest metadata from Geoserver
# 
#Da wir die API nicht ansteuern können, muss der Dublin-Core Metadatensatz zu einem Datenlayer manuell heuntergeladen werden.
#Der Metadatensatz wird in einem XML-File gespeichert.
#
#Metadaten einer Karte können nicht heruntergeladen werden.
# 
#Given an Dublin-Core XML metadata file

local_file = True

#Libraries
import xml.etree.ElementTree as ET

#Parameters for test
testdata = "K:\\FAIR.rdm AAArC 5\\Systeme\\ARIADNE RI\\Metadata_Tables_Tool\\Testläufe\Archaeobotanical Shea Tree Evidence_Dublin_Core_Metadata.xml"

#Constant Values only for this repository
# has language = german
# has_access_rights = BY-NC-ND 3.0
# has_access_policy = https://arachne.dainst.org/info/order

#Retrieves the whole json object and saves it to the variable data

def get_metadata(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()
    return root

#data, root = get_metadata(testdata)
#print(data, root)

#1. has_identifier
#set manually while creating a new dataset

#2. has_title
def get_title(root):
    for object in root.iter('{http://purl.org/dc/elements/1.1/}title'):
        title = object.text
    return title

title = get_title(get_metadata(testdata))
print(title)

#3. has_description
def get_description(root):
    for object in root.iter('{http://purl.org/dc/terms/}abstract'):
        description = object.text
    return description

description = get_description(get_metadata(testdata))
print(description)

#4. was_issued
def get_was_issued(root):
    for object in root.iter('{http://purl.org/dc/elements/1.1/}date'):
        was_issued = object.text
        was_issued = was_issued.split('T')[0]
    return was_issued

was_issued = get_was_issued(get_metadata(testdata))
print(was_issued)

#5. was_modified
def get_was_modified(root):
    for object in root.iter('{http://purl.org/dc/terms/}modified'):
        was_modified = object.text
        was_modified = was_modified.split('T')[0]
    return was_modified

was_modified = get_was_modified(get_metadata(testdata))
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
def get_creator(root):
    for object in root.iter('{http://purl.org/dc/elements/1.1/}creator'):
        has_creator = object.text 
    return has_creator

has_creator = get_creator(get_metadata(testdata))
print(has_creator)

#9. has_owner
#set manually
def get_owner(root):
    for object in root.iter('{http://purl.org/dc/elements/1.1/}creator'):
        has_owner = object.text
    return has_owner

has_owner = get_owner(get_metadata(testdata))
print(has_owner)

#10. has_responsible
#set manually
def get_responsible(data):
    has_responsible = 'not_defined'
    return has_responsible

#11. has_original_id
def get_original_id(root):
    for object in root.iter('{http://purl.org/dc/terms/}references'):
        if object.get('scheme') == 'WWW:LINK-1.0-http--link':
            has_original_id = object.text
            return has_original_id
    return 'not_defined'

has_original_id = get_original_id(get_metadata(testdata))
print(has_original_id)

#12. has_ARIADNE_subject
#set manually
def get_ariadne_subject(data):
    has_ariadne_subject = 'not_defined'
    return has_ariadne_subject

#13. has_native_subject
#set manually
def get_native_subject(root):
    subjects = []
    for object in root.iter('{http://purl.org/dc/elements/1.1/}subject'):
        subjects.append(object.text)
    has_native_subject = ", ".join(subjects)
    return has_native_subject

has_native_subject = get_native_subject(get_metadata(testdata))
print(has_native_subject)

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
def get_language(root):
    for object in root.iter('{http://purl.org/dc/elements/1.1/}language'):
        language = object.text
    return language

has_language = get_language(get_metadata(testdata))
print(has_language)

#17. was_created_on
#set manually
def get_was_created_on(data):
    was_created_on = 'not_defined'
    return was_created_on

#18. has_landing_page
#set manually while creating a new dataset

#19. has_access_policy
def get_access_policy(data):
    policy = 'not_defined'
    return policy

#has_access_policy = get_access_policy(data)
#print(has_access_policy)

#20. has_access_rights
def get_access_rights(data):
    rights = 'not_defined'
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
    native_period = 'not_defined'
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
def get_bb_coordinate_system(root):
    for object in root.iter('{http://purl.org/dc/terms/}spatial'):
        has_bb_coordinate_system = object.text
    return has_bb_coordinate_system

bb_cooidinate_system = get_bb_coordinate_system(get_metadata(testdata))
print(bb_cooidinate_system)

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
def get_bb_min_lat(root):
    for object in root.iter('{http://www.opengis.net/ows}LowerCorner'):
        has_bb_min_lat = object.text
        has_bb_min_lat = has_bb_min_lat.split(" ")[1]
    return has_bb_min_lat

bb_min_lat = get_bb_min_lat(get_metadata(testdata))
print(bb_min_lat)

#32. has_bounding_box_min_lon
def get_bb_min_lon(root):
    for object in root.iter('{http://www.opengis.net/ows}LowerCorner'):
        has_bb_min_lon = object.text
        has_bb_min_lon = has_bb_min_lon.split(" ")[0]
    return has_bb_min_lon

bb_min_lon = get_bb_min_lon(get_metadata(testdata))
print(bb_min_lon)

#33. has_bounding_box_max_lat
def get_bb_max_lat(root):
    for object in root.iter('{http://www.opengis.net/ows}UpperCorner'):
        has_bb_max_lat = object.text
        has_bb_max_lat = has_bb_max_lat.split(" ")[1]
    return has_bb_max_lat

bb_max_lat = get_bb_max_lat(get_metadata(testdata))
print(bb_max_lat)

#34. has_bounding_box_max_lon
def get_bb_max_lon(root):
    for object in root.iter('{http://www.opengis.net/ows}UpperCorner'):
        has_bb_max_lon = object.text
        has_bb_max_lon = has_bb_max_lon.split(" ")[0]
    return has_bb_max_lon

bb_max_lon = get_bb_max_lon(get_metadata(testdata))
print(bb_max_lon)

#Point

#if has_point
def has_point(data):
    value = 'not_defined'
    return value
    
#point = has_point(data)
#print(point)

#35. point_has_place_name
def point_get_place_name(data):
    place_name = 'not_defined'
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
    lat = 'not_defined'
    return lat

#point_lat = get_lat(data)
#print(point_lat)

#40. has_longitude
def get_lon(data):
    lon = 'not_defined'
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