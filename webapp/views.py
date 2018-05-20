from django.shortcuts import render
import urllib.request
import json
import csv
import re
from datetime import datetime

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

def allSpecies():
    # all endangered species
    return requesting(url_base + "species/category/EN" + token)

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
def getAllSpecies():
    return allSpecies()['result']

def switch(x):
    return {
        "EX": "Extinct",
        "EW": "Extinct in the wild",
        "CR": "Critically endangered",
        'EN': "Endangered",
        'VU': "Vulnerable",
        "NT": "Near threatened"
    }[x]

def switch2(x):
    return {
        "Extinct": 0,
        "Extinct in the wild": 1,
        "Critically endangered": 2,
        'Endangered': 3,
        'Vulnerable': 4,
        "Near threatened": 5
    }[x]

def filterThreats(threats):
    new = []
    for t in threats:
        scores = re.findall(r'\d+', t['score'])
        if len(scores) > 0:
            score = int(scores[0])
            if (score > 4):
                code = t['code'][0]
                print(code)
                new.append(t)
    return new

def filterHistory(history):
    years = []
    statuses = {}

    for h in history:
        if h['category'] != "Insufficiently Known":
            years.append(int(h['year']));
            statuses[h['year']] = h['category'];

    return statuses, sorted(years)
    #return history

def index(request):
    # RED PANDA EXAMPLE
    taxonid = "714"
    species_name = "Ailurus Fulgens"
    name = getName(taxonid)
    status = switch(getStatus(taxonid))

    statuses, history = filterHistory(getHistory(taxonid))
    minimalYear = history[0]

    threats = filterThreats(getThreats(taxonid))

    habitats_jsons = getHabitats(taxonid)
    habitats = []

    for i in habitats_jsons:
        habitats.append(i['habitat'])

    countries = getCountries(taxonid)

    return render(request, 'webapp/index.html', {'range': 5-switch2(status),
                                                 'name': name,
                                                 'latin_name': species_name,
                                                 'status': status,
                                                 'habitats': habitats,
                                                 'threats': threats,
                                                 'history': history,
                                                 'statuses': json.dumps(statuses),
                                                 'minimalYear': minimalYear})

def indexBeforeIndex(request):
    species_json = getAllSpecies();
    species = []

    return render(request, 'webapp/indexBeforeIndex.html')
