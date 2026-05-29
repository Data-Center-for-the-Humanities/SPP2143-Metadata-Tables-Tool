#this module creates the XML snippet for country description from Wikidata API. It takes in the 3-letter ISO 3166 code and returns the XML snippet with the by AO Cat required information

#It can be disabeld in xml_conversion.py if not needed. It's there called in No. 36 country_code for point, polygon and bbox.

#get country name from wikidata api
def get_country_name(wikidata_code):
    headers = {"User-Agent": "MTT/1.0 (lukas.lammers@uni-koeln.de)"}
    wikidata_code = wikidata_code.upper()
    url = "https://query.wikidata.org/sparql"

    query = """
    SELECT ?country ?countryLabel WHERE {
    ?country wdt:P298 "%s".
    SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    }
    """ % wikidata_code

    response = requests.get(
        url,
        params={"query": query, "format": "json"},
        headers=headers
    )
    #print(response)
    if response.status_code == 200:
        data = response.json()
        #print(data)
        bindings = data.get('results', {}).get('bindings', [])
        if not bindings:
            q_id = "Unknown"
            country_name = "Unknown"
            name_language = "Unknown"
            wikidata_code = wikidata_code
            return q_id, country_name, name_language, wikidata_code

        q_id = bindings[0]['country']['value'].split('/')[-1]
        country_name = bindings[0]['countryLabel']['value']
        name_language = bindings[0]['countryLabel']['xml:lang']
        return q_id, country_name, name_language, wikidata_code
    else:
        q_id = "Unknown"
        country_name = "Unknown"
        name_language = "Unknown"
        wikidata_code = wikidata_code
        return q_id, country_name, name_language, wikidata_code

#q_id, country_name, name_language = get_country_name(wikidata_country_code)
#print(f"The country name for Wikidata code '{wikidata_country_code}' is: {country_name} in language '{name_language}'")

def build_country_xml(q_id, country_name, name_language, wikidata_code):
    if q_id == "Unknown" or country_name == "Unknown" or name_language == "Unknown":
        return None
    else:
        first_row = '''<dch:wikidata_country>'''
        second_row = f'''<dch:wikidata_country_url>http://www.wikidata.org/entity/{q_id}</dch:wikidata_country_url>'''
        third_row = f'''<rdfs:label xml:lang="{name_language}">{country_name}</rdfs:label>'''
        fourth_row = '''</dch:wikidata_country>'''
        country_xml = f"{first_row}\n{second_row}\n{third_row}\n{fourth_row}"
        return country_xml
    
def process_country_codes(codestring):
    codes = codestring.split(", ")
    results = []
    for code in codes:
        q_id, country_name, name_language, wikidata_code = get_country_name(code)
        country_xml = build_country_xml(q_id, country_name, name_language, wikidata_code)
        if country_xml:
            results.append(country_xml)
    #Convert list of XML snippets into a single string
    results_xml = "".join(results)
    return results_xml


if __name__ == "__main__":
    import requests
    #test with this 3-letter Wikipedia ISO 3166
    wikidata_country_code = "EGY, RWA, LBY, -99"
    #q_id, country_name, name_language = get_country_name(wikidata_country_code)
    #print(f"The country name for Wikidata code '{wikidata_country_code}' is: {country_name} in language '{name_language}'")
    #country_xml = build_country_xml(q_id, country_name, name_language)
    #print(country_xml)
    print(process_country_codes(wikidata_country_code))
else:
    import requests
