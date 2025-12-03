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

if (isset($_POST['btnregister'])) {
    $Firstname = $_POST['Firstname'];
    $Lastname = $_POST['Lastname'];
    $Username = $_POST['Username'];
    $age = $_POST['age'];
    $password = $_POST['password'];
    $Email = $_POST['Email'];

    $query = "INSERT INTO signup (Firstname, Lastname, Username, age, password, Email) VALUES ('$Firstname', '$Lastname', '$Username', '$age', '$password', '$Email')";
    
    $results = mysqli_query($connection, $query);

    if ($results) {
        // Javascript to show a popup and then redirect
        echo "<script>
                alert('Registration Successful! Please Login.');
                window.location.href = 'login.html';
              </script>";
        exit; 
    } else {
        echo "Error: " . mysqli_error($connection);
    }

    mysqli_close($connection);
}
?>