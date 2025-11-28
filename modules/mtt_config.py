#Configuration file for Metadata Tables Tool

#1. CONSTANT VARIABLES

#Please use the tables in templates folder to set constant values for all metadata.

#2. GIT SYNC VARIABLES

local_folder="metadata_mirror"
repo_url="https://somekindofgit.de/something.git"
target_subdir="test_metadata"
token="enter-your-git-api-token-here"
branch="main"

#3. ONLINE INFRASTRUCTURE VARIABLES

git_repo = "https://somekindofgit.de/repo"
oai_pmh_status = "https://oai.yourdomain/admin/data-provider.do"
oai_pmh_list = "http://oai.yourdomain/provider?verb=ListRecords&metadataPrefix=oai_dc"
ariadne = "https://portal.ariadne-infrastructure.eu/"