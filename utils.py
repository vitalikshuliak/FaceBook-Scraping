from bs4 import BeautifulSoup
import requests
import re
import os

ACTION_URL = "https://m.facebook.com/login.php?refsrc=https%3A%2F%2Fm.facebook.com%2F&amp;refid=8"
def facebook_login(mail, pwd):
    session = requests.Session()
    r = session.get('https://www.facebook.com/')
    soup = BeautifulSoup(r.content,'html.parser')
    inputs = soup.find('form').find_all('input', {'type': ['hidden', 'submit']})
    post_data = {input.get('name'): input.get('value')  for input in inputs}
    post_data['email'] = mail
    post_data['pass'] = pwd
    scripts = soup.find_all('script')
    scripts_string = '/n/'.join([script.text for script in scripts])
    datr_search = re.search('\["_js_datr","([^"]*)"', scripts_string, re.DOTALL)
    if datr_search:
        datr = datr_search.group(1)
        cookies = {'_js_datr' : datr}
    else:
        return False
    return session.post(ACTION_URL, data=post_data, cookies=cookies, allow_redirects=False).cookies.get_dict()


def get_cookies():
    session = requests.Session()
    session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'})
    # Get cookies
    response = session.get('https://m.facebook.com')
    cookies = session.cookies.get_dict()
    # Save cookies to file
    with open('cookies.txt', 'w') as file:
        for key, value in cookies.items():
            file.write(f"{key}={value}\n")

def get_env_value(env_variable):
  """
  Get ENV value
  """
  try:
      return os.environ[env_variable]
  except KeyError:
      error_msg = "Set the {} environment variable".format(env_variable)
      print(error_msg)

def get_comments(comments):
    print(comments)

def get_city(user_dct):
    if 'வசித்த இடங்கள்' not in user_dct:
        return None
    else:
        city = user_dct['வசித்த இடங்கள்']
        if '\n' in city:
            return city.split("\n")[0]
        else:
            return city
    
