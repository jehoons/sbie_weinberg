<?php
if(!defined('__CL__')) exit();

//태그 있으면 제거 비밀번호는 특수문자를 인정하기 때문에 제거 하지 않는다.
$patient = dataCheck($_POST["patient"]);
$cancertype = dataCheck($_POST["cancertype"]);
$expression = dataCheck($_POST["expression"]);
$mutation = dataCheck($_POST["mutation"]);
$cnv = dataCheck($_POST["cnv"]);
$redirectAddress = $_SERVER["PHP_SELF"]."?module=analysis&act=list.php";

//데이터가 넘어왔는지 확인.
if($patient && $cancertype && $expression && $mutation && $cnv){

	//INSERT 실행. 
	$sql = "INSERT INTO patient
	VALUES (
	''
	,'$patient'
	,'$cancertype'
	,'$expression'
	,'$mutation'
	,'$cnv'
	)";
	
	//회원가입 성공.
	if ($conn->query($sql) === TRUE) {
		
		header("Location: $redirectAddress");
		die();
			
	//회원가입 실패.
	} else {

		echo "잘못된 경로로 접속하셨습니다.";
		
	}
	

}
?>