import argparse
import random
import os
from curl_cffi import requests as r_cffi
import requests as r_basic
from dotenv import load_dotenv
import time
import urllib3

BROWSER_LIST = ["chrome100", "chrome101", "chrome104", "chrome107", "chrome110"]

def isPageBlocked(text):
  if len(text) < 10000:
    return True
  indicators = [
      "checking your browser",
      "DDoS protection by Cloudflare",
      "Incapsula incident ID",
      "Website is protected against DDoS attacks",
      "Access Denied",
      "Access to this page has been denied",
      "Checking your browser before accessing",
      "Powered by DataDome",
      "BotDetect",
      "SoftBlock",
      "HardBlock",
      "recaptcha-script",
      "recaptcha_script",
      "arkose-challenge",
      "arkose_challenge",
      "arkose"
  ]

  if any(indicator.lower() in text.lower() for indicator in indicators):
    return True
  return False

def record_result(file, result):
  with open(file, "a") as result_file:
    result_file.write(result)

def write_logs(filename, result):
  with open(filename, "w", encoding="utf-8") as result_file:
    result_file.write(result)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--url", type=str, help="url to request")
  parser.add_argument("--urls", type=str, help="filename for a list of urls")
  args = parser.parse_args()

  if not args.url and not args.urls:
    print("No target url")
    exit()

  urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
  load_dotenv()
  URL_LIST = []
  PROXIES = []
  result_file_name = "request_results.txt"
  successful_requests = 0
  blocked_requests = 0

  if args.urls:
      try:
          with open(args.urls, "r") as txt_file:
              content = txt_file.read()
              URL_LIST = content.split("\n")
      except Exception as e:
          print("Error while parsing txt file : ", e)
          exit()
  else:
    URL_LIST.append(args.url)
  
  print("Starting the requests\n")
  for url in URL_LIST:
    result_string = f"{url} :"
    
    # Requete simple
    try:
      r = r_basic.get(url)
      print(1)
      write_logs("./logs/simple.txt", r.text)
      if r.status_code == 200 and not isPageBlocked(r.text):
        result_string += " 1" 
        successful_requests += 1
      else:
        result_string += " 0" 
        blocked_requests += 1
    except Exception as e:
      print(e)
      result_string += " X" 
      blocked_requests += 1
    
    # Requete simple + proxy faible
    try:
      r = r_basic.get(url, proxies={"http": os.getenv("WEAK_PROXY_URL"), "https": os.getenv("WEAK_PROXY_URL")})
      write_logs("./logs/simple_weak_proxy.txt", r.text)
      print(2)
      if r.status_code == 200 and not isPageBlocked(r.text):
        result_string += " 1" 
        successful_requests += 1
      else:
        result_string += " 0" 
        blocked_requests += 1
    except Exception as e:
      print(e)
      result_string += " X" 
      blocked_requests += 1
    
    # Requete simple + proxy fort
    try:
      r = r_basic.get(url, proxies={"http": os.getenv("STRONG_PROXY_URL"), "https": os.getenv("STRONG_PROXY_URL")}, verify=False)
      write_logs("./logs/simple_strong_proxy.txt", r.text)
      print(3)
      if r.status_code == 200 and not isPageBlocked(r.text):
        result_string += " 1" 
        successful_requests += 1
      else:
        result_string += " 0" 
        blocked_requests += 1
    except Exception as e:
      print(e)
      result_string += " X" 
      blocked_requests += 1
    
    # Requete avec curl_cffi
    try:
      r = r_cffi.get(url, impersonate=random.choice(BROWSER_LIST))
      print(4)
      write_logs("./logs/cffi.txt", r.text)
      if r.status_code == 200 and not isPageBlocked(r.text):
        result_string += " 1" 
        successful_requests += 1
      else:
        result_string += " 0" 
        blocked_requests += 1
    except Exception as e:
      print(e)
      result_string += " X" 
      blocked_requests += 1
    
    # Requete avec curl_cffi + proxy faible
    try:
      r = r_cffi.get(url, impersonate=random.choice(BROWSER_LIST), proxies={"http": os.getenv("WEAK_PROXY_URL"), "https": os.getenv("WEAK_PROXY_URL")})
      write_logs("./logs/cffi_weak_proxy.txt", r.text)
      print(5)
      if r.status_code == 200 and not isPageBlocked(r.text):
        result_string += " 1" 
        successful_requests += 1
      else:
        result_string += " 0" 
        blocked_requests += 1
    except Exception as e:
      print(e)
      result_string += " X" 
      blocked_requests += 1
    
    # Requete avec curl_cffi + proxy fort
    try:
      r = r_cffi.get(url, impersonate=random.choice(BROWSER_LIST), proxies={"http": os.getenv("STRONG_PROXY_URL"), "https": os.getenv("STRONG_PROXY_URL")}, verify=False)
      write_logs("./logs/cffi_strong_proxy.txt", r.text)
      print(6)
      if r.status_code == 200 and not isPageBlocked(r.text):
        result_string += " 1" 
        successful_requests += 1
      else:
        result_string += " 0" 
        blocked_requests += 1
    except Exception as e:
      print(e)
      result_string += " X" 
      blocked_requests += 1
    
    print(f"{url} done")
    record_result(result_file_name, f"{result_string}\n")
    time.sleep(5)
    
  print("\nStatistics:")
  record_result(result_file_name, "\nStatistics:\n")
  print(f"Total requests: {successful_requests + blocked_requests}")
  record_result(result_file_name, f"Total requests: {successful_requests + blocked_requests}\n")
  print(f"Successful requests: {successful_requests}")
  record_result(result_file_name, f"Successful requests: {successful_requests}\n")
  print(f"Blocked requests: {blocked_requests}")
  record_result(result_file_name, f"Blocked requests: {blocked_requests}\n")
