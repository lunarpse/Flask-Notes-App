from flask import Flask,request,render_template,redirect
from flask_sqlalchemy import SQLAlchemy;
from datetime import datetime
from flask_login import login_user,UserMixin,LoginManager,login_required,current_user,logout_user

app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_NOTIFICATIONS"]=False
app.secret_key = 'super secret key'
login_manager=LoginManager()
login_manager.login_view="login"
login_manager.init_app(app)


@app.errorhandler(403)
def not_authorized(e):
    return render_template("restricted.html")


@app.errorhandler(404)
def not_found(e):
    return render_template("not_found.html")



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



db=SQLAlchemy(app)

class Todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    desc=db.Column(db.String(200),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow())
    userid=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __repr__(self)->str:
        return f"{self.sno} - {self.title}"
    

class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(100),nullable=False)
    password=db.Column(db.String(100),nullable=False)
    name=db.Column(db.String(100),nullable=False)
    notes=db.relationship('Todo',backref='user',lazy=True)


with app.app_context():
    db.create_all()



@app.route("/")
def home():
     return render_template("index.html")

@app.route("/",methods=["POST"])
@login_required
def add_notes():

   
    title=request.form.get("title")
    desc=request.form.get("desc")
    print(title,desc)
    todo=Todo(title=title,desc=desc,user=current_user)
    
    db.session.add(todo)
    db.session.commit()
    return redirect("/items")


@app.route("/items")
@login_required
def items():
     user=User.query.filter_by(email=current_user.email).first()
     if not user:
         return redirect('/error')
     

     items=Todo.query.filter_by(user=user)
     print("{} sdfsdfreferfg".format(items))
     for i in items:
         print("{} ffffffff".format(i))
     return render_template("items.html",allitems=items)


@app.route("/delete/<int:sno>")
@login_required
def delete(sno):
    
    todo=Todo.query.filter_by(sno=sno,user=current_user).first()
    print(todo)
    db.session.delete(todo)
    db.session.commit()
    return redirect("/items")
   
@app.route("/update/<int:sno>",methods=["GET","POST"])
@login_required
def update(sno):
    if request.method=="POST":
        title=request.form.get("title")
        desc=request.form.get("desc")
        todo=Todo.query.filter_by(sno=sno,user=current_user).first()
        
        todo.title=title
        todo.desc=desc
        print("{} forjkad  ".format(todo.desc))
        db.session.add(todo)
        db.session.commit()
        return redirect("/items")
    todo=Todo.query.filter_by(sno=sno).first()
    return render_template("update.html",todo=todo)




@app.route("/signup",methods=["GET","POST"])
def signup():
    if request.method=="POST":
        name=request.form.get("name")
        email=request.form.get("email")
        password=request.form.get("password")
        print(email)
        user=User.query.filter_by(email=email).first()
        if user:
            return redirect("/signin")
        
        newuser=User(name=name,email=email,password=password)
        db.session.add(newuser)
        db.session.commit()
        return redirect("/signin")

    return render_template("signup.html")


@app.route("/signin",methods=["GET","POST"])
def signin():
    if request.method=="POST":
        email=request.form.get("email")
        password=request.form.get("password")
       
        user=User.query.filter_by(email=email,password=password).first()
        print( "{} sdsdfdf".format(user.email))
        if not user:
            return redirect("/signin")
        login_user(user)
        return redirect("/")
        
    return render_template("signin.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/signin")



if __name__=="__main__":
    app.run(debug=True)

