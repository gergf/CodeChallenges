// Straighforward line
function euclideanDistance(a,b){
	return dist(a.i, a.j, b.i, b.j); 
}

// Another heuristic 
function manhattanDistance(a,b){
	return abs(a.i - b.i) + abs(a.j - b.j); 
}
//
var cols = 40; 
var rows = 40; 
var grid = new Array(cols);
var wall_prob = 0.3; 

var openSet =  []; 
var closeSet = []; 
var start; 
var end; 

// to handle the size of each spot 
var w, h; 
var path = []; 

// Object to each spot in the grid 
function Spot(i, j){
	this.i = i; 
	this.j = j; 
 
	this.g = 0; 
	this.h = -1; 
	this.f = this.g + this.h; 

	this.neighbors = [];
	this.previous = undefined; 
	this.wall = false; 

	if (random(1) < wall_prob) {
		this.wall = true; 
	}

	this.show = function(color){
		if (this.wall)
			color = 0; 
		fill(color);
		noStroke(); 
		rect(this.i*w, this.j*h, w-1, h-1)
	}

	this.addNeighbors = function(grid){
		if( i < cols - 1) 
			this.neighbors.push(grid[this.i+1][this.j])
		if (i > 0) 
			this.neighbors.push(grid[this.i-1][this.j])
		if ( j < rows - 1)
			this.neighbors.push(grid[this.i][this.j+1])
		if ( j > 0) 
			this.neighbors.push(grid[this.i][this.j-1])

		// Diagonal neighbors 
		/*
		if (i > 0 && j > 0)
			this.neighbors.push(grid[this.i-1][this.j-1])
		if (i < cols - 1 && j > 0)
			this.neighbors.push(grid[this.i+1][this.j-1])
		if (i > 0 && j < rows - 1)
			this.neighbors.push(grid[this.i-1][this.j+1])
		if (i < cols - 1 && j < rows - 1)
			this.neighbors.push(grid[this.i+1][this.j+1])
		*/
	}

	this.updateCostValue = function(){
		this.f = this.g + this.h; 
	}

	this.updateHeuristic = function(end){
		this.h = manhattanDistance(this, end);
	}
}

function setup(){
	createCanvas(400,400);

	w = width / cols; 
	h = height / rows; 

	for (var i = 0; i < cols; i++){
		grid[i] = new Array(rows); 
	}

	for (var i = 0; i < cols; i++){
		for (var j = 0; j < rows; j++){
			grid[i][j] = new Spot(i, j); 
		}
	}
	for (var i = 0; i < cols; i++){
		for (var j = 0; j < rows; j++){
			grid[i][j].addNeighbors(grid); 
		}
	}

	// start at top-left 
	start = grid[0][0]
	// end at bottom-right 
	end = grid[cols-1][rows-1]
	end.wall = false; // end cant be a wall 

	openSet.push(start);
}

function draw() {

	// START A STAR ALGORITHM

	if (openSet.length > 0) {
		// keep going 
		var bestSpotIndex = 0; 
		for (var i = 0; i < openSet.length; i++){
			if(openSet[i].h == -1){
				// initialize value
				openSet[i].updateHeuristic(end); 
				openSet[i].updateCostValue();
			}
			if(openSet[i].f < openSet[bestSpotIndex].f){
				bestSpotIndex = i; 
			}
		}
		var current = openSet[bestSpotIndex]; 

		// if the current spot is the end 
		if (current === end){
			console.log("Finished!");
			noLoop();
		}

		openSet.splice(openSet.indexOf(current) , 1); 
		closeSet.push(current);

		// check every neighbor
		var neighbors = current.neighbors; 
		for (var i = 0; i < neighbors.length; i++){
			var neighbor = neighbors[i]; 
			// if the neighbor is not in the closeSet 
			if (!closeSet.includes(neighbor) && !neighbor.wall){
				var tmpG = current.g + manhattanDistance(neighbor, current);  

				// check if this post has been evaluated before
				if (openSet.includes(neighbor)){
					// if the new G is better than the old one 
					if (tmpG < neighbor.g){
						// update G 
						neighbor.g = tmpG; 
						// update previous 
						neighbor.previous = current;
					}
				}else{
					// if the neighbor is not in the openSet, add to the set
					neighbor.g = tmpG;
					neighbor.updateCostValue();
					openSet.push(neighbor)
					// update previous 
					neighbor.previous = current;
				}

				// heuristc 
				neighbor.h = manhattanDistance(neighbor, end); 
				// update f(n) = g(n) + h(n)
				neighbor.f = neighbor.g + neighbor.h; 
			}
		}
	}else{
		// no solution 
		console.log("There is no way to go from the start to the end"); 
		noLoop();
		return;
	}

	// END A STAR ALGORITHM

	background(0);

	// draw all the spots in the grid 
	for (var i = 0; i < cols; i++){
		for (var j = 0; j < rows; j++){
			grid[i][j].show(color(255));
		}
	}

	// close spots will be red 
	for (var i = 0; i < closeSet.length; i++) {
		closeSet[i].show(color(255,0,0));
	}

	// open spots will be blue 
	for (var i = 0; i < openSet.length; i++) {
		openSet[i].show(color(0,0,255));
	}

	//end spot will be purple
	end.show(color(128,0,128));

	//Find the path 
	path = []; 
	var aux = current;
	
	path.push(aux);
	while(aux.previous){
		path.push(aux.previous);
		aux = aux.previous;
	}
	
	// spots in the path will be yellow 
	for (var i = 0; i < path.length; i++) {
		path[i].show(color(255,255,0));
	} 
}