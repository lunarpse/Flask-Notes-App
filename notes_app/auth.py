from flask import Blueprint,request,render_template

auth=Blueprint("auth",__name__)

@auth.route("/signup",methods=["POST"])
def signup():
    if request.method=="POST":
        name=request.form.get("name")
        email=request.form.get("email")
        password=request.form.get("password")

        print(email)

    return render_template("signup.html")


@auth.route("/signin",methods=["POST"])
def signin():
    return render_template("signin.html")
