from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from collections import OrderedDict
import re
from datetime import datetime
from selenium.webdriver.chrome.service import Service as ChromeService

chrome_driver_path = "/Users/kashifumer/Development/chromedriver"
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument("--headless")
service = ChromeService(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)


car_list = []
for i in range(1, 2):  # Change the range to include the desired number of pages
    driver.get("https://www.trademe.co.nz/a/motors/cars?page=" + str(i))
    details = driver.find_elements(By.CLASS_NAME, 'tm-motors-search-card__details')
    listing_cards = driver.find_elements(By.CLASS_NAME, 'tm-motors-search-card__link')
    listing_price = driver.find_elements(By.CLASS_NAME, 'tm-motors-search-card__footer')

    for detail, each_price, card in zip(details, listing_price, listing_cards):
        try:
            title = detail.find_element(By.XPATH, ".//div[contains(@class, 'tm-motors-search-card__title')]").text
            km = detail.find_element(By.XPATH, ".//span[contains(@class, 'tm-motors-search-card__body-odometer')]").text
            # price_element = detail.find_element(By.XPATH,
            #                                     ".//div[contains(@class, 'tm-motors-search-card__asking-price')]")
            # price = price_element.find_element(By.CLASS_NAME, 'tm-motors-search-card__price').text
            prices = each_price.find_elements(By.CLASS_NAME, 'tm-motors-search-card__price')
            if len(prices) >= 2:
                final_price = prices[1]
            else:
                final_price = prices[0]
            second_last_price = final_price.text
            price = second_last_price.replace('$', '').replace(',', '')

            location = detail.find_element(By.XPATH, ".//div[contains(@class, 'tm-motors-search-card__location')]").text
            location = location.split('\n')[0]

            # Extracting year and name from the title
            title_parts = title.split(' ')
            year = title_parts[0]
            name = ' '.join(title_parts[1:])
            href = card.get_attribute('href')

            each_item = {
                'year': year,
                'name': name,
                'km': km,
                'price': price,
                'location': location,
                'link': href,
            }
            car_list.append(each_item)
        except NoSuchElementException:
            each_item = {
                'year': "-",
                'name': "-",
                'km': "-",
                'price': "-",
                'location': "-",
                'link': "-",
            }
            car_list.append(each_item)


# Sort the car_list by name and then by year
car_list.sort(key=lambda x: (x['name'], x['year']))

# Create an ordered dictionary to group cars by name and then by year
sorted_car_dict = OrderedDict()
for car_detail in car_list:
    name = car_detail['name']
    if name not in sorted_car_dict:
        sorted_car_dict[name] = []
    sorted_car_dict [name].append(car_detail)

# Sort the car details for each category by price in descending order
for name, car_details in sorted_car_dict.items():
    sorted_car_dict[name] = sorted(car_details, key=lambda x: float(re.sub(r'[^\d.]', '', x['price'])) if x['price'] != '-' else 0, reverse=True)

# Create a new DataFrame from the ordered dictionary
final_car_list = []
for name, car_details in sorted_car_dict.items():
    final_car_list.extend(car_details)

df = pd.DataFrame(final_car_list)
df.insert(0, 'Row_number', range(1, len(df) + 1))

current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M')
csv_file_path = f"/Users/kashifumer/Downloads/cars_data_{current_datetime}.csv"

df.to_csv(csv_file_path, index=False)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
# pd.set_option('display.expand_frame_repr', False)
# print(df)
driver.quit()





































