from SinCity.colors import RED, RESET, BLUE

from modules.helper import helpMultiUserMod
from modules.config import users_dir
from webMail import WebMail
import os, json, sys

def initMultiUserMod():
    if not os.path.exists(users_dir):
        os.makedirs(users_dir)
        sys.exit(
                f'{RED}'
                f'Создана директория для многопользовательского режима\n'
                f'Добавьте конфигурации пользователей'
                f'{RESET}')
    list_users = []
    for user in os.listdir(users_dir):
        if '.json' in user:list_users.append(f'{users_dir}/{user}')
    if len(list_users) > 0:
        return list_users
    if len(list_users) == 0:
        sys.exit(f'{RED}Конфигурации пользователей не обнаружены!{RESET}')

if __name__ == '__main__':
    params = sys.argv
    if '--help' in params:
        helpMultiUserMod()
   
    else:
        users = initMultiUserMod()

        number_user = 0
        for user in users:
            number_user+=1
            print(f'[{number_user}]\t\t{user}')
            WebMail(login_config=user)

    
