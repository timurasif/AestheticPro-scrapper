import os
import csv
import time
import shutil
import urllib.request
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, WebDriverException


def parse_client(url):
    url.send_keys(Keys.CONTROL + Keys.RETURN)
    time.sleep(2)
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[2])
    time.sleep(1)

    client_id = driver.find_element_by_xpath("//td[@class='lpad add-bottom-border' and contains(text(), 'Client ID')]//following-sibling::td")
    client_id = client_id.text
    print('Parsing Client ID: ' + client_id + ' now...')

    name = driver.find_element_by_xpath(
        "//td[@class='lpad add-bottom-border' and contains(text(), 'Name')]//following-sibling::td")
    name = name.text

    home_phone = driver.find_element_by_xpath(
        "//td[@class='lpad add-bottom-border' and contains(text(), 'Home Phone')]//following-sibling::td")
    home_phone = home_phone.text

    work_phone = driver.find_element_by_xpath(
        "//td[@class='lpad add-bottom-border' and contains(text(), 'Work Phone')]//following-sibling::td")
    work_phone = work_phone.text

    mobile_phone = driver.find_element_by_xpath(
        "//td[@class='lpad add-bottom-border' and contains(text(), 'Mobile Phone')]//following-sibling::td")
    mobile_phone = mobile_phone.text

    try:
        email = driver.find_element_by_xpath("//span[@id='Detail_Email']/a")
        email = email.text
    except NoSuchElementException:
        email = ''

    address1 = driver.find_element_by_xpath("//span[@id='Detail_Address']")
    address1 = address1.text
    address2 = driver.find_element_by_xpath("//span[@id='Detail_PostalInfo']")
    address2 = address2.text
    address = address1 + ' ' + address2
    if address == ' ,':
        address = ''

    gender = driver.find_element_by_xpath("//span[@id='Detail_Gender']")
    gender = gender.text

    active = driver.find_element_by_xpath("//span[@id='Detail_Active']")
    active = active.text

    birthdate = driver.find_element_by_xpath("//span[@id='Detail_BDay']")
    birthdate = birthdate.text

    marital_status = driver.find_element_by_xpath("//span[@id='Detail_MaritalStatus']")
    marital_status = marital_status.text

    marketing_campaign_id = driver.find_element_by_xpath("//td[@class='lpad add-bottom-border' and contains(text(), 'Marketing')]//following-sibling::td//descendant::div[@id='campaigndivsingle']//descendant::tr/td")
    marketing_campaign_id = marketing_campaign_id.text

    referred_by = driver.find_element_by_xpath("//span[@id='ClientReferralSpan']")
    referred_by = referred_by.text

    do_not_disturb = driver.find_element_by_xpath("//span[@id='Detail_DND']")
    do_not_disturb = do_not_disturb.text

    entered_by = driver.find_element_by_xpath("//td[@class='lpad add-bottom-border' and contains(text(), 'Entered')]//following-sibling::td")
    entered_by = entered_by.text

    client_location = driver.find_element_by_xpath("//span[@id='Detail_Location']")
    client_location = client_location.text

    staff = driver.find_element_by_xpath("//span[@id='Detail_Staff']")
    staff = staff.text

    cid = driver.find_element_by_xpath("//span[@id='Detail_CID']")
    cid = cid.text

    misc = driver.find_element_by_xpath("//span[@id='Detail_MISC']")
    misc = misc.text

    client_type = driver.find_element_by_xpath("//td[@class='lpad add-bottom-border' and contains(text(), 'Client Type')]//following-sibling::td")
    client_type = client_type.text

    # Collecting Display Pictures
    client_photo_btn = driver.find_element_by_xpath("//h3[contains(text(), 'Client Photo')]")
    client_photo_btn.click()
    time.sleep(0.5)
    try:
        display_pic = driver.find_element_by_xpath(
            "//span[@id='showimagehide']//descendant::img[contains(@src,'photoicon')]")
        dp_flag = 0
    except NoSuchElementException:
        display_pic = driver.find_element_by_xpath("//span[@id='showimagehide']//descendant::img")
        dp_flag = 1
        src = display_pic.get_attribute('src')
        image_name = client_id + '_Display_Picture.jpg'
        urllib.request.urlretrieve(src, image_name)
        destination = r'C:\Users\Lenovo\PycharmProjects\AestheticPro\AestheticPro_data\Client_Attachments\Display_Pictures'
        source = r'C:\Users\Lenovo\PycharmProjects\AestheticPro' + '\\' + image_name
        shutil.move(source, destination)

    # Write data into CSV
    data = [client_id, name, home_phone, work_phone, mobile_phone, email, address, gender, active, birthdate, marital_status, marketing_campaign_id, referred_by, do_not_disturb, entered_by, client_location, staff, cid, misc, client_type, dp_flag]

    with open(r'C:\Users\Lenovo\PycharmProjects\AestheticPro\AestheticPro_data\Client_Details.csv', 'a', newline='') as f2:
        writer2 = csv.writer(f2)
        writer2.writerow(data)

    time.sleep(2)

    # Collecting Client Notes
    notes_flag = 0
    try:
        client_notes_btn = driver.find_element_by_xpath("//h3[contains(text(), 'Client Notes')]")
        client_notes_btn.click()
        time.sleep(0.5)
        notes = driver.find_elements_by_xpath("//div[@id='ClientNotediv']/descendant::tr[contains(@class, 'bg')]/td[1]")
        time.sleep(0.5)
        notes_list = []
        for note in notes:
            notes_list.append(note.text)
        if len(notes_list) > 0:
            notes_flag = 1
        with open(r'C:\Users\Lenovo\PycharmProjects\AestheticPro\AestheticPro_data\Client_Notes.csv', 'a', newline='') as f2:
            for note in notes_list:
                data = [client_id, note]
                writer2 = csv.writer(f2)
                writer2.writerow(data)
    except NoSuchElementException:
        pass

    # Collecting Client Appointments
    appointments_text = driver.find_element_by_xpath("//*[@id='OtherHalf']/table/tbody/tr/td/table/tbody/tr[3]//tbody//td")
    time.sleep(1)
    appointments_text = appointments_text.text
    if 'client has no appointment history' in appointments_text:
        appointments_flag = 0
    else:
        appointments_flag = 1

    if appointments_flag:
        appointments = driver.find_elements_by_xpath("//*[@id='OtherHalf']/table/tbody/tr/td/table/tbody/tr")
        time.sleep(1)
        appointments = appointments[2:]
        for appointment in appointments:
            appt_id = appointment.find_element_by_xpath(".//b")
            appt_id = appt_id.text
            appt_id.replace('[', '')
            appt_id.replace(']', '')
            appt_date = appointment.find_element_by_xpath("./td[3]")
            appt_date = appt_date.text
            appt_date = appt_date[:6] + appt_date[8:]
            appt_date = datetime.strptime(appt_date, '%m/%d/%y')
            appt_date = appt_date.date()
            now = datetime.now().date()
            if now < appt_date:
                time.sleep(1)
                appt_time = appointment.find_element_by_xpath("./td[4]")
                appt_time = appt_time.text
                staff = appointment.find_element_by_xpath("./td[5]")
                staff = staff.text
                room = appointment.find_element_by_xpath("./td[6]")
                room = room.text
                equip = appointment.find_element_by_xpath("./td[7]")
                equip = equip.text
                status = appointment.find_element_by_xpath("./td[8]")
                status = status.text
                invoice = appointment.find_element_by_xpath("./td[9]")
                invoice = invoice.text

                # Write data into CSV
                data = [client_id, appt_id, appt_date, appt_time, staff, room, equip, status, invoice]

                with open(r'C:\Users\Lenovo\PycharmProjects\AestheticPro\AestheticPro_data\Client_Appointments.csv', 'a',
                          newline='') as f2:
                    writer2 = csv.writer(f2)
                    writer2.writerow(data)

    if notes_flag == 1:
        time.sleep(1)
        close_popup = driver.find_element_by_xpath("//button[@title='Close']")
        close_popup.click()
        time.sleep(1)

    # Collecting Client Documents
    client_records = driver.find_element_by_xpath("//a[contains(text(),'Client Records')]")
    client_records.click()
    time.sleep(2)

    # Collecting Photos
    photo_gallery = driver.find_element_by_xpath("//span[text()='Photo Gallery']")
    photo_gallery.click()
    time.sleep(0.5)
    try:
        no_photos = driver.find_element_by_xpath("//td[contains(text(),'No photos')]")
    except NoSuchElementException:
        photos = driver.find_elements_by_xpath("//span[@id='showphotos']//img")
        num = 1
        for photo in photos:
            image_name = client_id + '_' + str(num) + '.jpg'
            num = num + 1
            src = photo.get_attribute('src')
            path = r'C:\Users\Lenovo\PycharmProjects\AestheticPro\AestheticPro_data\Client_Attachments\Other _Attachments' + '\\' + client_id + '\\' + image_name
            urllib.request.urlretrieve(src, path)

    try:
        level1 = driver.find_elements_by_xpath("//div[@class='sidebarItem level1']")
        for item in level1:
            doc_date = item.find_element_by_xpath(".//div[@class='eritem']")
            doc_date = doc_date.text
            doc_date = doc_date[:10]
            doc_date = doc_date.replace('/', '-')
            clickable = item.find_element_by_xpath(".//span[@class='icon-tree']")
            clickable.click()
            time.sleep(0.5)
            level2 = item.find_elements_by_xpath("./div[@class='sidebarItem level2 show']")
            for item2 in level2:
                item2.click()
                time.sleep(0.5)
                level3 = item2.find_elements_by_xpath("./div[@class='sidebarItem level3 file show']//span[@class='icon-file-blank']/following-sibling::a")
                for item3 in level3:
                    item3.click()
                    time.sleep(3)
                    dir = client_id
                    parent_dir = r'C:\Users\Lenovo\PycharmProjects\AestheticPro\AestheticPro_data\Client_Attachments\Other _Attachments'
                    path = os.path.join(parent_dir, dir)
                    if os.path.isdir(path):
                        pass
                    else:
                        os.mkdir(path)
                    time.sleep(0.5)
                    try:
                        download_btn = driver.find_element_by_xpath("//td[contains(text(),'Email/Download')]")
                        download_btn.click()
                        time.sleep(5)
                        driver.switch_to.frame("myiframe")
                        time.sleep(1)
                        download_btn2 = WebDriverWait(driver, 50).until(
                            EC.presence_of_element_located((By.XPATH, "//span[@id='showb']/div[@class='lgbuttons']")))
                        download_btn2.click()
                        time.sleep(0.5)
                        dl_wait = True
                        while dl_wait:
                            time.sleep(0.5)
                            dl_wait = False
                            for fname in os.listdir(r'C:\Users\Lenovo\Downloads'):
                                if fname.endswith('.crdownload'):
                                    dl_wait = True
                        filename = max([r'C:\Users\Lenovo\Downloads' + "\\" + f for f in os.listdir(r'C:\Users\Lenovo\Downloads')], key=os.path.getctime)
                        index = filename.find('Downloads')
                        index2 = index + 10
                        time.sleep(2)
                        filename = filename[index2:]
                        new_filename = client_id + '_' + doc_date + '_' + filename
                        time.sleep(3)
                        if os.path.isfile(
                                r'C:\Users\Lenovo\Downloads' + '\\' + new_filename):
                            pass
                        else:
                            os.rename(r'C:\Users\Lenovo\Downloads' + "\\" + filename, r'C:\Users\Lenovo\Downloads' + '\\' + new_filename)
                            destination = r'C:\Users\Lenovo\PycharmProjects\AestheticPro\AestheticPro_data\Client_Attachments\Other _Attachments' + '\\' + client_id
                            source = r'C:\Users\Lenovo\Downloads' + '\\' + new_filename
                        if os.path.isfile(r'C:\Users\Lenovo\PycharmProjects\AestheticPro\AestheticPro_data\Client_Attachments\Other _Attachments' + '\\' + client_id + '\\' + new_filename):
                            pass
                        else:
                            shutil.move(source, destination)
                        time.sleep(1)
                        driver.switch_to.default_content()
                        time.sleep(3)
                        close_window = driver.find_element_by_xpath("/html/body/div[4]/div[1]/button/span[1]")
                        close_window.click()
                        time.sleep(1)
                    except NoSuchElementException:
                        try:
                            images = driver.find_elements_by_xpath("//a[contains(text(),'image')]")
                            for image in images:
                                image.click()
                                time.sleep(0.5)
                                dl_wait = True
                                while dl_wait:
                                    time.sleep(0.5)
                                    dl_wait = False
                                    for fname in os.listdir(r'C:\Users\Lenovo\Downloads'):
                                        if fname.endswith('.crdownload'):
                                            dl_wait = True
                                filename = max([r'C:\Users\Lenovo\Downloads' + "\\" + f for f in
                                                os.listdir(r'C:\Users\Lenovo\Downloads')], key=os.path.getctime)
                                index = filename.find('Downloads')
                                index2 = index + 10
                                time.sleep(2)
                                filename = filename[index2:]
                                new_filename = client_id + '_' + doc_date + '_' + filename
                                time.sleep(3)
                                os.rename(r'C:\Users\Lenovo\Downloads' + "\\" + filename,
                                          r'C:\Users\Lenovo\Downloads' + "\\" + new_filename)
                                destination = r'C:\Users\Lenovo\PycharmProjects\AestheticPro\AestheticPro_data\Client_Attachments\Other _Attachments' + '\\' + client_id
                                source = r'C:\Users\Lenovo\Downloads' + '\\' + new_filename
                                shutil.move(source, destination)
                        except NoSuchElementException:
                            pass
                    time.sleep(1)
                    close_tab = WebDriverWait(driver, 50).until(
                            EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Remove Tab')]")))
                    close_tab.click()
                    time.sleep(5)

    except NoSuchElementException:
        pass

    print('Client ID: ' + client_id + ' parsed.')

    # Close the tab and switch to the previous tab
    driver.close()
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[1])


