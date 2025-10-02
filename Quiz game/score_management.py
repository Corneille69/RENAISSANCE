import json
import pprint

read_json='C:\Users\USER\Desktop\Quiz game\Data\questions\easy.json'

with open('read_json', 'r') as jsonfil:
    lecture=json.load(jsonfil)
    print(lecture)