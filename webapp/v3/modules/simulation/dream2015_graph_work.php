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
$cancer_type = $_POST["cancer_type"];
$cellline = $_POST["cell"];
$drug1 = $_POST["drug1"];
$drug2 = $_POST["drug2"];

$single_cellline = $_POST["cell-single"];
$single_drug = $_POST["drug-single"];

//save input as json
$json_output = array(
    'cancer_type' => $cancer_type,
    'cellline' => $cellline,
    'drug1' => $drug1,
    'drug2' => $drug2
);
$now = DateTime::createFromFormat('U.u', number_format(microtime(true), 6, '.', ''));
$local = $now->setTimeZone(new DateTimeZone('Asia/Seoul'));
$cur_time = $local->format("Y-m-d-H-i-s.u");
$json_file = '/data/cellline_input/input' . $cur_time . '.json';
$fp = fopen($json_file, 'w');
fwrite($fp, json_encode($json_output));
fclose($fp);


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
$optimal_combi_sql = "
SELECT COMPOUND_A, COMPOUND_B, avg(PREDICTION) AS maxVal
FROM dream2015
WHERE CELL_LINE='$cellline'
GROUP BY COMPOUND_A, COMPOUND_B
ORDER BY maxVal DESC
LIMIT 10
";
$result_opt = $conn->query($optimal_combi_sql);
$outp = '{"histo":{"cols":[{"type":"string"},{"type":"number"}],"rows": [';
while($row = $result->fetch_assoc()) {
    if ($outp != '{"histo":{"cols":[{"type":"string"},{"type":"number"}],"rows": [') {$outp .= ",";}
    $outp .= '{"c":[{"v":""},{"v":' . $row["PREDICTION"] . '}]}';
}
$outp .=']},"max":[';

$num = 1;
while($row_opt = $result_opt->fetch_assoc()) {
    $outp .= '["'.$num.'","'.$row_opt["COMPOUND_A"].'","'.$row_opt["COMPOUND_B"].'","'.$row_opt["maxVal"].'"]';
    if($num != 10){$outp .= ",";}
    $num++;
}

$outp .=']}';

$single_sql = "
SELECT *
FROM single_drug
WHERE cell_line = '$single_cellline' AND drug = '$single_drug'
";
$single_result = $conn->query($single_sql);

$single_sql_total = "
SELECT *
FROM single_drug
WHERE cell_line = '$single_cellline'
ORDER BY ic50 ASC
";
$single_result_total = $conn->query($single_sql_total);


$single_temp = '{"histo":{"cols":[{"type":"string"},{"type":"number"}],"rows": [';
while($row = $single_result_total->fetch_assoc()) {
#for($cc=1;$cc<3;$cc++) {
#    $row = $single_result_total->fetch_assoc();
    if ($single_temp != '{"histo":{"cols":[{"type":"string"},{"type":"number"}],"rows": [') {$single_temp .= ",";}
    $single_temp .= '{"c":[{"v":""},{"v":' . $row["ic50"] . '}]}';
}
$row = $single_result->fetch_assoc();
$single_temp .=']},"ic50":'.$row["ic50"].',"source":"'.$row["source"].'","max":[';

$single_sql_opt = "
SELECT *
FROM single_drug
WHERE cell_line = '$single_cellline'
ORDER BY ic50 ASC
LIMIT 10
";
$single_result_opt = $conn->query($single_sql_opt);
$num = 1;
while($row_opt = $single_result_opt->fetch_assoc()) {
    $single_temp .= '["'.$num.'","'.$row_opt["drug"].'","'.$row_opt["ic50"].'","'.$row_opt["source"].'"]';
    if($num != 10){$single_temp.= ",";}
    $num++;
}

$single_temp .= ']}';

$callpy = 'python /data/platform_scripts/python/v3_single_plot.py ' . $single_cellline . ' ' . $single_drug . ' ' . $cur_time;
exec($callpy);

$im = file_get_contents('/data/single_model_plot/plot'.$cur_time.'.png');

$total_outp = '{"dream":'.$outp.', "single":'.$single_temp.', "single_im":"'.base64_encode($im).'"}';


echo $total_outp;


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
