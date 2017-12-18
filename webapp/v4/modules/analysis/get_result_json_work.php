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
$sfa_json = $sample["SFA_NETWORK_JSON"];

$jd = array('result' => $sfa_json);
echo json_encode($jd);

//echo '{"asdf":'.$patient_id. ', "qwer":'.$drugs.'}';
?>
