import os
import json

def get_author(windy,request,environ):
	file=os.path.join(windy.confdir,'author.json')
	with open(file,'r') as f:
		json_dict=json.load(f)
		request['author']=json_dict.get('author','Nope')
		
	return request
			