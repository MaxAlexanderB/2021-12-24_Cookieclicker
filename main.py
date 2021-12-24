from selenium import webdriver
import time

# --------Set up driver--------#
chrome_driver_path = r"C:\Users\maxal\PycharmProjects\chromedriver.exe"

driver = webdriver.Chrome(executable_path=chrome_driver_path)
driver.get('http://orteil.dashnet.org/experiments/cookie/')

# --------Get cookie --------#
cookie = driver.find_element_by_id("cookie")

# --------Get upgrade item ids--------#
items = driver.find_elements_by_css_selector("#store div")
item_ids = [item.get_attribute("id") for item in items]

# --------Set timers-------#
timeout = time.time() + 5
five_min = time.time() + 60 * 5  # 5minutes from now

while True:
    cookie.click()

    # --------5 sec interval--------#
    if time.time() > timeout:

        # --------get prices--------#
        all_prices = driver.find_elements_by_css_selector("#store b")
        item_prices = []

        for price in all_prices:
            element_text = price.text
            if element_text != "":
                cost = int(element_text.split("-")[1].strip().replace(",", ""))
                item_prices.append(cost)

        # -------dictionary with prices--------#
        cookie_upgrades = {}
        for n in range(len(item_prices)):
            cookie_upgrades[item_prices[n]] = item_ids[n]

        # ------get money---------#
        money_element = driver.find_element_by_id("money").text
        if "," in money_element:
            money_element = money_element.replace(",", "")
        cookie_count = int(money_element)

        # --------locate affordable upgrades-------#
        affordable_upgrades = {}
        for cost, id in cookie_upgrades.items():
            if cookie_count > cost:
                affordable_upgrades[cost] = id

        # --------Get most expensive upgrade--------#
        highest_price_affordable_upgrade = max(affordable_upgrades)
        print(highest_price_affordable_upgrade)
        to_purchase_id = affordable_upgrades[highest_price_affordable_upgrade]
        print(to_purchase_id)

        driver.find_element_by_id(to_purchase_id).click()

        # -------Add 5 sec until next check-----------#
        timeout = time.time() + 5

    # ----------Stop after 5 min and find cookie/s---------#
    if time.time() > five_min:
        cookie_per_s = driver.find_element_by_id("cps").text
        print(cookie_per_s)
        break