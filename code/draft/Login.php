<?php

session_start();

$host = 'localhost';
$user = 'root';
$dragon = ''; 
$database = 'dragon';

$connection = mysqli_connect($host, $user, $dragon, $database);

if (!$connection) {
    die("Connection Failed: " . mysqli_connect_error());
}

if (isset($_POST['btnlogin'])) { 

    $Username = $_POST['Username']; 
    $password = $_POST['password'];

    $query = "SELECT * FROM `signup` WHERE Username = '$Username' AND password = '$password'";

    $results = mysqli_query($connection, $query);

    if (mysqli_num_rows($results) > 0) {
        
        $_SESSION['Username'] = $Username;
        header('Location: templates/index.html');
        exit; 

    } else {
        echo "<script>
                alert('Invalid Username or Password!');
                window.location.href = 'login.html';
              </script>";
    }

    mysqli_close($connection);
}
?>