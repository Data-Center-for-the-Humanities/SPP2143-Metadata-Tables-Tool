#Configuration file for Metadata Tables Tool

#1. CONSTANT VARIABLES

#Please use the tables in templates folder to set constant values for all metadata.

#2. LANGUAGES
#You can use this list to set the languages in the dropdown menu.
languages = ["http://www.lexvo.org/page/iso639-3/deu", "http://www.lexvo.org/page/iso639-3/eng"]

#2. GIT SYNC VARIABLES

local_folder="metadata_mirror"
repo_url="https://gitlab.dh.uni-koeln.de/your_repo.git"
target_subdir="test_metadata"
token="your_token_here"
branch="main"

#3. ONLINE INFRASTRUCTURE VARIABLES

getty_aat = "https://www.getty.edu/research/tools/vocabularies/aat/"
ariadne_portal = "https://portal.ariadne-infrastructure.eu/"
staging_portal = "https://ariadne-portal-staging.d4science.org/"
staging_graph_db = "https://ariadne-graphdb-test.cloud.d4science.org/graphs"
chronontology = "https://chronontology.dainst.org/"
periodo = "https://client.perio.do/?page=open-backend"
ao_cat = "https://zenodo.org/records/21476199"
lexvo = "http://www.lexvo.org/"
git_repo = "https://gitlab.dh.uni-koeln.de/your_repo.git"
oai_pmh_status = "https://oai.dch.phil-fak.uni-koeln.de/admin/data-provider.do"
oai_pmh_list = "http://oai.dch.phil-fak.uni-koeln.de/provider?verb=ListRecords&metadataPrefix=oai_dc"
three_m = "https://demos.isl.ics.forth.gr/3m/"
git_hub = "https://github.com/Data-Center-for-the-Humanities/SPP2143-Metadata-Tables-Tool"
