from PIL import Image
from secrets import token_hex
import os
from flask import current_app
from flask_mail import Message
from .. import mail
from flask import url_for

# This function used to modify and save
# the recieved pictures
def crop_pic(pic):
    _,f_ext = os.path.splitext(pic.filename)
    picture_name = f"[AppName]-{token_hex(8)}" + f_ext
    picture_path = os.path.join(current_app.root_path, f'static/Profiles/{picture_name}')
    
    size = (400,400)
    pic = Image.open(pic)
    pic.thumbnail(size)

    pic.save(picture_path)
    return picture_name

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Reset Password Request', recipients=[user.email])
    msg.body = f"""To reset your password, visite the following link: {url_for('users.reset_token', token=token, _external=True)}

    If you did not make this request then simply ignore this email and no change will be made.
    """
    mail.send(msg)