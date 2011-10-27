# -*- coding: utf8 -*-
from django.core.mail import send_mail
from AAapp import settings

def send_notice_email(expense):
    subject = u'人人AAapp消费记录 - %s' % expense.title
    for user in expense.participants.all():
        if expense.money > 0:
            ty = u'消费'
        else:
            ty = u'充入'
        content = u'''
            你于 %d年%d月%d日 %d点%02d分 %s了 %d人民币。
            你现在的余额是%d人民币。
            要查看你的消费记录，请访问 dustr.info:8000
        ''' % (expense.pub_datetime.year,
                expense.pub_datetime.month,
                expense.pub_datetime.day,
                expense.pub_datetime.hour,
                expense.pub_datetime.minute,
                ty,
                abs(expense.each()),
                user.accountinfo.balence)
        
        send_mail(subject, content, settings.SEND_MAIL_USER,
                [user.email],
                fail_silently=False)
