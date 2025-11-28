#this module creates the XML snippet for country description from Wikidata API. It takes in the 3-letter ISO 3166 code and returns the XML snippet with the by AO Cat required information

#It can be disabeld in xml_conversion.py if not needed. It's there called in No. 36 country_code for point, polygon and bbox.

#get country name from wikidata api
def get_country_name(wikidata_code):
    url = f"https://query.wikidata.org/sparql?query=SELECT%20%3Fcountry%20%3FcountryLabel%20WHERE%20%7B%20%3Fcountry%20wdt%3AP298%20%22{wikidata_code}%22%20.%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22en%22%20%7D%20%7D&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        q_id = data['results']['bindings'][0]['country']['value'].split('/')[-1]
        country_name = data['results']['bindings'][0]['countryLabel']['value']
        name_language = data['results']['bindings'][0]['countryLabel']['xml:lang']
        return q_id, country_name, name_language
    else:
        q_id = "Unknown"
        country_name = "Unknown"
        name_language = "Unknown"
        return q_id, country_name, name_language

#q_id, country_name, name_language = get_country_name(wikidata_country_code)
#print(f"The country name for Wikidata code '{wikidata_country_code}' is: {country_name} in language '{name_language}'")

def build_country_xml(q_id, country_name, name_language):
    first_row = f'''<rdf:Description rdf:about="http://www.wikidata.org/entity/{q_id}">'''
    second_row = f'''<rdfs:label xml:lang="{name_language}">{country_name}</rdfs:label>'''
    third_row = '''</rdf:Description>'''
    country_xml = f"{first_row}\n{second_row}\n{third_row}"
    return country_xml

#country_xml = build_country_xml(q_id, country_name, name_language)
#print(country_xml)

if __name__ == "__main__":
    import requests
    #test with this 3-letter Wikipedia ISO 3166
    wikidata_country_code = "EGY"
    q_id, country_name, name_language = get_country_name(wikidata_country_code)
    print(f"The country name for Wikidata code '{wikidata_country_code}' is: {country_name} in language '{name_language}'")
    country_xml = build_country_xml(q_id, country_name, name_language)
    print(country_xml)
else:
    import requests