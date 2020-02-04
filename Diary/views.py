import datetime
import os
import random
import string

from flask import Flask, render_template, redirect, session
from loopyCryptor import md5

from .Diary import Diary
from .forms import VerifyForm, DiaryForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "".join(
    random.sample(string.ascii_letters + string.digits, 16)
)
app.config["SESSION_PERMANENT"] = False
TOKEN_2MD5 = ""
WEBSITE = "https://www.chinacourt.org/article/detail/2017/11/id/3036068.shtml"


def is_robot():
    if "count" in session:
        session["count"] += 1
    else:
        session["count"] = 0
    return session["count"] > 100


def check(token=None):
    if "token_md5" in session:
        return md5(session["token_md5"]) == TOKEN_2MD5
    else:
        if token is None:
            return False
        session["token_md5"] = md5(token)
        return check()


@app.route("/", methods=["GET", "POST"])
def index():
    if is_robot():
        return render_template(
            "diary.html",
            msg="Due to frequent operations, you are currently banned from server.",
        )

    form = VerifyForm()
    if form.validate_on_submit():
        try:
            if not check(form.data["password"]):
                return redirect(WEBSITE)
            else:
                return redirect("./Diary")
        except Exception as e:
            return render_template("diary.html", verify_form=form, msg=e)
    else:
        return render_template("diary.html", verify_form=form)


@app.route("/Diary", methods=["GET", "POST"])
def write():
    if is_robot():
        return render_template(
            "diary.html",
            msg="Due to frequent operations, you are currently banned from server.",
        )
    if not check():
        return redirect(WEBSITE)

    form = DiaryForm()
    if form.validate_on_submit():
        if not check():
            return redirect(WEBSITE)
        else:
            try:
                Diary(form["content"].data, "./Diary/static").to_diary()
                return render_template("diary.html", msg="Done")
            except Exception as e:
                return render_template("diary.html", msg=e, diary_form=form)
    else:
        date = datetime.date.today()
        if os.path.isfile("./Diary/{}.Diary".format(date)):
            msg = "! Diary already exist"
        else:
            msg = "{}{}周{}".format(
                date.isoformat(), "&nbsp;" * 3, "一二三四五六日"[date.isoweekday()]
            )
        return render_template("diary.html", msg=msg, diary_form=form)
