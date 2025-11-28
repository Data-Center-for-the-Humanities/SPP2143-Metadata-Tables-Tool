def rec_repo(uri):
    if "arachne" in uri:
        module_to_use = "metadataimport_arachne"
    elif "geoserver" in uri:
        module_to_use = "metadataimport_geoserver"
    elif "lac" in uri:
        module_to_use = "metadataimport_lac"
    elif "neotoma" in uri:
        module_to_use = "metadataimport_neotoma"
    elif "repo" in uri:
        module_to_use = "metadataimport_repo"
    elif "zenodo" in uri:
        module_to_use = "metadataimport_zenodo"
    else:
        module_to_use = "not_recognized"
    return module_to_use