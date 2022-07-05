<?php
  $host="localhost";
  $user="root";
  $password="qwerASDF1234!@#$";
  $db_name="YoutubeLab";
  
  $con = mysqli_connect($host,$user,$password,$db_name);
  
  if(mysqli_connect_errno()){
	  die("Failed to connect with MYSQL:".mysqli_connect_error());

  }       
?>

