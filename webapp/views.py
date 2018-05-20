from django.shortcuts import render
import urllib.request
import json

token = "?token=9bb4facb6d23f48efbf424bb05c0c1ef1cf6f468393bc745d42179ac4aca5fee"
url_base = "http://apiv3.iucnredlist.org/api/v3/"
speciesById = "species/id/"

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

def switch(x):
    return {
        "EX": "Extinct",
        "EW": "Extinct in the wild",
        "CR": "Critically endangered",
        'EN': "Endangered",
        'VU': "Vulnerable",
        "NT": "Near threatened"
    }[x]

"""
def filterThreats(threats):
    new = []
    for t in threats:
        if t['timing'] == "Ongoing" and
"""

def index(request):
    # RED PANDA EXAMPLE
    taxonid = "714"#"68427761"
    species_name = "ailurus%20fulgens"
    name = getName(taxonid)
    status = switch(getStatus(taxonid))


    history = getHistory(taxonid)
    threats = getThreats(taxonid)

    habitats_jsons = getHabitats(taxonid)
    habitats = []

    for i in habitats_jsons:
        habitats.append(i['habitat'])

    countries = getCountries(taxonid)

    return render(request, 'webapp/index2.html', {'range': range(4),
                                                 'name': name,
                                                 'status': status,
                                                 'habitats': habitats,
                                                 'threats': threats,
                                                 'taxonid': taxonid})