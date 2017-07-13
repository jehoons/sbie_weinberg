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
$node1 = ($node1 == NULL)?'0':'1';
$node2 = $_POST["node2"]; // On is 1, Off is null
$node2 = ($node2 == NULL)?'0':'1';
$node3 = $_POST["node3"]; // On is 1, Off is null
$node3 = ($node3 == NULL)?'0':'1';
$node4 = $_POST["node4"]; // On is 1, Off is null
$node4 = ($node4 == NULL)?'0':'1';
$node5 = $_POST["node5"]; // On is 1, Off is null
$node5 = ($node5 == NULL)?'0':'1';
$input_nodes = $node1.$node2.$node3.$node4.$node5;

$target1 = $_POST["target1"];
$target1_on = $_POST["target1_on"]; // On is 1, Off is 0
$target1_on = ($target1_on == NULL)?'0':'1';
$target2 = $_POST["target2"];
$target2_on = $_POST["target2_on"]; // On is 1, Off is 0
$target2_on = ($target2_on == NULL)?'0':'1';

$mutation = $_POST["mutation"];
if ($mutation == NULL) {
    $mutation = "normal";
}
$tablename = ($mutation == "normal")?"attractor":"attractor_apc";

$sql_control = "
SELECT attractors, state_key
FROM $tablename
WHERE input_nodes='$input_nodes'
AND column_get(target1, 'target1' as char)=''
AND column_get(target2,'target2' as char)=''
";
$result = $conn->query($sql_control);
$record_control = $result->fetch_assoc();
$att_con = json_decode($record_control["attractors"]);
$sk_con = json_decode($record_control["state_key"]);
$i = 0;
$class0_con = 0;
$class1_con = 0;
$class2_con = 0;
foreach($att_con as $key=>$val) {
    if ($val->type != 'unknown') {
        $con_att_keys[$i] = $key;
        foreach($val->class_weight as $key_=>$val_) {
            if($key_ == '0') {
                $class0_con = $class0_con + ($val->ratio * $val_);
            } elseif($key_ == '1') {
                $class1_con = $class1_con + ($val->ratio * $val_);
            } else {
                $class2_con = $class2_con + ($val->ratio * $val_);
            }
        }
        $i = $i + 1;
    }
}

$sql = "
SELECT attractors, state_key
FROM $tablename
WHERE input_nodes='$input_nodes'
AND column_get(target1, 'target1' as char)='$target1'
AND column_get(target1, 'target1_state' as char)='$target1_on'
AND column_get(target2,'target2' as char)='$target2'
AND column_get(target2, 'target2_state' as char)='$target2_on'
UNION
SELECT attractors, state_key
FROM $tablename
WHERE input_nodes='$input_nodes'
AND column_get(target1, 'target1' as char)='$target2'
AND column_get(target1, 'target1_state' as char)='$target2_on'
AND column_get(target2,'target2' as char)='$target1'
AND column_get(target2, 'target2_state' as char)='$target1_on'
";
$result = $conn->query($sql);
$record = $result->fetch_assoc();
$att = json_decode($record["attractors"]);
$sk = json_decode($record["state_key"]);

$i = 0;
$class0 = 0;
$class1 = 0;
$class2 = 0;
foreach($att as $key=>$val) {
    if ($val->type != 'unknown') {
        $exp_att_keys[$i] = $key;
        foreach($val->class_weight as $key_=>$val_) {
            if($key_ == '0') {
                $class0 = $class0 + ($val->ratio * $val_);
            } elseif($key_ == '1') {
                $class1 = $class1 + ($val->ratio * $val_);
            } else {
                $class2 = $class2 + ($val->ratio * $val_);
            }
        }
        $i = $i + 1;
    }
}

// make json for control attractor
$i = 0;
$outp_con = '{"cols":[{"type":"string"},{"type":"number"}],"rows": [';
#foreach($att_con as $key=>$val) {
#    if ($val->type != 'unknown') {
#        if ($outp_con != '{"cols":[{"type":"string"},{"type":"number"}],"rows": [') {$outp_con .= ",";}
#        $outp_con .= '{"c":[{"v":"'. $key . '"},{"v":' . $val->ratio . '}]}';
#        $total_attractor[$i] = $key;
#        $i = $i + 1;
#    }
#}
#foreach($exp_att_keys as $val) {
#    if(!in_array($val,$total_attractor)) {
#        if ($outp_con != '{"cols":[{"type":"string"},{"type":"number"}],"rows": [') {$outp_con .= ",";}
#        $outp_con .= '{"c":[{"v":"'. $val . '"},{"v":0}]}';
#        $total_attractor[$i] = $val;
#        $i = $i + 1;
#    }
#}
$outp_con .= '{"c":[{"v":"Apoptosis"},{"v":' . $class0_con . '}]}';
$outp_con .= ',{"c":[{"v":"Proliferation"},{"v":' . $class1_con . '}]}';
$outp_con .= ',{"c":[{"v":"Quiescent"},{"v":' . $class2_con . '}]}';
$outp_con .="]}";

$outp = '{"cols":[{"type":"string"},{"type":"number"}],"rows": [';
#foreach($total_attractor as $val) {
#    if(!in_array($val,$exp_att_keys)) {
#        if ($outp != '{"cols":[{"type":"string"},{"type":"number"}],"rows": [') {$outp .= ",";}
#        $outp .= '{"c":[{"v":"'. $val . '"},{"v":0}]}';
#    }
#    else {
#        if ($outp != '{"cols":[{"type":"string"},{"type":"number"}],"rows": [') {$outp .= ",";}
#        $outp .= '{"c":[{"v":"'. $val. '"},{"v":' . $att->$val->ratio . '}]}';
#    }
#}
$outp .= '{"c":[{"v":"Apoptosis"},{"v":' . $class0 . '}]}';
$outp .= ',{"c":[{"v":"Proliferation"},{"v":' . $class1 . '}]}';
$outp .= ',{"c":[{"v":"Quiescent"},{"v":' . $class2 . '}]}';
$outp .="]}";

//echo '{"node1":"'.$node1.'", "node2":"'.$node2.'", "node3":"'.$node3.'" , "node4":"'.$node4.'" , "node5":"'.$node5.'" , "target1":"'.$target1.'" , "target1_on":"'.$target1_on.'" , "target2":"'.$target2.'" , "target2_on":"'.$target2_on.'", "input_nodes":"'.$input_nodes.'", "attractors":'.$record["attractors"].', "state_key":'.$record["state_key"].'}';

$total_out =  '{"target1":"'.$target1.'" , "target1_on":"'.$target1_on.'" , "target2":"'.$target2.'" , "target2_on":"'.$target2_on.'", "att_exp":'.$outp.', "att_control":'.$outp_con.',';

$sql_opt = "
SELECT column_get(target1, 'target1' as char) as t1, column_get(target2, 'target2' as char) as t2
FROM $tablename
WHERE input_nodes='$input_nodes'
ORDER BY rand()
limit 10
";
$result_opt = $conn->query($sql_opt);

$total_out .='"max":[';
$num = 1;
while($row_opt = $result_opt->fetch_assoc()) {
    $total_out .= '["'.$num.'","'.$row_opt["t1"].'","'.$row_opt["t2"].'","'.((10+mt_rand()/mt_getrandmax()-$num)/10).'"]';
    if($num != 10){$total_out .= ",";}
    $num++;
}

$total_out .=']}';

echo $total_out;
?>
