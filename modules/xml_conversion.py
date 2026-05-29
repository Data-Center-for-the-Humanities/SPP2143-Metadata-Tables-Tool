#Conversion from tabular metatdata to XML format

#Libraries
import pandas as pd
import xml.dom.minidom
import os
from wikidata_country_info import process_country_codes

##############################################
#Testdata
#df_current_data = pd.read_excel('Z:/FAIR.rdm AAArC 5/Systeme/ARIADNE RI/Metadata_Tables_Tool/metadata_tables/Mege_Test.xlsx', sheet_name='metadata')
#df_current_data = df_current_data.fillna('not_defined')
#print(df_current_data.head())

#convert dataframe to dictionary with first column as key and second column as value and ignore the headers
#data_dict = df_current_data.set_index(df_current_data.columns[0]).T.to_dict()
#print(data_dict)

#############################################

#Retrieve registered persons

#df_registered_persons = pd.read_excel('Z:\\FAIR.rdm AAArC 5\\Systeme\\ARIADNE RI\\Metadata_Tables_Tool\\metadata_tables\\registered_persons.xlsx', sheet_name='person')
metadata_tables_path = os.path.join(os.path.dirname(__file__), "../metadata_tables")
df_registered_persons = pd.read_excel(os.path.join(metadata_tables_path, "registered_persons.xlsx"), sheet_name="person")


#print(df_registered_persons)




#Createe XML Namespace section

header = '<oai_dc:dc xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/" xmlns:crm="http://www.cidoc-crm.org/cidoc-crm/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dct="http://purl.org/dc/terms/" xmlns:foaf="http://xmlns.com/foaf/0.1/" xmlns:geo="http://www.w3.org/2003/01/geo/wgs84_pos#" xmlns:dch="http://oai.dch.phil-fak.uni-koeln.de/" xmlns:owl ="http://www.w3.org/2002/07/owl#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#">'
footer = '</oai_dc:dc>'

#Create Error Log
log = []

#Add error message to log
def error_log(message):
    log.append(message)

#Process and display error log
def display_error_log():
    if log:
        logsting = "\n".join(log)
        print(logsting)
        #empty log for next conversion
        log.clear()
        return logsting
    else:
        pass

#Check string for invalid characters
def check_string(valuesting):
    if "&" in valuesting:
        valuesting = valuesting.replace("&", "&amp;")
    if "<" in valuesting:
        valuesting = valuesting.replace("<", "&lt;")
    if ">" in valuesting:
        valuesting = valuesting.replace(">", "&gt;")
    if "'" in valuesting:
        valuesting = valuesting.replace("'", "&apos;")
    if '"' in valuesting:
        valuesting = valuesting.replace('"', "&quot;")
    if '/n' in valuesting:
        valuesting = valuesting.replace('/n', ' ')
    return valuesting

#Get person data from registered persons dataframe
def get_person_data(name, df_registered_persons):
    person_data = df_registered_persons[df_registered_persons['Name'] == name]
    if person_data.empty:
        xml_data = 'INVALID PERSON NAME. PLEASE CHECK SPELLING OR CREATE NEW ENTRY IN REGISTERED PERSONS.'
        return xml_data
    else:
        person_data.iloc[0].to_dict()
        #24. has_name, foaf, mandatory
        name = person_data['Name'].values[0]
        if name == "not_defined":
            name = "<foaf:name />"
        else:
            name = check_string(name)
            name = f"<foaf:name>{name}</foaf:name>"
        #25. has_agent_identifier, foaf, desirable
        identifier = person_data['Identifier'].values[0]
        if identifier == "not_defined":
            identifier = "<foaf:identifier />"
        else:
            identifier = check_string(identifier)
            identifier = f"<foaf:identifier>{identifier}</foaf:identifier>"
        #26. has_email, foaf, desirable
        email = person_data['Email'].values[0]
        if email == "not_defined":
            email = "<foaf:mbox />"
        else:
            email = check_string(email)
            email = f"<foaf:mbox>{email}</foaf:mbox>"
        #27. has_homepage, foaf, optional
        homepage = person_data['Homepage'].values[0]
        if homepage == "not_defined":
            homepage = "<foaf:homepage />"
        else:
            homepage = check_string(homepage)
            homepage = f"<foaf:homepage>{homepage}</foaf:homepage>"
        #28. has_institution, foaf, optional
        has_institution = person_data['HasInstitution'].values[0]
        if has_institution == "not_defined":
            has_institution = "<foaf:member />"
        else:
            has_institution = check_string(has_institution)
            has_institution = f"<foaf:member>{has_institution}</foaf:member>"
        xml_data = f"{name}{identifier}{email}{homepage}{has_institution}"
    return xml_data

