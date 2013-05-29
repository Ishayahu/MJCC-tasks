# -*- coding:utf-8 -*-
# coding=<utf8>

from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives

def send_email_alternative(subject,message,to,fio):
    message_html = htmlize(message)
    good_mails=[mail for mail in to if mail!='']
    # good_mails.remove(fio.mail)
    # send_mail(subject,message,"meoc-it@mail.ru",good_mails)
    from_email = "meoc-it@mail.ru"
    # text_content = 'This is an important message.'
    # html_content = '<p>This is an <strong>important</strong> message.</p>'
    msg = EmailMultiAlternatives(subject, message, from_email, good_mails)
    msg.attach_alternative(message_html, "text/html")
    msg.send()