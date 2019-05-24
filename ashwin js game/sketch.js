
// Your web app's Firebase configuration
var firebaseConfig = {
  apiKey: "AIzaSyBRrqkX8m1u5oFNCBreqsnzIRoz_2d9GUY",
  authDomain: "leaderboard-b02d4.firebaseapp.com",
  databaseURL: "https://leaderboard-b02d4.firebaseio.com",
  projectId: "leaderboard-b02d4",
  storageBucket: "leaderboard-b02d4.appspot.com",
  messagingSenderId: "764742816924",
  appId: "1:764742816924:web:64d83e192c59088f"
};
// Initialize Firebase
firebase.initializeApp(firebaseConfig);

let database = firebase.database()

let x = 200
let y = 200
let x2 = 300
let y2 = 150
let speed = 2
let score = 0
let x3 = [50,200,350,500,650]
let y3 = [50,150,250,350,450]
let direction = [1,1,1,1,1]
let enemy_length = 5
let time = 10
let name
let whatever = document.getElementById("whatever")
let scores = {}

  
function setup() {
  createCanvas(windowWidth, windowHeight);
  s = width/700
}

function draw() {
  if (time > 0) {
  background(220);
  text("time: " + time.toFixed(0), 50, 100)
  //x = x + 1
  //y = y + 1
  
  fill(50)
  circle(x*s,y,40*s)
  
  if (width > 350) {
	  if (keyIsDown(LEFT_ARROW)) {
	    x = x-4
	  }
	  if (keyIsDown(RIGHT_ARROW)) {
	    x = x+4
	  }
	  if (keyIsDown(UP_ARROW)) {
	    y = y-4
	  }
	  if (keyIsDown(DOWN_ARROW)) {
	    y = y+4
	  }
  }
  else {
	x = mouseX
	y = mouseY
	  }
    
  fill(0,255,0)
  circle(x2*s, y2, 30*s)
  x2 = x2 + 4
  
  if (x2*s > width) {
    x2 = 0
  }
  
  for (i=0; i<enemy_length; i=i+1) {
    fill(255,0,0)
    circle(x3[i]*s, y3[i], 25*s)

    if (dist(x*s,y,x3[i]*s,y3[i]) < 40*s + 25*s) {
      score = score - 1
    }

    y3[i] = y3[i] + 3*direction[i]

    if (y3[i] > height || y3[i] < 0) {
      direction[i] = direction[i]*-1
    }
  }
  
  fill(0,0,0)
  textSize(25)
  text("score: " + score, 50, 50)
  
  if (dist(x*s,y,x2*s,y2) < 30*s + 40*s) {
    score = score + 1
  
  }
  
  if (score > 200 && score < 300) {
    x3.push.apply(x3, [220, 350])
    direction.push.apply(direction, [1,1])
    y3.push.apply(y3, [250,350])
    enemy_length = 7 
  }
  if (score >= 300) {
    x3.push.apply(x3, [270, 380])
    direction.push.apply(direction, [1,1])
    y3.push.apply(y3, [250,350])
    enemy_length = 9 
  }
  

  time = time - 0.03
  }
  else {
    whatever.innerHTML = "Name? <input id='idk'> <input type='submit' onclick='submit()'> <button onclick='generate_alltime_leaderboard()'>All-time Leaderboard</button>"
    noLoop()
  }
  
}

function submit() {
  name = idk.value
	database.ref(name).set(score)
  if (name != "") {
    scores[name] = score
  }
  alert("Scoreboard: " + JSON.stringify(scores,null,1))
  time = 10
  score = 0
  loop()
  whatever.innerHTML = ""
  leaderboard()
}

function leaderboard() {
  values = Object.values(scores)
  names = Object.keys(scores)
  
  if (names.length > 2) {
    let leaders = {}
    for (i=0; i<3; i=i+1) {
      max = Math.max(...values)
      index = values.indexOf(max)
      leaders[names[index]] = max
      names.splice(index,1)
      values.splice(index,1)
    }
    alert("Leaderboard: " + JSON.stringify(leaders,null,1))
  }
}

function generate_alltime_leaderboard() {
	let alltime_leaderboard = { }
	database.ref().orderByValue().limitToLast(3).on("value", function(snapshot) {
		snapshot.forEach(function(data) {
  	   //alert(data.key + " : " + data.val())
		alltime_leaderboard[data.key] = data.val()
		});
    });
	if (Object.values(alltime_leaderboard).length > 0) {
		alert("All-time leaderboard: " + JSON.stringify(alltime_leaderboard,null,1))
    }
}

generate_alltime_leaderboard()
