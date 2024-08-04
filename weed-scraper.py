from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run headless Chrome
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set the path to the ChromeDriver
service = Service("/run/current-system/sw/bin/chromedriver")

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

# Parse product information
products = driver.find_elements(By.CSS_SELECTOR, "div.productCard5G_root__fEcGF")

product_data = []
for product in products:
    try:
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

# Convert to DataFrame
df = pd.DataFrame(product_data)

# Save to Excel file
df.to_excel("product_data.xlsx", index=False)

print("Product data has been saved to product_data.xlsx")
