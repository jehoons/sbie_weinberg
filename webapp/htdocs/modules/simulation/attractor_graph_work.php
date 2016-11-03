<?php
/* --------------------------------

module/simulation/attractor_graph_work.php
attractor 그래프를 그리는 ajax 페이지.

*ajax 오류 점검 :
1. form action에 정확한 주소가 입력 되었는가?
2. 전송하는 데이터가 잘 들어가는가?
3. 해당 주소의 페이지가 정당한 json 형식을 가지는가?

-------------------------------- */

//__CL__ 정의 되지 않았다면 false 를 return.
if(!defined('__CL__')) exit();

// php 페이지 로딩 시간을 최대 5분(60*5)으로 연장. default는 30초.
ini_set('max_execution_time', 300);

$node1 = $_POST["node1"]; // On is 1, Off is null
$node2 = $_POST["node2"]; // On is 1, Off is null
$node3 = $_POST["node3"]; // On is 1, Off is null
$node4 = $_POST["node4"]; // On is 1, Off is null
$node5 = $_POST["node5"]; // On is 1, Off is null

$target1 = $_POST["target1"];
$target1_on = $_POST["target1_on"]; // On is 1, Off is null
$target2 = $_POST["target2"];
$target2_on = $_POST["target2_on"]; // On is 1, Off is null

/*
$sql = "
SELECT *
FROM attractor
WHERE 
select attractors, state_key from attractor where input_nodes='00000' and column_get(target1, 'target1' as char)='S_Gli' and column_get(target1, 'target1_state' as char)='0' and column_get(target2,'target2' as char)='' and column_get(target2, 'target2_state' as char)='0';
";
$result = $conn->query($s ql);
*/

echo '{"node1":"'.$node1.'", "node2":"'.$node2.'", "node3":"'.$node3.'" , "node4":"'.$node4.'" , "node5":"'.$node5.'" , "target1":"'.$target1.'" , "target1_on":"'.$target1_on.'" , "target2":"'.$target2.'" , "target2_on":"'.$target2_on.'" }';
?>