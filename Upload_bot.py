import csv
import os
import time
from datetime import datetime
import requests
import pandas as pd

try:
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.support import expected_conditions as ec
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import Select
    from selenium.webdriver.chrome.options import Options
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys

    from selenium.common.exceptions import ElementClickInterceptedException
except ModuleNotFoundError:
    print("Please install Selenium Module in your IDE")

website_url = "https://app.aestheticrecord.com/login"
website_credentials = {
    'Username': 'demo4@aestheticrecord.com',
    'Password': '123456'
}
# ahsan@migration.com

# "https://aestheticrecord.com/clients/documents/add/id/profile" add docs
# "https://aestheticrecord.com/clients/customer-notes/id/profile" add notes
# "https://aestheticrecord.com/appointment/create/client/id" create appointment

download_dir = "C://Users/123/PycharmProjects/AestheticRecord/Data/"
path_to_image = os.path.join(download_dir, "upload.jpg")
path_to_pdf = os.path.join(download_dir, "upload.pdf")
data_dir = "C://Users/123/PycharmProjects/AestheticRecord/Clients/MindBody/Data/"


# def log_in(driver):
#     WebDriverWait(driver, 10000).until(
#         ec.visibility_of_element_located((By.CLASS_NAME, "login-form-submit-anchor")))
#     driver.find_element_by_xpath('//*[@id="UserEmailId"]').send_keys(website_credentials.get('Username'))
#     time.sleep(1)
#     driver.find_element_by_xpath('//*[@id="UserPassword"]').send_keys(website_credentials.get('Password'))
#     driver.find_element_by_class_name('login-form-submit-anchor').click()
#     time.sleep(15)
#     # Handle already login case.
#     # "Already logged in"  //node()[@id='model_title']
#     # //button[text()='Login'] click
#
#     # https://aestheticrecord.com/clients ______after login url
#     print("Account Logged In.!")
#     # if driver.current_url == 'https://aestheticrecord.com/dashboard':
#     #     driver.get(url="https://aestheticrecord.com/clients")
#     #     WebDriverWait(driver, 30).until(
#     #         lambda x: x.execute_script('return document.readyState') == 'complete')
#     #     time.sleep(2)


def upload_images_and_documents(driver, data, index, flag):
    i = 0
    path = ''
    while i < len(data):
        url = data[i]
        file_name = url.split('/')[-1]
        response = requests.get(url)
        if response.status_code == 200:
            if not flag:
                path = path_to_image
            else:
                path = path_to_pdf
            f = open(path, 'wb')
            f.write(response.content)
            f.close()
        driver.implicitly_wait(1000)
        time.sleep(10)
        driver.find_elements_by_xpath("//input[@type='file']")[index].send_keys(path)
        driver.find_elements_by_xpath("//input[@name='document_name']")[index].send_keys(file_name)
        time.sleep(10)
        driver.implicitly_wait(1000)
        if i + 1 < len(data):
            driver.find_element_by_xpath('//*[@class="add-document-btns"]/a').click()
            driver.implicitly_wait(1000)
        driver.implicitly_wait(1000)
        i = i + 1
        index = index + 1


def temp_fun(driver, row):
    driver.find_element_by_xpath('//table[@class="table-updated juvly-table min-w-1000"]/tbody//td[2]').click()
    WebDriverWait(driver, 10000).until(
        ec.visibility_of_element_located((By.ID, "dropdownMenu1")))
    time.sleep(3)
    driver.find_element(By.ID, "dropdownMenu1").click()
    time.sleep(3)
    driver.find_element_by_xpath(
        "//a[@class='header-unselect-btn setting modal-link']").click()  # //a[text()='Documents']
    time.sleep(3)
    driver.find_element_by_xpath('//*[@class="add-file-btn pull-right"]/a').click()
    driver.implicitly_wait(1000)

    # Here we upload all images and documents
    images_list = row['Images'].split('\n')
    images_list = list(filter(None, images_list))
    upload_images_and_documents(driver, images_list, 0, False)
    documents_list = row['PDFs'].split('\n')
    documents_list = list(filter(None, documents_list))
    if documents_list:
        driver.find_element_by_xpath('//*[@class="add-document-btns"]/a').click()
    upload_images_and_documents(driver, documents_list, len(images_list), True)
    time.sleep(20)

    driver.find_element_by_xpath('//div[@class="footer-static"]/a[text()="Save"]').click()
    time.sleep(10)
    driver.find_element_by_xpath('//a[@href="/clients"]').click()
    driver.implicitly_wait(1000)

    # print(f'Record No {i} is Uploaded')


def create_client(driver, client_id):
    client_data = pd.read_csv(r'C:\Users\Lenovo\PycharmProjects\AestheticPro\AestheticPro_data\Client_Details.csv',
                              encoding='cp1252')
    time.sleep(10)
    WebDriverWait(driver, 10000).until(
        ec.visibility_of_element_located((By.CLASS_NAME, "blue-btn")))
    driver.find_element_by_class_name("blue-btn").click()
    time.sleep(5)

    name = client_data['Name'][client_data['Client ID'] == client_id]
    name = name.values[0]
    first_name = name.split(' ')[0]
    last_name = name.split(' ')[1]
    driver.find_element_by_xpath('//input[@name="firstname"]').send_keys(first_name)
    time.sleep(1)
    driver.find_element_by_xpath('//input[@name="lastname"]').send_keys(last_name)
    time.sleep(1)
    driver.find_element_by_xpath('//input[@name="nick_name"]').send_keys(' ')
    time.sleep(1)

    email = client_data['Email'][client_data['Client ID'] == client_id]
    email = email.values[0]
    if '@' in str(email):
        email = ' '
    driver.find_element_by_xpath('//input[@name="email"]').send_keys(email)
    time.sleep(1)

    phone = client_data['Mobile Phone'][client_data['Client ID'] == client_id]
    phone = phone.values[0]
    if any(char.isdigit() for char in str(phone)):
        pass
    else:
        phone = client_data['Home Phone'][client_data['Client ID'] == client_id]
        phone = phone.values[0]
        if any(char.isdigit() for char in str(phone)):
            pass
        else:
            phone = client_data['Work Phone'][client_data['Client ID'] == client_id]
            phone = phone.values[0]
            if any(char.isdigit() for char in str(phone)):
                pass
            else:
                phone = ' '
    driver.find_element_by_xpath('//input[@name="phoneNumber"]').send_keys(phone)
    time.sleep(1)

    gender = client_data['Gender'][client_data['Client ID'] == client_id]
    gender = gender.values[0]
    driver.find_element_by_xpath('//select[@name="gender"]').click()
    gender_val = '0' if gender == 'Male' else '1' if gender == 'Female' else '2'
    driver.find_element_by_xpath('//select[@name="gender"]/option[@value=' + gender_val + ']').click()
    time.sleep(1)

    dob = client_data['Birthdate'][client_data['Client ID'] == client_id]
    dob = dob.values[0]
    dob = str(dob)
    if '-' in dob or '/' in dob:
        if '-' in dob:
            day = dob.split('-')[1]
            month = dob.split('-')[0]
            year = '19' + dob.split('-')[2]
        else:
            day = dob.split('/')[1]
            month = dob.split('/')[0]
            year = dob.split('/')[2]
        if day[0] == '0':
            day = day[1]
        if month[0] == '0':
            month = month[1]
        month = int(month) - 1
        month = str(month)
        driver.find_element_by_xpath("//div[@class='react-datepicker-wrapper']").click()
        date = driver.find_element_by_xpath("//input[@class='setting-input-box p-r-40 react-datepicker-ignore-onclickoutside']")
        date.click()
        year_picker = driver.find_element_by_xpath("//select[@class='react-datepicker__year-select']")
        year_picker.click()
        time.sleep(0.5)
        year_to_select = driver.find_element_by_xpath("//option[@value='" + year + "']")
        year_to_select.click()
        time.sleep(0.5)
        month_picker = driver.find_element_by_xpath("//select[@class='react-datepicker__month-select']")
        month_picker.click()
        time.sleep(0.5)
        month_to_select = driver.find_element_by_xpath("//option[@value='" + month + "']")
        month_to_select.click()
        time.sleep(0.5)

        driver.find_element_by_xpath("//div[@aria-disabled='false' and text()='" + day + "']").click()
        time.sleep(2)

    # driver.find_element_by_xpath('//select[@name="referral_source"]').click()
    # driver.find_element_by_xpath(
    #     '//select[@name="referral_source"]/option[text()=' + data['Referral Source'] + ']').click()
    # time.sleep(1)

    driver.find_element_by_xpath('//select[@name="clinic_id"]').click()
    driver.find_element_by_xpath('//select[@name="clinic_id"]/option[@value="2"]').click()
    time.sleep(1)

    # driver.find_element_by_xpath('//input[@name="ssn_number"]').send_keys(data['SSN'])
    # time.sleep(1)

    address = client_data['Address'][client_data['Client ID'] == client_id]
    address = address.values[0]
    driver.find_element_by_xpath('//input[@name="address_line_1"]').send_keys(address)
    time.sleep(1)

    city = client_data['Client Location'][client_data['Client ID'] == client_id]
    city = city.values[0]
    driver.find_element_by_xpath('//input[@name="city"]').send_keys(city)
    time.sleep(1)

    time.sleep(1)
    # driver.find_element_by_xpath('//*[@id="saveConsultation"]').click()
    # time.sleep(10)
    # WebDriverWait(driver, 100).until(
    #     ec.visibility_of_element_located((By.CLASS_NAME, "blue-btn")))
    print('Client Added successfully!!')

    # add_documents(driver)
    # temp_fun(driver, data)
    # print("Files added successfully..!")


