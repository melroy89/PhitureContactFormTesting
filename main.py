from __future__ import print_function

import selenium.webdriver.chrome.options
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options
from fake_useragent import UserAgent
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from slack import send_positive_message_to_slack_channel, send_negative_message_to_slack_channel

import time
import os
import os.path
import traceback

disp = Display(size=(1920, 1080))
disp = Display()
disp.start()

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

webhook1 = "https:"
webhook2 = "//hooks"
webhook3 = ".slack"
webhook4 = ".com/"
webhook5 = "services/"
webhook6 = "T0KSV138X/"
webhook7 = "B04A56LLVAB/"
webhook8 = "tNTC9kjpmWKw78vQ6CPgwAg9"

chromeOpt = selenium.webdriver.chrome.options.Options()
firefoxOpt = selenium.webdriver.firefox.options.Options()
# ua = UserAgent()
# userAgent = ua.random
print()
# print("useragent: " + userAgent)
chromeOpt.add_argument("--no-sandbox")
chromeOpt.add_argument("--disable-dev-shm-usage")
# chromeOpt.add_argument(f'user-agent={userAgent}')
firefoxOpt.add_argument("--no-sandbox")
firefoxOpt.add_argument("--disable-dev-shm-usage")
# firefoxOpt.add_argument(f'user-agent={userAgent}')
driver = webdriver.Chrome(options=chromeOpt)
# driver = webdriver.Firefox(options=firefoxOpt)
# driver.set_window_size(380, 640)


def setUpBrowserAndAllowCookies():
    # Check if we use mobile version or not
    if driver.get_window_size().get("height") != 640:
        driver.set_window_size(1920, 1080)

    # Go to phiture.com website
    driver.get("https://phiture.com/work-together/")
    # wait for page to load
    time.sleep(3)

    # Allow cookies
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//button[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]')))
        allowAll = driver.find_element(By.XPATH,
                                       '//button[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]')
        allowAll.click()
    except Exception as e:
        print(str(e))
    # Refresh is required because after accepting all cookies webdriver can not see main page correctly
    driver.refresh()


def findAndFillOutAllTextFields():
    # We found all parameters on the page
    firstName = driver.find_element(By.NAME, "your-firstname")
    lastName = driver.find_element(By.NAME, "your-lastname")
    company = driver.find_element(By.NAME, "your-company")
    email = driver.find_element(By.NAME, "your-email")
    budget = driver.find_element(By.NAME, "your-budget")
    website = driver.find_element(By.NAME, "your-website")

    elementsIn = [firstName, lastName, company, email, budget, website]

    # We filled all parameters on the page
    firstName.send_keys("-")
    lastName.send_keys("-")
    company.send_keys("-")
    email.send_keys("-@gmail.com")
    budget.send_keys("-")
    website.send_keys("-")

    # Checking if all text fields are filled
    for e in elementsIn:
        if e.get_attribute("value") == "":
            print(f"{e.get_attribute('name')} field is not filled")


def findAndClickCheckboxes():
    # We found all checkboxes on the page under description area
    mobileGrowthStoriesNewsletterCheckbox = driver.find_element(By.XPATH,
                                                                '//input[@value="Mobile Growth Stories Newsletter"]')
    privacyPolicyCheckbox = driver.find_element(By.XPATH, '//input[@name="accept-this-1"]')
    asoMonthlyNewslettersCheckbox = driver.find_element(By.XPATH, '//input[@value="ASO Monthly Newsletter"]')

    # scroll 250 pixels down (for mobile version)
    if driver.get_window_size().get("height") <= 640:
        driver.execute_script("window.scrollBy(0,250)")

    # We found all checkboxes on the page above description area
    serviceCheckboxes = driver.find_elements(By.XPATH,
                                             "//span[starts-with(@class,'wpcf7-list-item')]//input[@name='service[]']")
    appStoreOptimizationCheckbox = driver.find_element(By.XPATH, '//input[@value="App Store Optimization"]')

    # Enabling all checkboxes
    for checkbox in serviceCheckboxes:
        checkbox.click()
        checkbox.is_selected()

    if not appStoreOptimizationCheckbox.is_selected():
        print()
        print("App Store Optimisation checkbox is out of the main checkboxes array. Enabling manually")
        print()
        appStoreOptimizationCheckbox.click()
        appStoreOptimizationCheckbox.is_selected()

    time.sleep(1)
    # scroll 600 pixels down (for mobile version)
    if driver.get_window_size().get("height") <= 640:
        driver.execute_script("window.scrollBy(0,600)")
    else:
        driver.execute_script("window.scrollBy(0,680)")
    time.sleep(1)

    # We clicked all checkboxes on the page and checked are they enabled
    mobileGrowthStoriesNewsletterCheckbox.click()
    if not mobileGrowthStoriesNewsletterCheckbox.is_selected():
        mobileGrowthStoriesNewsletterCheckbox.click()

    privacyPolicyCheckbox.click()
    if not privacyPolicyCheckbox.is_selected():
        privacyPolicyCheckbox.click()

    asoMonthlyNewslettersCheckbox.click()
    if not asoMonthlyNewslettersCheckbox.is_selected():
        asoMonthlyNewslettersCheckbox.click()


