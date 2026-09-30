from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time


class LoginBot:
    """Automates login testing and basic form interactions using Selenium."""

    def __init__(self, base_url: str):
        self.base_url = base_url
        options = Options()
        options.add_experimental_option("prefs", {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False
        })
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-features=PasswordLeakDetection,PasswordCheck,AutofillServerCommunication")
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 20)

    def open_login_page(self):
        self.driver.get(f"{self.base_url}/login")
        self.wait.until(EC.presence_of_element_located((By.ID, "username")))

    def login(self, username: str, password: str):
        username_field = self.driver.find_element(By.ID, "username")
        username_field.clear()
        username_field.send_keys(username)

        password_field = self.driver.find_element(By.ID, "password")
        password_field.clear()
        password_field.send_keys(password)

        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    def get_message(self) -> str:
        try:
            message = self.wait.until(
                EC.visibility_of_element_located((By.ID, "flash"))
            )
            return message.text
        except Exception as e:
            print("---- DEBUG INFO ----")
            print("Current URL:", self.driver.current_url)
            print("Page title:", self.driver.title)
            self.driver.save_screenshot("debug_screenshot.png")
            print("Screenshot saved as debug_screenshot.png in your project folder")
            print("--------------------")
            raise e

    def test_valid_login(self):
        self.open_login_page()
        self.login("tomsmith", "SuperSecretPassword!")
        result = self.get_message()
        print(f"[Valid login test] Result: {result.strip()}")

    def test_invalid_login(self):
        self.open_login_page()
        self.login("wronguser", "wrongpassword")
        result = self.get_message()
        print(f"[Invalid login test] Result: {result.strip()}")

    def test_dropdown(self):
        self.driver.get(f"{self.base_url}/dropdown")
        dropdown = Select(self.wait.until(EC.presence_of_element_located((By.ID, "dropdown"))))
        dropdown.select_by_visible_text("Option 2")
        print(f"[Dropdown test] Selected: {dropdown.first_selected_option.text}")

    def test_checkbox(self):
        self.driver.get(f"{self.base_url}/checkboxes")
        checkboxes = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#checkboxes input")))
        checkboxes[0].click()
        print(f"[Checkbox test] Checkbox 1 checked: {checkboxes[0].is_selected()}")

    def close(self):
        time.sleep(2)
        self.driver.quit()


if __name__ == "__main__":
    bot = LoginBot(base_url="https://the-internet.herokuapp.com")
    bot.test_valid_login()
    bot.test_invalid_login()
    bot.test_dropdown()
    bot.test_checkbox()
    bot.close()