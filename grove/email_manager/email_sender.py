"""
This modules provides functionality to send an email to a person
from the Grove House email ("grovehouse.vr@gmail.com")
"""
import io
import os


from bs4 import BeautifulSoup
from PIL import Image


def _image_to_bytes(img_location: str) -> bytes:
    """Opens a image and transforms it into bytes

    Parameters
    ----------
    img_location: str
        The image file location

    Returns
    -------
    bytes
        The image converted into bytes
    """

    img_byte_arr = io.BytesIO()
    Image.open(img_location).save(img_byte_arr, format="PNG")
    return img_byte_arr.getvalue()


def _insert_msg_in_html(html_file_location: str, text: str) -> str:
    """Opens HTML file and inserts a custom text in a 'div' element with class 'message'

    Parameters
    ----------
    html_file: str
        The HTML file location

    text: str
        The text to insert into the HTML

    Returns
    -------
    str
        The modified HTML
    """
    with open(html_file_location) as html_file:
        soup = BeautifulSoup(html_file.read(), features="html.parser")
        soup.find("div", {"class": "message"}).string.replace_with(text)
        return soup.prettify()


import smtplib

from email.mime.text import MIMEText


# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.

# Send the message via local SMTP server.


def send_mail(email_dest: str, subject: str, body_msg: str):
    """Send an email from GroveHouse to destinatary

    Parameters
    ----------
    email_dest: str
        Adress to send email

    subject: str
        The email's subject

    body_msg: str
        The message to insert in the email html template body
    """
    message = _insert_msg_in_html("grove/email_manager/template.html", body_msg)

    html_body = MIMEText(message, "html")
    html_body["Subject"] = subject
    server = smtplib.SMTP("smtp.gmail.com", 587)

    server.ehlo()

    server.starttls()  # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    server.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASSWORD"))

    server.sendmail(os.getenv("EMAIL_USER"), email_dest, html_body.as_string())