def get_filename(s):
    return s.split(' ', 1)[1][::-1].split(' ', 3)[3][::-1]


# def add_notes_double_check(driver, client_id, dictdata):
#     driver.get(
#         f"https://app.aestheticrecord.com/clients/customer-notes/{client_id}/profile")
#     WebDriverWait(driver, 30).until(
#         lambda x: x.execute_script('return document.readyState') == 'complete')
#     time.sleep(3.5)
#
#     status = driver.find_elements_by_xpath("//div[@class='circle']")
#     if len(status) == 0:
#         driver.find_element_by_xpath("//node()[@id='notes']").send_keys(
#             dictdata['Notes'].strip())
#         time.sleep(3.5)
#
#         if len(dictdata['Notes']) > 100:
#             time.sleep(3)
#         notesaveflag = False
#         while notesaveflag is False:
#             try:
#
#                 driver.find_element_by_xpath("//input[@type='submit']").click()
#                 WebDriverWait(driver, 30).until(
#                     lambda x: x.execute_script('return document.readyState') == 'complete')
#                 time.sleep(5)
#                 notesaveflag = True
#             except ElementClickInterceptedException:
#                 time.sleep(5)
#
#         print('Notes added successfully!!')
#         return 1
#     else:
#         print('Already Added.!!')
#         return 0


# def add_docs_server_issue(driver, client_id, dictdata, missingfiles_writer):
#     # Short save time path
#     driver.get(f"https://app.aestheticrecord.com/clients/documents/add/{client_id}/profile")
#     WebDriverWait(driver, 30).until(
#         lambda x: x.execute_script('return document.readyState') == 'complete')
#     time.sleep(2)
#     # *******Target page reached.
#
#     directory = dictdata['ID']
#     doc_list = dictdata['Documents'].split('\n')
#     print("  >>>>Total docs:", len(doc_list))
#     i = 0
#     filename = ''
#     for doc in doc_list:
#
#         retry_times_add_more_doc = 3
#         filename = get_filename(doc)
#         # print(filename)
#         path = os.path.join(data_dir, f'{directory}/{filename}')
#         # print(path, ' **** ', os.path.exists(path))
#         if os.path.exists(path):  # if file-path exist
#             driver.find_elements_by_xpath("//input[@type='file']")[-1].send_keys(path)
#             driver.find_elements_by_xpath("//input[@name='document_name']")[-1].send_keys(
#                 filename)
#             WebDriverWait(driver, 30).until(
#                 lambda x: x.execute_script('return document.readyState') == 'complete')
#             time.sleep(3)
#             driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
#             time.sleep(1)
#             if i + 1 < len(doc_list):
#                 addmoredocflag = False
#                 while addmoredocflag is False:
#                     try:
#                         driver.find_element_by_xpath(
#                             "//a[text()='Add More Documents']").click()
#                         driver.implicitly_wait(100)
#                         addmoredocflag = True
#                     except ElementClickInterceptedException:
#                         retry_times_add_more_doc -= 1
#                         if retry_times_add_more_doc > 0:
#                             if filename[len(filename) - 1] == 'f':
#                                 time.sleep(15)
#                             else:
#                                 time.sleep(10)
#                         else:
#                             print(
#                                 f">>>> Internet or server down (1) retrying.       "
#                                 f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
#                             add_docs_server_issue(driver, client_id, dictdata, missingfiles_writer)
#                             print("returing back")
#                             return
#
#         else:
#             print(f'{directory} missing file {filename}')
#             missingfiles_writer.writerow([directory, client_id, filename])
#         driver.implicitly_wait(100)
#         i = i + 1
#
#     retry_times = 3
#     docsaveflag = False
#     while docsaveflag is False:
#         try:
#             driver.find_element_by_xpath(
#                 '//div[@class="footer-static"]/a[text()="Save"]').click()
#             WebDriverWait(driver, 30).until(
#                 lambda x: x.execute_script('return document.readyState') == 'complete')
#             time.sleep(4)
#             docsaveflag = True
#             print("doc saved.")
#         except ElementClickInterceptedException:
#             retry_times -= 1
#             if retry_times > 0:
#                 if filename[len(filename) - 1] == 'f':
#                     time.sleep(15)
#                 else:
#                     time.sleep(10)
#             else:
#                 print(f">>>> Internet or server down (2) retrying.     {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
#                 add_docs_server_issue(driver, client_id, dictdata, missingfiles_writer)
#                 print("returning no save")
#                 return


# TODO at the end we may need to remove missingfilescsv dup based upon filenames


