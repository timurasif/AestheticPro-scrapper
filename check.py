import pandas as pd


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

# service = appointments_data['Service'][appointments_data['Client ID'] == 314]
# service = service.values[0]
# service_list = service.split(",")
# print(service_list)
# print(len(service_list))

# appt_date = appointments_data['Appt Date'][appointments_data['Client ID'] == 314]
# appt_date = appt_date.values[0]
# appt_time = appointments_data['Time'][appointments_data['Client ID'] == 314]
# appt_time = appt_time.values[0]
# date_time = f'{appt_date} {appt_time}'
# appt_year = appt_date.split('-')[2]
# appt_year = '20' + appt_year
# print(appt_year)

client_data = pd.read_csv(r'C:\Users\Lenovo\PycharmProjects\AestheticPro\AestheticPro_data\Client_Details.csv',
                              encoding='cp1252')

# phone = client_data['Home Phone'][client_data['Client ID'] == 223]
# phone = phone.values[0]
# if any(char.isdigit() for char in str(phone)):
#     print(phone)
# else:
#     phone = client_data['Mobile Phone'][client_data['Client ID'] == 223]
#     phone = phone.values[0]
#     if any(char.isdigit() for char in str(phone)):
#         print(phone)
#     else:
#         phone = client_data['Work Phone'][client_data['Client ID'] == 223]
#         phone = phone.values[0]
#         if any(char.isdigit() for char in str(phone)):
#             print(phone)
#         else:
#             print('Number not available')

dob = client_data['Birthdate'][client_data['Client ID'] == 397]
dob = dob.values[0]
print(dob)
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
    print(day)
    print(month)
    print(year)
else:
    print('No DOB found')