###
#Individual functions to get XML elements from the data table

#1. has_identifier, dct, optional
def get_identifier(dict):
    value = dict.get('has_identifier')
    value = value.get('Metadata Value')
    value = str(value)
    if value == 'not_defined':
        value = '<dct:identifier />'
    else:
        value = check_string(value)
        value = f'<dct:identifier>{value}</dct:identifier>'
    return value

#Test single functions like this:
#identifier = get_identifier(data_dict)
#print(identifier)

#2. has_title, dct, mandatory, multiple values
def get_title(dict):
    value = dict.get('has_title')
    value = value.get('Metadata Value')
    value = str(value)
    if value == 'not_defined':
        value = '<dct:title />'
    else:
        value = check_string(value)
        value = value.split(", ")
        titles = []
        for element in value:
            if "@" not in element:
                error_log("Error: Title element does not contain language tag. Please check the format of the title element. It should be in the format 'Title@language'.")
                break
            element = element.split("@")
            lang = element[1]
            title = element[0]
            value = f'<dct:title xml:lang="{lang}">{title}</dct:title>'
            titles.append(value)
        value = "".join(titles)
    return value

#3. has_description, dct, desirable
def get_description(dict):
    value = dict.get('has_description')
    value = value.get('Metadata Value')
    if value == 'not_defined':
        value = '<dct:description />'
    else:
        value = check_string(value)
        value = f'<dct:description>{value}</dct:description>'
    return value

#4. was_issued, crm, mandatory
def get_issued(dict):
    value = dict.get('was_issued')
    value = value.get('Metadata Value')
    if value == 'not_defined':
        value = '<crm:P81_ongoing_through />'
    else:
        if "-" in value:
            date_elements = value.split("-")
            if len(date_elements) == 3:
                year = date_elements[0]
                month = date_elements[1]
                day = date_elements[2]
                if len(year) == 4 and len(month) == 2 and len(day) == 2:
                    month = int(month)
                    day = int(day)
                    if month < 1 or month > 12:
                        error_log("Error: Date value was_issued needs to be in the format 'YYYY-MM-DD' and month needs to be between 01 and 12.")
                    if day < 1 or day > 32:
                        error_log("Error: Date value was_issued needs to be in the format 'YYYY-MM-DD' and day needs to be between 01 and 31.")
                else:
                    error_log("Error: Date value was_issued needs to be in the format 'YYYY-MM-DD'")
            else:
                error_log("Error: Date value was_issued needs to be in the format 'YYYY-MM-DD'")
        else:
            error_log("Error: Date value was_issued needs to be in the format 'YYYY-MM-DD'")
        value = f'<crm:P81_ongoing_through>{value}</crm:P81_ongoing_through>'
    return value

