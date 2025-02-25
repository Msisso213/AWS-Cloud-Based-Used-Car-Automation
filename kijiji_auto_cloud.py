import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import time

def monitor_cars(url, recipient_email):
    seen_cars = set()

    while True:
        car_listings = get_car_listings(url)
        
        for car in car_listings:
            car_tuple = (car['title'], car['price'])
            if car_tuple not in seen_cars:
                seen_cars.add(car_tuple)
                email_body = f"New Car Listing!\nTitle: {car['title']}\nPrice: {car['price']}\n"
                send_email('New Car Listing', email_body, recipient_email)

        time.sleep(3600)  # Check every hour

def get_car_listings(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        cars = []
        for item in soup.select('.bcNN7t'):
            title_elem = item.select_one('.G2jAym.fcN7dZ.z2jAym.p2jAym.b2jAym')
            price_elem = item.select_one('.G2jAym.d3uM7V.C2jAym.p2jAym.b2jAym')
            car_info = {
                'title': title_elem.text.strip() if title_elem else "N/A",
                'price': clean_price(price_elem.text.strip()) if price_elem else 0,
            }
            cars.append(car_info)
        return cars
    else:
        print(f"Failed to retrieve data: {response.status_code}\nResponse: {response.text}")
        return []
    
def clean_price(price_str):
    try:
        cleaned_price = price_str.replace('\xa0', '').replace('$', '').replace('*', '').strip()
        return int(cleaned_price.replace(',', ''))
    except ValueError:
        return 0


def send_email(subject, body, recipient_email):
    sender_email = 'cheapflight819@gmail.com'
    sender_password = 'plfz qtml eeui ssvy'  # Use an app password if 2FA is enabled

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print('Email sent successfully!')
    except Exception as e:
        print(f'Failed to send email: {e}')


marque = input("Marque (NA pour aucune preference):")
modele = input("Modèle (NA pour aucune preference):")
url = ""
if marque.lower() == "na":
    url += 'https://www.kijijiautos.ca/fr/voitures/'
elif modele.lower() =="na":
    url += 'https://www.kijijiautos.ca/fr/voitures/'+ marque + '/'
else:
    url = 'https://www.kijijiautos.ca/fr/voitures/'+ marque + '/' + modele
url += '#ms=11000%3B5&od=down&sb=ct'

#print(url)
#print(get_car_listings(url))
recipient_email = 'aymenzebentout@gmail.com'
monitor_cars(url, recipient_email)
