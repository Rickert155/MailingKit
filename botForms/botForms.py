from SinCity.colors import RED, RESET, GREEN, BLUE
from modules.form import ProcessingDomain
from modules.miniTools import (
        InitBot, 
        ListBase,
        CheckDoneDomains,
        RecordingDoneDomain
        )
import csv, sys

def botFormStart():
    try:
        InitBot()
    
        complite_domain = CheckDoneDomains()

        list_base = ListBase()
        for base in list_base:
            with open(base, 'r') as file:
            
                number_domain = 0

                for row in csv.DictReader(file):
                    domain = row['Domain'].lower()
                    company = row['Company']
                
                    if domain not in complite_domain:
                        number_domain+=1
                        print(f'{GREEN}[{number_domain}] {domain}{RESET}')
                    
                        ProcessingDomain(domain=domain, company=company)
                    
                        RecordingDoneDomain(domain=domain)

                if number_domain == 0:
                    print(f"{GREEN}Все домены пройдены!{RESET}")
    except KeyboardInterrupt:
        print(f'{RED}\nExit...{RESET}')
        sys.exit()

if __name__ == '__main__':
    botFormStart()
