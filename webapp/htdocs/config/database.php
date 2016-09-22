<?php
/* --------------------------------

config/database.php
MySQL 연결과 관련 함수 설정.

-------------------------------- */

//  __CL__ 정의 되지 않았다면 false 를 return.
if(!defined('__CL__')) exit();

// 호스트, 사용자, 비밀번호, 사용하는 database 설정
$servername = "localhost";
$username = "root";
$password = "5262";
$dbname = "kaist";

// Connect
$conn = new mysqli($servername, $username, $password, $dbname);
 // Check connection
 if ($conn->connect_error) {
     die("Connection failed: " . $conn->connect_error);
}
?>