#5. was_modified, dch, mandatory
def get_modified(dict):
    value = dict.get('was_modified')
    value = value.get('Metadata Value')
    if value == 'not_defined':
        value = '<dch:was_modified />'
    else:
        if "-" in value:
            date_elements = value.split("-")
            if len(date_elements) == 3:
                year = date_elements[0]
                month = date_elements[1]
                day = date_elements[2]
                if len(year) == 4 and len(month) == 2 and len(day) == 2:
                    month = int(month)
                    day = int(day)
                    if month < 1 or month > 12:
                        error_log("Error: Date value was_modified needs to be in the format 'YYYY-MM-DD' and month needs to be between 01 and 12.")
                    if day < 1 or day > 32:
                        error_log("Error: Date value was_modified needs to be in the format 'YYYY-MM-DD' and day needs to be between 01 and 31.")
                else:
                    error_log("Error: Date value was_modified needs to be in the format 'YYYY-MM-DD'")
            else:
                error_log("Error: Date value was_modified needs to be in the format 'YYYY-MM-DD'")
        else:
            error_log("Error: Date value was_modified needs to be in the format 'YYYY-MM-DD'")
        value = f'<dch:was_modified>{value}</dch:was_modified>'
    return value

#6. has_publisher, dct, mandatory, harvested from person register via name
def get_publisher(dict):
    value = dict.get('has_publisher')
    value = value.get('Metadata Value')
    value = get_person_data(value, df_registered_persons)
    value = f'<dct:publisher>{value}</dct:publisher>'
    return value

#7. has_contributor, dct, mandatory, harvested from person register via name
def get_contributor(dict):
    value = dict.get('has_contributor')
    value = value.get('Metadata Value')
    value = get_person_data(value, df_registered_persons)
    value = f'<dct:contributor>{value}</dct:contributor>'
    return value

#8. has_creator, dct, mandatory, harvested from person register via name
def get_creator(dict):
    value = dict.get('has_creator')
    value = value.get('Metadata Value')
    value = get_person_data(value, df_registered_persons)
    value = f'<dct:creator>{value}</dct:creator>'
    return value

#9. has_owner, dch, mandatory, harvested from person register via name
def get_owner(dict):
    value = dict.get('has_owner')
    value = value.get('Metadata Value')
    value = get_person_data(value, df_registered_persons)
    value = f'<dch:has_owner>{value}</dch:has_owner>'
    return value

#10. has_responsible, dch, mandatory, harvested from person register via name
def get_responsible(dict):
    value = dict.get('has_responsible')
    value = value.get('Metadata Value')
    value = get_person_data(value, df_registered_persons)
    value = f'<dch:has_responsible>{value}</dch:has_responsible>'
    return value

#11. has_original_id, dch, mandatory
def get_original_id(dict):
    value = dict.get('has_original_id')
    value = value.get('Metadata Value')
    #value could be an int or float, make sure it is a string
    value = str(value)
    if value == 'not_defined':
        value = '<dch:has_original_id />'
    else:
        value = check_string(value)
        value = f'<dch:has_original_id>{value}</dch:has_original_id>'
    return value

#12. has_ariadne_subject, dch, mandatory
def get_ariadne_subject(dict):
    value = dict.get('has_ariadne_subject')
    value = value.get('Metadata Value')
    if value == 'not_defined':
        value = '<dch:has_ariadne_subject />'
    else:
        value = check_string(value)
        value = f'<dch:has_ariadne_subject>{value}</dch:has_ariadne_subject>'
    return value

#13. has_native_subject, dc, mandatory, multiple values
def get_native_subject(dict):
    value = dict.get('has_native_subject')
    value = value.get('Metadata Value')
    if value == 'not_defined':
        value = '<dc:subject />'
    else:
        value = check_string(value)
        value = value.split(', ')
        values = []
        for item in value:
            item = f'<dc:subject>{item}</dc:subject>'
            values.append(item)
        value = ''.join(values)
    return value

#14. has_derived_subject_uri, dch, mandatory, multiple values
def get_derived_subject_uri(dict):
    value = dict.get('has_derived_subject_uri')
    value = value.get('Metadata Value')
    if value == 'not_defined':
        value = '<dch:has_derived_subject_uri />'
    else:
        value = value.split(', ')
        values = []
        for item in value:
            item = f'<dch:has_derived_subject_uri>{item}</dch:has_derived_subject_uri>'
            values.append(item)
        value = ''.join(values)
    return value

