import json as json_parser


with open('./example/data/demo.json') as read_file:
    superDemoExample = json_parser.load(read_file)


json_string = json_parser.dumps(superDemoExample)

print ( type( superDemoExample ) )
print ("DUMP JSON")
print (json_string)