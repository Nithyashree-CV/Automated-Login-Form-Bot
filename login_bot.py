from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time


class LoginBot:
    """Automates login testing and basic form interactions using Selenium."""

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.driver = webdriver.Chrome()   # Selenium 4+ auto-manages the driver
        self.wait = WebDriverWait(self.driver, 10)

    def open_login_page(self):
        self.driver.get(f"{self.base_url}/login")

    def login(self, username: str, password: str):
        self.driver.find_element(By.ID, "username").clear()
        self.driver.find_element(By.ID, "username").send_keys(username)
        self.driver.find_element(By.ID, "password").clear()
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    def get_message(self) -> str:
        message = self.wait.until(
            EC.presence_of_element_located((By.ID, "flash"))
        )
        return message.text

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
        dropdown = Select(self.driver.find_element(By.ID, "dropdown"))
        dropdown.select_by_visible_text("Option 2")
        selected = dropdown.first_selected_option.text
        print(f"[Dropdown test] Selected: {selected}")

    def test_checkbox(self):
        self.driver.get(f"{self.base_url}/checkboxes")
        checkboxes = self.driver.find_elements(By.CSS_SELECTOR, "#checkboxes input")
        checkboxes[0].click()
        print(f"[Checkbox test] Checkbox 1 checked: {checkboxes[0].is_selected()}")

    def close(self):
        time.sleep(2)  # brief pause so you can see the final state
        self.driver.quit()


if __name__ == "__main__":
    bot = LoginBot(base_url="https://the-internet.herokuapp.com")
    bot.test_valid_login()
    bot.test_invalid_login()
    bot.test_dropdown()
    bot.test_checkbox()
    bot.close()
