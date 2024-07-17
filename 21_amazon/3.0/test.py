import requests

# Create a session object
session = requests.Session()

# Make a request to Youtube
session.get('https://www.blisscomputers.net')

# Print cookies stored in the session
print("Cookies after setting them:")
for cookie in session.cookies:
  print(f'{cookie.name} = {cookie.value}')