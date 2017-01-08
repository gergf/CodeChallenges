var n = 0; // point order first, second, third...
var c = 3; // scaling factor 
var maxPoints = 1000; 
var angle = 137.5; 
var angleTwo = 137.3;

// flowerTwo 
var raiseColor = true; 

// colors 
var f1_color = 0; 
var f2_color = 0; 


function setup() {
	createCanvas(300,300);
	angleMode(DEGREES); 
	colorMode(HSB); 
	background(0); 
}


function draw(){

	flowerThree(); 
	// each frame is a new point
	n++; 
	if ( n > maxPoints){
		noLoop();  
		console.log("Finished"); 
	}
}

function flowerOne() {
	// Polar coord of the point 
	var phi = n * angle; 
	var r = c * sqrt(n); 
	// Polar to cartesian, centered in the screen
	var x = r * cos(phi) + width/2; 
	var y = r * sin(phi) + height/2; 

	fill(f1_color, 255, 255);
	noStroke(); 
	ellipse(x, y, 4, 4); 

	// update colors 
	f1_color = (f1_color + 1)%256;
}

function flowerTwo() {
	// Polar coord of the point 
	var phi = n * angle; 
	var r = c * sqrt(n); 
	// Polar to cartesian, centered in the screen
	var x = r * cos(phi) + width/2; 
	var y = r * sin(phi) + height/2; 

	fill(f2_color, 255, 255);
	noStroke(); 
	ellipse(x, y, 4, 4); 

	// update color 
	if (f2_color == 255){
		raiseColor = false; 
	}
	if (f2_color == 0){
		raiseColor = true; 
	}

	if (raiseColor)
		f2_color++; 
	else 
		f2_color--; 
}

function flowerThree() {
	// Polar coord of the point 
	var phi = n * angleTwo; 
	var r = c * sqrt(n); 
	// Polar to cartesian, centered in the screen
	var x = r * cos(phi) + width/2; 
	var y = r * sin(phi) + height/2; 

	fill(f2_color, 255, 255);
	noStroke(); 
	ellipse(x, y, 4, 4); 

	// update color 
	if (f2_color == 255){
		raiseColor = false; 
	}
	if (f2_color == 0){
		raiseColor = true; 
	}

	if (raiseColor)
		f2_color++; 
	else 
		f2_color--;  
}