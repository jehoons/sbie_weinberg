<?php
//__CL__ 정의 되지 않았다면 false 를 return.
if(!defined('__CL__')) exit();
?>

<?php
// member 테이블 생성
$sql=" 
	CREATE TABLE IF NOT EXISTS patient (
pt_rowid					int not null auto_increment
,pt_name					varchar(255) not null default ''
,pt_cancertype				varchar(255)
,pt_expression		 		varchar(255)
,pt_mutation				varchar(255)
,pt_cnv						varchar(255)
,PRIMARY KEY(pt_rowid)
	)ENGINE=InnoDB DEFAULT CHARSET=utf8 
";
$result = $conn->query($sql);

if($result){
	echo "1. Table patient created successfully<br />";
}else{
	echo "1. Error creating member table: " . mysqli_error($conn)."(".mysqli_errno($conn).")<br />";
}
?> 