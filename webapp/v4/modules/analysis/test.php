<?php

$sql = "
SELECT *
FROM ANALYSIS_RESULT
WHERE ANALYSIS_ID = 99 AND TREATMENT_ID = 1
";

$result = $conn->query($sql);
$sample = $result->fetch_assoc();
$sfa_json = $sample["SFA_NETWORK_JSON"];

echo $sfa_json;

?>
