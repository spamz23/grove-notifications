"""
This modules provides functionality to send an email to a person
from the Grove House email ("grovehouse.vr@gmail.com")
"""
import io
import os

import sendgrid
from sendgrid.helpers.mail import Mail, To, From, Content, Subject

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
    # TODO: Insert image into html
    # img = _image_to_bytes("grove/email_manager/grove.jpg")
    send_grid_api = sendgrid.SendGridAPIClient(
        api_key=os.environ.get("SENDGRID_API_KEY")
    )
    from_email = From("grovehouse.vr@gmail.com")
    subject = Subject(subject)
    to_email = To(email_dest)
    content = Content("text/html", message)
    mail = Mail(from_email, to_email, subject, content)

    send_grid_api.send(mail)
