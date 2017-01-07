var order = 3; 
var ngrams = {};
var beginnings = [];
var button; 
var outputSize = 50; 

function preload() {
	corpus = loadStrings('sex.txt'); 
}

function setup() {
	noCanvas(); 
	// Loop everu phrase in corpus 
	for (var i = 0; i < corpus.length; i++){
		var phrase = corpus[i];
		// split into words 
		phrase = phrase.split(" ") 
		// make ngrams of the words in that phrase 
		for (var j = 0; j <= phrase.length - order; j++) {
			// build gram 
			var gram = phrase.slice(j, j+order);
			gram = gram.join(" "); 
			// if it's the first, add to beginnings list 
			if ( j == 0 ) {
				beginnings.push(gram); 
			}
			// if it has not seen before, then
			if (!ngrams[gram]) {
				ngrams[gram] = [];
			}
			// add the word that follows that gram 
			ngrams[gram].push(phrase[j+order]);  
		}
	}

	// GUI // 
	button = createButton("Generate"); 
	button.mousePressed(markovIt); 
	// console.log(ngrams); 
}

function markovIt() {
	// Get a random gram from the beginnings list 
	var currentGram = random(beginnings); 
	var result = currentGram; 

	// Generate 
	for (var i = 0; i < outputSize; i++){
		// get the possible followers to that gram 
		var possibilites = ngrams[currentGram]; 
		// if the list is null, end
		if (possibilites[0] == undefined){
			console.log(result)
			break; 
		}
		// get next word 
		var next = random(possibilites);
		// add to the current phrase 
		result += " " + next;
		// transfor string into array to update n-Gram
		result = result.split(" "); 
		// update current n-Gram 
		var len = result.length;
		currentGram = result.slice(len-order, len).join(" ");
		// array into string again 
		result = result.join(" ")
	} 

	createP(result); 
}
