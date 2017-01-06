class Circle {
 float x; 
 float y; 
 float r; 
 
 Circle(float x_, float y_) {
   x = x_; 
   y = y_;
   r = 50; 
 }
 
 void show() {
   stroke(255);
   strokeWeight(2); 
   noFill(); 
   ellipse(x,y,r*2,r*2);  
 } 
}