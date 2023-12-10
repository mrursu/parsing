import requests
from bs4 import BeautifulSoup
import lxml
import json
import time
import random
import datetime
import os 




# download img in the folders
def img_downloaders(lst):
    img_counter = 1
    for item in lst:
        replace_name = item['product_name'].replace('/','_')
        response = requests.get(item['product_href']).content
        
        with open(f"{img_counter}_{replace_name}.jpg", "wb") as file:
            file.write(response)
       
        print(f'{img_counter}. {item["product_name"]} - DONE ...')
        time.sleep(random.randrange(2, 5))
        img_counter += 1
   
    
# parsring data
def get_data():
    print('\n' +'PARSING TOPKIOSK.RU'.center(60,'-') + '\n')
    count = 1
    start_time = datetime.datetime.now()
    lst = []
    url = 'https://topkiosk.ru/vidy-pavilionov/torgovye-paviliony-foto/'
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, 'lxml')
    products = soup.find(id = 'gallery-2').find_all('dl',class_='gallery-item')

    for item in products:
        try:
            product_name = item.find('dd', class_ = 'wp-caption-text').text.strip()
        except AttributeError:
            product_name = 'no text'
            
        products_href = item.find('dt', class_ = 'gallery-icon').find('a').get('href')
        
        lst.append({
            'product_name': product_name,
            'product_href': products_href
        })
    with open('topkiosk.ru/data_list.json', 'w') as file:
        json.dump(lst, file, indent=4,ensure_ascii= False)
    step = 0
    lenlst = len(lst) // 3
    os.chdir('topkiosk.ru/data')
    for x in range(lenlst):
        if not os.path.isdir(str(count)):
            os.mkdir(str(count))  
        os.chdir(str(count))
        listslice = lst[step:step+3]
        img_downloaders(listslice)
        os.chdir('..')
        step+= 3
        count+= 1
        print('-' * 60)


def main():
    start = datetime.datetime.now()
    result = get_data()
    end = datetime.datetime.now()
    print(f"[+] Total time: {end - start}")
    

if __name__ == '__main__':
    main()
    
