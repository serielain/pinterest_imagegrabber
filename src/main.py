import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException

#make sure you change the URL and the folder path to your own
url = "Pinterest Board URL HERE"
folder_path = "Y:\\EXAMPLEFOLDER"
# Create a new Firefox browser instance
driver = webdriver.Firefox()

# Navigate to the webpage
driver.get(url)

#counts the time it takes to run the code
start_time = time.time()

# Set of image URLs
image_urls = set()
scroll_position = 0
time.sleep(5)
try:
    # Scroll and extract image URLs 
    for _ in range(9999999999):  # Adjust this value based on your needs
        # Scroll down the page in steps
        for _ in range(2):  # Adjust this value based on your needs (default:2)
            scroll_position += 150  # Scroll down 150 default
            driver.execute_script(f"window.scrollTo(0, {scroll_position});")
            time.sleep(0.05)  # Adjust this value based on your needs

        # Click the "Mehr anzeigen" button if it appears
        try:
            button = WebDriverWait(driver, 0).until(
                EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Mehr anzeigen']"))
            )
            button.click()
        except TimeoutException:
            print("No 'Mehr anzeigen' button found")
        time.sleep(0)


        # Parse the webpage's content
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Find all image elements on the page
        image_elements = soup.find_all("img")

        # Extract and save the image URLs
        for image_element in image_elements:
            image_url = image_element.get("src")
            if image_url:
                image_urls.add(image_url)
        print(f"Number of URLs: {len(image_urls)}")
except WebDriverException:
    print("Browser closed. Starting to process the image URLs...")

# Create or open a .txt file to save the modified image URLs
with open("changed_list.txt", "w") as file:
    # Save each unique image URL to the .txt file
    for image_url in image_urls:
        # Replace "75x75_RS" and "236x" with "originals"
        modified_url = image_url.replace("75x75_RS", "originals").replace("140x140_RS", "originals").replace("170x", "originals").replace("222x", "originals").replace("236x", "originals").replace("280x280_RS", "originals").replace("1200x", "originals").replace("236x", "originals").replace("236x", "originals")
        file.write(modified_url + "\n")

print("All modified image URLs saved successfully!")

# Count the number of saved URLs
with open("changed_list.txt", "r") as file:
    url_count = sum(1 for line in file)
print(f"Number of saved URLs: {url_count}")

# Read the modified image URLs from the .txt file and download each image
image_counter = 0
with open("changed_list.txt", "r") as file:
    for line in file:
        image_url = line.strip()
        image_name = image_url.split("/")[-1]
        save_path = os.path.join(folder_path, image_name)

        # Send a GET request to download the image
        image_response = requests.get(image_url)

        # Save the image to the specified directory
        with open(save_path, "wb") as image_file:
            image_file.write(image_response.content)
        image_counter += 1
        print(f"Number {image_counter} / {len(image_urls)} downloaded: {image_name}")

    

def check_and_redownload_images():
    # Read the modified image URLs from the .txt file
    with open("changed_list.txt", "r") as file:
        for line in file:
            image_url = line.strip()
            image_name = image_url.split("/")[-1]
            save_path = os.path.join(folder_path, image_name)

            # Check if the image file exists and is valid
            if os.path.isfile(save_path):
                try:
                    # Open the image file
                    img = Image.open(save_path)
                    img.verify()
                except (IOError, SyntaxError) as e:
                    print(f"Invalid image: {image_name}")
                    # If the image is invalid, re-download it with "564x" instead of "originals"
                    redownload_url = image_url.replace("originals", "564x")
                    redownload_image(redownload_url, save_path)
            else:
                print(f"Image not found: {image_name}")
                # If the image file does not exist, download it
                download_image(image_url, save_path)

def download_image(image_url, save_path):
    # Send a GET request to download the image
    image_response = requests.get(image_url)

    # Save the image to the specified directory
    with open(save_path, "wb") as image_file:
        image_file.write(image_response.content)

    print(f"Downloaded: {os.path.basename(save_path)}")

def redownload_image(image_url, save_path):
    # Delete the invalid image file
    os.remove(save_path)

    # Re-download the image
    download_image(image_url, save_path)

def count_elements_in_folder(folder_path):
    """Count the number of elements (files and directories) in a folder."""
    return len(os.listdir(folder_path))

# Call the function to check and re-download images
check_and_redownload_images()

# Call the function and print the result
element_count = count_elements_in_folder(folder_path)
print(f"Number of Elements in Folder: {element_count}")

#time to run the code
end_time = time.time()
total_time = end_time - start_time
print(f'The total time used to run the code is: {total_time} seconds')