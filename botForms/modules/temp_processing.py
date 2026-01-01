import sys

def processingLine(line:str, pattern:str):
    if pattern in line:
        result = int(line.split(pattern)[1])
        return result

def readFile(file_name:str):
    pattern_unknown = 'Форма с неизвестным полем - '
    pattern_succes = 'Успешная отправка - '
    pattern_redirect = 'Редирект домена - '
    pattern_long_time = 'Долгая загрузка страниц - '
    pattern_not_defined = 'Не найдено форм - '
    
    pattern_succ_processing = 'Успешная обработка:	'
    
    unknown = 0
    success = 0
    redirect = 0
    long_time = 0
    not_defined = 0

    succ_processing = 0

    with open(file_name, 'r') as file:
        for line in file.readlines():
            if pattern_unknown in line:
                unknown+=processingLine(line=line, pattern=pattern_unknown)
            if pattern_succes in line:
                success+=processingLine(line=line, pattern=pattern_succes)
            if pattern_redirect in line:
                redirect+=processingLine(line=line, pattern=pattern_redirect)
            if pattern_long_time in line:
                long_time+=processingLine(line=line, pattern=pattern_long_time)
            if pattern_not_defined in line:
                not_defined+=processingLine(line=line, pattern=pattern_not_defined)
    
    succ_processing = unknown+success+redirect+not_defined
    print(
            f'Неизвестное поле:\t\t{unknown}\n'
            f'Успешная отправка:\t\t{success}\n'
            f'Редирект домена:\t\t{redirect}\n'
            f'Долгая загрузка:\t\t{long_time}\n'
            f'Не найдено форм:\t\t{not_defined}\n\n'
            f'Успешно обработано: {succ_processing}'
            )
          
if __name__ == '__main__':
    file_name = sys.argv[1]
    readFile(file_name=file_name)
