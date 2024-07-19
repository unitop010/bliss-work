import requests

session = requests.Session()

response = session.get('https://www.laptopscreen.com/English/')

print("Cookies after setting them:")
print(response.status_code)
print(response.headers)
# for cookie in session.cookies:
#   print(f'{cookie.name} = {cookie.value}')