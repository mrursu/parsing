import requests
from bs4 import BeautifulSoup
import cssselect
import gettext
from cssselect import GenericTranslator, SelectorError
from parsel import Selector
from faker import Faker
import psycopg2
from psycopg2.extras import execute_batch
from psycopg2.extras import execute_batch
from faker import Faker
import pandas as pd
import json
from dbconnect import connect
import xlsxwriter


def insert(lst):
    conn = connect()
    cursor = conn.cursor()
    
    query = """INSERT INTO author(author_name) VALUES (%(genres)s)
    """
 
    try:
        execute_batch(cursor,query,lst)
        conn.commit()
        
    except Exception as _ex:
        print(_ex)
    finally:
        if conn:
            cursor.close()
            conn.close()
            print("[INFO] PostgreSQL connection closed") 
            
def create_tables():
    
    # CREATE TABLES 
    conn = connect()
    cursor = conn.cursor()
    
    commands = (
    """
    CREATE TABLE IF NOT EXISTS author(
        author_id SERIAL PRIMARY KEY,
        author_name VARCHAR(50) NOT NULL
    )
    """,
    
    """
    CREATE TABLE IF NOT EXISTS genre (
        genre_id INT PRIMARY KEY,
        name_genre VARCHAR(30)
        )
    """
    )
    
    
    try:
        for command in commands:
            cursor.execute(command)
        
        conn.commit()
    except Exception as _ex:
        print(_ex)
    finally:
        if conn:
            cursor.close()
            conn.close()
            print("[INFO] PostgreSQL connection closed") 
def writeinxls(lst):
    workbook = xlsxwriter.Workbook('kinopoisk.ru/data/excel_data.xlsx')
    worksheet = workbook.add_worksheet()
    cell_format = workbook.add_format()
    cell_format.set_font_size(16)
    
    cell_format1 = workbook.add_format({'bold': True,
                                       'font_size':14 
                                       })
    font_format = workbook.add_format({'font_size': 13})
    
    worksheet.write_row(0,0,lst[0],cell_format1)
        
    for row_num, row_data in enumerate(lst,start=1):
        worksheet.write(row_num, 0, row_data['title_book'],font_format)
        worksheet.write(row_num, 1, row_data['contributor'],font_format)
        worksheet.write(row_num, 2, ', '.join(row_data['genres']),font_format)
        worksheet.write(row_num, 3, int(row_data['rating_star']),font_format)
        worksheet.write(row_num, 4, int(row_data['reading']),font_format)
        worksheet.write(row_num, 5, int(row_data['planned']),font_format)
        worksheet.write(row_num, 6, int(row_data['read']),font_format)
        worksheet.write(row_num, 7, int(row_data['not_finish_read']),font_format)
        worksheet.write(row_num, 8, int(row_data['discuss']),font_format)
        worksheet.write(row_num, 9, row_data['cited'],font_format)
        worksheet.write(row_num, 10, row_data['book_description'],font_format)
 

    worksheet.autofit()
    workbook.close()
    
    print('[INFO] Файл успешен записан...')
def faker_test():
    fake = Faker()
    all_names = {}

    for z in range(2):
        #возможно создание данных из нескольких локаций fake = Faker(['en_US', 'ja_JP'])
        fake = Faker(['uk_UA'])
        all_names.setdefault("Имя и фамилия", []).append(fake.name())
        all_names.setdefault("Полный адрес", []).append(fake.address())
        all_names.setdefault("Телефон", []).append(fake.phone_number())
        all_names.setdefault("Банковский счет", []).append(fake.aba())
        all_names.setdefault("Город", []).append(fake.city())
        all_names.setdefault("Страна", []).append(fake.country())
        all_names.setdefault("Индекс", []).append(fake.postcode())
        all_names.setdefault("Улица", []).append(fake.street_address())
        all_names.setdefault("Пароль", []).append(fake.pystr())
        all_names.setdefault("e-mail (фейковый))", []).append(fake.free_email())
        all_names.setdefault("Номер кредитной карты", []).append(fake.credit_card_number())
        all_names.setdefault("Компания", []).append(fake.company())
        all_names.setdefault("Должность", []).append(fake.job())
        all_names.setdefault("Дата рождения", []).append(fake.date())
        
    print(all_names)
    # df = pd.DataFrame(data=all_names)
    # print(df)

    # df.to_excel('./fakenamegeneration.xlsx')


# Insert data in Databases
def insert_data(lst): 
    """ Insert data in Database"""
    conn = connect()
    cursor = conn.cursor()
    try:
        query = """INSERT INTO user_info(card,age) VALUES (%(title_book)s, %(contributor)s)"""
        execute_batch(cursor, query,lst)
        conn.commit()
        print("[INFO] Data was succefully inserted")
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if conn:
            cursor.close()
            conn.close()
            print("[INFO] PostgreSQL connection closed") 
   
    

def get_data():
    url = 'https://readrate.com/rus/ratings/top100?iid=8126&offset=all&format=json'
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, 'lxml')

    book_card = soup.select('div.no-gutters')
    lst_data = []
    step = 0
    for item in book_card:
        genres_list = item.select('ul.genres-list li a')
        genres_list = [item.text.strip() for item in genres_list]
        title_link = item.select_one('h4').text.strip()
        contributor = item.select_one('li.contributor').text
        rating_stars = item.select_one('.rating-stars span.rates-count').text.strip()
        statistics_list = item.select('ul.statistics-list>li')
        reading = statistics_list[0].text.strip()
        planned = statistics_list[1].text.strip()
        read = statistics_list[2].text.strip()
        not_finish_read = statistics_list[3].text.strip()
        discuss = statistics_list[4].text.strip()
        cited = statistics_list[5].text.strip()
        
        book_description = item.select_one('div.book-description').text.strip()
        
        
        lst_data.append({
            'title_book': title_link,
            'contributor': contributor,
            'genres': genres_list,
            'rating_star': rating_stars,
            'reading': reading,
            'planned': planned,
            'read': read,
            'not_finish_read': not_finish_read,
            'discuss': discuss,
            'cited': cited,
            'book_description': book_description
        })  
        
        # yield lst_data[step:len(lst_data)]
        # step += 1
    with open('kinopoisk.ru/data/data_lst.json','w') as file:
        json.dump(lst_data,file,indent=4, ensure_ascii= False)
        
    return lst_data
    

def main():
    lst = get_data()
    writeinxls(lst)
    # insert_data(lst)
    # create_tables()
    insert(lst)
 
if __name__ == '__main__':
    main()






