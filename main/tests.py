from django.test import TestCase, Client, LiveServerTestCase
from main.models import Item
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from django.contrib.auth.models import User


class MainTest(TestCase):
    def test_main_url_is_exist(self):
        response = Client().get('')
        self.assertEqual(response.status_code, 200)

    def test_main_using_main_template(self):
        response = Client().get('')
        self.assertTemplateUsed(response, 'main.html')

    def test_nonexistent_page(self):
        response = Client().get('/burhan_always_exists/')
        self.assertEqual(response.status_code, 404)


class FootballNewsFunctionalTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.browser.quit()

    def setUp(self):
        self.test_user = User.objects.create_user(
            username='testadmin',
            password='testpassword'
        )

    def tearDown(self):
        self.browser.delete_all_cookies()
        self.browser.execute_script("window.localStorage.clear();")
        self.browser.execute_script("window.sessionStorage.clear();")
        self.browser.get("about:blank")

    def login_user(self):
        self.browser.get(f"{self.live_server_url}/login/")
        username_input = self.browser.find_element(By.NAME, "username")
        password_input = self.browser.find_element(By.NAME, "password")
        username_input.send_keys("testadmin")
        password_input.send_keys("testpassword")
        password_input.submit()

    def test_login_page(self):
        self.login_user()
        wait = WebDriverWait(self.browser, 10)
        wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, "h1"), "NewGames Shop"))

        h1_element = self.browser.find_element(By.TAG_NAME, "h1")
        self.assertEqual(h1_element.text, "NewGames Shop")

        logout_button = self.browser.find_element(By.XPATH, "//button[contains(text(), 'Logout')]")
        self.assertTrue(logout_button.is_displayed())

    def test_register_page(self):
        self.browser.get(f"{self.live_server_url}/register/")

        h1_element = self.browser.find_element(By.TAG_NAME, "h1")
        self.assertEqual(h1_element.text, "Register")

        username_input = self.browser.find_element(By.NAME, "username")
        password1_input = self.browser.find_element(By.NAME, "password1")
        password2_input = self.browser.find_element(By.NAME, "password2")

        username_input.send_keys("newuser")
        password1_input.send_keys("complexpass123")
        password2_input.send_keys("complexpass123")
        password2_input.submit()

        wait = WebDriverWait(self.browser, 10)
        wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, "h1"), "Login"))
        login_h1 = self.browser.find_element(By.TAG_NAME, "h1")
        self.assertEqual(login_h1.text, "Login")

    def test_create_items(self):
        self.login_user()

        wait = WebDriverWait(self.browser, 120)
        add_button = self.browser.find_element(By.PARTIAL_LINK_TEXT, "Add Product")
        add_button.click()

        name_input = self.browser.find_element(By.NAME, "name")
        price_input = self.browser.find_element(By.NAME, "price")
        description_input = self.browser.find_element(By.NAME, "description")
        thumbnail_input = self.browser.find_element(By.NAME, "thumbnail")
        category_select = self.browser.find_element(By.NAME, "category")
        is_featured_checkbox = self.browser.find_element(By.NAME, "is_featured")
        stock_input = self.browser.find_element(By.NAME, "stock")
        brand_input = self.browser.find_element(By.NAME, "brand")

        name_input.send_keys("Test Futsal Ball")
        price_input.send_keys("250000")
        description_input.send_keys("Bola futsal untuk pengujian selenium")
        thumbnail_input.send_keys("https://example.com/image.jpg")

        select = Select(category_select)
        select.select_by_value("bola")

        is_featured_checkbox.click()
        stock_input.clear()
        stock_input.send_keys("10")
        brand_input.send_keys("Specs")

        submit_button = self.browser.find_element(By.XPATH, "//input[@type='submit' and @value='Add ITEMS']")
        submit_button.click()

        wait = WebDriverWait(self.browser, 120)
        wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Test Futsal Ball")))
        product_title = self.browser.find_element(By.PARTIAL_LINK_TEXT, "Test Futsal Ball")
        self.assertTrue(product_title.is_displayed())


    def test_item_detail(self):
        self.login_user()
        item = Item.objects.create(
            name="Detail Test Item",
            price=100000,
            description="Description for detail testing",
            thumbnail="https://example.com/image.jpg"
            category="bola",
            user=self.test_user
        )
        self.browser.get(f"{self.live_server_url}/items/{item.id}/")
        self.assertIn("Detail Test Item", self.browser.page_source)
        self.assertIn("Description for detail testing", self.browser.page_source)

    def test_logout(self):
        self.login_user()
        logout_button = self.browser.find_element(By.XPATH, "//button[contains(text(), 'Logout')]")
        logout_button.click()

        wait = WebDriverWait(self.browser, 10)
        wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, "h1"), "Login"))
        h1_element = self.browser.find_element(By.TAG_NAME, "h1")
        self.assertEqual(h1_element.text, "Login")

    def test_filter_main_page(self):
        Item.objects.create(
            name="My Test Item",
            price=50000,
            description="My item content",
            category="bola",
            user=self.test_user
        )
        Item.objects.create(
            name="Other User Item", 
            price=75000,
            description="Other content",
            category="bola",
            user=self.test_user
        )

        self.login_user()

        wait = WebDriverWait(self.browser, 120)

        all_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='All Products']"))
        )
        all_button.click()
        self.assertIn("My Test Item", self.browser.page_source)
        self.assertIn("Other User Item", self.browser.page_source)

        my_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='My Products']"))
        )
        my_button.click()
        self.assertIn("My Test Item", self.browser.page_source)
        self.assertNotIn("Other User Item", self.browser.page_source)

