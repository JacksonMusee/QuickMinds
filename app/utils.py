"""This module contains general utility functions.
"""
import os
import json
import random
from functools import wraps
from flask_login import current_user
from flask import flash, redirect, request, url_for, session
from datetime import datetime, timezone, timedelta
from flask_mail import Message
from app import mail


def admin_required(f):
    """A decorator to ensure a user is admin.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash(message="Access to this page is restricted to Admins",
                  category="danger")
            return redirect(request.referrer) if request.referrer else redirect(url_for('ordinary_bp.index'))
        return f(*args, **kwargs)
    return decorated_function


def generate_otp(email):
    """Generates, stringfyies and Stores a random six digit otp in session.
    """
    otp = str(random.randint(100000, 999999))
    session["otp"] = otp
    session["otp_expiry"] = datetime.now(timezone.utc) + timedelta(minutes=5)
    session["email"] = email

    return otp


def send_otp(email, otp):
    """Send an OTP to user via email
    """
    msg = Message(
        subject="OTP",
        recipients=[email],
        body=f"Your OTP is: {otp}"
    )
    mail.send(msg)


def verify_otp(otp):
    """Verifies if user entered otp matches what is in session and not expired
    """
    session_otp = session.get("otp")
    expiry = session.get("otp_expiry")
    now = datetime.now(timezone.utc)

    print(f"Session otp: {session_otp} {type(session_otp)}")
    print(f"User otp: {otp} {type(otp)}")
    if otp != session_otp:
        return False, "Wrong OTP"

    elif now > expiry:
        return False, "OTP expired."

    else:
        return True, None
