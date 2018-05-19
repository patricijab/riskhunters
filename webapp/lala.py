import urllib.request
import json

token = "?token=9bb4facb6d23f48efbf424bb05c0c1ef1cf6f468393bc745d42179ac4aca5fee"
url_base = "http://apiv3.iucnredlist.org/api/v3/"
speciesById = "species/id/"

# RED PANDA EXAMPLE
taxonid = "714"
name = "ailurus%20fulgens"

def requesting( urlstr ):
	return json.loads(urllib.request.urlopen(urlstr).read().decode("utf-8"))

# urls
def speciesById( idstr ):
	return requesting(url_base + "species/id/" + idstr + token)

def historicalById( idstr ):
	return requesting(url_base + "species/history/id/" + idstr + token)
def threatsById ( idstr ):
	return requesting(url_base + "threats/species/id/" + idstr + token)
def habitatsById ( idstr ):
	return requesting(url_base + "habitats/species/id/" + idstr + token)
def countryById ( idstr ):
	return requesting(url_base + "species/countries/id/" + idstr + token)

# get data
def getName( idstr ):
	return speciesById(idstr)['result'][0]['main_common_name']
def getStatus ( idstr ):
	return speciesById(idstr)['result'][0]['category']
def getHistory ( idstr ):
	return historicalById(idstr)['result']
def getThreats ( idstr ):
	return threatsById(idstr)['result']
def getHabitats ( idstr ):
	return habitatsById(idstr)['result']
def getCountries ( idstr ):
	return countryById(idstr)['result']

print(requesting(url_base + "species/id/" + taxonid + token)['result'][0]['main_common_name'])
print(getThreats(taxonid))

