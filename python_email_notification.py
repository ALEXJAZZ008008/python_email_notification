# Copyright University College London 2021
# Author: Alexander Whitehead, Institute of Nuclear Medicine, UCL
# For internal research only.


import os
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib
import socket


# https://towardsdatascience.com/notify-with-python-41b77d51657e
def message(subject="Python Notification", text="", img=None, attachment=None):
    print("message")

    # build message contents
    msg = MIMEMultipart()
    msg["Subject"] = subject  # add in the subject
    msg.attach(MIMEText(text))  # add text contents

    # check if we have anything given in the img parameter
    if img is not None:
        # if we do, we want to iterate through the images, so let's check that
        # what we have is actually a list
        if type(img) is not list:
            img = [img]  # if it isn't a list, make it one

        # now iterate through our list
        for one_img in img:
            img_data = open(one_img, "rb").read()  # read the image binary data
            # attach the image data to MIMEMultipart using MIMEImage, we add
            # the given filename use os.basename
            msg.attach(MIMEImage(img_data, name=os.path.basename(one_img)))

    # we do the same for attachments as we did for images
    if attachment is not None:
        if type(attachment) is not list:
            attachment = [attachment]  # if it isn't a list, make it one

        for one_attachment in attachment:
            with open(one_attachment, "rb") as f:
                # read in the attachment using MIMEApplication
                file = MIMEApplication(f.read(), name=os.path.basename(one_attachment))

            # here we edit the attached file metadata
            file["Content-Disposition"] = f"attachment; filename='{os.path.basename(one_attachment)}'"
            msg.attach(file)  # finally, add the attachment to our message object

    return msg


# https://towardsdatascience.com/notify-with-python-41b77d51657e
def send(msg, receive_email, server="smtp.gmail.com", port="587"):
    print("send")

    # contain following in try-except in case of momentary network errors
    try:
        # initialise connection to email server, the default is GMail
        smtp = smtplib.SMTP(server, port)
        # this is the 'Extended Hello' command, essentially greeting our SMTP or ESMTP server
        smtp.ehlo()
        # this is the 'Start Transport Layer Security' command, tells the server we will
        # be communicating with TLS encryption
        smtp.starttls()

        send_email = "ALEXJAZZ008008.test.email@gmail.com"
        pwd = "test_email"

        # login to outlook server
        smtp.login(send_email, pwd)
        # send notification to self
        smtp.sendmail(send_email, receive_email, msg.as_string())
        # disconnect from the server
        smtp.quit()
    except socket.gaierror:
        print("Network connection error, email not sent.")

    return True


def main(text="Done!", img=None, attachment=None, receive_email="alexander.whitehead.18@ucl.ac.uk"):
    print("main")

    # build a message object
    msg = message(text=text, img=img, attachment=attachment)
    send(msg, receive_email)  # send the email (defaults to GMail)

    return True


if __name__ == "__main__":
    main()
