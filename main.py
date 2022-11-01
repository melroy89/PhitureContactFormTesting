from __future__ import print_function
from pyvirtualdisplay import Display

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import random
import time
import os.path

from slack import send_message_to_slack_channel

# disp=Display(size=(1920, 1080))
# disp = Display()
# disp.start()

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

opt = Options()
ua = UserAgent()
userAgent = ua.random
print()
print("useragent: " + userAgent)
opt.add_argument("--no-sandbox")
opt.add_argument("--disable-dev-shm-usage")
opt.add_argument(f'user-agent={userAgent}')
driver = webdriver.Chrome(options=opt)

hex_number = random.randint(1118481, 16777215)
hex_number = str(hex(hex_number))
hex_number = '#' + hex_number[2:]


def findAndFillOutAllTextFields():
    # Check if we use mobile version or not
    if driver.get_window_size().get("height") != 640:
        driver.maximize_window()

    # Go to phiture.com website
    driver.get("https://phiture.com/work-together/")

    # Allow cookies
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//a[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]')))
    allowAll = driver.find_element(By.XPATH, '//a[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]')
    allowAll.click()

    # Refresh is required because after accepting all cookies webdriver can not see main page correctly
    driver.refresh()

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
    checkHereCheckbox = driver.find_element(By.XPATH, '//input[@name="accept-this-1"]')
    asoMonthlyNewslettersCheckbox = driver.find_element(By.XPATH, '//input[@value="ASO Monthly Newsletter"]')

    # scroll 250 pixels down (for mobile version)
    if driver.get_window_size().get("height") <= 640:
        driver.execute_script("window.scrollBy(0,250)")
    # We found all checkboxes on the page above description area
    serviceCheckboxes = driver.find_elements(By.XPATH,
                                             "//span[starts-with(@class,'wpcf7-list-item')]//input[@name='service[]']")
    appStoreOptimizationCheckbox = driver.find_element(By.XPATH, '//input[@value="App Store Optimization"]')
    appStoreOptimizationCheckbox.click()
    appStoreOptimizationCheckbox.is_enabled()

    for checkbox in serviceCheckboxes:
        checkbox.click()
        checkbox.is_enabled()

    # scroll 600 pixels down (for mobile version)
    if driver.get_window_size().get("height") <= 640:
        driver.execute_script("window.scrollBy(0,600)")

    # We clicked all checkboxes on the page and checked are they enabled
    mobileGrowthStoriesNewsletterCheckbox.click()
    mobileGrowthStoriesNewsletterCheckbox.is_enabled()
    checkHereCheckbox.click()
    checkHereCheckbox.is_enabled()
    asoMonthlyNewslettersCheckbox.click()
    asoMonthlyNewslettersCheckbox.is_enabled()


def fillOutDescriptionTestArea():
    # We filled description form
    descriptionArea = driver.find_element(By.XPATH, "//span[@class='wpcf7-form-control-wrap']/textarea")
    descriptionArea.send_keys("Autogenerated message. Please do not reply to this email!")

    # Click the button "Lets connect" to send contact form message
    letsConnectButton = driver.find_element(By.XPATH, '//input[@value="Let\'s connect"]')
    letsConnectButton.click()

    # If we got an error, we terminate the script and close the driver
    if driver.find_element(By.XPATH, '//div[contains(@class, "response-output")]').is_displayed():
        print("Failed to send your message. Please try later or contact the administrator by another method.")
        print("It happens because of we are using selenium and recaptcha security system always can detect it.")
        print("That's why we have to use random user-agent generator.")
        driver.close()
        quit()

    # Waiting some time because messages arrive late
    time.sleep(2)


# Getting messages from email using GMAIL API
def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
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
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            print("Message full description: ", end=' ')
            print(msg)
        print()

        for ms in messages:
            service.users().messages().modify(userId='me', id=ms['id'],
                                              body={'removeLabelIds': ['UNREAD']}).execute()
            print(f"The message number {ms['id']} has been marked from the status UNREAD to READ")

            # For every received email we send a message to a slack channel "phiture-site-automated-tests"
            send_message_to_slack_channel(
                "https://hooks.slack.com/services/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",
                f"You have new autogenerated message with id{ms['id']}",
                "FROM: Iskandar Khanbekov",
                "Testing website contact form",
                hex_number
            )
    except HttpError as error:
        print(f'An error occurred: {error}')
    # We need to male a screenshot and close the browser
    # driver.save_screenshot("screenshot.png")
    # driver.close()
    # disp.stop()


# Calling all methods
if __name__ == '__main__':
    findAndFillOutAllTextFields()
    findAndClickCheckboxes()
    fillOutDescriptionTestArea()
    time.sleep(5)
    main()
    driver.close()