#15. has_derived_subject_term, dch, mandatory, multiple values
def get_derived_subject_label(dict):
    value = dict.get('has_derived_subject_term')
    value = value.get('Metadata Value')
    if value == 'not_defined':
        value = '<dch:derived_subject_label />'
    else:
        value = value.split(', ')
        values = []
        for item in value:
            item = f'<dch:derived_subject_label>{item}</dch:derived_subject_label>'
            values.append(item)
        value = ''.join(values)
    return value

#16. has_language, crm, mandatory, multiple values
def get_language(dict):
    value = dict.get('has_language')
    value = value.get('Metadata Value')
    if value == 'not_defined':
        value = '<crm:P72_has_language />'
    else:
        value = value.split(', ')
        values = []
        for item in value:
            item = f'<crm:P72_has_language>{item}</crm:P72_has_language>'
            values.append(item)
        value = ''.join(values)
    return value

#17. was_created_on, dct, mandatory
def get_created_on(dict):
    value = dict.get('was_created_on')
    value = value.get('Metadata Value')
    if value == 'not_defined':
        value = '<dct:created />'
    else:
        if "-" in value:
            date_elements = value.split("-")
            if len(date_elements) == 3:
                year = date_elements[0]
                month = date_elements[1]
                day = date_elements[2]
                if len(year) == 4 and len(month) == 2 and len(day) == 2:
                    month = int(month)
                    day = int(day)
                    if month < 1 or month > 12:
                        error_log("Error: Date value was_created_on needs to be in the format 'YYYY-MM-DD' and month needs to be between 01 and 12.")
                    if day < 1 or day > 32:
                        error_log("Error: Date value was_created_on needs to be in the format 'YYYY-MM-DD' and day needs to be between 01 and 31.")
                else:
                    error_log("Error: Date value was_created_on needs to be in the format 'YYYY-MM-DD'")
            else:
                error_log("Error: Date value was_created_on needs to be in the format 'YYYY-MM-DD'")
        else:
            error_log("Error: Date value was_created_on needs to be in the format 'YYYY-MM-DD'")
        value = f'<dct:created>{value}</dct:created>'
    return value

#18. has_landing_page, dch, optional
def get_landing_page(dict):
    value = dict.get('has_landing_page')
    value = value.get('Metadata Value')
    if value == 'not_defined':
        value = '<dch:landing_page />'
    else:
        value = f'<dch:landing_page>{value}</dch:landing_page>'
    return value

#19. has_access_policy, dch, desirable
def get_access_policy(dict):
    value = dict.get('has_access_policy')
    value = value.get('Metadata Value')
    if value == 'not_defined':
        value = '<dch:access_policy />'
    else:
        value = check_string(value)
        value = f'<dch:access_policy>{value}</dch:access_policy>'
    return value

# 20. has_access_rights, dct, mandatory
def get_access_rights(dict):
    value = dict.get('has_access_rights')
    value = value.get('Metadata Value')
    if value == 'not_defined':
        value = '<dct:accessRights />'
    else:
        value = check_string(value)
        value = f'<dct:accessRights>{value}</dct:accessRights>'
    return value

#21. has_extent, dct, optional
def get_extent(dict):
    value = dict.get('has_extent')
    value = value.get('Metadata Value')
    if value == 'not_defined':
        value = '<dct:extent />'
    else:
        value = check_string(value)
        value = f'<dct:extent>{value}</dct:extent>'
    return value

#22. has_temporal_coverage, specified by 29.-33., desirable
def get_temporal_coverage(dict):
    periodo = get_period(dict)
    native_period = get_native_period(dict)
    from_date = get_from(dict)
    until_date = get_until(dict)
    temporal_coverage_xml = f'<dch:has_temporal_coverage>{periodo}{native_period}{from_date}{until_date}</dch:has_temporal_coverage>'
    return temporal_coverage_xml

#23. has_spatial_coverage, specified by 34.-44., mandatory

#24., 25., 26., 27. and 28. are harvested from the person register via has_name

#29. has_periodo_uri, dch, desirable
def get_period(dict):
    value = dict.get('has_periodo_uri')
    value = value.get('Metadata Value')
    if value == 'not_defined':
        value = '<dch:period />'
    else:
        value = f'<dch:period>{value}</dch:period>'
    return value

