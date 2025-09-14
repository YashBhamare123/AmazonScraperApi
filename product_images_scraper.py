from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from dataclasses import dataclass
import time
from concurrent.futures import ThreadPoolExecutor

@dataclass
class CONFIG:
    url : str
    num_threads : int = 4


url = 'https://www.amazon.in/Whirlpool-Refrigerator-205-WDE-CLS/dp/B0BSRVL2VV'


def driver_setup() -> webdriver.Chrome: 
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = options)
    return driver


def product_image(driver, url :str, thread : int) -> str | None:
    try:
        driver.get(url) 
        view_more= WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "a-declarative")))
        view_more.click()

        thumb = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, f'ivImage_{thread}')))
        thumb.click()

        img = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "ivLargeImage")))
        img_url = img.find_element(By.TAG_NAME, 'img').get_attribute('src')
        driver.quit()
        return img_url

    except Exception as e:
        return None


def main():
    config = CONFIG(url = url, num_threads= 4)
    drivers = [driver_setup() for _ in range(config.num_threads)]

    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers= config.num_threads) as excecutor:
        futures = [excecutor.submit(product_image, drivers[i], config.url, i) for i in range(config.num_threads)]

        for future in futures:
            print(future.result())

    end = time.perf_counter()
    print(f"TIME TAKEN: {end - start}")

if __name__ == "__main__":
    main()

