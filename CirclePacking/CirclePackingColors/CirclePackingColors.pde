Circle c; 

ArrayList<Circle> circles; 
ArrayList<PVector> spots; 
PImage img; 

void setup() {
  size(714, 714); 
  spots = new ArrayList<PVector>(); 
  circles = new ArrayList<Circle>(); 
  img = loadImage("me.jpg");
  img.loadPixels(); 
  background(200);
}

void draw() {
  
  int total = 50; 
  int count = 0;
  int attempts = 0; 
  int maxAttempts = 2000; 
  
  while ( count < total ) {
    Circle newC = newCircle(); 
    if (newC != null) {
      circles.add(newC);
      count++; 
    }
    attempts++;   
    if (attempts > maxAttempts){
      save("cool_me.png");
      noLoop();
      println("FINISHED"); 
      break;
    }
  }
  
  for (Circle c : circles) {
    if (c.growing){
      // if the circles touchs the edges STOP GROWING
      if (c.edges()){
        c.growing = false; 
      } else {
        // if the circle touchs another circle STOP GROWING
        for (Circle another : circles) {
          if ( c != another ) {
            float d = dist(c.x, c.y, another.x, another.y); 
            if ( (d) < (c.r + another.r)){
              c.growing = false; 
              break;
            }
          }
        } // end for // 
      }
    }
    c.show();
    c.grow();
  }
}

Circle newCircle(){ 
  
  float x = random(width);
  float y = random(height); 
  
  boolean valid = true; 
  for (Circle c : circles){
    // distance from the point x,y to the center of the circle 
    float d = dist(x,y,c.x,c.y);
    // the point is inside the circle 
    if ((d) < c.r) {
      valid = false;
      break;
    }
  }
  if (valid){
    int index = int(x) + int(y) * img.width; 
    return new Circle(x,y, img.pixels[index]); 
  } else {
    return null; 
  }

}