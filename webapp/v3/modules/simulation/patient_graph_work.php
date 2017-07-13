<?php
/* --------------------------------
module/simulation/patient_graph_work.php
patient 그래프를 그리는 ajax 페이지.
*ajax 오류 점검 :
1. form action에 정확한 주소가 입력 되었는가?
2. 전송하는 데이터가 잘 들어가는가?
3. 해당 주소의 페이지가 정당한 json 형식을 가지는가?
-------------------------------- */
//__CL__ 정의 되지 않았다면 false 를 return.
if(!defined('__CL__')) exit();
// php 페이지 로딩 시간을 최대 5분(60*5)으로 연장. default는 30초.
ini_set('max_execution_time', 300);
$cancer_type = $_POST["cancer_type"];
$mutation = $_POST["mutation"];
$target1 = $_POST["target1"];
$target2 = $_POST["target2"];

// for window, mac   \r\n
$mutation = explode("\r\n",$mutation);

// for linux   \n
//$mutation = explode("\n",$mutation);

//save input as json
$json_output = array(
    'cancer_type' => $cancer_type,
    'mutation' => $mutation,
    'target1' => $target1,
    'target2' => $target2
);
$json_file = '/data/patient_input/input' . date("Y-m-d-H-i-s") . '.json';
$fp = fopen($json_file, 'w');
fwrite($fp, json_encode($json_output));
fclose($fp);


$outp = '{}';
echo $outp;


?>
