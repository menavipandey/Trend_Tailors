from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import os
from image_analysis import classify_image

# Initialize WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

def instagram_login(driver, username, password):
    driver.get("https://www.instagram.com/")
    time.sleep(2)  # Let the page load

    # Enter username
    username_input = driver.find_element(By.NAME, "username")
    username_input.send_keys(username)

    # Enter password
    password_input = driver.find_element(By.NAME, "password")
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)

    time.sleep(5)  # Wait for login to complete

def scrape_hashtag(driver, hashtag):
    driver.get(f"https://www.instagram.com/explore/tags/{hashtag}/")
    time.sleep(3)  # Let the page load

    post_links = set()
    for _ in range(5):  # Adjust the range for more scrolling
        links = driver.find_elements(By.TAG_NAME, "a")
        for link in links:
            post_link = link.get_attribute("href")
            if "/p/" in post_link:
                post_links.add(post_link)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

    print(f"Collected {len(post_links)} post links")
    return post_links

def scrape_post_details(driver, post_links):
    outfits = []
    for post_link in post_links:
        driver.get(post_link)
        try:
            # Wait for images to load
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "img")))
            
            # Find all image elements
            images = driver.find_elements(By.TAG_NAME, "img")
            
            # Extract image URLs
            for img in images:
                img_url = img.get_attribute("src")
                if img_url and img_url.startswith("https://"):
                    outfits.append(img_url)
        except Exception as e:
            print(f"Failed to scrape {post_link}: {e}")
    
    return outfits

def download_images(image_urls, save_dir):
    os.makedirs(save_dir, exist_ok=True)
    
    for idx, url in enumerate(image_urls):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                # Save image to file
                with open(os.path.join(save_dir, f"image_{idx+1}.jpg"), 'wb') as f:
                    f.write(response.content)
                print(f"Downloaded image_{idx+1}.jpg")
            else:
                print(f"Failed to download {url}. Status code: {response.status_code}")
        except Exception as e:
            print(f"Failed to download {url}: {str(e)}")

def main():
    username = "sampleaccount171"
    password = "smriti@2009"
    hashtag = "fashiontrends"
    save_dir = "D:/Myntra/images"  # Replace with your desired directory

    # Log in to Instagram
    instagram_login(driver, username, password)

    # Scrape hashtag
    post_links = scrape_hashtag(driver, hashtag)

    # Scrape post details
    outfits = scrape_post_details(driver, post_links)

    # Download images
    download_images(outfits, save_dir)

    # Process downloaded images
    for filename in os.listdir(save_dir):
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
            image_path = os.path.join(save_dir, filename)
            
            # Classify image type (lower wear, upper wear, dress)
            category = classify_image(image_path)
            
            # Extract dominant colors
            colors = extract_dominant_colors(image_path, num_colors=3)
            
            # Print or store results
            print(f"Image: {filename}")
            print(f"Category: {category}")
            print(f"Dominant Colors RGB Values:")
            print(colors)
            print("-----------------------------")

    # Close the driver
    driver.quit()

if __name__ == "__main__":
    main()