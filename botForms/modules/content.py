from SinCity.colors import RED, RESET, BLUE
from modules.config import (
        content_file_path,
        content_dir
        )
import json, sys, os

def Content(full_attrs:str, target_company:str):
    full_attrs = full_attrs.strip().lower()
    content = None
    try:
        with open(content_file_path, 'r') as file:
            data = json.load(file)
        first_name = data['first_name']
        last_name = data['last_name']
        user_name = data['name']
        full_name = data['full_name']
        email = data['email']
        phone = data['phone']
        company = data['company']
        your_project = data['your_project']
        site = data['site']
        location = data['location']
        region = data['region']
        state = data['state']
        zip_code = data['zip_code']
        price = data['price']
        job_title = data['job_title']
        subject = data['subject']
        message = data['message']
        
        template = "[COMPANY NAME]"
        if template in subject:subject = subject.replace(template, target_company)
        if template in message:message = message.replace(template, target_company)

        if 'first' in full_attrs:content = first_name
        
        elif 'last' in full_attrs or 'surname' in full_attrs:content = last_name
        elif 'lnam' in full_attrs:content = last_name
        
        elif 'full' in full_attrs:content = full_name
        
        elif 'email' in full_attrs or 'mail' in full_attrs:content = email
        
        elif 'phone' in full_attrs:content = phone
        elif 'tel' in full_attrs:content = phone
        
        elif 'company' in full_attrs:content = company
        elif 'firma' in full_attrs:content = company
        elif 'organiz' in full_attrs:content = company

        elif 'project' in full_attrs:content = your_project
        
        elif 'site' in full_attrs or 'url' in full_attrs:content = site
        
        elif 'subj' in full_attrs or 'theme' in full_attrs:content = subject

        elif 'location' in full_attrs:content = location
        elif 'region' in full_attrs:content = region
        elif 'state' in full_attrs:content = state
        elif 'zip' in full_attrs:content = zip_code
        elif 'ort' in full_attrs:content = zip_code
        elif 'job' in full_attrs or 'title' in full_attrs:content = job_title

        elif 'price' in full_attrs or 'budget' in full_attrs:content = price

        elif 'message' in full_attrs:content = message
        elif 'body' in full_attrs:content = message
        elif 'help' in full_attrs:content = message
        elif 'comment' in full_attrs:content = message
        elif 'nachricht' in full_attrs:content = message
        elif 'quest' in full_attrs:content = message
        elif 'textarea' in full_attrs:content = message
        
        elif 'name' in full_attrs:content = user_name
        elif 'naam' in full_attrs:content = user_name
        elif 'nome' in full_attrs:content = user_name
        elif 'wpforms[fields][1]' in full_attrs:content = user_name
        
        else:
            content = full_name 

        return content

    except FileNotFoundError:
        if not os.path.exists(content_dir):os.makedirs(content_dir)
        print(f"{RED}Отсутствует файл с контентом: {content_file_path}{RESET}")
        sys.exit()
    except Exception as err:
        print(f"{RED}{err}{RESET}")

def GenerateContent(full_attrs:str, company:str):
    content = Content(target_company=company, full_attrs=full_attrs) 
    if content != False:
        print(f"{BLUE}{content}{RESET}")
        return content
    if content == False:
        print(f'{RED}Контент не определен!{RESET}')
        return False


if __name__ == '__main__':
    params = sys.argv
    if len(params) > 1:
        full_attrs = params[1]
        GenerateContent(company='Digital', full_attrs=full_attrs)
    if len(params) == 1:
        print("Введите параметром имя!")
