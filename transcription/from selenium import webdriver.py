from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# URL of the webpage to scrape
url = "https://www.transcriptforest.com/en/lex-fridman-podcast/8908-ray-dalio-principles-the-economic-machine-artificial-intelligence-and038-the-ar-2019-12-03"

# Configure headless browsing with Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no browser window)

# Initialize the WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Open the webpage
driver.get(url)

# Wait for the desired content to load (you may need to adjust the timeout)
wait = WebDriverWait(driver, 30)
content = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="next"]/div/div/div/div[2]/div/div/p')))

# Extract the text
extracted_text = content.text

# Close the WebDriver
driver.quit()

# Print or use the extracted text as needed
print(extracted_text)
