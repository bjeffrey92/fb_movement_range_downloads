import mechanicalsoup
import crayons
import pickle

URL = "https://www.facebook.com/login/?next=https%3A%2F%2Fwww.facebook.com%2Fgeoinsights-portal%2F"
BASE = "https://www.facebook.com/geoinsights-portal/downloads"


class FbGeoinsights:
    def __init__(self, credentials=None, verbose=True, max_download=100):
        self.verbose = verbose
        self.browser = mechanicalsoup.StatefulBrowser()

        self.log("Connecting...", False)
        self.browser.open(URL)
        self.log(crayons.green("OK"))
        self.browser.select_form('form[id="login_form"]')
        if type(credentials) is str:
            self.log("Loading cookies!...", False)
            with open(credentials, "rb") as f:
                cookies = pickle.load(f)
            self.browser.set_cookiejar(cookies)
            self.log(crayons.green("OK"))
        else:
            self.browser["email"] = credentials["email"]
            self.browser["pass"] = credentials["password"]
            self.log("Logging in...", False)
            response = self.browser.submit_selected()
            self.response = response
            if not response.ok:
                print("Login failed!")
            self.log(crayons.green("OK"))
        self.counter = 0
        self.max_download = max_download

    def dump_cookies(self, path):
        with open(path, "wb") as f:
            pickle.dump(self.browser.get_cookiejar(), f)

    def fetch(self, name, loc_id, date, time, type):
        if self.counter > self.max_download:
            raise Exception(
                "Stopping now as {} already downloaded".format(self.counter)
            )
        title = "{} ({}/{})".format(name, date, time)
        url = self.url(loc_id, date, time, type)
        return self.download(title, url)

    def log(self, message, newline=True):
        if self.verbose:
            if newline:
                print(message)
            else:
                print(message, end="", flush=True)

    def url(self, loc_id, date, time, type):
        return "{base}/{type}/?id={loc_id}&ds={date}%20{time}".format(
            base=BASE, type=type, loc_id=loc_id, date=date, time=time
        )

    def download(self, title, url):
        self.counter += 1
        code = None
        try:
            self.log("Downloading {}...".format(title), False)
            response = self.browser.get(url=url)
            code = response.status_code
            if (
                response.status_code == 200
                and response.text != "Not found"
                and not response.text.startswith("<!DOCTYPE html>")
            ):
                return {"success": True, "value": response.text, "code": code}
        except Exception:
            pass
        return {"success": False, "value": None, "code": code}