try:
    options = Options()
    # options.headless = True
    # options.add_argument('--no-sandbox')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36")
    # options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(r'C:\Users\Lenovo\Downloads\chromedriver_win32\chromedriver', options=options)
except WebDriverException:
    print('Webdriver not found!')

url = 'https://www.myaestheticspro.com/dsp_login.cfm'
driver.get(url)
time.sleep(3)
print(driver.current_url)
print(driver.title)

# Enter credentials and hit submit
username = driver.find_element_by_xpath('//input[@name="username"]')
username.clear()
username.send_keys('Krobertus1')

password = driver.find_element_by_xpath('//input[@type="password"]')
password.clear()
password.send_keys('Graduated1!')
print('Credentials added')

loginType = driver.find_element_by_xpath('//select[@name="LoginType"]')
loginType.click()
time.sleep(1)

loginTypeSelect = driver.find_element_by_xpath('//option[@value="1"]')
loginTypeSelect.click()
time.sleep(1)

login = driver.find_element_by_xpath('//button[@id="login"]')
login.click()

launchApp = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//a[text()="Launch"]')))
launchApp.click()

driver.switch_to.window(driver.window_handles[1])
time.sleep(2)

clients = driver.find_element_by_xpath('//a[@navtarget="clients"]')
clients.click()
time.sleep(1)

