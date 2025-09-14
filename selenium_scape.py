from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dataclasses import dataclass
import time
from selenium.webdriver.common.by import By
from concurrent.futures import ThreadPoolExecutor


urls = [
    "https://www.amazon.in/Whirlpool-Refrigerator-205-WDE-CLS/dp/B0BSRVL2VV",
    "https://www.amazon.in/Haier-Direct-Refrigerator-HRD-2203BS-Brushline/dp/B08KH7VF4Q",
    "https://www.amazon.in/Godrej-Refrigerator-EDGE-205B-WRF/dp/B0BS6XQVD1",
    "https://www.amazon.in/LG-Inverter-Frost-Free-Refrigerator-GL-I292RPZX/dp/B08X72GY5Q",
    "https://www.amazon.in/Samsung-Inverter-Refrigerator-RR20C1724CU-HL/dp/B0BR3VMT96",
    "https://www.amazon.in/Haier-Direct-Single-Refrigerator-HED-171RS-P/dp/B0BTHLCK15",
    "https://www.amazon.in/Godrej-Refrigerator-EONVALOR-260C-RCIF/dp/B0BVR5JXZG",
    "https://www.amazon.in/LG-Frost-Free-Inverter-Refrigerator-GL-B257HDSY/dp/B0BX4FBVQB"
]


@dataclass
class CONFIG:
    urls : list
    num_threads : int = 4

config = CONFIG(urls= urls, num_threads= len(urls))


def driver_setup():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options= options)
    return driver

def scrape_amazon(driver, url : str):
    driver.get(url)
    time.sleep(1)
    element = driver.find_element(By.ID, "imgTagWrapperId")
    img_link = element.find_element(By.TAG_NAME, "img").get_attribute('src')
    return img_link


def main():
    drivers = [driver_setup() for _ in range(config.num_threads)]

    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=config.num_threads) as excecutor:
        futures = [excecutor.submit(scrape_amazon, drivers[i], config.urls[i]) for i in range(config.num_threads)]

        for future in futures:
            print(future.result())
    end = time.perf_counter()

    for driver in drivers:
        driver.quit()

    print(f"TIME TAKE : {end - start}")

if __name__ == "__main__":
    main()