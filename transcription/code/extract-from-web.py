import requests
from bs4 import BeautifulSoup

# URL of the webpage to scrape
url = "https://www.transcriptforest.com/en/lex-fridman-podcast/8908-ray-dalio-principles-the-economic-machine-artificial-intelligence-and038-the-ar-2019-12-03"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    html_content = response.text
else:
    print("Failed to fetch the webpage. Status code:", response.status_code)
    html_content = None

# If HTML content was successfully fetched, proceed with scraping
if html_content:
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all the <p> tags
    paragraphs = soup.find_all('p')

    # Initialize a flag to check if the desired text has started
    start_flag = False

    # Initialize an empty string to store the extracted text
    extracted_text = ""

    # Iterate through paragraphs and append text once the desired phrase is found
    for paragraph in paragraphs:
        text = paragraph.get_text()
        if "The following is a conversation with" in text:
            start_flag = True
        if start_flag:
            extracted_text += text + "\n"

    # Print or use the extracted text as needed
    print(extracted_text)
