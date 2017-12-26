<?php
if(!defined('__CL__')) exit();
$patient_id = $_GET[PATIENT_ID];
$treatment_id = $_GET[TREATMENT_ID];

$sql = "
SELECT  *
FROM ANALYSIS_RESULT
WHERE ANALYSIS_ID=$patient_id and TREATMENT_ID=$treatment_id
";
$result = $conn->query($sql);
$sample = $result->fetch_assoc();
$att_json = $sample["ATT_STATES_JSON"];

$jd = array('result' => $att_json);
echo json_encode($att_json);

//echo '{"asdf":'.$patient_id. ', "qwer":'.$drugs.'}';