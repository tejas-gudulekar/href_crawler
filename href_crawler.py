#!/usr/bin/env python2

import requests
import re
import urlparse

target_link_list = []  # List to store only unique list


# Function to find out the all the href tag in all the respones
def extract_info(url):
    response = session.get(url)
    return re.findall('(?:href=")(.*?)"', response.content)


# Function to crawl to different part/link of the website
def crawl(url):
    href_links = extract_info(url)  # Getting all the links from the current webpage
    for link in href_links:  # For all links found from the current page
        link = urlparse.urljoin(url, link)  # First completing the incomplete link

        # Getting only unique url by removing on-page navigation link
        if "#" in link:
            link = link.split("#")[0]

        # Checking if the link belongs to domain and it is unique
        if target in link and link not in target_link_list:
            target_link_list.append(link)
            print(link)# Adding in list
            crawl(link)  # Recursively calling the crawl function


def login_to_website():
    data_dict = {}
    login_url = raw_input("Enter the login url!! --> ")
    login_id = raw_input("Enter your login ID!! --> ")
    login_password = raw_input("Enter your login Password!! --> ")
    login_attribute_value = raw_input("Enter 'name' attribute value for Login_ID!! --> ")
    password_attribute_value = raw_input("Enter 'name' attribute value for Password!! --> ")
    button_attribute_value = raw_input("Enter the 'name' attribute value for the Login_Button!! --> ")
    button_type = raw_input("Enter the Button type!! --> ")
    data_dict[login_attribute_value] = login_id
    data_dict[password_attribute_value] = login_password
    data_dict[button_attribute_value] = button_type
    x = session.post(login_url, data_dict)
    if x.status_code == requests.codes.ok:
        print("\033[92m[+] Your Login-In Details submitted!!")
    else:
        print("\033[93m[+] Error while logging!")
        print("\033[93m[+] Please look for the values you passed for the Login")
        print("\033[94m[+] Continuing without logging in!")


def write_file(path, content):
    with open(path, "w") as file:
        for each in content:
            file.write("\n" + each)


try:
    session = requests.Session()
    target = raw_input("\033[01mEnter the target link!! --> ").strip()
    is_login = raw_input("Is there any login page in the website!! (yes/no) --> ").lower()
    try:
        if is_login == "yes" or is_login == "y":
            login_to_website()
        file_name = raw_input("\033[94mEnter the file name to save the output!! --> ")
        if ".txt" not in file_name:
            file_name = file_name + ".txt"
        print("\033[92m[+] Running the crawler!!")
        crawl(target)
        print("\033[92m[+] Writing the Crawler output in " + file_name)
        write_file(file_name, target_link_list)
        print("\033[94m[+] Output saved in " + file_name)
    except requests.exceptions.MissingSchema:
        print("\033[91m[-] Invalid url, do you mean http://" + target)
except KeyboardInterrupt:
    print("\033[93m\nQuitting the script!! ")
