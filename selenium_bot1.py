from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import mysql.connector
from time import sleep

# Getting MySQL database connection requirements
print("\nGive following information to build MySQL connection.")
Host = input("Enter your host.\n")
User = input("Enter your MySQL username.\n")
Password = input("Enter your MySQL password.\n")
Database =  input("Enter your MySQL database name.\n")

# Building Database connection
try:
    conn = mysql.connector.connect(
            host=Host,
            user= User,     
            password= Password, 
            database= Database  
        )
except Exception as e:
    print(e)
else:
    cursor = conn.cursor()

# Function for creating Table, if table exist first delete it and then creat.
def Table_creation():

    table_name = "Laptop_Products"

    table_exists_query = """
    SELECT COUNT(*)
    FROM information_schema.tables
    WHERE table_schema = '{database}'
        AND table_name = '{table}'
    """.format(database= Database, table=table_name)

    cursor.execute(table_exists_query)
    table_exists = cursor.fetchone()[0]

    if table_exists:
        # Table exists, so delete it
        delete_table_query = "DROP TABLE {table}".format(table=table_name)
        cursor.execute(delete_table_query)
        print("Table deleted successfully.")
    else:
        print("Table does not exist.")

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
    cursor.execute(create_table_query)
    print("Table created successfully.")


# Scraping Daraz Laptop category Products
def Scraping(start_page,page_increment,max_retrieves,chromedriver_path):

    count = 1
    page = start_page
    pageincrement = page_increment
    maxretrieves = max_retrieves

    website = "https://www.daraz.pk/laptops/?page="+str(page) +"&spm=a2a0e.home.cate_7.5.5a494076JWE33V&style=list"
    path = chromedriver_path

    service =   Service(executable_path =path)
    driver = webdriver.Chrome(service=service)

    driver.maximize_window()
    driver.get(website)
    driver.set_page_load_timeout(10)

    print("Scraping page ",page)
    while True:
        
        try:
            if pageincrement*page > maxretrieves:
                break
            if count>pageincrement:
                count = 1
                page +=1
                
                print("Scraping page ",page)
                website = "https://www.daraz.pk/laptops/?page="+str(page) +"&spm=a2a0e.home.cate_7.5.5a494076JWE33V&style=list"
                driver.get(website)
                driver.set_page_load_timeout(30)

            try:
                xpathTitle = '//*[@id="root"]/div/div[2]/div[1]/div/div[1]/div[2]/div['+str(count)+']/div/div[2]/div[2]/a'
                title = driver.find_element(by='xpath',value=xpathTitle)
            except Exception as e:
                print(e)
                title_text = ''
            else:
                title_text = title.text
            finally:
                title.click()
                driver.implicitly_wait(10)

            try:
                xpathdescription = '//*[@id="module_product_detail"]/div/div[1]/div[1]/ul'
                description = driver.find_element(by='xpath',value=xpathdescription)
            except Exception as e:
                print(e)
                description_text = ''
            else:
                description_text = description.text
            finally:
                driver.implicitly_wait(10)

            try:
                xpathprice = '//*[@id="module_product_price_1"]/div/div/span'
                price = driver.find_element(by='xpath',value=xpathprice)
            except Exception as e:
                print(e)
                price_text = ''
            else:
                price_text = price.text
            finally:
                driver.execute_script("window.scrollBy(0,2000)","")
                driver.implicitly_wait(4)

            try:
                xpathRating = '//*[@id="module_product_review"]/div/div/div[1]/div[2]/div/div/div[1]/div[1]'
                Rating = driver.find_element(by='xpath',value=xpathRating)
            except Exception as e:
                print(e)
                Rating_text = ''
            else:
                Rating_text = Rating.text.split('/')[0]
            finally:
                driver.implicitly_wait(4)

            try:
                xpathTotal_reviews = '//*[@id="module_product_review"]/div/div/div[1]/div[2]/div/div/div[1]/div[3]'
                Total_reviews = driver.find_element(by='xpath',value=xpathTotal_reviews)
            except Exception as e:
                print(e)
                Total_reviews_text = ''
            else:
                Total_reviews_text = Total_reviews.text.split('R')[0]
            finally:
                driver.implicitly_wait(4)

            website = "https://www.daraz.pk/laptops/?page="+str(page) +"&spm=a2a0e.home.cate_7.5.5a494076JWE33V&style=list"
            driver.get(website)
            driver.set_page_load_timeout(20)


            insert_query = f"INSERT INTO Laptop_Products (Product_title, Product_price, No_of_Reviews, Product_Rating, Product_description) VALUES (%s,%s,%s,%s,%s)"
            data = (title_text, price_text, int(Total_reviews_text), float(Rating_text), description_text)
            cursor.execute(insert_query,data)
            conn.commit()

            count+=1
        except Exception as e:
            print(e)
            count+=1

            if pageincrement*page >maxretrieves:
                break
            if count>pageincrement:
                count = 1
                page +=1
            
            website = "https://www.daraz.pk/laptops/?page="+str(page) +"&spm=a2a0e.home.cate_7.5.5a494076JWE33V&style=list"
            driver.get(website)
            driver.set_page_load_timeout(20)

    driver.close()



Chromedriver_path = "C:/Users/dell/Desktop/selenium_bot/chromedriver_win32/chromedriver"
Table_creation()

print("Enter basic Scraping details: ")

startpage = int(input("Enter the page number from which you want to start scraping.\n"))
pageincrement = int(input("Enter how many products you want to scrap per page.\n(Note: the number should be <= to total number of products per page)\n"))
maxretrieve = int(input("Enter max number of products you want to scrap.\n"))
Scraping(startpage,pageincrement,maxretrieve,Chromedriver_path)