# from selenium import webdriver
# from selenium.webdriver.common.by import By
#
# chrome_driver_path = "/Users/kashifumer/Development/chromedriver"
# options = webdriver.ChromeOptions()
# options.add_experimental_option("detach", True)
# driver = webdriver.Chrome(options=options)
#
# # driver.get("https://www.trademe.co.nz/a/motors/cars")
# # details = driver.find_element(By.CLASS_NAME, 'tm-motors-search-card__details')
#
# for i in range(1, 2):
#     driver.get("https://www.trademe.co.nz/a/motors/cars?page=" + str(i))
#     details = driver.find_elements(By.CLASS_NAME, 'tm-motors-search-card__details')
#     for detail in details:
#         title = detail.find_element(By.XPATH, "//div[contains(@class, 'tm-motors-search-card__title')]").text
#         km = detail.find_element(By.XPATH, "//span[contains(@class, 'tm-motors-search-card__body-odometer')]").text
#         price = detail.find_element(By.XPATH, "//div[contains(@class, 'tm-motors-search-card__asking-price')]").text
#         print(title, km, price)
#     i += 1
#
# driver.quit()

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException
#
# chrome_driver_path = "/Users/kashifumer/Development/chromedriver"
# options = webdriver.ChromeOptions()
# options.add_experimental_option("detach", True)
# driver = webdriver.Chrome( options=options)
#
# for i in range(1, 3):  # Change the range to include the desired number of pages
#     driver.get("https://www.trademe.co.nz/a/motors/cars?page=" + str(i))
#     details = driver.find_elements(By.CLASS_NAME, 'tm-motors-search-card__details')
#     for detail in details:
#         try:
#             title = detail.find_element(By.XPATH, ".//div[contains(@class, 'tm-motors-search-card__title')]").text
#             km = detail.find_element(By.XPATH, ".//span[contains(@class, 'tm-motors-search-card__body-odometer')]").text
#             price = detail.find_element(By.XPATH,
#                                         ".//div[contains(@class, 'tm-motors-search-card__asking-price')]").text
#             print(title, km, price)
#         except NoSuchElementException:
#             print("-")
#     i += 1
# driver.quit()

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException
# import pandas as pd
#
# chrome_driver_path = "/Users/kashifumer/Development/chromedriver"
# options = webdriver.ChromeOptions()
# options.add_experimental_option("detach", True)
# driver = webdriver.Chrome( options=options)
#
# car_list = []
# for i in range(1, 3):  # Change the range to include the desired number of pages
#     driver.get("https://www.trademe.co.nz/a/motors/cars?page=" + str(i))
#     details = driver.find_elements(By.CLASS_NAME, 'tm-motors-search-card__details')
#     for detail in details:
#         try:
#             title = detail.find_element(By.XPATH, ".//div[contains(@class, 'tm-motors-search-card__title')]").text
#             km = detail.find_element(By.XPATH, ".//span[contains(@class, 'tm-motors-search-card__body-odometer')]").text
#             price_element = detail.find_element(By.XPATH,
#                                                 ".//div[contains(@class, 'tm-motors-search-card__asking-price')]")
#             price = price_element.find_element(By.CLASS_NAME, 'tm-motors-search-card__price').text
#             location = detail.find_element(By.XPATH, ".//div[contains(@class, 'tm-motors-search-card__location')]").text
#             location = location.split('\n')[0]
#             each_item = {
#                 'title': title,
#                 'km': km,
#                 'price': price,
#                 'location': location,
#             }
#             car_list.append(each_item)
#         except NoSuchElementException:
#             each_item = {
#                 'title': "-",
#                 'km': "-",
#                 'price': "-",
#                 'location': "-",
#             }
#             car_list.append(each_item)
# df = pd.DataFrame(car_list)
# print(df)
# driver.quit()

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException
# import pandas as pd
#
# chrome_driver_path = "/Users/kashifumer/Development/chromedriver"
# options = webdriver.ChromeOptions()
# options.add_experimental_option("detach", True)
# driver = webdriver.Chrome(options=options)
#
# car_list = []
# for i in range(1, 8):  # Change the range to include the desired number of pages
#     driver.get("https://www.trademe.co.nz/a/motors/cars?page=" + str(i))
#     details = driver.find_elements(By.CLASS_NAME, 'tm-motors-search-card__details')
#     for detail in details:
#         try:
#             title = detail.find_element(By.XPATH, ".//div[contains(@class, 'tm-motors-search-card__title')]").text
#             km = detail.find_element(By.XPATH, ".//span[contains(@class, 'tm-motors-search-card__body-odometer')]").text
#             price_element = detail.find_element(By.XPATH,
#                                                 ".//div[contains(@class, 'tm-motors-search-card__asking-price')]")
#             price = price_element.find_element(By.CLASS_NAME, 'tm-motors-search-card__price').text
#             location = detail.find_element(By.XPATH, ".//div[contains(@class, 'tm-motors-search-card__location')]").text
#             location = location.split('\n')[0]
#
#             # Extracting year and name from the title
#             title_parts = title.split(' ')
#             year = title_parts[0]
#             name = ' '.join(title_parts[1:])
#
#             each_item = {
#                 'year': year,
#                 'name': name,
#                 'km': km,
#                 'price': price,
#                 'location': location,
#             }
#             car_list.append(each_item)
#         except NoSuchElementException:
#             each_item = {
#                 'year': "-",
#                 'name': "-",
#                 'km': "-",
#                 'price': "-",
#                 'location': "-",
#             }
#             car_list.append(each_item)
#
# df = pd.DataFrame(car_list)
# print(df)
# driver.quit()


# Next time you run the script fix the 'km' column here only ###### ########
# Leave this for now as things are working fine. Something you can consider in the future, for now focus on money ###





























