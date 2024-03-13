from kavenegar import *

def user_image_path(instance, filename):
    user_id = instance.id if instance.id else 'temp'
    today = instance.created_at.strftime('%Y/%m/%d')
    return f'users/{user_id}/{today}/{filename}'

def category_image_path(instance, filename):
    return f'category/{instance.name}/{filename}'

def product_image_path(instance, filename):
    return f'products/{instance.category.name}/{instance.name}/{filename}'

def news_image_path(instance, filename):
    return f'news/{instance.title}/{filename}'


from django.core.mail import send_mail

def send_otp_email(email, otp):
    subject = 'Your OTP Code'
    message = f'Your OTP code is: {otp}'
    from_email = 'mkalhor81126@gmail.com'
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)

# from kavenegar import *
# try:
#     api = KavenegarAPI('2F6B33347A696134443838414A6F487372493455516749386A6548736B6C4B5467446E58782B41764734303D')
#     params = {
#         'receptor': '09016058919',
#         'template': '',
#         'token': '',
#         'type': 'sms',#sms vs call
#     }   
#     response = api.verify_lookup(params)
#     print(response)
# except APIException as e: 
#     print(e)
# except HTTPException as e: 
#     print(e)