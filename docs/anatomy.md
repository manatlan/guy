# Anatomy : how it works

A guy's app can be seen as a single application. It could be true for `app` & `cef` mode. 

Under the hood : it's basically 2 things:

* [Server Side](server.md) : An http & socket server
* [Client Side](client.md) : A javascript lib which make the glue with the server.

For `app` & `cef` mode : guy run the two in a windowed app. (there is one server & one client)

For `server` mode : guy run the server, and a classical browser can be a client, when connected. (there is one server & many clients)

In all cases : the http server serve the client as a html component. And the client communicate with the server with a websocket.