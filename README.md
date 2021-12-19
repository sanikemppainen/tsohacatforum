# Cat Forum 

The Cat Forum is a place where users can discuss all things related to cats. In addition to a forum with threads on various topics, there s a voting page where a competition on 'the cutest cat' is always ongoing. 

This website was created using Flask, PostgreSQL, Python, CSS and HTML and is deployed in Heroku.

https://catforum.herokuapp.com/

When opening the forum, the user will see list of threads along with information on when and by who it was created by. Threads are in order of the latest one created being the top one. Messages in threads are the opposite, so the first message is the top one. There is a search button, an option to choose how many threads are shown, information on number of topics and the most popular (most commented) thread. There is a navigation bar with links to login page, registeration page, admin oage and voting page.

## Functions  

There are three types of users. An unregistered visitor, a registered user and an admin user and they all have different level of functions at their disposal.

Unregistered visitors can:
<ul>
  <li>Scroll through threads and read messages
  <li>See who created a thread or a message and when it was created. Also tags are visible. 
  <li>Vote for their favourite cat
  <li>See how many threads there are and which one has the most messages
  <li>Search tags, topics and messages with a key word
  <li>Decide how many threads are shown per page
  <li>Create a new user account by registering as a user
</ul>

In addition to previously mentioned functions, registered users can also:
<ul>
  <li>Login
  <li>Start a new thread by writing the first message and topic. This also includes functionality to add a picture and/or a tag to the thread. 
   <li>Send a new message to an existing thread. This also includes functionality to send a photo along with the messageS
   <li>They can see if they are logged in or not and which uesr they are logged in as. 
</ul>

In addition to previously mentioned functions, admin user can also:
<ul>
  <li>Access the admin page
  <li>Delete users and/or threads by username or thread topic name
</ul>

Admin functionality can be tested with the following user:
username: adm
password: adm

## User experience
User experience has been taken into consideration when creating the forum. For example, if the user is trying to register a new user or log in whilst already being logged in, the website sends a message informing that this is not possible. There is also a browser warning if the user tries to create a thread or send a message without a topic or a message.

User safety was also noted by making the application resistant against SQL injections and taking notes of XSS and csfr vulnerabilities.

