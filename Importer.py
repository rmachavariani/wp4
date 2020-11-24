import json

with open('data.json', 'r') as j:
    json_input = json.load(j)

array = [[2, 2], [3, 1], [1, 4], [8, 4]]
json_input["input"]["fastener"]["coord_list"] = str(array)

with open('data.json', 'w') as j:
    json.dump(json_input, j)
