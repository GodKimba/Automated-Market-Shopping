from subprocess import TimeoutExpired
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import os
import time


# ZS credentials
username = os.environ.get('username_key')
password = os.environ.get('password_key')
first_name = os.environ.get('first_name_key')
last_name = os.environ.get("last_name_key")
cpf = os.environ.get("cpf_key")
phone_number = os.environ.get("phone_number_key")
building_number = os.environ.get("building_number_key")
complement_number = os.environ.get("complement_number_key")
ship_receiver_name = first_name
cep = os.environ.get("cep_key")

# Credit Card Info
card_number = os.environ.get("card_number_key")
on_card_name = os.environ.get('on_card_name_key')
card_expiration_month = os.environ.get('card_expiration_month_key')
card_expiration_year = os.environ.get('card_expiration_year_key')
card_security_number = os.environ.get('card_security_number_key')


# Initialize Chrome driver
chrome_driver_path = Service("/Users/Rafa/Desktop/programação/chromedriver")
driver = webdriver.Chrome(service=chrome_driver_path)
actions = webdriver.common.action_chains.ActionChains(driver)
driver.get("https://autenticacao.zonasul.com.br/login")
timeout = 15

# Loging in
driver.find_element(by=By.NAME, value="document").send_keys(
    username + "\n"
)  # Getting username

# Waiting page to load and getting password
try:
    password_present_in_page = EC.presence_of_element_located((By.NAME, "password"))
    WebDriverWait(driver, timeout).until(password_present_in_page)
except TimeoutExpired:
    print("Timed out waiting for page to load")

driver.find_element(by=By.NAME, value="password").send_keys(password + "\n")

# Waiting page to load and entering the homepage
try:
    enter_site_present_in_page = EC.presence_of_element_located(
        (By.XPATH, '//*[@id="app"]/div/div[2]/div/a')
    )
    WebDriverWait(driver, timeout).until(enter_site_present_in_page)
except TimeoutExpired:
    print("Timed out waiting for page to load")

driver.find_element(by=By.XPATH, value='//*[@id="app"]/div/div[2]/div/a').click()


# Entering in mylist page and adding mylist to mycart
driver.get("https://www.zonasul.com.br/minhas-listas")
time.sleep(15)

# Getting rid of mf popup so I can add items to cart
insert_to_cart_position = driver.find_element(by=By.CLASS_NAME, value="card__btn")
actions.click(insert_to_cart_position)
actions.perform()

time.sleep(5)
driver.find_element(by=By.CLASS_NAME, value="card__btn").click()
driver.find_element(
    by=By.CLASS_NAME, value="zonasul-region-selector-0-x-inputCepModal"
).send_keys(cep + "\n")

try:
    delivery_button_in_page = EC.presence_of_element_located(
        (By.CLASS_NAME, "zonasul-region-selector-0-x-newModalDeliveryDeliveryButton")
    )
    WebDriverWait(driver, timeout).until(delivery_button_in_page)
except TimeoutExpired:
    print("Timed out waiting for page to load")

driver.find_element(
    by=By.CLASS_NAME, value="zonasul-region-selector-0-x-newModalDeliveryDeliveryButton"
).click()

time.sleep(8)
try:
    close_icon_in_page = EC.presence_of_element_located(
        (By.CLASS_NAME, "zonasul-zonasul-minicart-0-x-closeIcon")
    )
    WebDriverWait(driver, timeout).until(close_icon_in_page)
except TimeoutExpired:
    print("Timed out waiting for page to load")

driver.find_element(
    by=By.CLASS_NAME, value="zonasul-zonasul-minicart-0-x-closeIcon"
).click()
driver.find_element(by=By.CLASS_NAME, value="card__btn").click()
time.sleep(2)
# Checking out
driver.get("https://www.zonasul.com.br/cart")
driver.find_element(
    by=By.ID,
    value="proceed-to-checkout",
).click()
time.sleep(2)

# Filling in personal data form
driver.find_element(by=By.ID, value="client-first-name").send_keys(first_name)
driver.find_element(by=By.ID, value="client-last-name").send_keys(last_name)
driver.find_element(by=By.ID, value="client-document").send_keys(cpf)
driver.find_element(by=By.ID, value="client-phone").send_keys(phone_number)
driver.find_element(by=By.ID, value="go-to-shipping").click()
try:
    ship_number_present_in_page = EC.presence_of_element_located((By.ID, "ship-number"))
    WebDriverWait(driver, timeout).until(ship_number_present_in_page)
except TimeoutExpired:
    print("Timed out waiting for page to load")
# Filling in shipping data form
driver.find_element(by=By.ID, value="ship-number").send_keys(building_number)
driver.find_element(by=By.ID, value="ship-complement").send_keys(complement_number)
driver.find_element(by=By.ID, value="ship-receiverName").send_keys(ship_receiver_name)

# Selecting shipping time
driver.find_element(
    by=By.ID,
    value="scheduled-delivery-choose-Entrega-Zona Sul das 08h as 10h",
).click()

driver.find_element(
    by=By.ID, value="scheduled-delivery-choose-Entrega-Zona Sul das 08h as 10h"
).send_keys(Keys.ENTER)

# Going to payment and finishing order
driver.find_element(by=By.ID, value="btn-go-to-payment").click()
time.sleep(3)

# Switching to the frame that keeps credit card inputs
driver.switch_to.frame(0)  
time.sleep(1)
driver.find_element(
    by=By.XPATH, value='//*[@id="creditCardpayment-card-0Number"]'
).send_keys(card_number)
driver.find_element(
    by=By.XPATH, value='//*[@id="creditCardpayment-card-0Name"]'
).send_keys(on_card_name)

select_card_year = Select(
    driver.find_element(by=By.XPATH, value='//*[@id="creditCardpayment-card-0Year"]')
)
select_card_month = Select(
    driver.find_element(by=By.XPATH, value='//*[@id="creditCardpayment-card-0Month"]')
)

select_card_month.select_by_value(card_expiration_month)
select_card_year.select_by_value(card_expiration_year)
driver.find_element(by=By.ID, value="creditCardpayment-card-0Code").send_keys(
    card_security_number
)
driver.find_element(by=By.ID, value="holder-document-0").send_keys(cpf)


driver.close()


# Selecting day to ship, using css class and f string to get only tuesdays
# ship_day = 0
# if calendar.TUESDAY == True:
#     ship_day = date.today().day + 1
# time.sleep(5)
# driver.find_element(
#     by=By.CLASS_NAME, value=f"react-datepicker__day react-datepicker__day--010"
# ).click()


"""
Bug relacionado ao carregamento da pagina de confirmacao do cep(as vezes fica rodando e da erro de elemento nao presente)
    talvez criar um wait until element present ou depois de timeout recarregar a pagina e continuar de onde estava

Bug relacionado a 'proceed to checkout' quando o carrinho ainda esta vazio
    pensar numa forma de confirmar se o carrinho esta vazio. Deve ter algum elemento em html ou css no codigo fonte que forneca essa informacao
"""
