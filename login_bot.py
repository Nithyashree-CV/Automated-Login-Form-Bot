"""Automated login bot: tests valid and invalid credentials on a demo site."""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

LOGIN_URL = "https://the-internet.herokuapp.com/login"

# Public demo credentials published by the test site itself.
VALID_USER = "tomsmith"
VALID_PASSWORD = "SuperSecretPassword!"


class LoginBot:
    def __init__(self, headless=True, timeout=10):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, timeout)

    def login(self, username, password):
        """Submit the login form and return the flash message text."""
        self.driver.get(LOGIN_URL)
        self.driver.find_element(By.ID, "username").send_keys(username)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        flash = self.wait.until(EC.visibility_of_element_located((By.ID, "flash")))
        return flash.text

    def check(self, label, username, password, expected):
        message = self.login(username, password)
        passed = expected in message
        print(f"[{'PASS' if passed else 'FAIL'}] {label}: {message.splitlines()[0]}")
        return passed

    def close(self):
        self.driver.quit()


def main():
    bot = LoginBot()
    try:
        results = [
            bot.check("Valid credentials", VALID_USER, VALID_PASSWORD,
                      "You logged into a secure area!"),
            bot.check("Invalid username", "wronguser", VALID_PASSWORD,
                      "Your username is invalid!"),
            bot.check("Invalid password", VALID_USER, "wrongpassword",
                      "Your password is invalid!"),
        ]
    finally:
        bot.close()
    raise SystemExit(0 if all(results) else 1)


if __name__ == "__main__":
    main()
