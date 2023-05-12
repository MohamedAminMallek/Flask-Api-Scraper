from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.common.exceptions import TimeoutException
import datetime


def scrape_product(product_title_search, num_elements_to_scrap=1):

    list_products = []

    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless')
    opts.add_argument('--no-sandbox')         
    opts.add_argument('--disable-dev-shm-usage')                 

    driver = webdriver.Remote("http://selenium:4444/wd/hub", DesiredCapabilities.CHROME, options=opts)

    driver.get("https://www.amazon.fr")

    sleep(2)

    continuer_without_accepting_cookies_id = "sp-cc-rejectall-container"
    driver.find_element(By.ID, continuer_without_accepting_cookies_id).click()

    sleep(2)

    search_bar_id = "twotabsearchtextbox"
    search_bar_input_element = driver.find_element(By.ID, search_bar_id)
    search_bar_input_element.send_keys(product_title_search)

    search_bar_input_element.send_keys(Keys.ENTER)

    search_result_container_id = "search"
    
    try:
        wait = WebDriverWait(driver, 30)
        wait.until(visibility_of_element_located((By.ID, search_result_container_id)))
    except TimeoutException:
        driver.quit()
        return None
       

    search_restul_element = driver.find_element(By.ID, search_result_container_id)

    result_elements = search_restul_element.find_element(By.XPATH, "div/div/div/span/div").find_elements(By.XPATH, "div")[1:]

    for result_element in result_elements:
        try:
            is_a_result = result_element.get_attribute("data-component-type") == "s-search-result"
        except:
            is_a_result = False
        
        if is_a_result:
            product_elements = result_element.find_elements(By.XPATH, "div/div/div/div/div")
            product_with_amazon_label = len(product_elements) == 3
            
            product_cover_index = 1 if product_with_amazon_label else 0
            product_details_index = product_cover_index + 1

            product_cover_elemnt = product_elements[product_cover_index]
            product_cover_image_link = product_cover_elemnt.find_element(By.XPATH, "span/a/div/img").get_attribute("src")

            product_details_elements = product_elements[product_details_index].find_elements(By.XPATH, "div")

            product_title_element = product_details_elements[0]
            product_title_text = product_title_element.find_element(By.XPATH, "h2/a/span").text


            product_link_text = product_title_element.find_element(By.XPATH, "h2/a").get_attribute("href")

            product_reviews_element = product_details_elements[1]
            product_reviews_stars_text = product_reviews_element.find_element(By.XPATH, "div/span/span/a/i/span").get_attribute("innerHTML")
            product_reviews_number = product_reviews_element.find_element(By.XPATH, "div/span[2]/a/span").text

            product_price_element = product_details_elements[2]

                    
            # soup = BeautifulSoup(product_price_element.get_attribute("innerHTML"), 'html.parser')
            # print(soup.prettify())

            try:
                product_price_text = product_price_element.find_element(By.CLASS_NAME, "a-price").text
            except:
                continue

            
            if product_with_amazon_label:
                print(product_elements[0].text)

            print("Title: ", product_title_text)
            print("link: ", product_link_text)
            print("Reviews: ", product_reviews_stars_text)
            print("Reviews number: ", product_reviews_number)
            print("Price: ", product_price_text)
            print("=====================================")
            num_elements_to_scrap -= 1
            
            list_products.append({
                "name": product_title_text,
                "price": float(product_price_text.split("€")[0].replace(",", ".")),
                "reviews": float(product_reviews_stars_text.split(" ")[0].replace(",", ".")),
                "image_link": product_cover_image_link,
                "product_link": product_link_text,
                "scraped_at": f"{datetime.datetime.utcnow()}"

            })
        
        if num_elements_to_scrap == 0:
            break
    
    driver.quit()
    return list_products