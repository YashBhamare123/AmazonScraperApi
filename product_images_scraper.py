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


url = 'https://www.amazon.in/Sunfeast-Yumfills-Whoopie-Chocolate-Chip/dp/B06WGM2HK2'


def driver_setup() -> webdriver.Chrome: 
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--window-size=1920,1080") 
    options.add_argument("--start-maximized")
    
    driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = options)
    return driver


def product_image(driver, url :str, thread : int) -> str | None:
    driver.get(url) 
    view_more= WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.LINK_TEXT, "Click to see full view")))
    view_more.click()

    try:
        thumb = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, f'ivImage_{thread}')))
        thumb.click()
        time.sleep(2)

        img = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "ivLargeImage")))
        img_url = img.find_element(By.TAG_NAME, 'img').get_attribute('src')
    except Exception as e:
        img_url = None

    driver.quit()
    return img_url


def main():
    config = CONFIG(url = url, num_threads= 8)

    starti = time.perf_counter()
    drivers = [driver_setup() for _ in range(config.num_threads)]
    endi = time.perf_counter()


    startp = time.perf_counter()
    with ThreadPoolExecutor(max_workers= config.num_threads) as excecutor:
        futures = [excecutor.submit(product_image, drivers[i], config.url, i) for i in range(config.num_threads)]

        for future in futures:
            print(future.result())
    endp = time.perf_counter()

    print(f"INITIALIZATION TIME: {endi - starti}")
    print(f"PROCESSING TIME: {endp-startp}")

if __name__ == "__main__":
    main()

