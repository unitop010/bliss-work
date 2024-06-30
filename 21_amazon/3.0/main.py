import requests
from bs4 import BeautifulSoup
import json

payload = {"customer-action":"pagination"}

# headers = {
#   "Accept": "text/html,image/webp,ajax/ajax,*/*",
#   "Accept-Encoding": "gzip, deflate, br, zstd",
#   "Accept-Language": "en-US,en;q=0.9,ru;q=0.8",
#   "Content-Length": "32",
#   "Content-Type": "application/json",
#   "Cookie": "session-id=143-4836774-8659924; session-id-time=2082787201l; i18n-prefs=USD; ubid-main=135-2563515-6550518; lc-main=en_US; session-token=fqs503rNgMFqm5GI4E0zv0C1rayzb0MAEiQdw+u4aJZF2/nvY7AcVoxRjecfF+9IN3N9SRpwe1WzQBFWafo0H+fUjLTTlIPU62+HQFVrgYqDgyiUrccxBougWeoArt6o6xR7FrUsRCideDmKNJ5LCCk0tbdAAtoXS0CEz4kr0rq7DxrOJ8tBh3LNaRFEqlj8mSz2I/+NMGiED4q1lN0w82Qi2/ecaapBD+3RmiBWLuiWgF/LHXVCPrkB/CJVKx1WK1ZLBJ8CPD2Q0KyNBHCzNhzMIQ2xZ1vApH1m/fs4um6rOaXfnXsIH6P69Ip4xILL1VkL7znv6Q+W0ct75J4G6i+n4Q24A6H7; csm-hit=tb:M9YCF3HN48D0E49ZGV0A+s-6DS5GBQK1F8TP35V6683|1719559990013&t:1719559990013&adb:adblk_yes",
#   "Device-Memory": "8",
#   "Downlink": "1.25",
#   "Dpr": "1",
#   "Ect": "3g",
#   "Origin": "https://www.amazon.com",
#   "Priority": "u=1, i",
#   "Referer": "https://www.amazon.com/s?k=laptop+replacement+screens&i=computers&rh=n%3A3011391011%2Cn%3A2612045011&dc&page=2&crid=1AX23ZA34FITZ&qid=1719558589&refresh=1&rnid=2941120011&sprefix=replacement+screens%2Caps%2C141&ref=sr_pg_2",
#   "Rtt": "250",
#   "Sec-Ch-Device-Memory": "8",
#   "Sec-Ch-Dpr": "1",
#   "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
#   "Sec-Ch-Ua-Mobile": "?0",
#   "Sec-Ch-Ua-Platform": "\"Windows\"",
#   "Sec-Ch-Ua-Platform-Version": "\"10.0.0\"",
#   "Sec-Ch-Viewport-Width": "1920",
#   "Sec-Fetch-Dest": "empty",
#   "Sec-Fetch-Mode": "cors",
#   "Sec-Fetch-Site": "same-origin",
#   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
#   "Viewport-Width": "1920",
#   "X-Amazon-Rush-Fingerprints": "AmazonRushAssetLoader:1202F8AA9B9E3A62A246BF3FA42812770110C222|AmazonRushFramework:5A82CF8689ED82AAA920893CD095BCCCED05133A|AmazonRushRouter:1F95DFA8ABBD44B9003CFFA46D316B571F75C03E",
#   "X-Amazon-S-Fallback-Url": "https://www.amazon.com/s?k=laptop+replacement+screens&i=computers&rh=n%3A3011391011%2Cn%3A2612045011&dc&page=3&crid=1AX23ZA34FITZ&qid=1719558793&refresh=1&rnid=2941120011&sprefix=replacement+screens%2Caps%2C141&ref=sr_pg_3",
#   "X-Amazon-S-Mismatch-Behavior": "FALLBACK",
#   "X-Amazon-S-Swrs-Version": "B59F10D79BFF3926C548C31470843F9A,D41D8CD98F00B204E9800998ECF8427E",
#   "X-Requested-With": "XMLHttpRequest"
# }

# response = requests.post("https://www.amazon.com/s/query?crid=1AX23ZA34FITZ&dc&i=computers&k=laptop%20replacement%20screens&page=500&qid=1719558793&ref=sr_pg_2&refresh=1&rh=n%3A3011391011%2Cn%3A2612045011&rnid=2941120011&sprefix=replacement%20screens%2Caps%2C141", json=payload, headers=headers)


headers = {
  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
  "Accept-Encoding": "gzip, deflate, br, zstd",
  "Accept-Language": "en-US,en;q=0.9,ru;q=0.8",
  "Cookie": "session-id=143-4836774-8659924; session-id-time=2082787201l; i18n-prefs=USD; ubid-main=135-2563515-6550518; lc-main=en_US; session-token=K1Or67SM0H7kDsJBvFYrA3nCSTruPKutu6+kRuvwg+szpyRXIv4yE06P/XUVWSyHl7HjGLo16hEj2mifol9XpnLWOBv9X6pyUxhKjNvYJILCPll3aH1dXyerf+vD31gTcHLyLwJESZZNtnz44qzN4xHFIgUv5Kj/vTmUHqqSleCPj95yw09EwrSto/XeZhLI4M5mphSeqMt6vas3uk9qx7z3ZaPmgMJvlEW7S+5sxwmcwpHoVZb1fnRuMgbfO13Pvki1i2TjkaUQG+rwYCaIUaTdztUbeonkoQU1sxIwctRhFRR0KssTPhPQDp7z/+p3eC91uG+cimGQVLQvLXby6ZO6CTcz394L; csm-hit=tb:M9YCF3HN48D0E49ZGV0A+s-23XJS872XZZWC06BWY6H|1719561222353&t:1719561222353&adb:adblk_yes",
  "Device-Memory": "8",
  "Downlink": "1.3",
  "Dpr": "1",
  "Ect": "4g",
  "Priority": "u=0, i",
  "Rtt": "250",
  "Sec-Ch-Device-Memory": "8",
  "Sec-Ch-Dpr": "1",
  "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
  "Sec-Ch-Ua-Mobile": "?0",
  "Sec-Ch-Ua-Platform": "\"Windows\"",
  "Sec-Ch-Ua-Platform-Version": "\"10.0.0\"",
  "Sec-Ch-Viewport-Width": "1920",
  "Sec-Fetch-Dest": "document",
  "Sec-Fetch-Mode": "navigate",
  "Sec-Fetch-Site": "none",
  "Sec-Fetch-User": "?1",
  "Upgrade-Insecure-Requests": "1",
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
  "Viewport-Width": "1920"
}

response = requests.get("https://www.amazon.com/s?k=laptop+replacement+screens&i=computers&rh=n%3A3011391011%2Cn%3A2612045011&dc&page=400&crid=1AX23ZA34FITZ&qid=1719558793&refresh=1&rnid=2941120011&sprefix=replacement+screens%2Caps%2C141&ref=sr_pg_3", headers=headers)

print(response.status_code)

# print(response.text)

print(response.text)
print("----------------------")


with open("3.html", "w", encoding="utf-8") as file:
    file.write(response.text)