<?php
/* --------------------------------

module/member/join_work.php
회원가입 ajax 페이지.

*ajax 오류 점검 :
1. form action에 정확한 주소가 입력 되었는가?
2. 전송하는 데이터가 잘 들어가는가?
3. 해당 주소의 페이지가 정당한 json 형식을 가지는가?


-------------------------------- */

//__CL__ 정의 되지 않았다면 false 를 return.
if(!defined('__CL__')) exit();

//데이터가 넘어왔는지 확인.
if($_POST["mb_email"] && $_POST["mb_pwd1"] && $_POST["mb_pwd2"] && $_POST["mb_name"] && $_POST["mb_organization"]){

	//태그 있으면  비밀번호는 특수문자를 인정하기 때문에 제거 하지 않는다.
	$mb_email = dataCheck($_POST["mb_email"]);
	$mb_pwd1 = $_POST["mb_pwd1"];
	$mb_pwd2 = $_POST["mb_pwd2"];
	$mb_name = dataCheck($_POST["mb_name"]);
	$mb_organization = dataCheck($_POST["mb_organization"]);
		
	//이미 가입한 회원인지 이메일 대조.
	$sql = "
	SELECT mb_rowid
	FROM member
	WHERE mb_email = '$mb_email'
	";
	$result = $conn->query($sql);
	$row = $result->fetch_assoc();
		
	//이미 등록된 이메일 이라면.
	if($row['mb_rowid']){
			
		$afterMessage = ("이미 등록된 이메일입니다.<br />다시 시도해 주십시오.");
		$afterWork = "close";
		$afterAddress = "empty";

	//등록된 이메일이 아니라면 그대로 진행.
	}else{

		//데이터 이전.
		$mb_email = $mb_email;
		$mb_pwd = $mb_pwd1;
		$mb_name = $mb_name;
		$mb_organization = $mb_organization;
		
		$mb_visitnum = 0;
		$mb_writedatetime = "now()";
		$mb_recentdatetime = "";
		$mb_updatedatetime = "";
		$mb_outdatetime = "";
		
		$mb_varchar1 = "";
		$mb_varchar2 = "";
		$mb_int1 = "";
		$mb_int2 = "";
		$mb_text = "";
		$mb_datetime = "";

		//유효성 검사.
		if (!filter_var($mb_email, FILTER_VALIDATE_EMAIL)) {
			$afterMessage = "'$email' is not a valid email address";
			$afterWork = "close";
			$afterAddress = "empty";
		}

		//INSERT 실행. 
		$sql = "INSERT INTO member
		VALUES (
		''
		,'$mb_email'
		,password('$mb_pwd')
		,'$mb_name'
		,'$mb_organization'
		,'$mb_visitnum'
		,now()
		,'$mb_recentdatetime'
		,'$mb_updatedatetime'
		,'$mb_outdatetime'
			
		,'$mb_varchar1'
		,'$mb_varchar2'
		,'$mb_int1'
		,'$mb_int2'
		,'$mb_text'
		,'$mb_datetime'
		)";
		
		//회원가입 성공.
		if ($conn->query($sql) === TRUE) {
			
			$afterMessage = "<span style='font-size:140%;'>".$mb_name."</span> 님을 진심으로 환영합니다.<br />회원가입이 정상적으로 완료 되었습니다.<br />입력하신 이메일과 암호로 로그인 하실 수 있습니다.";
			$afterWork = "move";
			$afterAddress = htmlspecialchars($_SERVER["PHP_SELF"])."?module=index&act=list.php";
				
		//회원가입 실패.
		} else {
			$afterMessage = "데이터베이스에 문제가 발생하여<br />데이터가 정상적으로 등록되지 않았습니다.<br />다시 시도해 주십시오.<br /><br />불편을 끼쳐 드려 죄송합니다.";
			$afterWork = "close";
			$afterAddress = "empty";
		}
	}
	
	//{"a":1,"b":2,"c":3,"d":4,"e":5} 식으로 만들기.
	$arr = array ('afterMessage'=>$afterMessage,'afterWork'=>$afterWork,'afterAddress'=>$afterAddress);
	
	//json으로 변환.
	echo json_encode($arr);
	
}
?>