#30. has_chronontology_uri, dch, desirable, combine with 31.
def get_chronontology(dict):
    value = dict.get('has_chronontology_uri')
    value = value.get('Metadata Value')
    if value == 'not_defined':
        value = ''
    else:
        value = f', temporal coverage in iDAI.chronontology: {value}'
    return value

#31. has_native_period, dch, mandatory, combine with 30.
def get_native_period(dict):
    value = dict.get('has_native_period')
    value = value.get('Metadata Value')
    if value == 'not_defined':
        value = '<dch:native_period />'
    else:
        value = check_string(value)
        chronontology = get_chronontology(dict)
        value = f'<dch:native_period>{value}{chronontology}</dch:native_period>'
    return value

#32. from, crm, desirable
def get_from(dict):
    value = dict.get('from')
    value = value.get('Metadata Value')
    if value == 'not_defined':
        value = '<crm:P79_beginning_is_qualified_by />'
    else:
        value = f'<crm:P79_beginning_is_qualified_by>{value}</crm:P79_beginning_is_qualified_by>'
    return value

#33. until, crm, desirable
def get_until(dict):
    value = dict.get('until')
    value = value.get('Metadata Value')
    if value == 'not_defined':
        value = '<crm:P80_end_is_qualified_by />'
    else:
        value = f'<crm:P80_end_is_qualified_by>{value}</crm:P80_end_is_qualified_by>'
    return value

#POINT

#34. has_place_name, crm, mandatory
def get_point_place_name(dict):
    value = dict.get('point_has_place_name')
    value = value.get('Metadata Value')
    if value == 'not_defined':
        value = '<crm:P87_is_identified_by />'
    else:
        value = check_string(value)
        value = f'<crm:P87_is_identified_by>{value}</crm:P87_is_identified_by>'
    return value

#35. has_coordinate_system, dch, optional
def get_point_coordinate_system(dict):
    value = dict.get('point_has_coordinate_system')
    value = value.get('Metadata Value')
    if value == 'not_defined':
        value = '<dch:coordinate_system />'
    else:
        value = check_string(value)
        value = f'<dch:coordinate_system>{value}</dch:coordinate_system>'
    return value

#36. has_country_code, crm, mandatory
def get_point_country_code(dict):
    value = dict.get('point_has_country_code')
    value = value.get('Metadata Value')
    if value == 'not_defined' or value == 'Is filled out automatically.':
        value = '<crm:P3_has_note />'
    else:
        value = process_country_codes(value)
    return value

#44. has_place_uri, dch, desirable
def get_point_place_uri(dict):
    value = dict.get('point_has_place_uri')
    value = value.get('Metadata Value')
    if value == 'not_defined':
        value = '<dch:place_uri />'
    else:
        value = f'<dch:place_uri>{value}</dch:place_uri>'
    return value

#37. has_latitude, geo, desirable
def get_latitude(dict):
    value = dict.get('has_latitude')
    value = value.get('Metadata Value')
    value = str(value)
    value = value.replace(" ", "")
    if value == 'not_defined':
        value = '<geo:lat />'
    else:
        value = f'<geo:lat>{value}</geo:lat>'
    return value

#38. has_longitude, geo, desirable
def get_longitude(dict):
    value = dict.get('has_longitude')
    value = value.get('Metadata Value')
    value = str(value)
    value = value.replace(" ", "")
    if value == 'not_defined':
        value = '<geo:long />'
    else:
        value = f'<geo:long>{value}</geo:long>'
    return value

#Build Point XML
def build_point_xml(data_dict):
    place_name = get_point_place_name(data_dict)
    coordinate_system = get_point_coordinate_system(data_dict)
    country_code = get_point_country_code(data_dict)
    place_uri = get_point_place_uri(data_dict)
    latitude = get_latitude(data_dict)
    longitude = get_longitude(data_dict)

    point_xml = f'<dch:Point>{place_name}{coordinate_system}{country_code}{place_uri}{latitude}{longitude}</dch:Point>'
    return point_xml

