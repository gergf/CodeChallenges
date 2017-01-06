Circle c; 

ArrayList<Circle> circles; 

void setup() {
  size(640, 360); 
  circles = new ArrayList<Circle>(); 
}

void draw() {
  background(0);
  
  int total = 10; 
  int count = 0;
  int attempts = 0; 
  int maxAttempts = 1000; 
  
  while ( count < total ) {
    Circle newC = newCircle(); 
    if (newC != null) {
      circles.add(newC);
      count++; 
    }
    attempts++; 
    if (attempts > maxAttempts){
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
            if ( (d - 2) < (c.r + another.r)){
              c.growing = false; 
              break;
            }
          }  
        }
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
    if ((d-2) < c.r) {
      valid = false;
      break;
    }
  }
  if (valid){
    return new Circle(x,y); 
  } else {
    return null; 
  }

}