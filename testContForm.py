import driver as driver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

# Getting a WebDriver (3 options: chrome, firefox, mobile version of any browser)
driver = webdriver.Chrome()
# driver = webdriver.Firefox()                                              #for Firefox testing
driver.set_window_size(360, 640)                                          #for mobile version of Chrome or Firefox

# Check if we use mobile version or not
if driver.get_window_size().get("height") != 640:
    driver.maximize_window()

# Go to phiture.com website
driver.get("https://phiture.com/work-together/")

# Allow cookies
allowAll = driver.find_element(By.XPATH, '//a[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]')
allowAll.click()

# Refresh is needed because after accepting all cookies webdriver can not see main page correctly
driver.refresh()

# We found all parameters on the page
firstName = driver.find_element(By.NAME, "your-firstname")
lastName = driver.find_element(By.NAME, "your-lastname")
company = driver.find_element(By.NAME, "your-company")
email = driver.find_element(By.NAME, "your-email")
budget = driver.find_element(By.NAME, "your-budget")
website = driver.find_element(By.NAME, "your-website")

# We filled all parameters on the page
firstName.send_keys("Johnny")
lastName.send_keys("Fisherman")
company.send_keys("Google")
email.send_keys("1234google@gmail.com")
budget.send_keys("1000000")
website.send_keys("google.com")

# We found all checkboxes on the page under description area
mobileGrowthStoriesNewsletterCheckbox = driver.find_element(By.XPATH, '//input[@value="Mobile Growth Stories Newsletter"]')
checkHereCheckbox = driver.find_element(By.XPATH, '//input[@name="accept-this-1"]')
asoMonthlyNewslettersCheckbox = driver.find_element(By.XPATH, '//input[@value="ASO Monthly Newsletter"]')

# scroll 250 pixels down

if driver.get_window_size().get("height") <= 640:
    driver.execute_script("window.scrollBy(0,250)")

# We found all checkboxes on the page above description area
serviceCheckboxes = driver.find_elements(By.XPATH, "//span[starts-with(@class,'wpcf7-list-item')]//input[@name='service[]']")
for checkbox in serviceCheckboxes:
    checkbox.click()
    checkbox.is_enabled()

# scroll 400 pixels down
driver.execute_script("window.scrollBy(0,400)")

# We clicked all checkboxes on the page and checked if they are selected
mobileGrowthStoriesNewsletterCheckbox.click()
mobileGrowthStoriesNewsletterCheckbox.is_enabled()
checkHereCheckbox.click()
checkHereCheckbox.is_enabled()
asoMonthlyNewslettersCheckbox.click()
asoMonthlyNewslettersCheckbox.is_enabled()

# We filled description form
descriptionArea = driver.find_element(By.XPATH, "//span[@class='wpcf7-form-control-wrap']/textarea")
descriptionArea.send_keys("We are Google. We wanna deal with you.")

# driver.find_element(By.XPATH, '//input[@value="Let\'s connect"]')

# We need to close browser
driver.close()