#BOUNDING BOX

#34. has_place_name, crm, mandatory
def get_bb_place_name(dict):
    value = dict.get('bb_has_place_name')
    value = value.get('Metadata Value')
    if value == 'not_defined':
        value = '<crm:P87_is_identified_by />'
    else:
        value = check_string(value)
        value = f'<crm:P87_is_identified_by>{value}</crm:P87_is_identified_by>'
    return value

#35. has_coordinate_system, dch, optional
def get_bb_coordinate_system(dict):
    value = dict.get('bb_has_coordinate_system')
    value = value.get('Metadata Value')
    if value == 'not_defined':
        value = '<dch:coordinate_system />'
    else:
        value = check_string(value)
        value = f'<dch:coordinate_system>{value}</dch:coordinate_system>'
    return value

#36. has_country_code, crm, mandatory
def get_bb_country_code(dict):
    value = dict.get('bb_has_country_code')
    value = value.get('Metadata Value')
    if value == 'not_defined' or value == 'Is filled out automatically.':
        value = '<crm:P3_has_note />'
    else:
        value = check_string(value)
        value = process_country_codes(value)
    return value

#44. has_place_uri, dch, desirable
def get_bb_place_uri(dict):
    value = dict.get('bb_has_place_uri')
    value = value.get('Metadata Value')
    if value == 'not_defined':
        value = '<dch:place_uri />'
    else:
        value = f'<dch:place_uri>{value}</dch:place_uri>'
    return value

#40. has_bounding_box_min_lat, dch, optional
def get_bounding_box_min_lat(dict):
    value = dict.get('has_bounding_box_min_lat')
    value = value.get('Metadata Value')
    value = str(value)
    #delete whitespaces
    value = value.replace(" ", "")
    if value == 'not_defined':
        value = '<dch:min_latitude />'
    else:
        value = check_string(value)
        value = f'<dch:min_latitude>{value}</dch:min_latitude>'
    return value

#41. has_bounding_box_min_lon, dch, optional
def get_bounding_box_min_lon(dict):
    value = dict.get('has_bounding_box_min_lon')
    value = value.get('Metadata Value')
    value = str(value)
    #delete whitespaces
    value = value.replace(" ", "")
    if value == 'not_defined':
        value = '<dch:min_longitude />'
    else:
        value = check_string(value)
        value = f'<dch:min_longitude>{value}</dch:min_longitude>'
    return value

#42. has_bounding_box_max_lat, dch, optional
def get_bounding_box_max_lat(dict):
    value = dict.get('has_bounding_box_max_lat')
    value = value.get('Metadata Value')
    value = str(value)
    #delete whitespaces
    value = value.replace(" ", "")
    if value == 'not_defined':
        value = '<dch:max_latitude />'
    else:
        value = check_string(value)
        value = f'<dch:max_latitude>{value}</dch:max_latitude>'
    return value

#43. has_bounding_box_max_lon, dch, optional
def get_bounding_box_max_lon(dict):
    value = dict.get('has_bounding_box_max_lon')
    value = value.get('Metadata Value')
    value = str(value)
    #delete whitespaces    
    value = value.replace(" ", "")
    if value == 'not_defined':
        value = '<dch:max_longitude />'
    else:
        value = check_string(value)
        value = f'<dch:max_longitude>{value}</dch:max_longitude>'
    return value

