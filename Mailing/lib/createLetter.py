from lib.config import letter_json
import json

def get_count_letter():
    with open(letter_json, 'r') as file:
        data = json.load(file)
    return len(data)

def processingTemplate(data:str, name:str=None, company:str=None):
    if '{name}' in data:data = data.replace('{name}', name)
    if '{company}' in data:data = data.replace('{company}', company)
    
    symbol = '\x1bE'
    if symbol in data:data = data.replace(symbol, '\n')

    return data

def generateLetter(count:int, email:str, company:str, name:str=None):
    with open(letter_json, 'r') as file:
        data = json.load(file)

    for info in data:
        id_letter = info['id']
        theme = info['theme']
        body = info['body']

        

        if count == id_letter:

            theme = processingTemplate(data=theme, name=name, company=company)
            body = processingTemplate(data=body, name=name, company=company)
            
            return theme, body
