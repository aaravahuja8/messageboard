Website: Video Game Forums by Aarav Ahuja

All images used are free stock images sourced from unsplash.com

To run this website, open the project folder on the terminal and set "export FLASK_APP=flasky" and run "flask run".

This website is a video game forum site where users can sign up for accounts and log in and then post messages on the message board as well as comment on those messages. The message board utilizes an infinite scrolling system where posts are progressively loaded in order of most recent to least until the end is reached. Each post's title can be clicked on to view only that post along with its comments from oldest to newest. A user must be logged in in order to post or comment, and this is verified using the flask login system. Each user also has their own profile which shows their details (and your email address if you are logged in seeing your own profile) and their most recent posts in pages of 5 each. The home page also has a link that takes you to the most recent post made.

Navigation is done through the navigation bar on top, which shows the home page and the message board on the left, and the log in and sign up pages on the right. All posts, comments, and the option to create a new post can be accessed through the message board. Once a user is logged in, the log in and sign up pages are replaced with the user's profile page and a log out page on the navigation bar.

Important URLs:
/ for the home page
/board for the full message board
/login to log in
/signup to sign up
/logout to log out (login required)
/users/<username> to view a user's profile
/posts/<postid> to view a specific post and its comments
/newpost to make a new post (login required)

The database has 3 tables, one to store the user data, one to store the post data, and one to store the comment data. The user table is linked to the post table in a one to many relationship, and so is the post table linked to comment table in a one to many relationship. The comment table also has a foreign key to indicate which user posted that comment. All tables have been set to empty for you to test the creation of users, posts, and comments.

Additional requirements completed:
1. User authentication
2. Additional database interactions (3 tables, all with insertion and deletion on posts (and deleting a post deletes its comments too))
3. AJAX utilized on board.html for the infinite scrolling