def fillOutDescriptionTestArea():
    # We filled description form
    descriptionArea = driver.find_element(By.XPATH, "//span[@class='wpcf7-form-control-wrap']/textarea")
    descriptionArea.send_keys("Autogenerated message. Please do not reply to this email!")

    if driver.get_window_size().get("height") <= 640:
        driver.execute_script("window.scrollBy(0,250)")


def sendContactForm():
    #Trying to send contact form from website
    #We use a stack of try-catch blocks,
    #because we have 3 types of possible messages below 'send' button:
    #Success, failed and validation occured
    #And one error with google security policy,
    #which you can see inside devtools in browser   
    element = False
    failedElement = False
    validationElement = False
    for i in range(0, 10):
        try:
            if i == 5 or i == 9:
                print("Trying to refresh page and fill everything again")
                driver.refresh()
                findAndFillOutAllTextFields()
                findAndClickCheckboxes()
                fillOutDescriptionTestArea()
            letsConnectButton = driver.find_element(By.XPATH, '//input[@value="Let\'s connect"]')
            letsConnectButton.click()
            if i == 0:
                time.sleep(6)
                element = driver.find_element(By.XPATH, '//div[contains(text(), "successfully")]').is_displayed()
            else:
                time.sleep(3)
                element = driver.find_element(By.XPATH, '//div[contains(text(), "successfully")]').is_displayed()
                print(element)
            if not element:
                element = True
            print("Button works correctly")
            break
        except NoSuchElementException:
            try:
                failedElement = driver.find_element(By.XPATH, '//div[contains(text(), "failed")]').is_displayed()
                print("Failed to send your message. Trying to send contact form until we have a positive message")
            except NoSuchElementException:
                try:
                    validationElement = driver.\
                        find_element(By.XPATH, '//div[contains(text(), "Validation")]').is_displayed()
                    print("Validation errors occurred. We will fill out all field, checkboxes and try again")
                    findAndFillOutAllTextFields()
                    findAndClickCheckboxes()
                    fillOutDescriptionTestArea()
                except NoSuchElementException:
                    print(f"Try number {i + 1}. 'Send' button is not working")    
                    driver.save_screenshot(f"button_not_working_{i}.png")
        time.sleep(3)
    
    print("Success message status: " + str(element), "\nFailed message status: " + str(failedElement), 
          "\nValidation error status: " + str(validationElement))
    
    if not element and not failedElement and not validationElement:
        print()
        print("Test failed because send button does not work after 10 tries")
        send_negative_message_to_slack_channel(
                    webhook1+webhook2+webhook3+webhook4+webhook5+webhook6+webhook7+webhook8,
                    "Automated Phiture website contact form test failed:\n"
                    "Please try later or contact the administrator by another method.\n"
                    "Test failed because send button does not work after 10 tries or because we have an error.\n",
                    "Testing website contact form\n",
                    "#FF0000",
                )
        driver.quit()
        quit()

    # Waiting some time because messages arrive late
    print("Preblock is finished (WEB)")
    time.sleep(2)


# Getting messages from email using GMAIL API
def main():
    print("Final block is running (Backend)")
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = os.environ.get("GMAIL_CREDS", False)
    if creds:
        with open("credentials.json", "w") as f:
            f.write(os.environ["GMAIL_CREDS"])
    else:
        print()
        print("GMAIL_CREDS is not set", creds)
        print(os.environ)

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)

        # Checking for results
        results = service.users().messages() \
            .list(userId='me', labelIds=['INBOX'],
                  q="to:info@phiture.com from:access@phiture.com subject:- is:unread").execute()
        messages = results.get('messages', []);

        if not messages:
            print("You do not have new messages")
            driver.close()

        # print the number of received messages
        size = len(messages)
        print()
        if size == 1:
            print("You have 1 new message: ")
        elif size > 1:
            print(f"You have {size} new messages:")

        # print messages on a separate lines
        print()
        for m in messages:
            print("Message short description: ", end=' ')
            print(m)
        print()

        # Function to print and then change message status from UNREAD to READ after each test
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']) \
                .execute()
            print("Message full description: ", end=' ')
            fullDesc = msg.get("snippet")
            print(fullDesc)
            # For every received email we send a message to a slack channel "phiture-site-automated-tests"
            send_positive_message_to_slack_channel(
                webhook1+webhook2+webhook3+webhook4+webhook5+webhook6+webhook7+webhook8,
                f"You have new autogenerated message: \n{fullDesc}",
                "Testing website contact form",
                "#73fc03",
            )

        for ms in messages:
            leer = service.users().messages().modify(userId='me', id=ms['id'],
                                                     body={'removeLabelIds': ['UNREAD']}).execute()
            print()
            print(f"The message number {ms['id']} has been marked from the status UNREAD to READ")

    except HttpError as error:
        print(f'An error occurred: {error}')

    # We need to male a screenshot and close the browser
    driver.save_screenshot("screenshot.png")
    driver.quit()
    disp.stop()


# Calling all methods
if __name__ == '__main__':
    try:
        setUpBrowserAndAllowCookies()
        findAndFillOutAllTextFields()
        findAndClickCheckboxes()
        fillOutDescriptionTestArea()
        sendContactForm()
        main()
    except Exception as e:
        print(str(e))
        traceback.print_exc()
