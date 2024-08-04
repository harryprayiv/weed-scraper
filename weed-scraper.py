import json
import os
import time
import keyboard
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Path to undetected-chromedriver
chrome_driver_path = "/nix/store/63i1vwkv01qs8r4ahk6g1khy38srp76r-undetected-chromedriver-126.0.6478.182/bin/undetected-chromedriver"

if not os.path.isfile(chrome_driver_path):
    raise ValueError(f"The path {chrome_driver_path} is not a valid file. Make sure undetected-chromedriver is installed.")

# Set up Chrome options
chrome_options = Options()
# Remove the headless argument to make the browser visible
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set the path to the undetected ChromeDriver
service = Service(chrome_driver_path)

# Initialize WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the URL
url = "https://quincycannabis.co/categories/vaporizers/?product_page=64d5111162140a0001a1ecc6"
driver.get(url)

# Give the page some time to load
time.sleep(5)

# Scroll to load all products (if there are lazy-loaded products)
body = driver.find_element(By.CSS_SELECTOR, 'body')
for _ in range(3):  # Adjust the range if needed to load more products
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(2)

# Instructions for interactive selection
print("Navigate to the desired part of the website.")
print("Press 'Ctrl + Shift + 1' to select the first product.")
print("Press 'Ctrl + Shift + 2' to select the last product.")

selected_elements = []

def on_press(key):
    try:
        if key.name == '1' and keyboard.is_pressed('ctrl') and keyboard.is_pressed('shift'):
            selected_elements.append(driver.switch_to.active_element)
            print("First product selected.")
        elif key.name == '2' and keyboard.is_pressed('ctrl') and keyboard.is_pressed('shift'):
            selected_elements.append(driver.switch_to.active_element)
            print("Last product selected.")
    except AttributeError:
        pass

keyboard.on_press(on_press)

# Wait for user to select elements
print("Waiting for selections...")
while len(selected_elements) < 2:
    time.sleep(1)

keyboard.unhook_all()

if len(selected_elements) != 2:
    print("Two elements were not selected correctly.")
    driver.quit()
    exit()

first_product, last_product = selected_elements

# Find the products within the range
products = driver.find_elements(By.CSS_SELECTOR, "div.productCard5G_root__fEcGF")

product_data = []
for product in products:
    try:
        if first_product.location['y'] <= product.location['y'] <= last_product.location['y']:
            name = product.find_element(By.CSS_SELECTOR, "div.productCard5G_name__X3tj+").text.strip()
            price = product.find_element(By.CSS_SELECTOR, "div.productCardPrice_price__NRKpF").text.strip()
            strain = product.find_element(By.CSS_SELECTOR, "div.joint-product-card-strain").text.strip()
            tac = product.find_element(By.CSS_SELECTOR, "div.joint-product-card-tac").text.strip()
            thc = product.find_element(By.CSS_SELECTOR, "div.joint-product-card-thc").text.strip()
            link = product.find_element(By.CSS_SELECTOR, "a.MuiLink-root").get_attribute('href')
            
            product_data.append({
                "Name": name,
                "Price": price,
                "Strain": strain,
                "TAC": tac,
                "THC": thc,
                "Link": link
            })
    except Exception as e:
        print(f"Error extracting product data: {e}")

# Close the WebDriver
driver.quit()

# Save to JSON file
with open("product_data.json", "w") as json_file:
    json.dump(product_data, json_file, indent=4)

print("Product data has been saved to product_data.json")
