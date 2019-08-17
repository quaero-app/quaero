import csv, re, json

def process_data(source_csv_file_path):
    with open(source_csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        data = [dict(x) for x in reader]
    return data



def do_search(data, query,  partial_res):
    result_list = list()
    if partial_res:
        data = partial_res

    # AND
    if " and " in query:
        subquery = query.split(' and ', 1)
        query1 = subquery[0]
        query2 = subquery[1]
        result_query1 = do_search(data, query1, partial_res)
        if result_query1 == []:
            return result_query1
        else:
            return do_search(data, query2, result_query1)

    # OR
    elif " or " in query:
        subquery = query.split(' or ', 1)
        query1 = subquery[0]
        query2 = subquery[1]
        or_list = do_search(data, query1, partial_res)
        or_list_2 = do_search(data, query2,  partial_res)
        for i in or_list_2:
            if i not in or_list:
                or_list.append(i)
        return or_list

    # NOT
    elif query.startswith("not "):
        subquery = query.replace('not ', '', 1)

        regex = r"\b" + re.escape(subquery) + r"\b"
        interegex = re.compile('[^a-zA-Z-" "]')
        for row in data:
            tar = row["text"]
            target = interegex.sub('', tar)
            target = re.sub(' +', ' ', target)
            search = re.search(regex, target, re.I)
            if not search:
                result_list.append(row)
        return result_list

    # BASECASE
    else:
        regex = r"\b" + re.escape(query) + r"\b"
        interegex = re.compile('[^a-zA-Z-" "]')
        for row in data:
            tar = row["text"]
            target = interegex.sub('', tar)
            target = re.sub(' +', ' ', target)
            if re.search(regex, target, re.I):
                result_list.append(row)
        return result_list



def geojsonize (data):

    min = 10000
    max = -10000
    geo_list = list()
    for dictionary in data:
        newdict = dict()
        propdict = dict()
        geomdict = dict()

        propdict["epigraph"] = dictionary["epigraph"]
        propdict["text"] = dictionary["text"]
        propdict["place"] = dictionary["place"]
        propdict["start"] = int(dictionary["start"])
        propdict["end"] = int(dictionary["end"])
        propdict["id"] = dictionary["id"]
        propdict["place_name"] = dictionary["place_name"]

        coordinates = list()
        coordinates.append(float(dictionary["lat"]))
        coordinates.append(float(dictionary["lng"]))

        geomdict["coordinates"] = coordinates
        geomdict["type"] = "Point"

        newdict["properties"] = propdict
        newdict["geometry"] = geomdict
        newdict["type"] = "Feature"
        geo_list.append(newdict)

        if propdict["start"] < min:
            min = propdict["start"]
        if propdict["end"] > max:
            max = propdict["end"]


    return geo_list, min, max