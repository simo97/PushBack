PushBack, Notification server
=======================

A light and very simple notification server for web apps based on WebSockets. PushBack is a self-hosted notification server built to be use in a web application. It is design to be very simple of use and lightweight.

## How it work ?

PushBack has been design to be simple a usage, from server to server or server to client. It work in a simple way, 4 steps to be specific :

* **Application creation**

All notifications which is been carried out through PushBack should be tied to an application, so all you need to do, is to create an application in your account, after which you will have an application's token which should be use in every request to the server.

At this level, the server already "knows" your application and you have an application token.

* **Users registration**

You should now register all your users in the notification server and the application, registering all the users is not about saving their first name etc, it is only about user's ID, in fact you will just provide a list (array) of those ID ```[id1, id2, etc]```. The concerned endpoint is : 
``` /api/v1/register/```

At this level the server already "knows" your users.

* **Send notifications**

Sending a notification is quite simple, it is a POST request to a HTTP endpoint on PushBack server:
```/api/v1/notify/```
the query's parameter are :

  - ```users``` : list of user concern by the notification 
  - ```conntent``` : the notification content, ideally it should be a JSON data but you are free to use any kind of text based content. 
  - ```app_token``` : the token related to your application.*

* **Receive a notification**

A javascript client sdk is available to enable a connected user to listen for the notification from the server, using it just require a pass the current user's ID and 2 callbacks, one to perform an action when a notification happen and a second when it is disconnected to the server. Here is a sample of code : 
```javascript
<script src="/static/core/js/pusher.js" ></script>
<script>
  PushBack.init(APP_TOKEN_HERE, USER_ID);
  PushBack.subscribe(
      function(e) {
          // when a notification happen
          console.log(e.data)
          alert(e.data);
      },
      function(e) {
          // when disconnected to the WS server (for example when changing a page)
          alert('deconnection');
      }
  );
</script>
```
That is all, you need to receive a notification, no need to embed the application's token in you client code.

## How to deploy it locally

Since it is a normal django application the deployment method it quite simple, here are the steps ( assuming you already have a python development evironment ready, if not check out this video : [Setup a dev env for python on ubuntu (french)](https://www.youtube.com/watch?v=z-EOW4qVM8Y)). You will also need to install [redis server](https://redis.io/) and let it run on the default port.

- Download this repo as a zip or clone it:
```bash
$ git clone https://github.com/simo97/PushBack.git
```
- Go inside the ```PushBack``` dir and install requirements:
```bash
$ cd PushBack/
$ pip install -r requirements.txt
```
- Initialise the databse and deine a admin user :
```bash
$ python manage.py createsuperuser
```
- Run the application :
```bash
$ python manage.py runserver
```

**It's done** the server will be available a [localhost:8000]('localhost:8000')

*You are done* 

## TODO

- write tests
- catch exceptions when errors happen
- fix eventual bugs

## Roadmap 

What i am planning for this project :
- Add a bootstrap template on it to let user browse it applicaitons and other content ( notifications, statistics, etc)
- Add a module for statistics (received notifications, delivered notification, etc)
- Add features for text based chat
- Add docker support
- **look for more ideas** ;-) 

## Contributing

You want to contribute ? it is simple just :
- *fork this repo*
- *made modifications, features, etc*
- *made a PR on a new branch named as the added feature , eg: **feat-statistic***

[PushBack Cloud](http://pushback-server.herokuapp.com/)