def add_docs(driver, client_id, url_client_id, name):

    driver.get(f"https://app.aestheticrecord.com/clients/documents/add/{url_client_id}/profile")
    WebDriverWait(driver, 30).until(
        lambda x: x.execute_script('return document.readyState') == 'complete')
    time.sleep(2)

    directory = r'C:\Users\Lenovo\PycharmProjects\AestheticPro\AestheticPro_data\Client_Attachments\Other _Attachments'
    client_file_path = os.path.join(f'{directory}\\{client_id}')
    doc_list = os.listdir(client_file_path)
    print("  >>>>Total docs:", len(doc_list))
    filename = ''
    i = 0
    for doc in doc_list:
        retry_times_add_more_doc = 3
        file_path = os.path.join(f'{client_file_path}\\{doc}')
        print(f'  >>>>File path {file_path}')
        filename = os.path.basename(file_path)
        print(f'  >>>>Adding {filename}...')
        if os.path.exists(file_path):
            driver.find_elements_by_xpath("//input[@type='file']")[-1].send_keys(file_path)
            driver.find_elements_by_xpath("//input[@name='document_name']")[-1].send_keys(
                filename)
            WebDriverWait(driver, 30).until(
                lambda x: x.execute_script('return document.readyState') == 'complete')
            time.sleep(3)
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(1)
            if i + 1 < len(doc_list):
                addmoredocflag = False
                while addmoredocflag is False:
                    try:
                        driver.find_element_by_xpath("//a[text()='Add More Documents']").click()
                        driver.implicitly_wait(100)
                        addmoredocflag = True
                    except ElementClickInterceptedException:
                        retry_times_add_more_doc -= 1
                        if retry_times_add_more_doc > 0:
                            if filename[len(filename) - 1] == 'f':
                                time.sleep(15)
                            else:
                                time.sleep(10)
                        else:
                            print(
                                f"  >>>>Internet or server down (1) retrying.       "
                                f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
                            return
        else:
            print(f'There is no file named {filename} in the directory {directory} ')
        driver.implicitly_wait(100)
        i = i + 1
    retry_times = 3
    docsaveflag = False
    while docsaveflag is False:
        try:
            driver.find_element_by_xpath(
                '//div[@class="footer-static"]/a[text()="Save"]').click()
            WebDriverWait(driver, 30).until(
                lambda x: x.execute_script('return document.readyState') == 'complete')
            time.sleep(7)
            docsaveflag = True
            print("  >>>>Doc saved from add_doc()")
        except ElementClickInterceptedException:
            retry_times -= 1
            if retry_times > 0:
                if filename[len(filename) - 1] == 'f':
                    time.sleep(15)
                else:
                    time.sleep(10)
            else:
                print(f">>>> Internet or server down (2) retrying.     {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
                print("  >>>>Returning without saving from add_doc()")
                return

    with open(r'C:\Users\Lenovo\PycharmProjects\AestheticPro\AestheticPro_data\Docs uploaded.csv', 'a',
              newline='') as uploaded:
        writer = csv.writer(uploaded)
        data = [client_id, name]
        writer.writerow(data)


def enter_dup_docs(driver):


    client_data = pd.read_csv(r'C:\Users\Lenovo\PycharmProjects\AestheticPro\AestheticPro_data\Duplicate Clients.csv',
                              encoding='cp1252')
    client_list = list(client_data['Client ID'])
    # client_list = client_list[33:]
    for client_id in client_list:
        name = client_data['Name'][client_data['Client ID'] == int(client_id)]
        name = name.values[0]
        print(f'Now processing {client_id}: {name}...')
        time.sleep(1)
        search_bar = driver.find_element_by_class_name('search-key')
        search_bar.clear()
        search_bar.send_keys(name + Keys.ENTER)
        WebDriverWait(driver, 30).until(
            lambda x: x.execute_script('return document.readyState') == 'complete')
        time.sleep(3)
        result_count = driver.find_element_by_xpath("//b[@id='customers_count']")
        print(f"   >>>> Total '{result_count.text}' patient(s) Found.")
        result = int(result_count.text.strip())
        if result == 0:
            print(f'  >>>>No record found for {name}')
            print(f'  >>>>Appending {name} to Clients not created list')
            with open(r'C:\Users\Lenovo\PycharmProjects\AestheticPro\AestheticPro_data\Clients not created.csv',
                      'a', newline='') as f2:
                wr = csv.writer(f2)
                row = [client_id, name]
                wr.writerow(row)
        elif result == 1:
            print(f'  >>>>Adding {name}\'s documents...')
            driver.find_element_by_class_name('td-clinic-name').click()
            WebDriverWait(driver, 30).until(
                lambda x: x.execute_script('return document.readyState') == 'complete')
            time.sleep(2)
            url_client_id = driver.current_url.split('/')[-1]
            time.sleep(1)
            add_docs(driver, client_id, url_client_id, name)
            time.sleep(2)
            driver.find_element_by_xpath("//label[text()='Clients']").click()
            time.sleep(2)


def enter_docs(driver):

    client_list = os.listdir(
        r'C:\Users\Lenovo\PycharmProjects\AestheticPro\AestheticPro_data\Client_Attachments\Other _Attachments')
    client_data = pd.read_csv(r'C:\Users\Lenovo\PycharmProjects\AestheticPro\AestheticPro_data\Client_Details.csv',
                              encoding='cp1252')
    # client_list = client_list[33:]
    for client_id in client_list:
        name = client_data['Name'][client_data['Client ID'] == int(client_id)]
        name = name.values[0]
        print(f'Now processing {client_id}: {name}...')
        time.sleep(1)
        search_bar = driver.find_element_by_class_name('search-key')
        search_bar.clear()
        search_bar.send_keys(name + Keys.ENTER)
        WebDriverWait(driver, 30).until(
            lambda x: x.execute_script('return document.readyState') == 'complete')
        time.sleep(3)
        result_count = driver.find_element_by_xpath("//b[@id='customers_count']")
        print(f"   >>>> Total '{result_count.text}' patient(s) Found.")
        result = int(result_count.text.strip())
        if result == 0 or result > 1:
            if result:
                print(f'  >>>>Duplicate result: {name}')
                print('   >>>>Searching through email now...')
                email = client_data['Email'][client_data['Client ID'] == int(client_id)]
                email = email.values[0]
                print(f'   >>>>Email: {email}')
                try:
                    if '@' in email:
                        search_bar.clear()
                        search_bar.send_keys(email + Keys.ENTER)
                        WebDriverWait(driver, 30).until(
                            lambda x: x.execute_script('return document.readyState') == 'complete')
                        time.sleep(3)
                        result_count = driver.find_element_by_xpath("//b[@id='customers_count']")
                        print(f"   >>>> Total '{result_count.text}' patient(s) Found.")
                        result = int(result_count.text.strip())
                        if result == 0 or result > 1:
                            with open(r'C:\Users\Lenovo\PycharmProjects\AestheticPro\AestheticPro_data\Duplicate Clients.csv',
                                      'a', newline='') as f2:
                                wr = csv.writer(f2)
                                row = [client_id, name]
                                wr.writerow(row)
                        elif result == 1:
                            print(f'   >>>>Adding {name}\'s documents...')
                            driver.find_element_by_class_name('td-clinic-name').click()
                            WebDriverWait(driver, 30).until(
                                lambda x: x.execute_script('return document.readyState') == 'complete')
                            time.sleep(2)
                            url_client_id = driver.current_url.split('/')[-1]
                            time.sleep(1)
                            add_docs(driver, client_id, url_client_id, name)
                            time.sleep(3)
                            driver.find_element_by_xpath("//label[text()='Clients']").click()
                            time.sleep(3)
                except TypeError:
                    print('   >>>>Email not found')
                    with open(r'C:\Users\Lenovo\PycharmProjects\AestheticPro\AestheticPro_data\Duplicate Clients.csv',
                              'a', newline='') as f2:
                        wr = csv.writer(f2)
                        row = [client_id, name]
                        wr.writerow(row)
            else:
                print(f'   >>>>No record found for {name}')
                print('   >>>>Searching through email now...')
                email = client_data['Email'][client_data['Client ID'] == int(client_id)]
                email = email.values[0]
                print(f'   >>>>Email: {email}')
                try:
                    if '@' in email:
                        search_bar.clear()
                        search_bar.send_keys(email + Keys.ENTER)
                        WebDriverWait(driver, 30).until(
                            lambda x: x.execute_script('return document.readyState') == 'complete')
                        time.sleep(3)
                        result_count = driver.find_element_by_xpath("//b[@id='customers_count']")
                        print(f"   >>>> Total '{result_count.text}' patient(s) Found.")
                        result = int(result_count.text.strip())
                        if result == 0:
                            print('  >>>>Still no records found.')
                            with open(r'C:\Users\Lenovo\PycharmProjects\AestheticPro\AestheticPro_data\Clients not created.csv',
                                      'a', newline='') as f2:
                                wr = csv.writer(f2)
                                row = [client_id, name]
                                wr.writerow(row)
                        elif result == 1:
                            print(f'  >>>>Adding {name}\'s documents...')
                            driver.find_element_by_class_name('td-clinic-name').click()
                            WebDriverWait(driver, 30).until(
                                lambda x: x.execute_script('return document.readyState') == 'complete')
                            time.sleep(2)
                            url_client_id = driver.current_url.split('/')[-1]
                            time.sleep(1)
                            add_docs(driver, client_id, url_client_id, name)
                            time.sleep(2)
                            driver.find_element_by_xpath("//label[text()='Clients']").click()
                            time.sleep(2)
                        else:
                            print(f'   >>>>Duplicate result')
                            with open(r'C:\Users\Lenovo\PycharmProjects\AestheticPro\AestheticPro_data\Duplicate Clients.csv',
                                      'a', newline='') as f2:
                                wr = csv.writer(f2)
                                row = [client_id, name]
                                wr.writerow(row)
                except TypeError:
                    print('   >>>>Email not found')
                    with open(r'C:\Users\Lenovo\PycharmProjects\AestheticPro\AestheticPro_data\Clients not created.csv',
                              'a', newline='') as f2:
                        wr = csv.writer(f2)
                        row = [client_id, name]
                        wr.writerow(row)
        else:
            print(f'   >>>>Adding {name}\'s documents...')
            driver.find_element_by_class_name('td-clinic-name').click()
            WebDriverWait(driver, 30).until(
                lambda x: x.execute_script('return document.readyState') == 'complete')
            time.sleep(2)
            url_client_id = driver.current_url.split('/')[-1]
            time.sleep(1)
            add_docs(driver, client_id, url_client_id, name)
            time.sleep(2)
            driver.find_element_by_xpath("//label[text()='Clients']").click()
            time.sleep(2)


def internet_access():
    while True:
        try:
            requests.get("https://www.example.com/")
            return
        except Exception as exc:
            print("Internet connection Lost. . .", exc)
            del exc
            time.sleep(15)


# def double_check_on_notes(driver):
#     csv_file1 = open('notes_processed_clients.csv', 'a', newline='', encoding="utf-8", errors="replace")
#     processed_writer = csv.writer(csv_file1)
#     # processed_writer.writerow(['AR_ID', 'Full Name', 'First Name', 'Last Name', 'Email'])
#
#     csv_file2 = open('notes_ar_duplicates.csv', 'a', newline='', encoding="utf-8", errors="replace")
#     dup_writer = csv.writer(csv_file2)
#     # dup_writer.writerow(['MB_ID', 'Full Name', 'First Name', 'Last Name', 'Email'])
#
#     csv_file3 = open('notes_ar_norecord.csv', 'a', newline='', encoding="utf-8", errors="replace")
#     norecord_writer = csv.writer(csv_file3)
#     # norecord_writer.writerow(['MB_ID', 'Full Name'])
#
#     csv_file4 = open('notes_already_clients.csv', 'a', newline='', encoding="utf-8", errors="replace")
#     already_processed_writer = csv.writer(csv_file4)
#     # already_processed_writer.writerow(['AR_ID', 'Full Name', 'First Name', 'Last Name', 'Email'])
#
#     with open('client_details.csv') as csvfile:
#         read_csv = csv.DictReader(csvfile)
#         for record_no, dictdata in enumerate(read_csv, 2):  #
#             if record_no < 1173:  # TODO IMPORTANT: record no has been processed use that number here
#                 print(f" >>Client{record_no}---{dictdata['Full Name']} Processing..!   "
#                       f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
#
#                 if dictdata['Full Name'] == '':
#                     # create_client(driver, dictdata)
#                     print('It\' time to end.')
#                     break
#                 else:
#
#                     if dictdata['Notes'] == '':
#                         # print(f"{len(dictdata['Notes'].strip())}----{dictdata['Document Flag']}")
#                         print('Don t need to process.', 'It has no notes')
#
#                     else:
#                         # print(len(dictdata['Notes'].strip()), '____', dictdata['Document Flag'])
#                         print('we ll process it')
#                         # internet_access()
#                         notes_len = len(dictdata['Notes'].strip())
#                         if dictdata['Notes'].strip()[notes_len - 1] == '.':
#                             driver.find_element_by_class_name('search-key').send_keys(
#                                 dictdata['Full Name'].strip() + Keys.ENTER)
#                             WebDriverWait(driver, 30).until(
#                                 lambda x: x.execute_script('return document.readyState') == 'complete')
#                             time.sleep(3)
#                             # time.sleep(7)
#                             result_count = driver.find_element_by_xpath("//b[@id='customers_count']")
#                             # result = driver.find_elements_by_class_name('react-contextmenu-wrapper')
#                             print(f"   >>>> Total '{result_count.text}' patient(s) Found.")
#                             result = int(result_count.text.strip())
#                             if result == 0 or result > 1:
#                                 if result:
#                                     print(f'Ambigous result.. {dictdata["Full Name"]}::{dictdata["ID"]} ')
#                                     dup_writer.writerow([dictdata["ID"], dictdata["Full Name"], dictdata['First Name'],
#                                                          dictdata['Last Name'], dictdata['Email']])
#                                 else:
#                                     print(f'No record found for {dictdata["Full Name"]}::{dictdata["ID"]} ')
#                                     norecord_writer.writerow([dictdata["ID"], dictdata["Full Name"]])
#
#                             else:
#                                 driver.find_element_by_class_name('td-clinic-name').click()
#                                 WebDriverWait(driver, 30).until(
#                                     lambda x: x.execute_script('return document.readyState') == 'complete')
#                                 time.sleep(2)
#                                 # time.sleep(3.5)
#                                 client_id = driver.current_url.split('/')[-1]
#                                 notes_mark = 0
#
#                                 # Add Notes
#                                 if dictdata['Notes'] != '':
#                                     # print(" >> <<<we'll add notes>>>")
#
#                                     notes_len = len(dictdata['Notes'].strip())
#                                     print(f" >>> Notes Length: {notes_len}")
#                                     if dictdata['Notes'].strip()[notes_len - 1] == '.':
#                                         print("notes should be added manually")
#                                         notes_mark += 1
#                                         if add_notes_double_check(driver, client_id, dictdata):
#                                             mark = '|*|' if notes_mark == 1 else ''
#                                             processed_writer.writerow([f'{mark}{client_id}', dictdata['Full Name'],
#                                                                        dictdata['First Name'], dictdata['Last Name'],
#                                                                        dictdata['Email']])
#                                         else:
#                                             mark = '|*|' if notes_mark == 1 else ''
#                                             already_processed_writer.writerow(
#                                                 [f'{mark}{client_id}', dictdata['Full Name'],
#                                                  dictdata['First Name'],
#                                                  dictdata['Last Name'],
#                                                  dictdata['Email']])
#
#                                 else:
#                                     print(" >>>> No notes to add.")
#
#                             driver.get("https://app.aestheticrecord.com/clients")
#                             WebDriverWait(driver, 30).until(
#                                 lambda x: x.execute_script('return document.readyState') == 'complete')
#                             time.sleep(3)
#
#     csv_file1.close()
#     csv_file2.close()
#     csv_file3.close()
#     csv_file4.close()


# def mb_notes_docs_to_ar(driver):
#     csv_file1 = open('processed_clients.csv', 'a', newline='', encoding="utf-8", errors="replace")
#     processed_writer = csv.writer(csv_file1)
#     # processed_writer.writerow(['AR_ID', 'Full Name', 'First Name', 'Last Name', 'Email'])
#
#     csv_file2 = open('ar_duplicates.csv', 'a', newline='', encoding="utf-8", errors="replace")
#     dup_writer = csv.writer(csv_file2)
#     # dup_writer.writerow(['MB_ID', 'Full Name', 'First Name', 'Last Name', 'Email'])
#
#     csv_file3 = open('ar_norecord.csv', 'a', newline='', encoding="utf-8", errors="replace")
#     norecord_writer = csv.writer(csv_file3)
#     # norecord_writer.writerow(['MB_ID', 'Full Name'])
#
#     csv_file4 = open('missing_files.csv', 'a', newline='', encoding="utf-8", errors="replace")
#     missingfiles_writer = csv.writer(csv_file4)
#     # missingfiles_writer.writerow(['MB_ID', 'AR_ID', 'File Names'])
#
#     with open('client_details.csv') as csvfile:
#         read_csv = csv.DictReader(csvfile)
#         for record_no, dictdata in enumerate(read_csv, 2):  #
#             # print(f'{record_no}---{dictdata["Full Name"]}')
#             # TODO: manually 216(notes) should be added.
#             if record_no > 2363:  # TODO IMPORTANT: record no has been processed use that number here
#                 print(f" >>Client{record_no}---{dictdata['Full Name']} Processing..!   "
#                       f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
#
#                 if dictdata['Full Name'] == '':
#                     # create_client(driver, dictdata)
#                     print('It\' time to end.')
#                     break
#                 else:
#
#                     if dictdata['Notes'] == '' and dictdata['Document Flag'] == '0':
#                         # print(f"{len(dictdata['Notes'].strip())}----{dictdata['Document Flag']}")
#                         print('Don t need to process.', 'It has no notes or docs to add.')
#
#                     else:
#                         # print(len(dictdata['Notes'].strip()), '____', dictdata['Document Flag'])
#                         print('we ll process it')
#                         # internet_access()
#                         # search client by email or full name
#                         if dictdata['Email'] != '':
#                             driver.find_element_by_class_name('search-key').send_keys(
#                                 dictdata['Email'].strip() + Keys.ENTER)
#                         else:
#                             driver.find_element_by_class_name('search-key').send_keys(
#                                 dictdata['Full Name'].strip() + Keys.ENTER)
#                         WebDriverWait(driver, 30).until(
#                             lambda x: x.execute_script('return document.readyState') == 'complete')
#                         time.sleep(3)
#                         # time.sleep(7)
#                         result_count = driver.find_element_by_xpath("//b[@id='customers_count']")
#                         # result = driver.find_elements_by_class_name('react-contextmenu-wrapper')
#                         print(f"   >>>> Total '{result_count.text}' patient(s) Found.")
#                         result = int(result_count.text.strip())
#                         if result == 0 or result > 1:
#                             if result:
#                                 print(f'Ambigous result.. {dictdata["Full Name"]}::{dictdata["ID"]} ')
#                                 dup_writer.writerow([dictdata["ID"], dictdata["Full Name"], dictdata['First Name'],
#                                                      dictdata['Last Name'], dictdata['Email']])
#                             else:
#                                 print(f'No record found for {dictdata["Full Name"]}::{dictdata["ID"]} ')
#                                 norecord_writer.writerow([dictdata["ID"], dictdata["Full Name"]])
#                             # reset search bar
#
#                         else:
#                             driver.find_element_by_class_name('td-clinic-name').click()
#                             WebDriverWait(driver, 30).until(
#                                 lambda x: x.execute_script('return document.readyState') == 'complete')
#                             time.sleep(2)
#                             # time.sleep(3.5)
#                             client_id = driver.current_url.split('/')[-1]
#                             notes_mark = 0
#
#                             # Add Notes
#                             if dictdata['Notes'] != '':
#                                 # print(" >> <<<we'll add notes>>>")
#
#                                 notes_len = len(dictdata['Notes'].strip())
#                                 print(f" >>> Notes Length: {notes_len}")
#                                 if dictdata['Notes'].strip()[notes_len - 1] == '.':
#                                     print("notes should be added manually")
#                                     notes_mark += 1
#
#                                 # driver.find_element_by_xpath("//a[text()='Customer Notes']").click()
#                                 # time.sleep(2.5)
#
#                                 if notes_mark == 0:
#                                     add_notes(driver, client_id, dictdata)
#
#                                     # #     if docs are also there we need to head back to profile page
#                                     # if dictdata['Document Flag'] == '1':
#                                     #     print(client_id)
#                                     #     driver.get(f'https://aestheticrecord.com/clients/profile/{client_id}')
#                                     #     time.sleep(4)
#
#                             else:
#                                 print(" >>>> No notes to add.")
#
#                             if dictdata['Document Flag'] == '1':
#                                 # print(" >> <<<we'll add documents>>>")
#
#                                 # if dictdata['Notes'] == '':
#                                 #     driver.find_element_by_class_name('td-clinic-name').click()
#                                 #     time.sleep(3.5)
#                                 # client_id = driver.current_url.split('/')[-1]
#
#                                 add_docs(driver, client_id, dictdata, missingfiles_writer)
#
#                             else:
#                                 print(" >>>> No docs to add.")
#                             mark = '*' if notes_mark == 1 else ''
#                             processed_writer.writerow([f'{mark}{client_id}', dictdata['Full Name'],
#                                                        dictdata['First Name'], dictdata['Last Name'],
#                                                        dictdata['Email']])
#
#                         driver.get(url="https://aestheticrecord.com/clients")
#                         WebDriverWait(driver, 30).until(
#                             lambda x: x.execute_script('return document.readyState') == 'complete')
#                         time.sleep(2)
#
#     csv_file1.close()
#     csv_file2.close()
#     csv_file3.close()
#     csv_file4.close()


def add_notes(driver, note):
    notes_btn = driver.find_element_by_xpath("//a[text()='Customer Notes']")
    notes_btn.click()
    WebDriverWait(driver, 30).until(
        lambda x: x.execute_script('return document.readyState') == 'complete')
    time.sleep(2)
    print("Adding note now...")
    driver.find_element_by_xpath("//node()[@id='notes']").send_keys(note)
    # WebDriverWait(driver, 30).until(
    #     lambda x: x.execute_script('return document.readyState') == 'complete')
    time.sleep(3)

    if len(note) > 100:
        time.sleep(3)
    notesaveflag = False
    while notesaveflag is False:
        try:
            driver.find_element_by_xpath("//input[@type='submit']").click()
            WebDriverWait(driver, 30).until(
                lambda x: x.execute_script('return document.readyState') == 'complete')
            time.sleep(5)
            notesaveflag = True
        except ElementClickInterceptedException:
            time.sleep(5)

    driver.execute_script("window.history.go(-1)")
    time.sleep(3)


def enter_notes(driver):

    # Create a file for duplicate clients
    with open(r'C:\Users\Lenovo\PycharmProjects\AestheticPro\AestheticPro_data\Duplicate Clients.csv', 'w', newline='') as dup:
        writer = csv.writer(dup)
        writer.writerow(['Client ID', 'Name'])

    # Create a file for clients not created
    with open(r'C:\Users\Lenovo\PycharmProjects\AestheticPro\AestheticPro_data\Clients not created.csv', 'w',
              newline='') as not_created:
        writer = csv.writer(not_created)
        writer.writerow(['Client ID', 'Name'])

    notes_data = pd.read_csv(r'C:\Users\Lenovo\PycharmProjects\AestheticPro\AestheticPro_data\Client_Notes.csv',
                       encoding='cp1252')
    client_data = pd.read_csv(r'C:\Users\Lenovo\PycharmProjects\AestheticPro\AestheticPro_data\Client_Details.csv',
                              encoding='cp1252')
    for index, client in notes_data.iterrows():
        id = client['Client ID']
        note = client['Note']
        name = client_data['Name'][client_data['Client ID'] == id]
        name = name.values[0]
        print(f'Now processing {name}...')
        time.sleep(1)
        search_bar = driver.find_element_by_class_name('search-key')
        search_bar.clear()
        search_bar.send_keys(name + Keys.ENTER)
        WebDriverWait(driver, 30).until(
            lambda x: x.execute_script('return document.readyState') == 'complete')
        time.sleep(3)
        result_count = driver.find_element_by_xpath("//b[@id='customers_count']")
        print(f"   >>>> Total '{result_count.text}' patient(s) Found.")
        result = int(result_count.text.strip())
        if result == 0 or result > 1:
            if result:
                print(f'  >>>>Duplicate result: {name}')
                print('  >>>>Searching through email now...')
                email = client_data['Email'][client_data['Client ID'] == id]
                email = email.values[0]
                print(f'  >>>>Email: {email}')
                search_bar.clear()
                search_bar.send_keys(email + Keys.ENTER)
                WebDriverWait(driver, 30).until(
                    lambda x: x.execute_script('return document.readyState') == 'complete')
                time.sleep(3)
                result_count = driver.find_element_by_xpath("//b[@id='customers_count']")
                print(f"   >>>> Total '{result_count.text}' patient(s) Found.")
                result = int(result_count.text.strip())
                if result > 1:
                    with open(r'C:\Users\Lenovo\PycharmProjects\AestheticPro\AestheticPro_data\Duplicate Clients.csv',
                              'a', newline='') as f2:
                        wr = csv.writer(f2)
                        row = [id, name]
                        wr.writerow(row)
                else:
                    driver.find_element_by_class_name('td-clinic-name').click()
                    WebDriverWait(driver, 30).until(
                        lambda x: x.execute_script('return document.readyState') == 'complete')
                    time.sleep(2)
                    add_notes(driver, note)
                    time.sleep(2)
                    driver.execute_script("window.history.go(-1)")
                    time.sleep(3)
            else:
                print(f'  >>>>No record found for {name}')
                print('  >>>>Searching through email now...')
                email = client_data['Email'][client_data['Client ID'] == id]
                email = email.values[0]
                print(f'  >>>>Email: {email}')
                search_bar.clear()
                search_bar.send_keys(email + Keys.ENTER)
                WebDriverWait(driver, 30).until(
                    lambda x: x.execute_script('return document.readyState') == 'complete')
                time.sleep(3)
                result_count = driver.find_element_by_xpath("//b[@id='customers_count']")
                print(f"   >>>> Total '{result_count.text}' patient(s) Found.")
                result = int(result_count.text.strip())
                if result == 0:
                    print('  >>>>Still no records found.')
                    with open(r'C:\Users\Lenovo\PycharmProjects\AestheticPro\AestheticPro_data\Clients not created.csv',
                              'a', newline='') as f3:
                        wr = csv.writer(f3)
                        row = [id, name]
                        wr.writerow(row)
                elif result == 1:
                    driver.find_element_by_class_name('td-clinic-name').click()
                    WebDriverWait(driver, 30).until(
                        lambda x: x.execute_script('return document.readyState') == 'complete')
                    time.sleep(2)
                    add_notes(driver, note)
                    time.sleep(2)
                    driver.execute_script("window.history.go(-1)")
                    time.sleep(3)
        else:
            driver.find_element_by_class_name('td-clinic-name').click()
            WebDriverWait(driver, 30).until(
                lambda x: x.execute_script('return document.readyState') == 'complete')
            time.sleep(5)
            add_notes(driver, note)
            time.sleep(2)
            driver.execute_script("window.history.go(-1)")
            time.sleep(3)

    dup.close()
    not_created.close()


# def add_appointments_slot_date_notexist_failed(driver, type):
#     csv_file1 = open(f'{type}appt_success.csv', 'a', newline='', encoding="utf-8", errors="replace")
#     writer_success = csv.writer(csv_file1)
#     # writer_success.writerow(['AR_ID', 'Full Name', 'Email'])
#
#     csv_file2 = open(f'{type}date_failed.csv', 'a', newline='', encoding="utf-8", errors="replace")
#     writer_date_failed = csv.writer(csv_file2)
#     # writer_date_failed.writerow(['AR_ID', 'Full Name', 'Email', 'Service', 'Category', 'Provider', 'DateTime'])
#
#     csv_file3 = open(f'{type}slot_failed.csv', 'a', newline='', encoding="utf-8", errors="replace")
#     writer_slot_failed = csv.writer(csv_file3)
#     # writer_slot_failed.writerow(['AR_ID', 'Full Name', 'Email', 'Service', 'Category', 'Provider', 'DateTime'])
#
#     csv_file4 = open(f'{type}notexist_failed.csv', 'a', newline='', encoding="utf-8", errors="replace")
#     writer_notexist_failed = csv.writer(csv_file4)
#     # writer_notexist_failed.writerow(['Full Name', 'Email', 'Service', 'Category', 'Provider', 'DateTime'])
#
#     csv_file5 = open(f'{type}duplicate_failed.csv', 'a', newline='', encoding="utf-8", errors="replace")
#     writer_duplicate_failed = csv.writer(csv_file5)
#     # writer_duplicate_failed.writerow(['Full Name', 'Email', 'Service', 'Category', 'Provider', 'DateTime'])
#
#     if type == 's_':
#         file_name = 'slot_failed.csv'
#     elif type == 'd_':
#         file_name = 'date_failed.csv'
#     else:
#         file_name = 'notexist_failed.csv'
#
#     with open(file_name) as csvfile:
#         read_csv = csv.DictReader(csvfile)
#         for record_no, dictdata in enumerate(read_csv, 2):
#             if record_no > 1:
#                 print(f'Processing {record_no}--{dictdata["Full Name"]}')
#                 driver.get("https://app.aestheticrecord.com/clients")
#                 WebDriverWait(driver, 30).until(
#                     lambda x: x.execute_script('return document.readyState') == 'complete')
#                 time.sleep(4)
#                 # search by name
#                 internet_access()
#                 driver.find_element_by_class_name('search-key').send_keys(dictdata['Full Name'].strip() + Keys.ENTER)
#                 WebDriverWait(driver, 30).until(
#                     lambda x: x.execute_script('return document.readyState') == 'complete')
#                 time.sleep(10)
#                 result_count = driver.find_element_by_xpath("//b[@id='customers_count']")
#                 print(f"   >>>> Total '{result_count.text}' patient(s) Found.")
#                 result = int(result_count.text.strip())
#                 if result == 1:
#
#                     create_appointment(driver, dictdata, writer_success, writer_date_failed, writer_slot_failed)
#
#                 elif result == 0:
#                     writer_notexist_failed.writerow([dictdata['Full Name'], dictdata['Email'], dictdata['Service'],
#                                                      dictdata['Category'], dictdata['Provider'], dictdata['DateTime']])
#                 else:
#                     print("Duplicates exist...!")
#                     writer_duplicate_failed.writerow([dictdata['Full Name'], dictdata['Email'], dictdata['Service'],
#                                                       dictdata['Category'], dictdata['Provider'], dictdata['DateTime']])
#
#     csv_file1.close()
#     csv_file2.close()
#     csv_file3.close()
#     csv_file4.close()
#     csv_file5.close()


# def updateapt():
#     csv_file1 = open('future_appointments(no Sonya).csv', 'w', newline='', encoding="utf-8", errors="replace")
#     writer = csv.writer(csv_file1)
#     writer.writerow(['Full Name', 'Email', 'Service', 'Category', 'Provider', 'DateTime'])
#
#     with open('appointments.csv') as csvfile:
#         read_csv = csv.DictReader(csvfile)
#         for record_no, dictdata in enumerate(read_csv, 2):
#             apptdatetime = dictdata['DateTime']
#             apptdate = apptdatetime.split(' ')[0]
#             month = int(apptdate.split('/')[0])
#             day = int(apptdate.split('/')[1])
#             # year = int(apptdate.split('/')[2])
#             if month == 7 and day > 15 or month > 7:
#                 if dictdata['Provider'] != 'Sonya Moussabeck':
#                     writer.writerow([dictdata['Full Name'], dictdata['Email'], dictdata['Service'],
#                                      dictdata['Category'], dictdata['Provider'], dictdata['DateTime']])


def add_appointments(driver):

    # with open(r'C:\Users\Lenovo\PycharmProjects\AestheticPro\AestheticPro_data\Appointment_Date_Failed.csv', 'w',
    #           newline='') as failed_date:
    #     writer = csv.writer(failed_date)
    #     writer.writerow(['Client ID', 'Name', 'Date', 'Time', 'Staff', 'Service'])
    #
    # with open(r'C:\Users\Lenovo\PycharmProjects\AestheticPro\AestheticPro_data\Appointment_Service_Unavailable.csv', 'w',
    #           newline='') as no_service:
    #     writer = csv.writer(no_service)
    #     writer.writerow(['Client ID', 'Name', 'Date', 'Time', 'Staff', 'Service'])
    #
    # with open(r'C:\Users\Lenovo\PycharmProjects\AestheticPro\AestheticPro_data\Appointment_Success.csv', 'w',
    #           newline='') as success:
    #     writer = csv.writer(success)
    #     writer.writerow(['Client ID', 'Name', 'Date', 'Time', 'Staff', 'Service'])

    appointments_data = pd.read_csv(r'C:\Users\Lenovo\PycharmProjects\AestheticPro\AestheticPro_data\Client_Appointments.csv',
                             encoding='cp1252')
    client_data = pd.read_csv(r'C:\Users\Lenovo\PycharmProjects\AestheticPro\AestheticPro_data\Client_Details.csv',
                              encoding='cp1252')
    appointments_data = appointments_data[53:]

    for index, client in appointments_data.iterrows():
        client_id = client['Client ID']
        name = client_data['Name'][client_data['Client ID'] == int(client_id)]
        name = name.values[0]
        email = client_data['Email'][client_data['Client ID'] == int(client_id)]
        email = email.values[0]
        phone = client_data['Mobile Phone'][client_data['Client ID'] == int(client_id)]
        phone = phone.values[0]
        print(f'Now processing {name}...')
        time.sleep(1)
        search_bar = driver.find_element_by_class_name('search-key')
        search_bar.clear()
        search_bar.send_keys(name + Keys.ENTER)
        WebDriverWait(driver, 30).until(
            lambda x: x.execute_script('return document.readyState') == 'complete')
        time.sleep(3)
        result_count = driver.find_element_by_xpath("//b[@id='customers_count']")
        print(f"   >>>> Total '{result_count.text}' patient(s) Found.")
        result = int(result_count.text.strip())

        if result == 0 or result > 1:
            if result:
                print(f'   >>>>Duplicate result: {name}')
                print('   >>>>Searching through email now...')
                print(f'   >>>>Email: {email}')
                try:
                    if '@' in email:
                        search_bar.clear()
                        search_bar.send_keys(email + Keys.ENTER)
                        WebDriverWait(driver, 30).until(
                            lambda x: x.execute_script('return document.readyState') == 'complete')
                        time.sleep(3)
                        result_count = driver.find_element_by_xpath("//b[@id='customers_count']")
                        print(f"   >>>> Total '{result_count.text}' patient(s) Found.")
                        result = int(result_count.text.strip())
                        if result == 0 or result > 1:
                            print(f'   >>>>Adding {name} in duplicates list')
                            with open(
                                    r'C:\Users\Lenovo\PycharmProjects\AestheticPro\AestheticPro_data\Duplicate Clients.csv',
                                    'a', newline='') as f2:
                                wr = csv.writer(f2)
                                row = [client_id, name]
                                wr.writerow(row)
                        elif result == 1:
                            print(f'   >>>>Got 1 patient now')
                            driver.find_element_by_class_name('td-clinic-name').click()
                            WebDriverWait(driver, 30).until(
                                lambda x: x.execute_script('return document.readyState') == 'complete')
                            time.sleep(2)
                            url_client_id = driver.current_url.split('/')[-1]
                            time.sleep(1)
                            create_appointment(driver, client_id, url_client_id, name, email, phone)
                            time.sleep(3)
                            driver.find_element_by_xpath("//label[text()='Clients']").click()
                            time.sleep(3)
                except TypeError:
                    print('   >>>>Email not found')
                    print(f'   >>>>Adding {name} in duplicates list')
                    with open(r'C:\Users\Lenovo\PycharmProjects\AestheticPro\AestheticPro_data\Duplicate Clients.csv',
                              'a', newline='') as f2:
                        wr = csv.writer(f2)
                        row = [client_id, name]
                        wr.writerow(row)
            else:
                print(f'   >>>>No record found for {name}')
                print('   >>>>Searching through email now...')
                print(f'   >>>>Email: {email}')
                try:
                    if '@' in email:
                        search_bar.clear()
                        search_bar.send_keys(email + Keys.ENTER)
                        WebDriverWait(driver, 30).until(
                            lambda x: x.execute_script('return document.readyState') == 'complete')
                        time.sleep(3)
                        result_count = driver.find_element_by_xpath("//b[@id='customers_count']")
                        print(f"   >>>> Total '{result_count.text}' patient(s) Found.")
                        result = int(result_count.text.strip())
                        if result == 0:
                            print('   >>>>Still no records found.')
                            print(f'   >>>>Adding {name} in Clients not found list')
                            with open(
                                    r'C:\Users\Lenovo\PycharmProjects\AestheticPro\AestheticPro_data\Clients not created.csv',
                                    'a', newline='') as f2:
                                wr = csv.writer(f2)
                                row = [client_id, name]
                                wr.writerow(row)
                        elif result == 1:
                            print(f'   >>>>Got 1 patient now')
                            driver.find_element_by_class_name('td-clinic-name').click()
                            WebDriverWait(driver, 30).until(
                                lambda x: x.execute_script('return document.readyState') == 'complete')
                            time.sleep(2)
                            url_client_id = driver.current_url.split('/')[-1]
                            time.sleep(1)
                            create_appointment(driver, client_id, url_client_id, name, email, phone)
                            time.sleep(2)
                            driver.find_element_by_xpath("//label[text()='Clients']").click()
                            time.sleep(2)
                        else:
                            print(f'   >>>>Duplicate result')
                            print(f'   >>>>Adding {name} in duplicates list')
                            with open(
                                    r'C:\Users\Lenovo\PycharmProjects\AestheticPro\AestheticPro_data\Duplicate Clients.csv',
                                    'a', newline='') as f2:
                                wr = csv.writer(f2)
                                row = [client_id, name]
                                wr.writerow(row)
                except TypeError:
                    print('   >>>>Email not found')
                    print(f'   >>>>Adding {name} in Clients not found list')
                    with open(r'C:\Users\Lenovo\PycharmProjects\AestheticPro\AestheticPro_data\Clients not created.csv',
                              'a', newline='') as f2:
                        wr = csv.writer(f2)
                        row = [client_id, name]
                        wr.writerow(row)
        else:
            driver.find_element_by_class_name('td-clinic-name').click()
            WebDriverWait(driver, 30).until(
                lambda x: x.execute_script('return document.readyState') == 'complete')
            time.sleep(2)
            url_client_id = driver.current_url.split('/')[-1]
            time.sleep(1)
            create_appointment(driver, client_id, url_client_id, name, email, phone)
            time.sleep(2)
            driver.find_element_by_xpath("//label[text()='Clients']").click()
            time.sleep(2)


def create_appointment(driver, client_id, url_client_id, name, email, phone):

    appointments_data = pd.read_csv(
        r'C:\Users\Lenovo\PycharmProjects\AestheticPro\AestheticPro_data\Client_Appointments.csv',
        encoding='cp1252')
    time.sleep(3)

    driver.get(f"https://app.aestheticrecord.com/appointment/create/client/{url_client_id}")
    WebDriverWait(driver, 30).until(
        lambda x: x.execute_script('return document.readyState') == 'complete')
    time.sleep(3)

    provider = appointments_data['Staff'][appointments_data['Client ID'] == client_id]
    provider = provider.values[0]
    select_provider(driver, provider)
    time.sleep(1)

    select_clinic(driver, 'Elan Medspa')
    time.sleep(1)

    service_string = appointments_data['Service'][appointments_data['Client ID'] == client_id]
    service_string = service_string.values[0]
    service_set_flag = select_service(driver, service_string)
    time.sleep(1)

    appt_date = appointments_data['Appt Date'][appointments_data['Client ID'] == client_id]
    appt_date = appt_date.values[0]
    appt_time = appointments_data['Time'][appointments_data['Client ID'] == client_id]
    appt_time = appt_time.values[0]

    if service_set_flag:
        written_duration = int(driver.find_element_by_xpath("//input[@name='duration-service-0']").
                               get_attribute('value'))
        date_time = f'{appt_date} {appt_time}'
        actual_duration = get_duration(date_time)

        if written_duration != actual_duration:
            set_duration(driver, actual_duration)

        write_result = set_date_time(driver, date_time)

        if write_result == 1:
            auto_set_email = driver.find_element_by_xpath("//input[@name='clientEmail']").get_attribute('value')
            if auto_set_email == '':
                try:
                    if email != '':
                        driver.find_element_by_xpath("//input[@name='clientEmail']").send_keys(email)
                except TypeError:
                    driver.find_element_by_xpath("//input[@name='clientEmail']").send_keys('sampleEmail@mail.com')
            time.sleep(2)
            auto_set_phone = driver.find_element_by_xpath("//input[@name='phone']").get_attribute("value")
            if auto_set_phone == '':
                driver.find_element_by_xpath("//input[@name='phone']").send_keys('111111111')
            driver.find_element_by_xpath("//div[@class='setting-title m-b-25 eventTitle']/a[@class='new-blue-btn pull-right']").click()
            WebDriverWait(driver, 30).until(
                lambda x: x.execute_script('return document.readyState') == 'complete')
            time.sleep(15)
            with open(r'C:\Users\Lenovo\PycharmProjects\AestheticPro\AestheticPro_data\Appointment_Success.csv', 'a',
                      newline='') as success:
                writer = csv.writer(success)
                writer.writerow([client_id, name, appt_date, appt_time, provider, service_string])
            print("   >>>>Appointment added successfully for ", name)
        else:
            print(f'   >>>>Date not available')
            print(f'   >>>>Adding in Appointment date failed list')
            with open(r'C:\Users\Lenovo\PycharmProjects\AestheticPro\AestheticPro_data\Appointment_Date_Failed.csv', 'a',
                      newline='') as failed_date:
                writer = csv.writer(failed_date)
                writer.writerow([client_id, name, appt_date, appt_time, provider, service_string])
    else:
        print(f'   >>>>Service not available')
        print(f'   >>>>Adding in Service unavailable list')
        with open(r'C:\Users\Lenovo\PycharmProjects\AestheticPro\AestheticPro_data\Appointment_Service_Unavailable.csv', 'a',
                  newline='') as no_service:
            writer = csv.writer(no_service)
            writer.writerow([client_id, name, appt_date, appt_time, provider, service_string])


def select_provider(driver, provider):
    driver.find_element_by_xpath("//select[@name='provider']").click()
    time.sleep(2.5)
    driver.find_element_by_xpath("//option[contains(text(),'" + provider + "')]").click()
    time.sleep(2)


def select_clinic(driver, client_name):
    driver.find_element_by_xpath("//select[@name='selectedClinic']").click()
    time.sleep(1.5)
    driver.find_element_by_xpath(
        "//option[contains(text(),'" + client_name + "')]").click()
    time.sleep(3.5)


def select_service(driver, service):  # service-0
    driver.find_element_by_xpath("//select[@name='service-0']").click()
    time.sleep(1.5)
    service_list = service.split(",")
    service_set_flag = False

    if len(service_list) > 1:
        for service in service_list:
            try:
                driver.find_element_by_xpath(
                    "//option[text()='" + service + "']").click()
                time.sleep(2)
                service_set_flag = True
                break
            except NoSuchElementException:
                pass

        if service_set_flag:
            notes_str = 'Services for this appointment include: '
            for service in service_list:
                notes_str += service + ', '
            appt_notes = driver.find_element_by_xpath("//textarea[@class='simpleTextarea auto-height']")
            appt_notes.clear()
            appt_notes.send_keys(notes_str)

    else:
        try:
            driver.find_element_by_xpath(
                "//option[text()='" + service + "']").click()
            time.sleep(2)
            service_set_flag = True
        except NoSuchElementException:
            pass

    time.sleep(3)
    return service_set_flag


def get_duration(appt_datetime):
    print(appt_datetime)
    appt_date = appt_datetime.split(' ')[0]
    month = appt_date.split('-')[0]
    day = appt_date.split('-')[1]
    year = appt_date.split('-')[2]
    apptcompletetime = appt_datetime.split(' ', 1)[-1].strip()
    # print(apptcompletetime)
    # print(apptcompletetime.split(' '))
    start = apptcompletetime.split(' ')[0]
    end = apptcompletetime.split(' ')[3]
    print('start:', start)
    strt_hr = int(start.split(':')[0].strip())
    strt_min = int(start.split(':')[-1].strip())
    end_hr = int(end.split(':')[0].strip())
    end_min = int(end.split(':')[-1].strip())

    if end_hr < strt_hr:
        end_hr = strt_hr + end_hr

    d1 = datetime(int(year), int(month), int(day), strt_hr, strt_min, 0)
    d2 = datetime(int(year), int(month), int(day), end_hr, end_min, 0)
    diff = d2 - d1
    # print("Difference:", diff)
    min_diff = divmod(diff.seconds, 60)
    # print("IN Minutes: ", min_diff[0], 'minutes', min_diff[1], 'seconds')
    apptduration = min_diff[0]
    print('Appointment durantion', apptduration)
    return apptduration


def set_duration(driver, duration):
    driver.find_element_by_xpath("//a[@class='xs-blue-btn pull-right']").click()
    time.sleep(1)
    driver.find_element_by_xpath("//input[@name='editDuration']").send_keys(
        Keys.BACKSPACE + Keys.BACKSPACE + str(duration))
    time.sleep(2)
    driver.find_element_by_xpath("//a[@class='new-blue-btn pull-left no-margin']").click()
    time.sleep(3)


def make_month_year(month, year):
    switcher = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December"
    }

    return f'{switcher.get(month)} {year}'


def set_date_time(driver, appt_datetime):
    driver.find_element_by_xpath("//input[@name='searchPickerDate']").click()
    time.sleep(1)
    next_month_btn = "//button[@aria-label='Next Month']"

    apptdate = appt_datetime.split(' ')[0]
    month = apptdate.split('-')[0]
    day = apptdate.split('-')[1]
    year = apptdate.split('-')[2]
    year = '20' + year
    month_year = make_month_year(int(month), year)
    print(month_year)

    current_month = driver.find_element_by_xpath("//div[@class='react-datepicker__current-month']").text.strip()
    while month_year != current_month:
        driver.find_element_by_xpath(next_month_btn).click()
        time.sleep(.5)
        current_month = driver.find_element_by_xpath("//div[@class='react-datepicker__current-month']").text.strip()

    print("Month Year set up!")

    time.sleep(2)
    try:
        driver.find_element_by_xpath("//div[@aria-disabled='false' and contains(text(), '" + day + "')]").click()
        time.sleep(3)
        print("Date set up...!")
        time.sleep(2)
    except NoSuchElementException:
        print('Date not Clickable.....!')
        return 0

    apptcompletetime = appt_datetime.split(' ', 1)[-1].strip()
    # print(apptcompletetime)
    # print(apptcompletetime.split(' '))
    start = apptcompletetime.split(' ')[0]

    # apptcompletetime = appt_datetime.split(' ', 1)[-1].strip()
    # apptcompletetime = appt_datetime.split(' ', 1)[1]
    # start = apptcompletetime.split(' ')[0]
    meridiem = apptcompletetime.split(' ')[1].strip()
    timeslot = f"{'0' + start if len(start) == 4 else start} {'AM' if meridiem == 'am' else 'PM'}"
    print('Time Slot is :', timeslot)
    try:
        driver.find_element_by_xpath("//button[contains(text(),'" + timeslot + "')]").click()
        time.sleep(3)
        print('Time Slot set up.')
    except NoSuchElementException:
        print("Time Slot not available.....!")
        return -1

    return 1


def make_files():
    # Create a file for duplicate clients
    with open(r'C:\Users\Lenovo\PycharmProjects\AestheticPro\AestheticPro_data\Duplicate Clients.csv', 'w',
              newline='') as dup:
        writer = csv.writer(dup)
        writer.writerow(['Client ID', 'Name'])

    # Create a file for clients not created
    with open(r'C:\Users\Lenovo\PycharmProjects\AestheticPro\AestheticPro_data\Clients not created.csv', 'w',
              newline='') as not_created:
        writer = csv.writer(not_created)
        writer.writerow(['Client ID', 'Name'])

    # Create a file for clients with docs uploaded
    with open(r'C:\Users\Lenovo\PycharmProjects\AestheticPro\AestheticPro_data\Docs uploaded.csv', 'w',
              newline='') as uploaded:
        writer = csv.writer(uploaded)
        writer.writerow(['Client ID', 'Name'])

    # Create a file for files not found
    with open(r'C:\Users\Lenovo\PycharmProjects\AestheticPro\AestheticPro_data\Files not found.csv', 'w',
              newline='') as not_found:
        writer = csv.writer(not_found)
        writer.writerow(['Client ID', 'Name'])


def main():
    driver = webdriver.Chrome(r'C:\Users\Lenovo\Downloads\chromedriver_win32\chromedriver')
    driver.get(website_url)
    WebDriverWait(driver, 70).until(
        lambda x: x.execute_script('return document.readyState') == 'complete')
    time.sleep(1)
    username = driver.find_element_by_xpath("//input[@name='email']")
    username.clear()
    username.send_keys(website_credentials.get('Username'))
    password = driver.find_element_by_xpath("//input[@name='password']")
    password.clear()
    password.send_keys(website_credentials.get('Password'))
    time.sleep(3)
    login = driver.find_element_by_xpath("//div/a[text()='Login']")
    login.click()
    time.sleep(3)
    try:
        login_again = driver.find_element_by_xpath("//button[text()='Login']")
        login_again.click()
        time.sleep(3)
    except NoSuchElementException:
        pass

    WebDriverWait(driver, 300).until(
        lambda x: x.execute_script('return document.readyState') == 'complete')
    time.sleep(3)
    driver.find_element_by_xpath("//label[text()='Clients']").click()
    time.sleep(3)

    # ***make_files()***

    # enter_notes(driver)
    # enter_docs(driver)
    # enter_dup_docs(driver)
    # add_appointments(driver)
    create_client(driver, 2)



    # add_appointments_slot_date_notexist_failed(driver, 's_')
    # print('>>>>>>>>>>>>>>ALL SLOT FAILED PROCESSED.')
    # add_appointments_slot_date_notexist_failed(driver, 'd_')
    # print('>>>>>>>>>>>>>>ALL DATE FAILED PROCESSED.')
    # add_appointments_slot_date_notexist_failed(driver, 'ne_')

    # mb_notes_docs_to_ar(driver)
    # add_appointments(driver)

    print('It\'s all done.')

    # create_client(driver)


if __name__ == "__main__":
    main()

# 1 c(charlie), Q(queen), L(lema), z(zebra), j(japan)