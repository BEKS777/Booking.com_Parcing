import requests
from selenium.webdriver import Chrome
from bs4 import BeautifulSoup
import json

url = "https://www.booking.com/searchresults.html?label=gen173nr-1FCAEoggI46AdIM1gEaIABiAEBmAExuAEHyAEM2AEB6AEB-AECiAIBqAIDuAK1mYWfBsACAdICJGJjNzI3ZTA4LTUwYzItNGQ3ZC1hMjQ0LTA5ZmZlMzRjZDc0ZtgCBeACAQ&aid=304142&dest_id=-2334218&dest_type=city&group_adults=null&req_adults=null&no_rooms=null&group_children=null&req_children=null&offset="
# url2 = "https://www.booking.com/hotel/kz/aykun.html?label=gen173nr-1FCAEoggI46AdIM1gEaIABiAEBmAExuAEHyAEM2AEB6AEB-AECiAIBqAIDuAK1mYWfBsACAdICJGJjNzI3ZTA4LTUwYzItNGQ3ZC1hMjQ0LTA5ZmZlMzRjZDc0ZtgCBeACAQ&aid=304142&ucfs=1&arphpl=1&dest_id=-2334218&dest_type=city&group_adults=2&req_adults=2&no_rooms=1&group_children=0&req_children=0&hpos=1&hapos=26&sr_order=popularity&srpvid=d670869f573203b9&srepoch=1675710528&from_sustainable_property_sr=1&from=searchresults#hotelTmpl"
driver = Chrome("chromedriver")
count = 0
for i in range(1, 28):
    driver.get(url + str(i*25))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    src = driver.page_source

    soap = BeautifulSoup(src, "lxml")

    links = []

    for link in soap.find_all(attrs={"data-testid": "title-link"}):
        item = link.get("href")
        links.append(item)

    for j in links:
        data = []
        facilities = []
        req = requests.get(j)
        src = req.text
        soap = BeautifulSoup(src, "lxml")
        try:
            title = soap.find("h2", class_="d2fee87262 pp-header__title").text
        except:
            continue
        try:
            address = soap.find("span", class_="hp_address_subtitle js-hp_address_subtitle jq_tooltip").text
        except:
            continue
        try:
            score = soap.find("div", class_="b5cd09854e d10a6220b4").text
        except:
            continue
        try:
            fac = soap.find(attrs={"data-testid": "property-most-popular-facilities-wrapper"}).find_all("span", class_="db312485ba")
        except:
            continue

        title = soap.find("h2", class_="d2fee87262 pp-header__title").text

        address = soap.find("span", class_="hp_address_subtitle js-hp_address_subtitle jq_tooltip").text

        score = soap.find("div", class_="b5cd09854e d10a6220b4").text

        fac = soap.find(attrs={"data-testid": "property-most-popular-facilities-wrapper"}).find_all("span", class_="db312485ba")

        for i in fac:
            facilities.append(i.text)
        data.append({
            "title": title,
            "address": address,
            "score": float(score),
            "facilities": facilities
        })

        with open("data_list.json", "a", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        print("#" + str(count) + "added")
        count+=1
