import datetime, json
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, logout_user, login_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from . import main
from .forms import SignUpForm, SignInForm, SignOutForm, PostForm, CommentForm, DeleteForm
from .. import db, login_manager
from ..models import User, Post, Comment


@main.route("/")
def index():
    recentpost = Post.query.order_by(Post.time.desc()).limit(1).first()
    if (recentpost != None):
        title = recentpost.title
        id = "/posts/" + str(recentpost.id)
    else:
        title = "No posts yet!"
        id = "/board"
    return render_template("index.html", title=title, id=id)

@main.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    db.create_all()

    if (form.validate_on_submit()):
        username = form.username.data
        password = form.password.data
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        if (makeUser(username, password, firstname, lastname, email) == True):
            flash("Account successfully created", category="success")
        else:
            flash("Username taken, please try another one", category="error")
        return redirect(url_for("main.signup"))


    return render_template("signup.html", form=form)

@main.route("/login", methods=["GET", "POST"])
def login():
    form = SignInForm()

    if (form.validate_on_submit()):
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if (user == None):
            flash("Username does not exist", category="error")
            return redirect(url_for("main.login"))
        elif (check_password_hash(user.password, password)):
            login_user(user, form.rememberme.data)
            return redirect(url_for("main.index"))
        else:
            flash("Incorrect password", category="error")
            return redirect(url_for("main.login"))

    return render_template("login.html", form=form)

@main.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    form = SignOutForm()

    if (form.validate_on_submit()):
        logout_user()
        flash("You have been logged out", category="success")
        return redirect(url_for("main.login"))

    return render_template("logout.html", form=form)

@main.route("/users/<username>")
def users(username):
    user = User.query.filter_by(username=username).first()
    posts = []
    postids = []

    if (user == None):
        return render_template("userpage.html", username=None)

    if (user.joindate.strftime("%d") == "1" or user.joindate.strftime("%d") == "21"
            or user.joindate.strftime("%d") == "31"):
        end = "st"
    elif (user.joindate.strftime("%d") == "2" or user.joindate.strftime("%d") == "22"):
        end = "nd"
    elif (user.joindate.strftime("%d") == "3" or user.joindate.strftime("%d") == "23"):
        end = "rd"
    else:
        end = "th"
    date = (user.joindate.strftime("%B") + " " + str(int(user.joindate.strftime("%d"))) + end + ", " +
            user.joindate.strftime("%Y"))

    for i in range(len(user.posts)):
        posts.append(user.posts[len(user.posts)-i-1].title)
        postids.append(user.posts[len(user.posts)-i-1].id)

    pagecount = int(user.postcount/5+0.9)

    return render_template("userpage.html", username=user.username, firstname=user.firstname,
                           lastname=user.lastname, email=user.email, joindate=date, postcount=user.postcount,
                           posts=posts, pagecount=pagecount, min=min, postids=postids)

@main.route("/board")
def board():
    totalposts = Post.query.count()

    return render_template("board.html", totalposts=totalposts)

@main.route("/load<num>")
def load(num):
    posts = Post.query.order_by(Post.time.desc()).limit(5).offset(int(num)).all()
    titles = []
    subtitles = []
    content = []
    commentmessages = []

    for i in range(len(posts)):
        titles.append("<a class='noshow' href='/posts/" + str(posts[i].id) + "'>" + posts[i].title + "</a>")
        subtitles.append("By <a class='postlink' href='/users/" + posts[i].username + "'>" + posts[i].username +
                         "</a> " + "at " + posts[i].time.strftime("%-I:%M %p on %B %d, %Y"))
        content.append(posts[i].content)
        if (posts[i].commentcount == 0):
            commentmessages.append("0 comments")
        elif (posts[i].commentcount == 1):
            commentmessages.append(str(posts[i].commentcount) + " comment")
        else:
            commentmessages.append(str(posts[i].commentcount) + " comments")

    postdict = {
        "titles": titles,
        "subtitles": subtitles,
        "content": content,
        "comments": commentmessages
    }

    postinfo = json.dumps(postdict)

    return postinfo

@main.route("/newpost", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()

    if (form.validate_on_submit()):
        title = form.title.data
        content = form.content.data
        username = current_user.get_id()
        makePost(title, content, username)
        return redirect(url_for("main.board"))

    return render_template("newpost.html", form=form)

@main.route("/posts/<id>", methods=["GET", "POST"])
def posts(id):
    post = Post.query.filter_by(id=int(id)).first()
    commentsubtitles = []
    commentcontent = []
    form = CommentForm()

    if (post == None):
        return render_template("post.html", post=False)

    title = post.title
    subtitle = ("By <a class='postlink' href='/users/" + post.username + "'>" + post.username + "</a> " +
                "at " + post.time.strftime("%-I:%M %p on %B %d, %Y"))
    content = post.content

    for i in range(len(post.comments)):
        commentsubtitles.append("Comment by <a class='postlink' href='/users/" + post.comments[i].username +
                                "'>" + post.comments[i].username + "</a> " + "at " +
                            post.comments[i].time.strftime("%-I:%M %p on %B %d, %Y"))
        commentcontent.append(post.comments[i].content)

    if (form.validate_on_submit()):
        if (current_user.is_authenticated):
            content = form.content.data
            username = current_user.get_id()
            makeComment(content, post, username)
            return redirect(url_for("main.posts", id=id))
        else:
            flash("Please log in to your account in order to comment")
            return redirect(url_for("main.login"))

    if (current_user.is_authenticated):
        if (current_user.get_id() == post.username):
            form2 = DeleteForm()

            if (form2.validate_on_submit()):
                deletePost(post)
                return redirect(url_for("main.board"))
        else:
            form2 = None
    else:
        form2 = None

    return render_template("post.html", post=True, title=title, subtitle=subtitle,
                           content=content, commentcount=len(post.comments), commentsubtitles=commentsubtitles,
                           commentcontent=commentcontent, form=form, id=id, form2=form2)

def makeUser(username, password, firstname, lastname, email):
    if (User.query.filter_by(username=username).first() == None):
        user = User(username = username, password = generate_password_hash(password), firstname = firstname,
                    lastname= lastname, email = email, joindate=datetime.datetime.now().date(), postcount=0)
        db.session.add(user)
        db.session.commit()
        return True
    else:
        return False

def makePost(title, content, username):
    post = Post(title=title, content=content, time=datetime.datetime.now(), username=username, commentcount=0)
    db.session.add(post)
    user = User.query.filter_by(username=username).first()
    user.postcount = user.postcount+1
    user.posts.append(post)
    db.session.commit()

def makeComment(content, post, username):
    comment = Comment(content=content, time=datetime.datetime.now(), postid=post.id, username=username)
    db.session.add(comment)
    post.commentcount = post.commentcount+1
    post.comments.append(comment)
    db.session.commit()

def deletePost(post):
    user = User.query.filter_by(username=post.username).first()
    user.postcount = user.postcount-1
    for i in range(len(post.comments)):
        db.session.delete(post.comments[i])
    db.session.delete(post)
    db.session.commit()

@login_manager.unauthorized_handler
def unauthorized():
    if (request.path == "/newpost"):
        flash("Please log in to your account in order to post", "error")
    else:
        flash("Please log in to your account to view the selected page", "error")

    return redirect(url_for("main.login"))
