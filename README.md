# django-blog
### Description
Django blog app that performs the following functionality:
* #### Database:
  * Model Post (id, author, title, content, date created, views count, status, likes, dislikes) - it is a post with an author, title, content, date of publication, a post view counter that displays the number of times the post has been viewed, the status of the post, which indicates whether the post has been published or is under moderation, the number of likes and dislikes.
  * Model Comment (id, post, author, content, date created, status) - it represents comments related to the post to which this comment belongs, having the author of the comment, the content, the date and time of creation, the status of the comment, which indicates whether the comment has been published or it is under moderation.
* #### Views:
  * ListView / - the home page where the posts are located
  * DetailView post/<int:pk>/ - the page that displays a specific post, has a column with the most popular posts, allows you to like/dislike and leave a comment
  * CreateView make_post/ - the page that allows you to create a post
  * UpdateView edit_post/<int:pk>/ - the page that allows you to edit the post
  * DeleteView delete_post/<int:pk>/ - the page that allows you to delete the post
  * CreateView register/ - registration page
  * LoginView login/ - login page
* #### Moderation
  When you create or edit a post, or leave a comment on any post, moderation is emulated using Celery and the Redis broker: within 3-5 seconds, this task is "moderating", and then its status changes to "published".
* #### Notifications
  After your post or comment gets the status "published", using Django Channels via the websocket using the Redis channel layer backend, you will receive a notification of successful publication, no matter which blog page you are on.
* #### Containerization
  All services are deployed using docker compose.

## Technologies
* Python
* Django
* PostgreSQL
* Django Channels
* Redis
* Celery
* Docker Compose

## Installation and usage
Clone the repository
```
git clone git@github.com:fooniquler/django-blog.git
```
Go to the django-blog directory
```
cd django-blog
```
Run docker-compose
```
docker-compose up --build
```
