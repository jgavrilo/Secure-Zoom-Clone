# Secure-Zoom-Clone
In one terminal go to the project directory and implement the following commands:
npm i express ejs socket.io
npm i uuid
npm i --save-dev nodemon

These three lines are our dependencies:
Express is the server we are using
Ejs as our templating language for our rooms
Socket.io allows for communication with the server
Uuid allows us to create our room url's
Nodemon is our dev dependency which allows for us to refresh the server while we work on it

Finally run the following command to run the server:
npm run devStart

In a second terminal go to the project directory and implement the following commands:
code .
npm install
peerjs --port 3001

This allows other users to joing the room and communicate with people in it
