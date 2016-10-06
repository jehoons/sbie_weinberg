<?php
/* --------------------------------

module/member/delete_work.php
암호수정 ajax 페이지.

-------------------------------- */

//__CL__ 정의 되지 않았다면 false 를 return.
if(!defined('__CL__')) exit();

//데이터가 넘어왔는지 확인.
if($_POST["mb_pwd"]){
		
	//태그 있으면 제거 비밀번호는 특수문자를 인정하기 때문에 제거 하지 않는다.
	$mb_pwd = $_POST["mb_pwd"];
	$mb_outreason = $_POST["mb_outreason"];

	//이전 암호 확인
	$sql = "
	SELECT mb_rowid
	FROM member
	WHERE mb_rowid = '$_SESSION[mb_rowid]' AND mb_pwd = password('$mb_pwd')
	";
	$result = $conn->query($sql);
	$row = $result->fetch_assoc();
		
	//현재 암호가 맞다면.
	if($row['mb_rowid']){

		//암호 수정 시행. mb_code 10은 탈퇴 처리!
		$sql = "UPDATE member

		SET

		mb_code = 10
		,mb_outreason = '$mb_outreason'
		,mb_outdatetime = now()
		
		WHERE

		mb_rowid = '$_SESSION[mb_rowid]'
		";

		//회원수정 성공.
		if ($conn->query($sql) === TRUE) {
			
			$afterMessage = "계정이 삭제되었습니다.";
			$afterWork = "move";
			$afterAddress = htmlspecialchars($_SERVER["PHP_SELF"])."?module=member&act=logout_work.php&logout=true";

		//회원수정 실패.
		} else {
			
			$afterMessage = "데이터베이스에 문제가 발생하여<br />데이터가 정상적으로 등록되지 않았습니다.<br />다시 시도해 주십시오.<br /><br />불편을 끼쳐 드려 죄송합니다.";
			$afterWork = "close";
			$afterAddress = "empty";
			
		}
		
	//현재 암호가 맞지 않다면.
	}else{

		$afterMessage = ("암호를 잘못 입력하셨습니다.<br />다시 시도해 주십시오.");
		$afterWork = "close";
		$afterAddress = "empty";

	}
	
	//{"a":1,"b":2,"c":3,"d":4,"e":5} 식으로 만들기.
		$arr = array ('afterMessage'=>$afterMessage,'afterWork'=>$afterWork,'afterAddress'=>$afterAddress);
		
		//json으로 변환.
		echo json_encode($arr);;
	
}
?>