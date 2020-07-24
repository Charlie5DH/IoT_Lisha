import json

json_string = '''
{
    "researcher": {
        "name": "Ford Prefect",
        "species": "Betelgeusian",
        "relatives": [
            {
                "name": "Zaphod Beeblebrox",
                "species": "Betelgeusian"
            }
        ]
    }
}
'''

data = json.loads(json_string)   #load a string to Json format

print ('no indent')
print (json.dumps(data))
print ('indent = 2')
print (json.dumps(data, indent=2))
print ('indent = 4')
print (json.dumps(data, indent=4))