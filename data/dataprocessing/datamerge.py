from pymantic import sparql
import csv, json
server = sparql.SPARQLServer('http://127.0.0.1:9999/blazegraph/sparql')


geo_file = open('edhGeographicData.json')
geo_str = geo_file.read()
geo_data = json.loads(geo_str)["features"]

# Executing query
result = server.query('PREFIX dcterms: <http://purl.org/dc/terms/> PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX skos: <http://www.w3.org/2004/02/skos/core#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> PREFIX nmo: <http://nomisma.org/ontology#> PREFIX epi: <http://edh-www.adw.uni-heidelberg.de/edh/ontology#> PREFIX dc: <http://purl.org/dc/terms/> PREFIX lawd: <http://lawd.info/ontology/> PREFIX foaf: <http://xmlns.com/foaf/0.1/> PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#> SELECT distinct ?epigraph ?text ?place ?start ?end WHERE {  ?epigraph epi:hasEditionText ?text. ?epigraph lawd:foundAt ?place. ?epigraph nmo:hasStartDate ?start. ?epigraph nmo:hasEndDate ?end . }')
data= list()

count = 0
for b in result['results']['bindings']:
    count += 1
    print(count)
    dictio = dict()
    dictio["epigraph"] = b["epigraph"]["value"]
    dictio["text"] = b["text"]["value"]
    dictio["place"] = b["place"]["value"]
    dictio["start"] = b["start"]["value"]
    dictio["end"] = b["end"]["value"]
    dictio["id"] = b["epigraph"]["value"].replace("http://edh-www.adw.uni-heidelberg.de/edh/inschrift/","")
    for place in geo_data:
        if str(place["properties"]["uri"]).replace("https", "http") == str(b["place"]["value"]):
            dictio["lat"] = place["geometry"]["coordinates"][0]
            dictio["lng"] = place["geometry"]["coordinates"][1]
            try:
                dictio["place_name"] = place["properties"]["ancient_findspot"]
            except:
                dictio["place_name"] = "Unknown"
            data.append(dictio)

keys = data[0].keys()
with open('Quaero_data.csv', 'w', encoding='utf8') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(data)


