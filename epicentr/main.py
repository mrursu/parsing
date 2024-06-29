from bs4 import BeautifulSoup
import lxml
import requests
import json
import time
import random

def get_url_name(url):
    # url = 'https://epicentrk.ua/ua/shop/shtukaturka/'
    for item in url:
        response = requests.get(item)
        soup = BeautifulSoup(response.text, 'lxml')
        title_href= []
        price = []
        article = soup.find_all('div', '_V1Bazw')
        json_data = []
        for num,item in enumerate(article):
            product_name = item.find('div',class_= '_HHLSg4').text
            product_href = 'https://epicentrk.ua/' + item.find('a', class_ = '_zJRTql').get('href')
            product_img  = item.find('a', class_ = '_Spiue2').find('img').get('src')
            product_price = item.find('div', '_YkdMDu').find('span').text.strip()
            product_review = item.find('span',class_= '_ACJ4+C').text
            product_review = ''.join(item for item in product_review if item.isdecimal())
            
            print(product_name)

            json_data.append({
                'product_name': product_name,
                'product_href': product_href,
                'product_img': product_img,
                'product_price': product_price,
                'product_review': product_review,
                # 'product_category:': [item.text for item in product_category]

            })
            
            print(f'[+INFO] {num+1}/{len(article)}')
            
            time.sleep(random.randrange(2, 5))
            
        with open('epicentr/data_list.json', 'w') as file:
            json.dump(json_data, file, indent=4,ensure_ascii= False)
            
        return json_data

def get_subcategory(url):
    url = url
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup
    


def get_category():
    url = 'https://epicentrk.ua/ua/shop/stroitelstvo-i-remont/'
    soup = get_subcategory(url)
    category_name = soup.select('div._o02lPn > ul > li')
    category_url = ['https://epicentrk.ua' + item.select_one('div._QE1J8R a').get('href') for item in category_name]
    
    # print(*category_url)

    for item in category_url[1:2]:
        soup = get_subcategory(item)
        category_name1 = soup.select('div._o02lPn > ul > li')
        
        sub_category = ['https://epicentrk.ua' + item.select_one('div._QE1J8R a').get('href') for item in category_name1]

        
    for item1 in sub_category[2:3]:
        soup = get_subcategory(item1)
        category_name1 = soup.select('div._o02lPn > ul > li')
        
        sub_category1 = ['https://epicentrk.ua' + item.select_one('div._QE1J8R a').get('href') for item in category_name1]
        
    get_url_name(sub_category1)
        
    
        
    
    
        
    
    
    # category_name = soup.select('div._o02lPn > ul > li')
    # category_url = ['https://epicentrk.ua' + item.select_one('div._QE1J8R a').get('href') for item in category_name]
    
    # for item in category_url[:1]:
    #     response = requests.get(item)
    #     soup = BeautifulSoup(response.text, 'lxml')
    #     category_name1 = soup.select('div._o02lPn > ul > li')
        
    #     sub_category = ['https://epicentrk.ua' + item.select_one('div._QE1J8R a').get('href') for item in category_name1]
    
        
    

    
    # print(category_url)
    
    
    
    # print(category_url)
    # for item in category_name:
    #     print(item.select_one('div._QE1J8R a').get('href'))
    

    
    # for item in category_name:
    #     sub_category = 'https://epicentrk.ua/' + item.get('href')
    #     print(sub_category)
        
        
        # response = requests.get(sub_category)
        # soup = BeautifulSoup(response.text, 'lxml')
        # category1 = soup.select('div._o02lPn > ul > li')[0].select('div._QE1J8R a')
        # print(category1)
        # for item in category1:
        #     cat = 'https://epicentrk.ua' + item.get('href')

def get_product():
    data = get_url_name()
    for item in data:
        print(item['product_href'])


def main():
    # get_product()
    get_category()

    
    
if __name__ == '__main__':
    main()

    