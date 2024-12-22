<?php 
$servername = "localhost"; 
$username = "root"; // Adjust accordingly 
$password = ""; // Adjust accordingly 

// Create connection 
$conn = new mysqli($servername, $username, $password); 

// Check connection 
if ($conn->connect_error) { 
    die("Connection failed: " . $conn->connect_error); 
}

// SQL to create database 
$sql = "CREATE DATABASE StudentDB"; 
if ($conn->query($sql) === TRUE) { 
    echo "Database StudentDB created successfully"; 
} else { 
    echo "Error creating database: " . $conn->error; 
}

$conn->close(); 
?>
