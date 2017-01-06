Circle c; 

ArrayList<Circle> circles; 

void setup() {
  size(640, 360); 
  circles.add(new Circle(200,200)); 
}

void draw() {
  background(0); 
  for (Circle c : circles) {
    c.show();
  }
}