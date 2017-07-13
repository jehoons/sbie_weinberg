<?php
/* --------------------------------

module/simulation/dream2015_cellline_work.php
dream2015 cell line을 가져오는 ajax 페이지.

*ajax 오류 점검 :
1. form action에 정확한 주소가 입력 되었는가?
2. 전송하는 데이터가 잘 들어가는가?
3. 해당 주소의 페이지가 정당한 json 형식을 가지는가?

-------------------------------- */

//__CL__ 정의 되지 않았다면 false 를 return.
if(!defined('__CL__')) exit();

// php 페이지 로딩 시간을 최대 5분(60*5)으로 연장. default는 30초.
ini_set('max_execution_time', 300);

$tissue = '';
$tissue_single = '';
$cancer_type = $_GET["cancertype"];
if($cancer_type=='colon'){
    $tissue = 'gastrointestinal tract (lower)';
    $tissue_single = 'large_intestine';
}else if($cancer_type=='breast'){
    $tissue = 'breast';
    $tissue_single = 'breast';
}else if($cancer_type=='lung'){
    $tissue = 'lung';
    $tissue_single = 'lung';
}

$sql = "
SELECT cell_name
FROM cellLine
WHERE tissue='$tissue';
";
$result = $conn->query($sql);

$sql_single = "
SELECT a.cell_name
FROM cellLine_single a
WHERE EXISTS ( SELECT *
FROM single_drug b
WHERE b.cell_line=a.cell_name)
AND site='$tissue_single';
";
$result_single = $conn->query($sql_single);


$outp = "[";
while($row = $result->fetch_assoc()) {
    if ($outp != "[") {$outp .= ",";}
    $outp .= '{"CELL_NAME":"'  . $row["cell_name"] . '"}'; 
}
$outp .="]";

$outp_single = "[";
while($row = $result_single->fetch_assoc()) {
    if ($outp_single != "[") {$outp_single .= ",";}
    $outp_single .= '{"CELL_NAME":"'  . $row["cell_name"] . '"}';
}
$outp_single .="]";

$total_out = '{"dream":'.$outp.', "single":'.$outp_single.'}';

echo $total_out;
?>
