import smtplib, socket, os, random
from email.message import EmailMessage

def test_message(recipient:str):
    print(f"test message > {recipient}")
    theme, body = createMessage()
    
    sendMessage(
            recipient=recipient, 
            user_message=body,
            user_theme=theme
            )
    

def sendMessage(
        recipient:str, 
        user_message:str, 
        user_theme:str
        ):

    domain = socket.gethostname()
    
    msg = EmailMessage()
    
    msg['From'] = f"Sin <sin@{domain}>"
    msg['To'] = recipient
    msg['Subject'] = f"{domain} {user_theme}"
    msg.set_content(user_message)

    with smtplib.SMTP("localhost", 25) as smtp:
        smtp.send_message(msg)

def createMessage():
    data_dir = 'data'
    message_dir = f'{data_dir}/message'
    theme_dir = f'{data_dir}/theme'

    all_message = []
    for message in os.listdir(message_dir):
        if '.txt' in message and message not in all_message:
            all_message.append(f"{message_dir}/{message}")
    
    all_theme = []
    for theme in os.listdir(theme_dir):
        if '.txt' in theme and theme not in all_theme:
            all_theme.append(f"{theme_dir}/{theme}")

    len_list_message = len(all_message)
    len_list_theme = len(all_theme)
    
    random_message = selectText(len_list=len_list_message, list_txt=all_message)
    random_theme = selectText(len_list=len_list_theme, list_txt=all_theme)

    return random_theme, random_message
    

def selectText(len_list:str, list_txt:[]):
    random_number = random.randint(0, len_list-1)
    random_txt = list_txt[random_number]
    with open(random_txt, 'r') as file:
        text = file.read()
        text = text.strip()
    return text

