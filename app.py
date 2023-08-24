import re
import requests
from bs4 import BeautifulSoup

def get_social_links(soup):
    social_links = []
    social_patterns = [
        r'facebook\.com',
        r'linkedin\.com',
        r'twitter\.com',
        r'instagram\.com',
    ]
    for link in soup.find_all('a', href=True):
        for pattern in social_patterns:
            if re.search(pattern, link['href']):
                social_links.append(link['href'])
    return social_links

def get_email(soup):
    email = None
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b')
    for paragraph in soup.find_all('p'):
        match = email_pattern.search(paragraph.get_text())
        if match:
            email = match.group(0)
            break
    return email

def get_contact(soup):
    contact = None
    contact_pattern = re.compile(r'\b(?:\+\d{1,2}\s*)?(?:\(\d{3}\)|\d{3})[\s.-]?\d{3}[\s.-]?\d{4}\b')
    for paragraph in soup.find_all('p'):
        match = contact_pattern.search(paragraph.get_text())
        if match:
            contact = match.group(0)
            break
    return contact

def main():
    url = input("Enter the URL: ")
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        social_links = get_social_links(soup)
        email = get_email(soup)
        contact = get_contact(soup)
        
        print("Social links:")
        for link in social_links:
            print(link)
        
        if email:
            print("Email:", email)
        else:
            print("Email not found.")
        
        if contact:
            print("Contact:", contact)
        else:
            print("Contact not found.")
    else:
        print("Failed to fetch the website.")

if __name__ == "__main__":
    main()
