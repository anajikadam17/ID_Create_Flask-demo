// scripts.js

// a couple of different backgrounds to style the shop
var background1 = 'white';
var background2 = 'firebrick';

// this lets us toggle the background state
var color = true;

// every 1 second, switch the background color, alternating between the two styles
setInterval(function () {
  document.body.style.backgroundColor = (color ? background1 : background1)
  color = !color;
}, 1000);