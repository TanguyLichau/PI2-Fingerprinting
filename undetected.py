import undetected_chromedriver as uc
import time
options = uc.ChromeOptions()
options.add_argument("--headless=new")
driver = uc.Chrome(options=options)
time.sleep(3)
driver.get('https://nowsecure.nl')
driver.save_screenshot('nowsecure.png')