#Build Bounding Box XML
def build_bounding_box_xml(data_dict):
    place_name = get_bb_place_name(data_dict)
    coordinate_system = get_bb_coordinate_system(data_dict)
    country_code = get_bb_country_code(data_dict)
    place_uri = get_bb_place_uri(data_dict)
    min_lat = get_bounding_box_min_lat(data_dict)
    min_lon = get_bounding_box_min_lon(data_dict)
    max_lat = get_bounding_box_max_lat(data_dict)
    max_lon = get_bounding_box_max_lon(data_dict)
    #validate box
    if min_lat == '<dch:min_latitude />' or min_lon == '<dch:min_longitude />' or max_lat == '<dch:max_latitude />' or max_lon == '<dch:max_longitude />':
        error_log("Error: Bounding box values are not properly defined.")
    else:
        min_lat_value = min_lat.replace('<dch:min_latitude>', '').replace('</dch:min_latitude>', '')
        min_lat_value = float(min_lat_value)
        min_lon_value = min_lon.replace('<dch:min_longitude>', '').replace('</dch:min_longitude>', '')
        min_lon_value = float(min_lon_value)
        max_lat_value = max_lat.replace('<dch:max_latitude>', '').replace('</dch:max_latitude>', '')
        max_lat_value = float(max_lat_value)
        max_lon_value = max_lon.replace('<dch:max_longitude>', '').replace('</dch:max_longitude>', '')
        max_lon_value = float(max_lon_value)
        if min_lat_value >= max_lat_value:
            error_log("Error: Bounding box values are not properly defined. Minimum latitude needs to be smaller than maximum latitude.")
        if min_lon_value >= max_lon_value:
            error_log("Error: Bounding box values are not properly defined. Minimum longitude needs to be smaller than maximum longitude.")
        if min_lat_value == max_lat_value or min_lon_value == max_lon_value:
            error_log("Error: Bounding box values are not properly defined. Minimum latitude and longitude cannot be the same as maximum latitude and longitude.")

    bounding_box_xml = f'<dch:BoundingBox>{place_name}{coordinate_system}{country_code}{place_uri}{min_lat}{min_lon}{max_lat}{max_lon}</dch:BoundingBox>'
    return bounding_box_xml

#POLYGON

#34. has_place_name, crm, mandatory
def get_polygon_place_name(dict):
    value = dict.get('polygon_has_place_name')
    value = value.get('Metadata Value')
    if value == 'not_defined':
        value = '<crm:P87_is_identified_by />'
    else:
        value = check_string(value)
        value = f'<crm:P87_is_identified_by>{value}</crm:P87_is_identified_by>'
    return value

#35. has_coordinate_system, dch, optional
def get_polygon_coordinate_system(dict):
    value = dict.get('polygon_has_coordinate_system')
    value = value.get('Metadata Value')
    if value == 'not_defined':
        value = '<dch:coordinate_system />'
    else:
        value = check_string(value)
        value = f'<dch:coordinate_system>{value}</dch:coordinate_system>'
    return value

#36. has_country_code, crm, mandatory
def get_polygon_country_code(dict):
    value = dict.get('polygon_has_country_code')
    value = value.get('Metadata Value')
    if value == 'not_defined' or value == 'Is filled out automatically.':
        value = '<crm:P3_has_note />'
    else:
        value = check_string(value)
        value = process_country_codes(value)
    return value

#44. polygon_has_place_uri, dch, desirable
def get_polygon_place_uri(dict):
    value = dict.get('polygon_has_place_uri')
    value = value.get('Metadata Value')
    if value == 'not_defined':
        value = '<dch:place_uri />'
    else:
        value = f'<dch:place_uri>{value}</dch:place_uri>'
    return value

#39. has_polygonal_representation, dch, optional
def get_polygon_representation(dict):
    value = dict.get('has_polygonal_representation')
    value = value.get('Metadata Value')
    if value == 'not_defined':
        value = '<dch:polygon />'
    else:
        if not value.startswith("POLYGON ((") or not value.endswith("))"):
            error_log("Error: Polygon representation needs to be in the format 'POLYGON ((x1 y1, x2 y2, x3 y3, x4 y4))'.")
        value = f'<dch:polygon>{value}</dch:polygon>'
    return value

#Build Polygon XML
def build_polygon_xml(data_dict):
    place_name = get_polygon_place_name(data_dict)
    coordinate_system = get_polygon_coordinate_system(data_dict)
    country_code = get_polygon_country_code(data_dict)
    place_uri = get_polygon_place_uri(data_dict)
    polygon_representation = get_polygon_representation(data_dict)

    polygon_xml = f'<dch:Polygon>{place_name}{coordinate_system}{country_code}{place_uri}{polygon_representation}</dch:Polygon>'
    return polygon_xml

