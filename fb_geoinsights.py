from datetime import date, timedelta
from getpass import getpass

import mechanicalsoup
import crayons

LOGIN_URL = "https://www.facebook.com/login/?next=https%3A%2F%2Fwww.facebook.com%2Fgeoinsights-portal%2F"  # noqa: E501
BASE_URL = [
    "https://www.facebook.com/geoinsights-portal/downloads/vector/",
    "&extra[crisis_name]=ETH_gadm_2",
]


class FbGeoinsights:
    def __init__(self, max_download: int = 100, verbose: bool = True):
        self.verbose = verbose

        self.browser = mechanicalsoup.StatefulBrowser()
        self.log("Connecting...", False)
        self.browser.open(LOGIN_URL)
        self.log(crayons.green("OK"))
        self.browser.select_form('form[id="login_form"]')
        self.browser["email"] = input("Email Address: ")
        self.browser["pass"] = getpass("Password: ")
        self.log("Logging in...", False)
        self.browser.submit_selected(btnName="login")

        response = self.browser.get(
            "https://www.facebook.com/geoinsights-portal/downloads/?id=746067446058242"  # noqa: E501
        )  # check login has succeeded
        if response.ok:
            self.log(crayons.green("OK"))
        else:
            self.log(crayons.red("FAILED"))
            raise Exception("Login Failed")

        self.counter = 0
        self.max_download = max_download

    def fetch(self, start_date, name: str, loc_id: str):
        start_date = date(*tuple(map(int, start_date.split("-"))))
        today = date.today()
        delta = today - start_date
        for i in range(delta.days + 1):
            day = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")

            if self.counter > self.max_download:
                raise Exception(
                    f"Stopping now as {self.counter} already downloaded"
                )
            name = name.replace(" ", "_").lower()  # snakecase
            title = f"{name}_{day}_movement_range_maps.csv"
            url = self.url(loc_id, day)
            status = self.download(title, url)
            if status["success"]:
                with open(title, "w") as a:
                    a.writelines(status["value"])
                self.log(crayons.green("OK"), True)
            else:
                self.log(crayons.red("FAILED"), True)

    def log(self, message: str, newline: bool = True):
        if self.verbose:
            if newline:
                print(message)
            else:
                print(message, end="", flush=True)

    def url(self, loc_id: str, day: str):
        return f"{BASE_URL[0]}?id={loc_id}&ds={day}{BASE_URL[1]}"

    def download(self, title: str, url: str):
        self.counter += 1
        try:
            self.log(f"Downloading {title}...", False)
            response = self.browser.get(url=url)
            if (
                response.status_code == 200
                and response.text != "Not found"
                and not response.text.startswith("<!DOCTYPE html>")
            ):
                return {
                    "success": True,
                    "value": response.text,
                    "code": response.status_code,
                }
        except Exception:
            pass
        return {"success": False, "value": None, "code": None}
