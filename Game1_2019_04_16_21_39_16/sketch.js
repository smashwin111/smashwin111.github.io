let value = 0
let value2 = 0
let circlex = 0
let circley = 200
let rectx = 0
let recty = 0
let lives = 100

circlesy = []



x = 300
y = 100

function setup() {
  createCanvas(400, 400);
  i = 0

  for (k=0; k<3; k=k+1) {
    circlesy.push(100+k*100)
  }

}

function draw() {
  background(120);
  fill(50,50,50)

  for (k=0; k<3; k=k+1) {
    circle(circlex, circlesy[k], 20)
  }
  
  /*
  for (let y of circlesy) {
     circle(circlex,y,20)
  }
  */
  
  if (i < 400) {
    circlex = i
  }
  else {
    circlex = 800-i 
  }
  if (i > 800) {
    i = 0
  }
  i = i + 3
  
  rect(200+value,300+value2,20,40,20)
  rectx = 200+value 
  recty = 300+value2
  
  for (let y of circlesy) {
    if (dist(circlex, y, rectx+10, recty+20) < 20) {
       lives = lives - 1 
    }
  }
  rect(x,y,10,10)
  
  if (dist(x,y,rectx,recty) < 25) {
    temp = x
    x = y
    y = temp
    lives = lives + 10
  }
  
  text(lives, 300,50)
  
}

function keyPressed() {
  if (keyCode === LEFT_ARROW) {
    value = value-10;
  } else if (keyCode === RIGHT_ARROW) {
    value = value+10;
  } else if (keyCode === UP_ARROW) {
    value2 = value2-10 
  } else if (keyCode === DOWN_ARROW) {
    value2 = value2+10 
  }
  
}

