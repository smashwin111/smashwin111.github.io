var config = {
    apiKey: "AIzaSyD90XsWJOANcVOu11tyrWUt0aDv0EBysX0",
    authDomain: "newcomments-4e8a0.firebaseapp.com",
    databaseURL: "https://newcomments-4e8a0.firebaseio.com",
    projectId: "newcomments-4e8a0",
    storageBucket: "",
    messagingSenderId: "182797535899"
};

// Initialize your Firebase app
firebase.initializeApp(config);

// Reference to the comment's object in your Firebase database
var comments = firebase.database().ref("comments");


// Save a new comment to the database, using the input in the form
var submitComment = function () {

  var title = $("#yourName").val();
  var remark = $("#yourComment").val();
  var link = $("#yourLink").val();

  comments.push({
    "title": title,
    "remark": remark,
    "link": link
  });
};

comments.limitToLast(10).on('child_added', function(childSnapshot) {

  comment = childSnapshot.val();

  $("#title").prepend('<tr><td>' + comment.title + '</td></tr>' + '<br> <br>')
  $("#remark").prepend('<tr><td>' + comment.remark + '</td></tr>' + '<br> <br>')
  $("#link").prepend('<tr><td><img id="image"></td></tr>' + '<br> <br>')

  
  var altWords = 'No \n Image'  
  // Make the link actually work and direct to the URL provided
  $("#image").attr("src", comment.link)
  $("#image").attr("alt", altWords) 
});


// When the window is fully loaded, call this function.
$(window).load(function () {
  $("#commentForm").submit(submitComment);
});
