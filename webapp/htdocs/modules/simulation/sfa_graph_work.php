<?php
/* --------------------------------

module/simulation/sfa_graph_work.php
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

$cell_name = $_POST["cell"];
$drug1 = $_POST["target1"];
$drug2 = $_POST["target2"];;
$sql = "
SELECT signal_flow, column_get(drug1, 'drug1_target' as char) AS dt1, column_get(drug2, 'drug2_target' as char) AS dt2
FROM sfa
WHERE cell_name='$cell_name'
AND column_get(drug1, 'drug1' as char)='$drug1'
AND column_get(drug2, 'drug2' as char)='$drug2'
";
$result = $conn->query($sql);
$record = $result->fetch_assoc();
$signal = json_decode($record["signal_flow"]);
$dt1 = $record["dt1"];
$dt2 = $record["dt2"];

$sql_opt = "
SELECT column_get(drug1, 'drug1' as char) AS d1, column_get(drug2, 'drug2' as char) AS d2
FROM sfa
LIMIT 10
";
$result_opt = $conn->query($sql_opt);

$outp = '{"signal":'.json_encode($signal).', "drug1_target":"'.$dt1.'", "drug2_target":"'.$dt2.'",';
$outp .='"max":[';
$num = 1;
while($row_opt = $result_opt->fetch_assoc()) {
    $outp .= '["'.$num.'","'.$row_opt["d1"].'","'.$row_opt["d2"].'","'.(20+mt_rand()/mt_getrandmax()-$num).'"]';
    if($num != 10){$outp .= ",";}
    $num++;
}

$outp .=']}';

echo $outp;

?>
