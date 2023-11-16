import json, os

json_list = []
with open(os.path.join('./images/debug/objectDetection/objectDetection.json'), "r") as json_file:
    json_list = json.load(json_file)
print(json_list)
with open(os.path.join('./images/debug/objectDetection/objectDetection.json', "w")) as json_file:
    json_list.sort(key=lambda x: x['name'])
    json.dump(json_list, json_file, indent=4)