#SPATIAL COVERAGE TYPE CHECK AND BUILDING
def get_spatial_coverage(dict):
    point = get_point_place_name(dict)
    bounding_box = get_bb_place_name(dict)
    polygon = get_polygon_place_name(dict)
    if point != '<crm:P87_is_identified_by />':
        spatial_coverage1 = build_point_xml(dict)
    if bounding_box != '<crm:P87_is_identified_by />':
        spatial_coverage2 = build_bounding_box_xml(dict)
    if polygon != '<crm:P87_is_identified_by />':
        spatial_coverage3 = build_polygon_xml(dict)
    if point == '' and bounding_box == '' and polygon == '':
        spatial_coverage = '<dch:has_spatial_coverage />'
    #If more than one spatial coverage type is filled out, combine them in one element
    spatial_xml = '<dch:has_spatial_coverage>'
    if point != '<crm:P87_is_identified_by />':
        spatial_xml += spatial_coverage1
    if bounding_box != '<crm:P87_is_identified_by />':
        spatial_xml += spatial_coverage2
    if polygon != '<crm:P87_is_identified_by />':
        spatial_xml += spatial_coverage3
    spatial_xml += '</dch:has_spatial_coverage>'

    spatial_coverage = spatial_xml

    return spatial_coverage

#45. has_visual_component, owl, optional
def get_visual_component(dict):
    value = dict.get('has_visual_component')
    value = value.get('Metadata Value')
    if value == 'not_defined':
        value = '<owl:sameAs />'
    else:
        value = check_string(value)
        value = f'<owl:sameAs>{value}</owl:sameAs>'
    return value

#46. is_part_of, dct, desirable
def get_is_part_of(dict):
    value = dict.get('is_part_of')
    value = value.get('Metadata Value')
    if value == 'not_defined':
        value = '<dct:isPartOf />'
    else:
        value = check_string(value)
        value = f'<dct:isPartOf>{value}</dct:isPartOf>'
    return value

#47. has_part is created using the is_part_relation reverse.

#48. has_data_type, dct, mandatory for individual data resources only
def get_data_type(dict):
    value = dict.get('has_data_type')
    value = value.get('Metadata Value')
    if value == 'not_defined':
        value = '<dct:type />'
    else:
        value = check_string(value)
        value = f'<dct:type>{value}</dct:type>'
    return value

#49. has_data_format, dch, optional for individual data resources only
def get_data_format(dict):
    value = dict.get('has_data_format')
    value = value.get('Metadata Value')
    if value == 'not_defined':
        value = '<dch:mime_type />'
    else:
        value = check_string(value)
        value = f'<dch:mime_type>{value}</dch:mime_type>'
    return value




#Building final XML data
#xmldata = f'{header}{get_identifier(data_dict)}{get_title(data_dict)}{get_description(data_dict)}{get_issued(data_dict)}{get_modified(data_dict)}{get_publisher(data_dict)}{get_contributor(data_dict)}{get_creator(data_dict)}{get_owner(data_dict)}{get_responsible(data_dict)}{get_original_id(data_dict)}{get_ariadne_subject(data_dict)}{get_native_subject(data_dict)}{get_derived_subject_uri(data_dict)}{get_derived_subject_label(data_dict)}{get_language(data_dict)}{get_created_on(data_dict)}{get_landing_page(data_dict)}{get_access_policy(data_dict)}{get_access_rights(data_dict)}{get_extent(data_dict)}{get_from(data_dict)}{get_until(data_dict)}{get_spatial_coverage(data_dict)}{get_visual_component(data_dict)}{get_is_part_of(data_dict)}{footer}'

#print(xmldata)

#Fortmatting the final XML data with indentation for better readability

#dom = xml.dom.minidom.parseString(xmldata)
#formatted_xml = dom.toprettyxml()

#print(formatted_xml)
