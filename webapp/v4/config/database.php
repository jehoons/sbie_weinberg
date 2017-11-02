<?php
/* --------------------------------

config/database.php
MySQL 연결과 관련 함수 설정.

-------------------------------- */

//  __CL__ 정의 되지 않았다면 false 를 return.
if(!defined('__CL__')) exit();

/*
weinberg.kaist.ac.kr
$servername = "localhost";
$username = "root";
$password = "sbl4365";
$dbname = "weinberg";

localhost
$servername = "localhost";
$username = "root";
$password = "5262";
$dbname = "kaist";
*/

$servername = "localhost";
$username = "root";
$password = "sbl4365";
$dbname = "v4";

// Connect
$conn = new mysqli($servername, $username, $password, $dbname);
 // Check connection
 if ($conn->connect_error) {
     die("Connection failed: " . $conn->connect_error);
}
?>