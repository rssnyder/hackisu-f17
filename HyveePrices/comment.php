<?php
  session_start();
  //Check if user is logged in
  if (isset($_SESSION['loggedin']) && $_SESSION['loggedin'] == true) {
    if($_SESSION['role'] != 2) {
      $_SESSION['error'] = true;
      $_SESSION['errorCode'] = "Not Permitted";
      header("Location: ../login.php");
      die("oops");
    }
  } else {
    $_SESSION['error'] = true;
    $_SESSION['errorCode'] = "Session Expired";
    header("Location: ../login.php?event=logout");
  }

  //TODO Grab all this from a file
  //Define sql database information
  $host="mysql.cs.iastate.edu";
  $port=3306;
  $socket="";
  $user="dbu309sab3";
  $password="SD0wFGqd";
  $dbname="db309sab3";
  //Connect to database
  $db = new mysqli($host, $user, $password, $dbname, $port, $socket) or die ('Could not connect to the database server' . mysqli_connect_error());

  $thread = $_GET['thread'];

  if($_GET['action'] == 'comment') {
    $comment = $_POST['comment'];

    //Check for empty comment
    if("" == trim($comment)) {
      header("Location: ../posts.php?class=" . $_GET['class'] . "&thread=" . $_GET['thread']);
      die("No comment");
    }

    //Get the values

    $parentID = $_POST['parentID'];
    //$comment = $_POST['comment'];
    $userID = $_SESSION['id'];
    $username = $_SESSION['username'];

    $query = "INSERT INTO replies
              (thread_id,
              owner_id,
              txt,
              user_name,
              parent)
              VALUES
              ($thread,
                $userID,
                '$comment',
                '$username',
                $parentID)";

    //Submit the comment
    $result = $db->query($query) or die($query);
    header("Location: ../posts.php?class=" . $_GET['class'] . "&thread=" . $thread);
    die("Comment posted.");
  }
  else if($_GET['action'] == 'flag') {
    $comment = $_GET['comment'];
    $query = "UPDATE replies
                SET
                flagged = 1
                WHERE ID = $comment";

    $result = $db->query($query) or die($query);
    header("Location: ../posts.php?class=" . $_GET['class'] . "&thread=" . $thread);
    die("Flag submitted.");
  }
  else if($_GET['action'] == 'flagThread') {
    $query = "UPDATE threads
                SET
                flagged = 1
                WHERE ID = $thread";

    $result = $db->query($query) or die($query);
    header("Location: ../posts.php?class=" . $_GET['class'] . "&thread=" . $thread);
    die("Flag submitted.");
  }
  else if($_GET['action'] == 'endorse') {
    $id = $_SESSION['id'];
    $comment = $_GET['comment'];
    $query = "UPDATE replies
                SET
                endorsed_user_id = $id
                WHERE ID = $comment";

    $result = $db->query($query) or die($query);
    header("Location: ../posts.php?class=" . $_GET['class'] . "&thread=" . $thread);
    die("Endorsed.");
  }
?>
