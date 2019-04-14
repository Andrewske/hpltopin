from flask import render_template
from .giphy import get_gif
from .class_pinterest import Pinterest
from flask_login import LoginManager, login_required, current_user

p = Pinterest()
user = current_user


def no_success(error):
    return render_template(
        "no_success.html", error=error, no_success_gif=get_gif("uh oh")
    )


def profile(message=None):
    return render_template(
        "profile.html",
        username=user.username,
        auth_url=p.get_auth_url(),
        access_token=user.access_token,
        message=message,
        profile_gif=get_gif("you made it"),
    )


def pin_list(hpl_url=None, username=None, listing_count=None, board_name=None):
    return render_template(
        "pin_list.html",
        username=username,
        listing_count=listing_count,
        board_name=board_name,
        hpl_url=hpl_url,
        just_do_it_gif=get_gif("just do it"),
    )


def success(data, title, board_url, message=None):
    return render_template(
        "success.html",
        data=data,
        title=title,
        board_url=board_url,
        message=message,
        success_gif=get_gif("success"),
    )
