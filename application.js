var config = {
  apiKey: "AIzaSyDSWybeVpfp7uxYIgkt6iAF4GRz1jQdlT8",
  authDomain: "vnvn-c0fb4.firebaseapp.com",
  databaseURL: "https://vnvn-c0fb4.firebaseio.com",
  projectId: "vnvn-c0fb4",
  storageBucket: "vnvn-c0fb4.appspot.com",
  messagingSenderId: "321513539224"
};

// Initialize your Firebase app
firebase.initializeApp(config);

// Reference to the comment's object in your Firebase database
var comments = firebase.database().ref("comments");


// Save a new comment to the database, using the input in the form
var submitComment = function () {

  var title = $("#yourName").val();
  var remark = $("#yourComment").val();
  //var link = $("#yourLink").val();

  comments.push({
    "title": title,
    "remark": remark,
    //"link": link
  });
};


comments.limitToLast(10).on('child_added', function(childSnapshot) {

  comment = childSnapshot.val();

  $("#title").prepend(comment.title + '<br> <br>')
  $("#remark").prepend(comment.remark + '<br> <br>')
  //$("#link").prepend(comment.link + '<br> <br>')

  // Make the link actually work and direct to the URL provided
  //$("#link").attr("href", comment.link)
});


// When the window is fully loaded, call this function.
$(window).load(function () {
  $("#commentForm").submit(submitComment);
});
