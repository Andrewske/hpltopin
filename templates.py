from flask import render_template
import giphy


def no_success(error):
    return render_template(
        "no_success.html", error=error, no_success_gif=giphy.get_gif("uh oh")
    )
