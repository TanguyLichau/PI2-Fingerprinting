import argparse
import random
from curl_cffi import requests as r_cffi
import requests as r_basic

BROWSER_LIST = ["chrome100", "chrome101", "chrome104", "chrome107", "chrome110"]

def isPageBlocked(text):
  indicators = [
      "checking your browser",
      "DDoS protection by Cloudflare",
      "Incapsula incident ID",
      "Website is protected against DDoS attacks",
      "Access Denied",
      "Access to this page has been denied",
      "Checking your browser before accessing",
      "Powered by DataDome",
      "waf"
  ]

  if any(indicator.lower() in text.lower() for indicator in indicators):
    return True
  return False

def record_result(file, result):
  with open(file, "a") as result_file:
    result_file.write(result)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--url", type=str, help="url to request")
  parser.add_argument("--urls", type=str, help="filename for a list of urls")
  args = parser.parse_args()

  if not args.url and not args.urls:
    print("No target url")
    exit()

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

  for url in URL_LIST:
    result_string = f"{url} :"

    # Requete simple
    r = r_basic.get(url)
    print(r.text)
    if r.status_code == 200 and not isPageBlocked(r.text):
      result_string += " 1" 
      successful_requests += 1
    else:
      result_string += " 0" 
      blocked_requests += 1
    
    # Requete simple + proxy faible
    r = r_basic.get(url, proxies={"http": "", "https": ""})
    if r.status_code == 200 and not isPageBlocked(r.text):
      result_string += " 1" 
      successful_requests += 1
    else:
      result_string += " 0" 
      blocked_requests += 1

    # Requete simple + proxy fort
    r = r_basic.get(url, proxies={"http": "", "https": ""})
    if r.status_code == 200 and not isPageBlocked(r.text):
      result_string += " 1" 
      successful_requests += 1
    else:
      result_string += " 0" 
      blocked_requests += 1
   
    # Requete avec curl_cffi
    r = r_cffi.get(url, impersonate=random.choice(BROWSER_LIST))
    print(r.text)
    if r.status_code == 200 and not isPageBlocked(r.text):
      result_string += " 1" 
      successful_requests += 1
    else:
      result_string += " 0" 
      blocked_requests += 1
    
    # Requete avec curl_cffi + proxy faible
    r = r_cffi.get(url, impersonate=random.choice(BROWSER_LIST), proxies={"http": "", "https": ""})
    if r.status_code == 200 and not isPageBlocked(r.text):
      result_string += " 1" 
      successful_requests += 1
    else:
      result_string += " 0" 
      blocked_requests += 1

    # Requete avec curl_cffi + proxy fort
    r = r_cffi.get(url, impersonate=random.choice(BROWSER_LIST), proxies={"http": "", "https": ""})
    if r.status_code == 200 and not isPageBlocked(r.text):
      result_string += " 1" 
      successful_requests += 1
    else:
      result_string += " 0" 
      blocked_requests += 1

    record_result(result_file_name, f"{result_string}\n")

  print("Statistics:")
  print(f"Total requests: {successful_requests + blocked_requests}")
  print(f"Successful requests: {successful_requests}")
  print(f"Blocked requests: {blocked_requests}")
