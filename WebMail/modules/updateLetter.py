from modules.config import data_dir, template_letter
import json, os

def processingText(text:str):
    template_agency = '[AGENCY NAME]'
    template_company = '[COMPANY NAME]'
    if template_agency in text:text = text.replace(template_agency, template_company)
    return text

def get_theme():
    theme = str(input("Theme: ")).strip()
    theme = processingText(text=theme)
    return theme

def get_body():
    body = str(input("Body: ")).strip()
    body = processingText(text=body)
    return body

#######################################
# Проверка наличия/Запись в JSON
#######################################
def CheckJson():
    if not os.path.exists(template_letter):
        data = []
        with open(template_letter, 'w') as file:
            json.dump(data, file, indent=4)
    
    else:
        divide_line = '='*40
        with open(template_letter, 'r') as file:
            data = json.load(file)
        for info in data:
            id_info = info["id"]
            theme = info["theme"]
            body = info["body"]
            print(
                    f"ID: {id_info}\nTheme: {theme}\n"
                    f"Body: {body}\n\n"
                    f"{divide_line}\n"
                    )
        if len(data) == 0:print(f'LIST TEMPLATE: VOID')
        
    return len(data)
        
def updateJson(id_current:int, theme:str, body:str):
    with open(template_letter, 'r') as file:
        data = json.load(file)

    new_id = id_current+1
    new_data = {
            "id":new_id,
            "theme":theme,
            "body":body
            }
    data.append(new_data)
    with open(template_letter, 'w') as file:
        json.dump(data, file, indent=4)

#######################################
# Основная функция
#######################################
def updateTemplate():
    """Провеярем темплейты"""
    count_template = CheckJson()

    theme = get_theme()
    body = get_body()

    print(
            f"\n"
            f"{theme}\n"
            f"{body}\n"
            )
    updateJson(id_current=count_template, theme=theme, body=body)

if __name__ == '__main__':
    try:
        updateTemplate()
    except KeyboardInterrupt:print('\nExit')

