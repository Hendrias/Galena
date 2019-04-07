import csv, json, numpy, cgi
from bokeh.plotting import figure, show, output_file
from urllib.parse import urlparse
from flask import Flask, render_template, request

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

def read_languages(): 
    #csv_file = open("csvdata.csv", 'r', encoding='utf-8')
    #json_file = open("jsondata.json", 'w')

    #field_names = "ID","Name in English","Name in French","Name in Spanish","Countries","Country codes alpha 3","ISO639-3 codes","Degree of endangerment","Alternate names","Name in the language","Number of speakers","Sources","Latitude","Longitude","Description of the location"
    #reader = csv.DictReader( csv_file, field_names)
    #for row in reader:
     #   json.dump(row, json_file)
      #  json_file.write('\n')

    languages = {}
    first_line = True

    file_name = "jsondata.json"
    counter = 0

    for line in open(file_name):
        if first_line:
            first_line = False
            continue

        # indices for data.csv
        # language name = 1
        # [0] countries spoken in = 4
        # [1] country codes = 5
        # [2] degree of endangerment = 7
        # [3] number of speakers = 10
        # [4] latitude = 12
        # [5] longitude = 13
        y = json.loads(line)

        key = y["Name in English"]
        value = [y["Countries"], y["Country codes alpha 3"], y["Degree of endangerment"], y["Number of speakers"], y["Latitude"], y["Longitude"]]
        languages[key] = value
    return languages

# takes in a specific language
# returns a list of the countries the language is spoken in
def get_countries(language):
    languages = read_languages()
    return languages.get(language)[0]


# returns every country with an endangered language
def get_all_countries():
    languages = read_languages()
    countries = set()
    for language in languages:
        if languages.get(language)[0].find(",") != -1:
            language_split = languages.get(language)[0].split(", ")
            for l in language_split:
                countries.add(l)
        else:
            countries.add(languages.get(language)[0])
    countries_json = json.dumps(countries, cls=SetEncoder)
    return countries_json


def get_country_code(language):
    languages = read_languages()
    return languages.get(language)[1]


def get_country_endangerment(language):
    languages = read_languages()
    return languages.get(language)[2]


def get_num_speakers(language):
    languages = read_languages()
    return languages.get(language)[3]


def get_latitude(language):
    languages = read_languages()
    return languages.get(language)[4]


def get_longitude(language):
    languages = read_languages()
    return languages.get(language)[5]


def get_status(status):
    languages = read_languages()
    lang = []
    for language in languages:
        if languages.get(language)[2] == status:
            value = [languages.get(language)[0], languages.get(language)[4], languages.get(language)[5]]
            lang.append(value)
    return lang


def display_data():
    N = 4000
    x = numpy.random.random(size=N) * 100
    y = numpy.random.random(size=N) * 100
    radii = numpy.random.random(size=N) * 1.5
    colors = [
        "#%02x%02x%02x" % (int(r), int(g), 150) for r, g in zip(50+2*x, 30+2*y)
    ]

    TOOLS="hover,crosshair,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo,reset,tap,save,box_select,poly_select,lasso_select,"

    p = figure(tools=TOOLS)

    p.scatter(x, y, radius=radii,
              fill_color=colors, fill_alpha=0.6,
              line_color=None)

    output_file("color_scatter.html", title="color_scatter.py example")

    show(p)  # open a browser


def get_less_than(number):
    languages = read_languages()
    lang = []
    for key, language in languages.items():
        try:
            if language[3] != '':
                if int(language[3]) < number:
                    value = [key, language[0], language[4], language[5]]
                    lang.append(value)
        except ValueError as e:
            pass
    return lang

#print(get_less_than(10))

def read_form(search_term):
    form = cgi.FieldStorage()
    lang = []
    if search_term in ['Vulnerable', 'Definitely endangered', 'Severely endangered', 'Critically endangered', 'Extinct']:
        lang = get_status(search_term)
    elif search_term == "countries":
        lang = get_all_countries()
    elif search_term == "number":
        lang = get_less_than(50000)
    # print(search_term, lang)
    return lang