allClients = driver.find_element_by_xpath('//a[contains(text(),"Client List")]')
allClients.click()
time.sleep(1)

# Create Client_Details CSV file
with open(r'C:\Users\Lenovo\PycharmProjects\AestheticPro\AestheticPro_data\Client_Details.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Client ID', 'Name', 'Home Phone', 'Work Phone', 'Mobile Phone', 'Email', 'Address', 'Gender', 'Active', 'Birthdate', 'Marital Status', 'Marketing Campaign ID', 'Referred by', 'Do not Disturb', 'Entered by', 'Client Location', 'Staff', 'CID', 'Misc', 'Client Type', 'DP flag'])

# Create Client_Notes CSV file
with open(r'C:\Users\Lenovo\PycharmProjects\AestheticPro\AestheticPro_data\Client_Notes.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Client ID', 'Note'])

# Create Client_Appointments CSV file
with open(r'C:\Users\Lenovo\PycharmProjects\AestheticPro\AestheticPro_data\Client_Appointments.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Client ID', 'Appt_ID', 'Appt Date', 'Time', 'Staff', 'Room', 'Equip', 'Status', 'Invoice'])

# Get links to all the alphabets
alphabets = driver.find_elements_by_xpath("//div[@class='alpha-container col-sm-10 col-xs-12 remove-pad']/a")

for alphabet in alphabets:
    alphabet.click()
    time.sleep(3)

    # Get links to all the clients in a particular alphabet
    clientList = driver.find_elements_by_xpath("//table[@class='report-table borderthin']//descendant::td[@class='listing']//descendant::td/a[contains(text(), '(')]")

    for link in clientList:
        parse_client(link)
        time.sleep(3)


driver.close()
driver.switch_to.window(driver.window_handles[0])
driver.close()