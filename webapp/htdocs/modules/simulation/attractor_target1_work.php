<?php
/* --------------------------------

module/simulation/attractor_target1_work.php
attractor target1 값을 가져오는 ajax 페이지.

*ajax 오류 점검 :
1. form action에 정확한 주소가 입력 되었는가?
2. 전송하는 데이터가 잘 들어가는가?
3. 해당 주소의 페이지가 정당한 json 형식을 가지는가?

-------------------------------- */

//__CL__ 정의 되지 않았다면 false 를 return.
if(!defined('__CL__')) exit();

$sql = "
SELECT *
FROM targets
";
$result = $conn->query($sql);


$outp = "[";
while($row = $result->fetch_assoc()) {
    if ($outp != "[") {$outp .= ",";}
    $outp .= '{"target1":"'  . $row["ta_target"] . '"}'; 
}
$outp .="]";
	
echo $outp;
?>