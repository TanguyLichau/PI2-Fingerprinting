import argparse
import json
import random
from curl_cffi import requests

BROWSER_LIST = ["chrome100", "chrome101", "chrome104", "chrome107", "chrome110"]

def isPageBlocked(text):
  # HEADERS (server : )
  return False

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--url", type=str, help="url to request")
  parser.add_argument("--urls", type=str, help="filename for list of urls")
  parser.add_argument("--proxies", type=str, help="filename for list of proxies")
  args = parser.parse_args()

  if not args.url and args.urls:
    print("No target url")
    exit()
  URL_LIST = []
  PROXIES = []
  # Ajout liste d'urls
  if args.urls:
    try:
      txt_file = open(args.proxies, "r")
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
    print(r.text)
    if r.status_code == 200 and not isPageBlocked(r.text):
      print("Simple request worked")
      exit()

    # Requete avec curl_cffi
    r = requests.get(url, impersonate=random.choice(BROWSER_LIST))
    if r.status_code == 200 and not isPageBlocked(r.text):
      print("Simple cffi request worked")
      exit()
    
    if not args.proxies:
      print("No proxy file provided")
      exit()

    # Requete simple avec proxy
    r = requests.get(url, proxies={"https": random.choice(PROXIES)})
    if r.status_code == 200 and not isPageBlocked(r.text):
      print("Simple request with proxy worked")
      exit()

    # Requete cffi avec proxy
    r = requests.get(url, impersonate=random.choice(BROWSER_LIST), proxies={"https": random.choice(PROXIES)})
    if r.status_code == 200 and not isPageBlocked(r.text):
      print("Simple cffi request worked")
      exit()

   
  
