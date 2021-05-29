"""
This is the code for querying all relavent academic papers using Microsoft's
Project Academic Knowledge API (documentation can be found in this link -
https://docs.microsoft.com/en-us/academic-services/project-academic-knowledge/).
The API key can be found here - https://msr-apis.portal.azure-api.net/

Relavent papers are described by a list of conferences - conflist, a start_year,
and an end_year. The relevant papers are those that appear in a conference
from conf_list in a year between start_year and end_year (both start and end
included).

Relavent papers and their attributes are found and stored in file_name in json
format. The attributes of a paper that are stored are - title, year of publication,
citation count, conference id, conference name, date, paper id, and ids of
references. Details of these attributes can be found here -
https://docs.microsoft.com/en-us/academic-services/project-academic-knowledge/reference-paper-entity-attributes
"""


import os, json
import httplib, urllib, base64

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': '', # Insert API key here
}

params = urllib.urlencode({
    # Request parameters
    'model': 'latest',
    'attributes': '{string}',
    'count': '10',
    'offset': '0',
})

def main():

    '''
    Change conflist, start_year, and end_year for custom area of interest and
    custom time range respectively. Supported conference names can be found here -
    https://www.microsoft.com/en-us/research/project/open-academic-graph/
    '''
    conflist = ["pkdd", "vldb", "pods", "kdd", "pkdd", "wkdd", "cidr", "sigmod", "icde", "icdt", "socc", "icdcs", "icdcsw", "ssdbm"]
    start_year = 2000
    end_year=2021
    # count is an upper bound on the total number of relavent papers obtained by
    # assuming that there are no more than 200 papers in an edition of a conference
    count = (end_year - start_year + 1) * 200
    file_name = "data.json"
    flag = True
    papers = []

    try:
        conn = httplib.HTTPSConnection('api.labs.cognitive.microsoft.com')
        params = "&count={}&attributes=Ti,Y,CC,C.CId,C.CN,D,Id,RId".format(count)
        for cname in conflist:
            conn.request("GET", "/academic/v1.0/evaluate?expr=AND(Y>{},COMPOSITE(C.CN=%27{}%27))".format(start_year,cname) + params, "{body}", headers)
            response = conn.getresponse()
            data = response.read()
            output = json.loads(data)["entities"]
            if not flag:
            	file = open(file_name,"r")
            	papers = json.load(file)
            	file.close()
            papers = papers + output
            file = open(file_name, "w")
            json.dump(papers, file)
            file.close()
            if(flag):
            	flag = False
        conn.close()
    except Exception as e:
        print("Exception ", e)

main()
