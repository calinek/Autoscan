import time
import pandas as pd
from selenium import webdriver


class AutoScan24:
    def __init__(self, make, model, version, year_from, year_to, power_from, power_to, powertype):
        self.make = make
        self.model = model
        self.version = version
        self.year_from = year_from
        self.year_to = year_to
        self.power_from = power_from
        self.power_to = power_to
        self.powertype = powertype
        self.base_url = ("https://www.autoscout24.pl/lst/{}/{}/ve_{}?atype=C&cy=D%2CA%2CB%2CE%2CF%2CI%2CL%2CNL&damaged_listing=exclude&desc=0&"
                         "fregfrom={}&fregto={}&powerfrom={}&powerto={}&powertype={}&sort=standard&"
                         "source=homepage_search-mask&ustate=N%2CU")
        self.listing_frame = pd.DataFrame(
            columns=["make", "model", "mileage", "fuel-type", "first-registration", "price"])
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--incognito")
        self.options.add_argument("--ignore-certificate-errors")
        self.browser = webdriver.Chrome(options=self.options)

    def generate_urls(self, num_pages):
        url_list = [self.base_url.format(self.make, self.model, self.version, self.year_from, self.year_to,
                                         self.power_from, self.power_to, self.powertype)]
        for i in range(2, num_pages + 1):
            url_to_add = (self.base_url.format(self.make, self.model, self.version, self.year_from, self.year_to,
                                               self.power_from, self.power_to, self.powertype) +
                          f"&page={i}&sort=standard&source=listpage_pagination&ustate=N%2CU")
            url_list.append(url_to_add)
        return url_list

    def scrape(self, num_pages, verbose=False):
        url_list = self.generate_urls(num_pages)

        for webpage in url_list:
            self.browser.get(webpage)
            listings = self.browser.find_elements("xpath", "//article[contains(@class, 'cldt-summary-full-item')]")

            for listing in listings:
                data_make = listing.get_attribute("data-make")
                data_model = listing.get_attribute("data-model")
                data_mileage = listing.get_attribute("data-mileage")
                data_fuel_type = listing.get_attribute("data-fuel-type")
                data_first_registration = listing.get_attribute("data-first-registration")
                data_price = listing.get_attribute("data-price")

                listing_data = {
                    "make": data_make,
                    "model": data_model,
                    "mileage": data_mileage,
                    "fuel-type": data_fuel_type,
                    "first-registration": data_first_registration,
                    "price": data_price
                }

                if verbose:
                    print(listing_data)

                frame = pd.DataFrame(listing_data, index=[0])
                self.listing_frame = self.listing_frame._append(frame, ignore_index=True)
                time.sleep(1)

    def save_to_csv(self, filename="listings.csv"):
        self.listing_frame.to_csv(filename, index=False)
        print("Data saved to", filename)

    def quit_browser(self):
        self.browser.quit()
