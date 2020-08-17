# Run using 'nohup python3 weather_scrape.py &' on the command line
from bs4 import BeautifulSoup as bs
import requests
import smtplib
import time
import schedule

URL = 'https://weather.com/weather/hourbyhour/l/Half+Moon+Bay+CA?canonicalCity\
Id=a44ff603208fa7ccf47d5524fe819c587e05a31524b1cb413667b576ac169ea9'
headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}

def check_weather():
    source = requests.get(URL, headers=headers).text

    soup = bs(source, 'lxml')

    hourly_details = soup.find_all('details', {'data-testid' : 'ExpandedDetailsCard'})

    for hour in hourly_details:
        time = hour.h2.text
        if time == '12 am':
            break
        spans = hour.find_all('span', limit=2)
        temp, condition = spans[0].text, spans[1].text
        temp = temp.strip('°')
        if int(temp) > 65 and condition in ['Sunny', 'Mostly Sunny', 'Partly Cloudy']:
            send_mail(time, temp, condition)
            break

def send_mail(time, temp, condition):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(""" Email address """, """ Temp password """)

    subject = 'It\'s a great day to go to the beach!'
    body = f'The weather in Half Moon Bay will be {condition} with a temperature of {temp} today at {time}. Get to the beach by then if you can!'

    message = f'Subject: {subject}\n\n{body}'

    server.sendmail(
        """ Sender email """,
        """ Recipient email """,
        message
    )

    server.quit()

def main():
    schedule.every().day.at("06:00").do(check_weather)
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
