import argparse
import random
from curl_cffi import requests

BROWSER_LIST = ["chrome100", "chrome101", "chrome104", "chrome107", "chrome110"]

def isPageBlocked(text):
  indicators = [
      "checking your browser",
      "please turn JavaScript on",
      "enable JavaScript and cookies",
      "DDoS protection by Cloudflare",
      "Ray ID",
      "captcha",
      "challenge",
      "Incapsula incident ID",
      "Website is protected against DDoS attacks",
      "Access Denied",
      "Access to this page has been denied",
      "Checking your browser before accessing",
      "Powered by DataDome"
  ]

  if any(indicator.lower() in text.lower() for indicator in indicators):
    return True
  
  if "document.createElement(\"div\")" in text or "g-recaptcha" in text:
    return True

  return False



if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--url", type=str, help="url to request")
  parser.add_argument("--urls", type=str, help="filename for list of urls")
  parser.add_argument("--proxies", type=str, help="filename for list of proxies")
  args = parser.parse_args()

  if not args.url and not args.urls:
    print("No target url")
    exit()
  URL_LIST = []
  PROXIES = []
  successful_requests = 0
  blocked_requests = 0

  # Ajout liste d'urls
  if args.urls:
    try:
      txt_file = open(args.urls, "r")
      content = txt_file.read()
      URL_LIST = content.split("\n")
    except Exception as e:
      print("Error while parsing txt file : ", e)
      exit()
    txt_file.close()
  else:
    URL_LIST.append(args.url)

  # Ajout list de proxies
  if args.proxies:
    try:
      txt_file = open(args.proxies, "r")
      content = txt_file.read()
      PROXIES = content.split("\n")
    except Exception as e:
      print("Error while parsing txt file : ", e)
      exit()
    txt_file.close()

  for url in URL_LIST:
    
    # Requete simple
    r = requests.get(url)
    #print(r.text)
    if r.status_code == 200 and not isPageBlocked(r.text):
      print("Simple request worked")
      successful_requests += 1
      continue
    print("Simple request failed")

    # Requete avec curl_cffi
    r = requests.get(url, impersonate=random.choice(BROWSER_LIST))
    if r.status_code == 200 and not isPageBlocked(r.text):
      print("Simple cffi request worked")
      successful_requests += 1
      continue
    print("Simple cffi request failed")

    if not args.proxies:
      print("No proxy file provided")
      blocked_requests += 1
      continue

    # Requete simple avec proxy
    r = requests.get(url, proxies={"https": random.choice(PROXIES)})
    if r.status_code == 200 and not isPageBlocked(r.text):
      print("Simple request with proxy worked")
      successful_requests += 1
      continue
    print("Simple request with proxy failed")  

    # Requete cffi avec proxy
    r = requests.get(url, impersonate=random.choice(BROWSER_LIST), proxies={"https": random.choice(PROXIES)})
    if r.status_code == 200 and not isPageBlocked(r.text):
      print("Simple cffi request with proxy worked")
      successful_requests += 1
      continue
    else:
      blocked_requests += 1
    print("Simple cffi request with proxy failed")
  print("Statistics:")
  print(f"Total requests: {successful_requests + blocked_requests}")
  print(f"Successful requests: {successful_requests}")
  print(f"Blocked requests: {blocked_requests}")