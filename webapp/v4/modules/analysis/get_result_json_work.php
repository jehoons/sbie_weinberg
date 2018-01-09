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

$sql = "
SELECT CANCER_ID
FROM PATIENT
WHERE ID=$patient_id
";
$result = $conn->query($sql);
$record = $result->fetch_assoc();
$cid = $record["CANCER_ID"];

$jd = array('result' => $sfa_json, 'cancer_id' => $cid);
echo json_encode($jd);

//echo '{"asdf":'.$patient_id. ', "qwer":'.$drugs.'}';
?>
