<?php
/* --------------------------------

module/simulation/dream2015_graph_work.php
dream2015 그래프를 그리는 ajax 페이지.

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
$drug2 = $_GET["drug2"];


$sql = "
SELECT *
FROM dream2015
WHERE CELL_LINE = '$cellline' AND COMPOUND_A='$drug1' AND COMPOUND_B='$drug2'
UNION
SELECT *
FROM dream2015
WHERE CELL_LINE = '$cellline' AND COMPOUND_A='$drug2' AND COMPOUND_B='$drug1'
ORDER BY PREDICTION ASC
";
$result = $conn->query($sql);


$outp = '{"cols":[{"type":"string"},{"type":"number"}],"rows": [';
while($row = $result->fetch_assoc()) {
    if ($outp != '{"cols":[{"type":"string"},{"type":"number"}],"rows": [') {$outp .= ",";}
    $outp .= '{"c":[{"v":"'. $row["CELL_LINE"] .', '. $row["COMPOUND_A"] .', '. $row["COMPOUND_B"] . '"},{"v":' . $row["PREDICTION"] . '}]}';
}
$outp .="]}";

echo $outp;

/* 아래와 같은 JSON 구조가 되어야 한다.
$outp = '{
	"cols": [
	{"type":"string"},{"type":"number"}
	],
	"rows": [
	{"c":[{"v":"Mushrooms"},{"v":3}]},
	{"c":[{"v":"Mushrooms"},{"v":4}]},
	{"c":[{"v":"Mushrooms"},{"v":5}]},
	{"c":[{"v":"Mushrooms"},{"v":6}]},
	{"c":[{"v":"Mushrooms"},{"v":7}]}
	]
}';
*/
?>