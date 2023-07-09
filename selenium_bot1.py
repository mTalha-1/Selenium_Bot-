from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import mysql.connector
from time import sleep
import logging

# Logging Configaration
logging.basicConfig(filename='bot_file.txt', filemode='w',level=logging.INFO, format= '%(asctime)s - %(levelname)s - %(message)s - %(lineno)d')

# Building Database connection
def connection_database(host,user,password,database):
    try:
        logging.info('Building Database Connection')
        conn = mysql.connector.connect(
                host= host,
                user= user,     
                password= password, 
                database= database 
            )
    except Exception as e:
        logging.critical(e)
    else:
        return conn

# Function for creating Table, if table exist first delete it and then creat.
def Table_creation(connection):
    conn = connection
    cursor = conn.cursor()
    table_name = "Laptop_Products"

# MySQL query that give result if table exist
    table_exists_query = """
    SELECT COUNT(*)
    FROM information_schema.tables
    WHERE table_schema = '{database}'
        AND table_name = '{table}'
    """.format(database= 'daraz_laptops_products', table=table_name)

    cursor.execute(table_exists_query)
    table_exists = cursor.fetchone()[0]

# Checking Table exist or not
    if table_exists:
        # Table exists, so delete it
        delete_table_query = "DROP TABLE {table}".format(table=table_name)
        cursor.execute(delete_table_query)
        logging.info("Table deleted successfully.")
    else:
        logging.info("Table does not exist.")

# MySQL query for creating table
    create_table_query = """
    CREATE TABLE {table} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        Product_title VARCHAR(500),
        Product_price VARCHAR(200),
        No_of_Reviews INT,
        Product_Rating FLOAT,
        Product_description VARCHAR(10000)
    )
    """.format(table=table_name)

    # Execute the table creation query
    try:
        cursor.execute(create_table_query)
    except Exception as e:
        logging.error(e)
    else:
        logging.info("Table created successfully.")

def webdriver_connection():
    try:
        service =   Service(executable_path = "/chromedriver")
        driver = webdriver.Chrome(service=service)
    except Exception as e:
        logging.critical(e)
    else:
        driver.maximize_window()
        return driver

def open_page(page,driver):
    website = "https://www.daraz.pk/laptops/?page="+str(page)+"&style=list"
    try:
        driver.set_page_load_timeout(100)
        driver.implicitly_wait(50)
        driver.get(website)
    except Exception as e:
        logging.error(e)

def find_element_extract_text(driver,el_xpath):
    try:
        description = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH,el_xpath))
        )
    except NoSuchElementException as e:
        logging.error(e)
        return ''
    else:
        return description.text
    
# Scraping Daraz Laptop category Products
def Scraping(start_page,page_increment,max_retrieves,connection):

    count = 1
    page = start_page
    pageincrement = page_increment
    maxretrieves = max_retrieves

#   Connecting with Chrome browser and opening daraz laptops category page

    driver = webdriver_connection()
    open_page(page,driver)

    print("Scraping page ",page)
    while True:
        
        try:
            if pageincrement*page > maxretrieves:
                break
            if count>pageincrement:
                count = 1
                page +=1

                print("Scraping page ",page)
                open_page(page,driver)

            # Scraping products titles
            try:
                driver.implicitly_wait(20)
                xpathTitle = '//*[@id="root"]/div/div[2]/div[1]/div/div[1]/div[2]/div['+str(count)+']/div/div[2]/div[2]/a'
                title = driver.find_element(by='xpath',value=xpathTitle)
            except NoSuchElementException as e:
                logging.error(e)
                title_text = ''
            else:
                title_text = title.text
                title.click()

            # Scraping products discription
            xpathdescription = '//*[@id="module_product_detail"]/div/div[1]/div[1]/ul'
            description = find_element_extract_text(driver,xpathdescription)

            # Scraping products price
            xpathprice = '//*[@id="module_product_price_1"]/div/div/span'
            price = find_element_extract_text(driver,xpathprice)

            driver.execute_script("window.scrollBy(0,2000)","")

            # Scraping products Rating
            xpathRating = '//*[@id="module_product_review"]/div/div/div[1]/div[2]/div/div/div[1]/div[1]'
            Rating =find_element_extract_text(driver,xpathRating).split('/')[0]
            
            # Scraping products Reviews
            xpathTotal_reviews = '//*[@id="module_product_review"]/div/div/div[1]/div[2]/div/div/div[1]/div[3]'
            Total_reviews =  find_element_extract_text(driver,xpathTotal_reviews).split('R')[0]

            # Inserting Data to Database
            conn = connection
            cursor = conn.cursor()
            insert_query = f"INSERT INTO Laptop_Products (Product_title, Product_price, No_of_Reviews, Product_Rating, Product_description) VALUES (%s,%s,%s,%s,%s)"
            data = (title_text, price, int(Total_reviews), float(Rating), description)
            cursor.execute(insert_query,data)
            conn.commit()

            open_page(page,driver)
                
            count+=1

        except Exception as e:
            logging.error(e)
            count+=1

            if pageincrement*page >maxretrieves:
                break
            if count>pageincrement:
                count = 1
                page +=1
            
            open_page(page,driver)

    # driver.close()
    # driver.quit()
    


if __name__ == '__main__':

# Getting MySQL database connection requirements

    print("\nGive following information to build MySQL connection.")
    Host = input("Enter your host.\n")
    User = input("Enter your MySQL username.\n")
    Password = input("Enter your MySQL password.\n")
    Database =  input("Enter your MySQL database name.\n")

    conn = connection_database(Host,User,Password,Database)
    Table_creation(conn)

    print("\nEnter basic Scraping details: \n")

    startpage = int(input("Enter the page number from which you want to start scraping.\n"))
    pageincrement = int(input("Enter how many products you want to scrap per page.\n(Note: the number should be <= to total number of products per page)\n"))
    maxretrieve = int(input("Enter how many max number of products you want to scrap.\n"))

    Scraping(1,pageincrement,maxretrieve,conn)
