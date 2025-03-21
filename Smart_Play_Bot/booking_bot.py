from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

import time
import re
from datetime import datetime

class BookingBot:
    
    def __init__(self, driver):
        self.driver = driver

    def _wait_located(self,
                      wait_time = 5,
                      locater = None,
                      _type = "xpath") -> None:

        assert locater != None, "XPath cannot be None"

        if _type == "xpath":
            by = By.XPATH
        elif _type == "class":
            by = By.CLASS_NAME
        else:
            raise ValueError("\nInvalid locator type. Use 'xpath' or 'class_name'.")

        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((by, locater))
            )

        except TimeoutException:
            raise TimeoutException(f"\nTimeout! Cannot find '{_type}': {locater}") from None
        
    def get_login_page(self):
        """ Load Smartplay Homepage and Redirect to Login Page """

        login_button_xpath = "/html/body/div[1]/header/div/div/div[2]/div[1]/ul/li[2]/a/span"

        self.driver.maximize_window()
        
        print("Loading to login page")

        self._wait_located(locater=login_button_xpath, _type="xpath")
        LoginButtonElement = self.driver.find_element(By.XPATH, login_button_xpath)
        self.driver.execute_script("arguments[0].click();", LoginButtonElement)

    def login(
        self,
        username = None,
        password = None            
    ):
        """ Input user account info and Login """

        username_xpath = "//input[@class='el-input__inner' and @name='pc-login-username']"
        password_xpath = "//input[@type='password' and @name='pc-login-password']"
        # login_button_xpath = "/html/body/div/div[2]/div/div[1]/div[2]/div/div[1]/div/div[3]/div"
        login_button_xpath = "//div[@data-v-8c95f640='' and @role='button']"

        ### Switch driver to new page
        self.driver.switch_to.window(self.driver.window_handles[-1])

        time.sleep(1)

        if username and password:
            UsernameField = self.driver.find_element(By.XPATH, username_xpath)
            UsernameField.send_keys(username)

            PasswordField = self.driver.find_element(By.XPATH, password_xpath)
            PasswordField.send_keys(password)

            time.sleep(0.5)

            LoginButtonElement = self.driver.find_element(By.XPATH, login_button_xpath)
            self.driver.execute_script("arguments[0].click();", LoginButtonElement)

            print("Logged in")

    def check_waiting_queue(self):
        image_xpath = "//img[@src='/static/img/virtual-queue.gif' and @alt='smartplay']"

        
        pass

    def search_available_period(self, month:int, day:int, district:str, sport:str):
        """ Redirect to timeslot selection page by given month, day """

        month, day = int(month), int(day)

        facility_button_xpath = "/html/body/div/div[1]/div[1]/div/div[1]/div/div[1]/ul/li[2]/div"

        sport_input_field_xpath = "/html/body/div/div[2]/div[1]/div[2]/div/div/div/div/div/div[3]/div[1]/div/div[1]"
        input_field_xpath = "/html/body/div/div[2]/div[1]/div[2]/div/div/div/div/div/div[3]/div[1]/div[2]/div[2]/div/div/div[1]/input"
        sport_type_xpath = f"//p[@data-v-21e43f8c and @data-v-42c8b4a0 and contains(text(),'{sport}')]"

        district_input_field_xpath = "/html/body/div[1]/div[2]/div[1]/div[2]/div/div/div/div/div/div[3]/div[3]/div[2]"
        district_xpath = f"//div[@class='programme-district-box' and .//div[text()='{district}']]"

        date_input_field_xpath = "/html/body/div[1]/div[2]/div[1]/div[2]/div/div/div/div/div/div[3]/div[3]/div[2]"

        _today = datetime.today()
        input_date = datetime(_today.year, month, day)

        if input_date.month > _today.month:
            date_xpath = f"//td[@class='next-month free-date' and .//span[normalize-space(text())={day}]]"
        elif input_date.day == _today.day:
            date_xpath = f"//td[@class='available today free-date' and .//span[normalize-space(text())={day}]]"
        else:
            date_xpath = f"//td[@class='available free-date' and .//span[normalize-space(text())={day}]]"

        search_button_xpath = "/html/body/div[1]/div[2]/div[1]/div[2]/div/div/div/div/div/div[3]/div[4]/div"


        ### Facility Home Page
        time.sleep(1)
        self._wait_located(locater=facility_button_xpath, _type="xpath")
        FacilityButtonElement = self.driver.find_element(By.XPATH, facility_button_xpath)
        self.driver.execute_script("arguments[0].click();", FacilityButtonElement)


        ### Select Sport Type
        time.sleep(1)
        self._wait_located(locater=sport_input_field_xpath, _type="xpath")
        SportInputFieldElement = self.driver.find_element(By.XPATH, sport_input_field_xpath)
        SportInputFieldElement.click()

        self._wait_located(locater=input_field_xpath, _type="xpath")
        InputFieldElement = self.driver.find_element(By.XPATH, input_field_xpath)
        InputFieldElement.send_keys(sport)

        self._wait_located(locater=sport_type_xpath, _type="xpath")
        SportTypeElement = self.driver.find_element(By.XPATH, sport_type_xpath)
        SportTypeElement.click()

        print("Select Sport Type")


        ### Select District
        time.sleep(1)
        self._wait_located(locater=district_input_field_xpath, _type="xpath")
        DistrictInputFieldElement = self.driver.find_element(By.XPATH, district_input_field_xpath)
        DistrictInputFieldElement.click()

        self._wait_located(locater=district_xpath, _type="xpath")
        DistrictElement = self.driver.find_element(By.XPATH, district_xpath)
        self.driver.execute_script("arguments[0].click();", DistrictElement)

        print("Select District")


        ### Select Date
        time.sleep(1)
        self._wait_located(locater=date_input_field_xpath, _type="xpath")
        DateInputFieldElement = self.driver.find_element(By.XPATH, date_input_field_xpath)
        self.driver.execute_script("arguments[0].click();", DateInputFieldElement)

        self._wait_located(locater=date_xpath, _type="xpath")
        DateElement = self.driver.find_element(By.XPATH, date_xpath)
        self.driver.execute_script("arguments[0].click();", DateElement)

        print("Select Date")

        ### Select Search Button
        SearchButtonElement = self.driver.find_element(By.XPATH, search_button_xpath)
        self.driver.execute_script("arguments[0].click();", SearchButtonElement)
        
        print("Click Search Button")


    def _classify_time(self, timeslot_str:str):
        """ Categorize timeslot_str into [Morning, Afternoon, Night] for redirection"""

        hour = int(re.search("\d+", timeslot_str).group())

        if "上午" in timeslot_str:
            return "Morning"
        
        elif "下午" in timeslot_str:
            if (1 <= hour < 6) or (hour == 12):
                return "Afternoon"
            elif 6 <= hour < 12:
                return "Night"

    def select_timeslot(self, timeslot_str:str, venuen_name:str, sport_item:str):
        """ Select the time and venuen """

        morning_button_xpath = "/html/body/div[1]/div[2]/div[4]/div[2]/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div/div/div[1]/div[1]"
        afternoon_button_xpath = "/html/body/div[1]/div[2]/div[4]/div[2]/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div/div/div[1]/div[2]"
        night_button_xpath = "/html/body/div[1]/div[2]/div[4]/div[2]/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div/div/div[1]/div[3]"

        continue_button_xpath = "//div[@data-v-8c95f640 and @class='xp-button xp-primary-d']//div[@tabindex='0' and @role='button']"
        cancel_button_xpath = "//div[@class='dialog-box' and @role='dialog']/div[@class='btn-box']/div[@class='cancel-button' and @role='button']"
        continue2_button_xpath = "/html/body/div/div[2]/div[4]/div/div/div/div[2]/div/div[2]/div[2]/div"

        checkbox1_xpath = "/html/body/div/div[2]/div[3]/div/div/div/div[1]/div[2]/div/div[1]/div/div[1]/img"
        checkbox2_xpath = "/html/body/div/div[2]/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div/div[1]/img"
        confirm_button_xpath = "/html/body/div/div[2]/div[3]/div/div/div/div[2]/div/div/div[1]/div[2]/div[2]/div"
        confirm_payment_xpath = "/html/body/div/div[2]/div[3]/div/div/div/div[3]/div[2]/div"

        time_type = self._classify_time(timeslot_str)

        if time_type == "Morning":
            time_type_xpath = morning_button_xpath
            print(f"Click {time_type}")

        elif time_type == "Afternoon":
            time_type_xpath = afternoon_button_xpath
            print(f"Click {time_type}")

        elif time_type == "Night":
            time_type_xpath = night_button_xpath
            print(f"Click {time_type}")


        timeslot_xpath = f"//h3[text()='{venuen_name}']/ancestor::div[contains(@class, 'chooseTime')]//div[contains(text(), '{sport_item}')]/following-sibling::div//div[contains(text(), '{timeslot_str}')]"
        
        # Click Morning / Afternoon / Night
        time.sleep(2)
        self._wait_located(locater=time_type_xpath, _type="xpath")
        TimeTypeElement = self.driver.find_element(By.XPATH, time_type_xpath)
        TimeTypeElement.click()

        # Click timeslot
        time.sleep(1)
        self._wait_located(locater=timeslot_xpath, _type="xpath")
        TimeslotElement = self.driver.find_element(By.XPATH, timeslot_xpath)
        self.driver.execute_script("arguments[0].click();", TimeslotElement)
        print(f"Click {timeslot_str}")
        

        time.sleep(1)
        self._wait_located(locater=continue_button_xpath, _type="xpath")
        ContinueButtonElement = self.driver.find_element(By.XPATH, continue_button_xpath)
        self.driver.execute_script("arguments[0].click();", ContinueButtonElement)

        time.sleep(1)
        self._wait_located(locater=cancel_button_xpath, _type="xpath")
        CancelButtonElement = self.driver.find_element(By.XPATH, cancel_button_xpath)
        self.driver.execute_script("arguments[0].click();", CancelButtonElement)

        time.sleep(1)
        self._wait_located(locater=continue2_button_xpath, _type="xpath")
        Continue2ButtonElement = self.driver.find_element(By.XPATH, continue2_button_xpath)
        self.driver.execute_script("arguments[0].click();", Continue2ButtonElement)

        # Click checkbox
        time.sleep(1)
        self._wait_located(locater=checkbox1_xpath, _type="xpath")
        Checkbox1Element = self.driver.find_element(By.XPATH, checkbox1_xpath)
        Checkbox1Element.click()
        
        # Click checkbox
        self._wait_located(locater=checkbox2_xpath, _type="xpath")
        Checkbox2Element = self.driver.find_element(By.XPATH, checkbox2_xpath)
        Checkbox2Element.click()

        # Continue button
        time.sleep(1)
        self._wait_located(locater=confirm_button_xpath, _type="xpath")
        ConfirmButtonElement = self.driver.find_element(By.XPATH, confirm_button_xpath)
        self.driver.execute_script("arguments[0].click();", ConfirmButtonElement)

        # Confirm payment
        time.sleep(1)
        self._wait_located(locater=confirm_payment_xpath, _type="xpath")
        ConfirmPaymentButtonElement = self.driver.find_element(By.XPATH, confirm_payment_xpath)
        self.driver.execute_script("arguments[0].click();", ConfirmPaymentButtonElement)
        print("Confirmed")

    def payment(self, cardholder:str, card_num:str, card_month:str, card_year:str, security_code:str):
        """ Select payment method and payment processing """

        mastercard_payment_xpath = "/html/body/div/div[2]/div[2]/div/div/div/div[2]/div[7]/div[2]/img"
        confirm_payment_xpath = "/html/body/div/div[2]/div[2]/div/div/div/div[4]/div[2]/div"

        iframe1_xpath = "/html/body/app-root/app-payment-detail-form/div/div/div/div/div[1]/div[2]/form/div[1]/app-payment-method-card-layout/div[2]/app-payment-method-card/div/div/div/div[1]/div/div[1]/div/iframe"
        iframe2_xpath = "/html/body/app-root/app-payment-detail-form/div/div/div/div/div[1]/div[2]/form/div[1]/app-payment-method-card-layout/div[2]/app-payment-method-card/div/div/div/div[2]/div/div[1]/div[1]/iframe"
        iframe3_xpath = "/html/body/app-root/app-payment-detail-form/div/div/div/div/div[1]/div[2]/form/div[1]/app-payment-method-card-layout/div[2]/app-payment-method-card/div/div/div/div[3]/div[1]/div[1]/div/span[1]/div/iframe"
        iframe4_xpath = "/html/body/app-root/app-payment-detail-form/div/div/div/div/div[1]/div[2]/form/div[1]/app-payment-method-card-layout/div[2]/app-payment-method-card/div/div/div/div[3]/div[1]/div[1]/div/span[2]/div/iframe"
        iframe5_xpath = "/html/body/app-root/app-payment-detail-form/div/div/div/div/div[1]/div[2]/form/div[1]/app-payment-method-card-layout/div[2]/app-payment-method-card/div/div/div/div[3]/div[2]/div[1]/div[1]/iframe"

        payment_button_xpath = "/html/body/app-root/app-payment-detail-form/div/div/div/div/div[1]/div[2]/form/div[2]/div/app-pay-button/app-button/div/button"


        # Mastercard payment
        time.sleep(1)
        self._wait_located(locater=mastercard_payment_xpath, _type="xpath")
        MastercardPaymentButtonElement = self.driver.find_element(By.XPATH, mastercard_payment_xpath)
        MastercardPaymentButtonElement.click()
        print("Select Mastercard")

        time.sleep(1)
        self._wait_located(locater=confirm_payment_xpath, _type="xpath")
        ConfirmPaymentButtonElement = self.driver.find_element(By.XPATH, confirm_payment_xpath)
        self.driver.execute_script("arguments[0].click();", ConfirmPaymentButtonElement)


        # Switch to the new payment tab
        time.sleep(10)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        time.sleep(1)

        print("input credit card info")


        # Card holder field
        iframe1_element = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, iframe1_xpath)))

        self.driver.switch_to.frame(iframe1_element) # Switch to the iframe

        cardholder_xpath = "//input[@type='text' and @id='nameOnCard']"
        self._wait_located(locater=cardholder_xpath, _type="xpath")
        self.driver.find_element(By.XPATH, cardholder_xpath).send_keys(cardholder)
        print("Input cardholder")

        self.driver.switch_to.default_content() # Switch back


        # Card number field
        iframe2_element = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, iframe2_xpath)))

        self.driver.switch_to.frame(iframe2_element) # Switch to the iframe

        card_number_xpath = "//input[@type='tel' and @id='number']"
        self.driver.find_element(By.XPATH, card_number_xpath).send_keys(card_num)
        print("Input card number")

        self.driver.switch_to.default_content()


        # Card expiry month
        iframe3_xpath = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, iframe3_xpath)))

        self.driver.switch_to.frame(iframe3_xpath) # Switch to the iframe

        expiry_month_xpath = "//input[@type='tel' and @id='expiryMonth']"
        self.driver.find_element(By.XPATH, expiry_month_xpath).send_keys(card_month)
        print("Input expiry month")

        self.driver.switch_to.default_content()


        # Card expiry year
        iframe4_xpath = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, iframe4_xpath)))

        self.driver.switch_to.frame(iframe4_xpath) # Switch to the iframe

        expiry_year_xpath = "//input[@type='tel' and @id='expiryYear']"
        self.driver.find_element(By.XPATH, expiry_year_xpath).send_keys(card_year)
        print("Input expiry year")

        self.driver.switch_to.default_content()


        # Card security code
        iframe5_xpath = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, iframe5_xpath)))

        self.driver.switch_to.frame(iframe5_xpath) # Switch to the iframe

        security_code_xpath = "//input[@type='tel' and @id='securityCode']"
        self.driver.find_element(By.XPATH, security_code_xpath).send_keys(security_code)
        print("Input security code")

        self.driver.switch_to.default_content()


        # Payment button
        time.sleep(1)
        self._wait_located(locater=payment_button_xpath, _type="xpath")
        PaymentButtonElement = self.driver.find_element(By.XPATH, payment_button_xpath)
        #self.driver.execute_script("arguments[0].click();", PaymentButtonElement)

        print("Click Payment Button")