<?php
  include('connection.php');
  $username=$_POST['user'];
  $password=$_POST['pass'];

  $sql="select * from user where username = '$username' and password='$password'";

  $result=mysqli_query($con,$sql);
  $count=mysqli_num_rows($result);

  if($count==1){
	  echo"<h1><center>Login Success</center></h1>";
		 }
  else{
	  echo"<h1>Login Failed </h1>";
		 }
  
?>
