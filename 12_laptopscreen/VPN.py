import pyautogui, csv
from win10toast import ToastNotifier
from datetime import datetime
from time import sleep

screen_width, screen_height = pyautogui.size()

def typing(content : str):
    for i in content:
        pyautogui.typewrite(i)  
        sleep(0.0005)

def create_timed_notification(title, message):
    # Create an instance of ToastNotifier
    toaster = ToastNotifier()
    
    # Show the notification
    toaster.show_toast(title, 
        message, 
        duration=5,  # The notification will stay for 5 seconds
        icon_path="E:\\Scraping\\VPN\\smalllogo.ico",  # You can specify an icon path here
        threaded=True)

def change_ip():
    create_timed_notification("Astrill VPN", "Your IP address will be change soon!")
    sleep(2)
    with open('IP_US_LS.csv', 'r+', encoding='utf-8') as ip:
        ips = ip.readlines()
    pyautogui.moveTo(screen_width - 40, 250)
    pyautogui.leftClick()
    typing(ips[0])
    # %A - full weekday name, %d - day of the month, %B - full month name, %Y - year, %H:%M:%S - time
    # print("\n-----", datetime.now().strftime("%A, %d %B %Y, %H:%M:%S"), "-----", ips[0])
    ips.append(ips.pop(0))
    with open('IP_US_LS.csv', 'w', encoding='utf-8') as ip:
        ip.writelines(ips)