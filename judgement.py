from flask import Flask, render_template, redirect, request, flash, g
from flask import session as session
import model
import jinja2
import api

app = Flask(__name__)

app.secret_key = '\xc1\xe2=\x1b\x8e\xdc\xfdbq\xdaKuO*}g\xfd'

@app.before_first_request
def setup_session():
    session.setdefault("logged_in", False)
    session.setdefault("user_id", None)

@app.before_request
def get_user():
    if session.get("user_id") is not None:
        g.logged_in = True
    else:
        g.logged_in = False

@app.route("/")
def index():
    user_list = model.session.query(model.User).limit(50).all()
    return render_template("user_list.html", users=user_list)

@app.route("/signup")
def sign_up():
    # Sign up form to add new user to database

    #also: need to check if input fields are valid
    #invalid entries redirect back to sign_up 
    #flash "please enter valid data for so and so"
    return render_template("sign_up.html")

@app.route("/signup", methods=["POST"])
def process_signup():
    #processess signup form and redirects to ??? if successful

    #if any values are null
    #flash("please fill out all fields")
    #redirect back to /signup (GET)
    print "Request is: ", request
    print "Request form is: ", request.form

    for value in request.form.values():
        if value == "": 
            flash("Please fill out all fields.")
            return redirect("/signup")

    user_check = api.get_user_by_email(request.form.get("email"))
    print "user_check", user_check
    if user_check:
        flash("Email already in use.")
        return redirect ('/signup')

    new_user = model.User()
    new_user.form_user(request.form)

    print "new_user", new_user

    #insert that user into the database
    # session.add(new_user)
    # session.commit()

    #redirect to login page 
    flash('Thanks for singing up! Please login!')
    return redirect("/login")



@app.route("/login")
def login():
    # Login form 
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def process_login():
    #processess login form and redirects to ??? if successful
    email = request.form.get("email")
    password = request.form.get("password")
    if api.check_login(email, password): #login successful 
        flash('login successful')
        return redirect("/")
    else: #login unsuccessful 
        flash('login unsuccessful')
        return redirect("/login")

@app.route("/logout")
def logout():
    api.logout()
    flash('logout successful')
    return redirect("/login")


@app.route("/users")
def display_all_users():
    #users need to be clickable
    #link needs to redirect to that user's ratings
    pass

@app.route("/user/<int:id>")
def display_movie_ratings_by_user(id):
    # Returns user's movie ratings
    current_user = api.get_user_from_db(id)
    user_ratings = current_user.ratings #what is this? list of rating objects
    #rating object will have
        #User_id
        #translate into movie title --> rating.movie.movie_title
        #Rating
    return render_template("user.html", user_ratings=user_ratings) #make this

@app.route("/ratemovie/<int:id>")
def rate_movie(id):
    #check if user logged in 
    if g.logged_in == False:
        flash("Please log in to rate a movie.")
        return redirect("/login")
    else:
        #when logged in, add or update rating for movie
        movie = api.get_movie_by_id(id)
        rating = api.get_users_rating_by_movie_id(session.get("user_id"), id)
        template_rating = None;
        if rating:
            template_rating = rating.rating
        return render_template("rate_movie.html", movie=movie, template_rating=template_rating)



if __name__ == "__main__":
    app.run(debug = True)

