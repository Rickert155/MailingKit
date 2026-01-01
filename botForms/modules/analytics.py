from SinCity.colors import RED, RESET, GREEN
from modules.config import analytics_dir, anal_result_dir
import os, sys, csv, shutil

def initAnalytics():
    if not os.path.exists(anal_result_dir):os.makedirs(anal_result_dir)
    if not os.path.exists(analytics_dir):
        os.makedirs(analytics_dir)
        print(
                f'{RED}Директория {analytics_dir} создана{RESET}\n'
                f'{RED}В нее необходимо добавить документы для обработки!{RESET}'
                )
        sys.exit()

def ListDocs():
    list_docs = []
    for doc in os.listdir(analytics_dir):
        new_name = doc
        if '.csv' in new_name:
            if ' ' in new_name:new_name = new_name.replace(' ', '_')
            if '(' in new_name:new_name = new_name.replace('(', '')
            if ')' in new_name:new_name = new_name.replace(')', '')

            shutil.move(f'{analytics_dir}/{doc}', f'{analytics_dir}/{new_name}')
            list_docs.append(f'{analytics_dir}/{new_name}')

    return list_docs
    
not_connected_type = []
not_defined_type = []
redirect_type = []
unknown_type = []
success_type = []

def checkTypeDoc(doc:str):
    global not_connected_type, not_defined_type, redirect_type, unknown_type, success_type
    
    if 'not_connected' in doc:not_connected_type.append(doc)
    elif 'not_defined' in doc:not_defined_type.append(doc)
    elif 'redirect' in doc:redirect_type.append(doc)
    elif 'unknown' in doc:unknown_type.append(doc)
    else:success_type.append(doc)


def processingDocs():
    global not_connected_type, not_defined_type, redirect_type, unknown_type, success_type

    updateResult(list_docs=not_connected_type , doc_type="not_connected")
    updateResult(list_docs=not_defined_type , doc_type="not_defined")
    updateResult(list_docs=redirect_type, doc_type="redirect")
    updateResult(list_docs=unknown_type, doc_type="unknown_field")
    updateResult(list_docs=success_type , doc_type="success")


def updateResult(list_docs:list, doc_type:str):
    new_file_name = f'update_{doc_type}.csv'
    
    count_domain = 0
    
    for doc in list_docs:
        with open(doc, 'r') as file:
            for row in csv.DictReader(file):
                domain = row['Domain']
                company = row['Company']
                time_recording = row['Time']
                try:reason = row['Reason']
                except:reason = 'success'
                count_domain+=1
                RecordingResult(
                        domain=domain, 
                        company=company, 
                        time_recording=time_recording, 
                        reason=reason,
                        file_name=new_file_name
                        )
    if '_' in doc_type:doc_type = doc_type.replace('_', ' ')
    print(f'{GREEN}{doc_type.upper()}:{RESET}\t{count_domain}')

def RecordingResult(domain:str, company:str, time_recording:str, reason:str, file_name:str):
    file_name = f'{anal_result_dir}/{file_name}'
    if not os.path.exists(file_name):
        with open(file_name, 'a') as file:
            write = csv.writer(file)
            write.writerow(['Domain', 'Company', 'Reason', 'Time'])

    with open(file_name, 'a+') as file:
        write = csv.writer(file)
        write.writerow([domain, company, reason, time_recording])



if __name__ == '__main__':
    initAnalytics()
    list_docs = ListDocs()
    if len(list_docs) != 0:
        print(f'{GREEN}Обнаружено документов: {len(list_docs)}{RESET}') 
        for doc in list_docs:
            checkTypeDoc(doc=doc)

        processingDocs()
    if len(list_docs) == 0:
        print(
                f'{RED}В директории {analytics_dir} '
                f'не обнаружено документов для обработки{RESET}'
                )
        sys.exit()

