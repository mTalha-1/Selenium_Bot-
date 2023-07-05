from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep


count = 1
page = 1
pageincrement = 40
maxretrieves = 1040

website = "https://www.daraz.pk/laptops/?page="+str(page) +"&spm=a2a0e.home.cate_7.5.5a494076JWE33V&style=list"
path = "C:/Users/dell/Desktop/selenium_bot/chromedriver_win32/chromedriver"
service =   Service(executable_path =path)
driver = webdriver.Chrome(service=service)
driver.maximize_window()
driver.get(website)
driver.set_page_load_timeout(10)

while True:
    
    try:
        if pageincrement*page > maxretrieves:
            break
        if count>pageincrement:
            count = 1
            page +=1

            website = "https://www.daraz.pk/laptops/?page="+str(page) +"&spm=a2a0e.home.cate_7.5.5a494076JWE33V&style=list"
            driver.get(website)
            driver.set_page_load_timeout(20)
    
        xpathTitle = '//*[@id="root"]/div/div[2]/div[1]/div/div[1]/div[2]/div['+str(count)+']/div/div[2]/div[2]/a'
        title = driver.find_element(by='xpath',value=xpathTitle)
        title_text = title.text
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
            Rating_text = Rating.text
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

        print("__________________ Product"+str(count)+"_________________________")
        print(title_text,"\n",price_text,"\n", description_text,"\n",Total_reviews_text,"\n", Rating_text, "\n\n")
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



