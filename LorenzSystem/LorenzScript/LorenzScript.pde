import peasy.*;
import peasy.org.apache.commons.math.*;
import peasy.org.apache.commons.math.geometry.*;

// Camara 
PeasyCam cam; 

// Lorenz system 
float x = 0.01; 
float y = 0; 
float z = 0; 

float phi = 10; 
float beta = 28; 
float rho = 8.0 / 3.0; 

// Gui 
boolean growing = true; 
ArrayList<PVector> points = new ArrayList<PVector>(); 

void setup() {
  size(800, 600, P3D);
  colorMode(HSB); 
  cam = new PeasyCam(this, 0,0,0, 1000); 
}

void draw() {
  background(0); 

  float dt = 0.01; 
  float dx = (phi * (y - x)) * dt;
  float dy = (x * (beta - z) - y) * dt;
  float dz = (x * y - rho * z) * dt;

  x = x + dx; 
  y = y + dy; 
  z = z + dz; 
  
  points.add(new PVector(x,y,z)); 

  scale(5); 
  noFill(); 
   
  LorenzSystem(); 
}

void LorenzSystem(){
  float hu = 0; 
  beginShape(); 
  for(PVector v : points){
    stroke(hu, 255, 255); 
    vertex(v.x, v.y, v.z);
    // Update direction 
    if (hu > 254)
      growing = false; 
    else if(hu <= 1)
      growing = true; 
    // Update color 
    if (growing) 
      hu += 0.5; 
    else 
      hu -= 0.5; 
  }
  endShape(); 
}