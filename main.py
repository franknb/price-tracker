import requests
from bs4 import BeautifulSoup
import re
from email.message import EmailMessage
import ssl
import smtplib
import os
import time
import pandas as pd
from datetime import datetime
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')


def get_price(flavor):
    assert flavor in ['unflavor', 'mocha']
    if flavor == 'unflavor':
        flavor_id = '11276659'
    elif flavor == 'mocha':
        flavor_id = '11352688'
    URL = f"https://us.myprotein.com/sports-nutrition/impact-whey-isolate/{flavor_id}.html?switchcurrency=USD&shippingcountry=US"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    banner = soup.find("div", class_="stripBanner").find('p')
    price = soup.find("p", class_="productPrice_price")
    discount = float(re.findall(r'\d+\.\d+|\d+', banner.text.strip())[0])
    p = float(re.findall(r'\d+\.\d+|\d+', price.text.strip())[0])
    final = p * (100 - discount) / 100
    return final


def send_email(to='frankxu0124@gmail.com', subject='test', body='test'):
    email_sender = 'xhzftg@gmail.com'
    email_password = 'zvcl kove dgid wmlp'
    email_receiver = to
    em = EmailMessage()
    em['From'] = 'xhzftg@gmail.com'
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl.create_default_context()) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

def create_figure(data):
    plt.figure(figsize=(12, 6))
    sns_plot = sns.lineplot(x='timestamp', y='value', hue='variable', data=pd.melt(data, ['timestamp']))
    sns_plot.tick_params(axis='x', labelrotation=30)
    sns_plot.figure.savefig(os.path.join(os.getcwd(), "static/output.pdf"), bbox_inches="tight")

data_path = os.path.join(os.getcwd(), 'data.csv')
if os.path.exists(data_path):
    data = pd.read_csv(data_path)
else:
    data = pd.DataFrame({'timestamp': [],
                         'mocha_price': [],
                         'unflavor_price': []})

if __name__ == "__main__":
    while True:
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        unflavor = get_price('unflavor')
        mocha = get_price('mocha')
        if unflavor <= 130 or mocha <= 130:
            body = f"Current price for unflavored is ${unflavor}, for mocha is ${mocha}.\n"
            body += f"Unflavored URL: https://us.myprotein.com/sports-nutrition/impact-whey-isolate/11276659.html?switchcurrency=USD&shippingcountry=US \n"
            body += f"Mocha URL: https://us.myprotein.com/sports-nutrition/impact-whey-isolate/11352688.html?switchcurrency=USD&shippingcountry=US"
            send_email(subject='Price Alert!', body=body)
        data.loc[len(data)] = [current_datetime, unflavor, mocha]
        create_figure(data)
        data.to_csv('data.csv', index=False)
        time.sleep(60)
