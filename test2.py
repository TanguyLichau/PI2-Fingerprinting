import ssl
import time
import json
import requests
from urllib3.poolmanager import PoolManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from requests.adapters import HTTPAdapter
import argparse
from urllib3.util.ssl_ import create_urllib3_context
from selenium import webdriver
from selenium_stealth import stealth

class CustomHTTPAdapter(HTTPAdapter):
    def __init__(self, ssl_options=0, **kwargs):
        self.ssl_options = ssl_options
        super(CustomHTTPAdapter, self).__init__(**kwargs)

    def init_poolmanager(self, *pool_args, **pool_kwargs):
        ctx = create_urllib3_context(ciphers=CIPHERS, cert_reqs=ssl.CERT_REQUIRED, options=self.ssl_options)
        self.poolmanager = PoolManager(*pool_args, ssl_context=ctx, **pool_kwargs)


CIPHERS = 'ECDHE-RSA-AES256-CBC-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384'
headers = {}

parser = argparse.ArgumentParser()
parser.add_argument("--url", type=str, help="url to request")
parser.add_argument("--proxy", type=str, help="proxy address")
parser.add_argument("--tls", type=str, help="tls version wanted (v1.3 by default)")
parser.add_argument("--headers", type=str, help="pass json file to add headers")
parser.add_argument("--selenium", type=str, help="use selenium or not")
args = parser.parse_args()

if not args.url:
    print("No target url")
    exit()

proxies, tls_version = None, None
if args.proxy:
    proxies = {'https': args.proxy}

if args.tls == '1.1':
    tls_version = ssl.OP_NO_TLSv1_3 | ssl.OP_NO_TLSv1_2
elif args.tls == '1.2':
    tls_version = ssl.OP_NO_TLSv1_3 | ssl.OP_NO_TLSv1_1

if args.headers:
    try:
        with open(args.headers, 'r') as json_file:
            json_headers = json.load(json_file)
        headers.update(json_headers)
    except FileNotFoundError:
        print("JSON file not found.")
        exit()
    except json.JSONDecodeError:
        print("Error decoding JSON file.")
        exit()

if args.selenium == "true" or args.selenium =="True":
  options = webdriver.ChromeOptions()
  options.add_argument("start-maximized")
  options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
  options.add_experimental_option('useAutomationExtension', False)
  options.add_argument('--disable-blink-features=AutomationControlled')
  options.add_argument('--no-sandbox')

  options.add_argument("user-data-dir=C:\\Users\\Tanguy\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
  #run in headless mode
  #options.add_argument("--headless")
  '''
  # disable extensions
  options.add_argument('--disable-extensions')
  
  # disable shared memory usage
  options.add_argument('--disable-dev-shm-usage')
  '''
  driver = webdriver.Chrome(options=options)
  driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: function() {return undefined}})")
  stealth(driver,
          languages=["fr-FR","fr","en-US", "en"],
          vendor="Google Inc.",
          platform="Win32",
          webgl_vendor="Google Inc. (NVIDIA)",
          renderer="ANGLE (NVIDIA, NVIDIA GeForce RTX 2070 SUPER (0x00001E84) Direct3D11 vs_5_0 ps_5_0, D3D11)",
          fix_hairline=True,
        )
  driver.get(args.url)
  #driver.save_screenshot(f"C:/Users/Tanguy/Desktop/PI2/Cli/Screenshots/{args.url}.png")
  #driver.save_screenshot("test.png")
  time.sleep(20)
  driver.quit()
  
else:
  session = requests.Session()

  session.mount("https://", CustomHTTPAdapter(tls_version))
  response = session.get(args.url, headers=headers, proxies=proxies, verify=False)

  print(response.status_code)
  print(response.text)
