
# Selenium Bot (Daraz Products Scrapper)

This is a Selenium Bot that scraps Daraz laptop categories products using Selenium automation, this bot also stores errors, warnings, critical errors and some info in log file that will help you to identify the problem if occur, and you can also schedule it that help you to scrap updated content.



## Prerequisites For Running Project

* First create a virtual environment in your directory location in which you want to run a program:
```
python -m venv env_name
```
* After creating a virtual environment, you have to activate the virtual environment:
    - For Windows:
    ```
    env_name\scripts\activate.bat
    ```
    - For Linux|macOS:
    ```
    source env_name/bin/activate
    ```
* After creating a virtual environment, clone my GitHub repository into the folder in which you created the virtual environment.
* The repository contain **chromedriver.exe** for **windows**, make sure that you save that file at that location where you saved project file. If you have other OS and version of chrome browser, then install **chromedriver** from this page [page](https://chromedriver.chromium.org/downloads).

* This project run, if you have **Chrome browser**, to run it for other browsers you have to install a web driver for your browser and change driver path in code.
* You should have also a MySQL database management system in your system, and create a database using the following query:
```
CREATE DATABASE database_name
```
* Then install **requirements.txt** file using following command:
```
pip install -r requirements.txt
```

Now, you can run the project and enjoy the scraping process.

## Features

- Scrap data of products from laptop categories of data.
- Support navigate pagination.
- Save basic Information, Errors, Warnings, and Critical Errors in a log file. 
- Store product data in MySQL database.
- You can schedule it to extract updated data.


## Scheduling the project using a task scheduler
1. First open the task scheduler in the window and then click on Create task the following window will pop up, write the name of the task and description (optional):
![Screenshot (117)](https://github.com/mTalha-1/Selenium_Bot_web_scraping/assets/121819520/f5d7fc3b-b0ca-4937-971d-e3487998e4ac)
2. Then click on Trigger on the top bar, select the trigger that suits you better, and press ok:
![Screenshot (118)](https://github.com/mTalha-1/Selenium_Bot_web_scraping/assets/121819520/98c7856b-7bfd-4e5a-88e7-81f282ad7361)
3. Now select actions from the top bar, before moving further first open the command prompt and write the following command and copy the first path:
```
where python
```
![Screenshot (120)](https://github.com/mTalha-1/Selenium_Bot_web_scraping/assets/121819520/7f51368a-0496-4aa9-bf4d-836c1d528c60)
4. Paste copied path in the program script text bar, then write the program name at the **add argument** bar and the program file path at **start in**:
![Screenshot (121)](https://github.com/mTalha-1/Selenium_Bot_web_scraping/assets/121819520/e669dd17-9c43-41a9-b7d4-6cfbb336f489)
5. Then press ok, and  write the password of the account profile:
![Screenshot (122)](https://github.com/mTalha-1/Selenium_Bot_web_scraping/assets/121819520/b51493fd-8724-439f-8536-630120107104)
## 🔗 Links
[![portfolio](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://www.novypro.com/profile_projects/m-talhaasif-shazad)

[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/muhammadtalha0a1/)

