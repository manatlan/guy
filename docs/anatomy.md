# Anatomy : how it works

A guy's app can be seen as a single application. It could be true for `app` & `cef` mode. 

Under the hood : it's basically 2 things:

* [Server Side](server.md) : An http & socket server
* [Client Side](client.md) : A javascript lib which make the glue with the server.

For `app` & `cef` mode : guy run the two in a windowed app. (there is one server & one client)

For `server` mode : guy run the server, and a classical browser can be a client, when connected. (there is one server & many clients)

In all cases : the http server serve the client as a html component. And the client communicate with the server with a websocket.

!!! info
    Although there is always a http server running, under the hood. Only the one in server mode is listening wide (0.0.0.0) to accept connections
    from all the world ;-). Thoses in app/cef mode are listening on localhost only (can't accept connections from another computer)

Technically : it's the marvellous [tornado](https://www.tornadoweb.org/en/stable/), an asynchronous networking library which handle http & socket. So **guy** can work for python >= 3.5 (ready for raspberry pi !)