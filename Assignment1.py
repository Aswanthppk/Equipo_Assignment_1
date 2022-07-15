import csv
import requests
from bs4 import BeautifulSoup
import re

headers={'user-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36'}

def scrape_data(url):

    response = requests.get(url, timeout=10,headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find_all('table')[0]

    rows = table.select('thead > tr')
    nextrows=table.select('tbody > tr')
    
    header=['Group','Categorey ','Code','Long Description               ','Short Description              ']
    #header = [th.text.rstrip() for th in rows[0].find_all('th')]
    
    
    with open('output.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)
        for row in nextrows[0:]:
            
            
            data = [ ''.join(e for e in th.text if e.isalnum()) for th in row.find_all('td')]
               
               
        
            data[1],data[2]=data[2],data[1]
            
            del data[-1]
            u=data[0]
            u=u[0]
            response = requests.get(url+'/'+u, timeout=10,headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            table = soup.find_all('table')[0]
            rows = table.select('tbody > tr')
            for row in rows[0:]:
                rdata=[ ''.join(e for e in th.text if e.isalnum()) for th in row.find_all('td')]
                link=rdata[0]
                response = requests.get(url+'/'+u+'/'+link, timeout=10,headers=headers)
                soup = BeautifulSoup(response.content, 'html.parser')
                try:
                    table = soup.find_all('table')[0]
                except:
                    continue
                rows = table.select('tbody > tr')
                for row in rows[0:1]:
                    r1data=[ ''.join(e for e in th.text if e.isalnum()) for th in row.find_all('td')]
                    del r1data[0]
                    print(data+rdata+r1data)
                    writer.writerow(data+rdata+r1data)
                

if __name__=="__main__":
    url = "https://www.hcpcsdata.com/Codes"
    scrape_data(url)