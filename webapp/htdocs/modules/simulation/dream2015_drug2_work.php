<?php
/* --------------------------------

module/simulation/dream2015_drug2_work.php
dream2015 module의 drug2 쿼리 get 방식의 ajax 페이지.

*ajax 오류 점검 :
1. form action에 정확한 주소가 입력 되었는가?
2. 전송하는 데이터가 잘 들어가는가?
3. 해당 주소의 페이지가 정당한 json 형식을 가지는가?

-------------------------------- */

//__CL__ 정의 되지 않았다면 false 를 return.
if(!defined('__CL__')) exit();

// php 페이지 로딩 시간을 최대 5분(60*5)으로 연장. default는 30초.
ini_set('max_execution_time', 300);

$cellline = $_GET["cellline"];
$drug1 = $_GET["drug1"];

// choonlog_member, choonlog_book 쿼리
$sql = "
SELECT CELL_LINE, COMPOUND_A, COMPOUND_B, PREDICTION
FROM dream2015
WHERE CELL_LINE = '$cellline' AND COMPOUND_A='$drug1'
GROUP BY COMPOUND_B
UNION
SELECT CELL_LINE, COMPOUND_B, COMPOUND_A, PREDICTION FROM dream2015
WHERE CELL_LINE = '$cellline' AND COMPOUND_B='$drug1'
GROUP BY COMPOUND_A;
";
$result = $conn->query($sql);


$outp = "[";
while($row = $result->fetch_assoc()) {
    if ($outp != "[") {$outp .= ",";}
    $outp .= '{"COMPOUND_B":"'  . $row["COMPOUND_B"] . '"}'; 
}
$outp .="]";
	
echo $outp;
?>