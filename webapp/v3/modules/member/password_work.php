<?php
/* --------------------------------

module/member/password_work.php
비밀번호 ajax 페이지.

*ajax 오류 점검 :
1. form action에 정확한 주소가 입력 되었는가?
2. 전송하는 데이터가 잘 들어가는가?
3. 해당 주소의 페이지가 정당한 json 형식을 가지는가?

-------------------------------- */

//__CL__ 정의 되지 않았다면 false 를 return.
if(!defined('__CL__')) exit();

//데이터가 넘어왔는지 확인.
if($_POST["mb_oldpwd"] && $_POST["mb_pwd1"] && $_POST["mb_pwd2"]){
	
	//태그 있으면 제거 비밀번호는 특수문자를 인정하기 때문에 제거 하지 않는다.
	$mb_pwd1 = $_POST["mb_pwd1"];
	$mb_pwd2 = $_POST["mb_pwd2"];
	
	//이전 암호 확인
	$sql = "
	SELECT mb_rowid
	FROM member
	WHERE mb_rowid = '$_SESSION[mb_rowid]' AND mb_pwd = password('$_POST[mb_oldpwd]')
	";
	$result = $conn->query($sql);
	$row = $result->fetch_assoc();

		//현재 암호가 맞다면.
		if($row['mb_rowid']){

		//데이터 이전.
		$mb_pwd = $mb_pwd1;

		//암호 수정 시행.
		$sql = "UPDATE member

		SET

		mb_pwd = password('$mb_pwd')
		,mb_pwdupdatedatetime = now()

		WHERE

		mb_rowid = '$_SESSION[mb_rowid]'
		";
	
			//회원가입 성공.
			if ($conn->query($sql) === TRUE) {
				
				$afterMessage = "암호를 수정하였습니다.";
				$afterWork = "move";
				$afterAddress = htmlspecialchars($_SERVER["PHP_SELF"])."?module=index&act=list.php";
					
			//회원가입 실패.
			} else {
				$afterMessage = "데이터베이스에 문제가 발생하여<br />데이터가 정상적으로 등록되지 않았습니다.<br />다시 시도해 주십시오.<br /><br />불편을 끼쳐 드려 죄송합니다.";
				$afterWork = "close";
				$afterAddress = "empty";
			}
			
		
		} else {
			$afterMessage = "현재 암호를 잘못 입력하셨습니다.<br />다시 시도해 주십시오.";
			$afterWork = "close";
			$afterAddress = "empty";
		}
		
		//{"a":1,"b":2,"c":3,"d":4,"e":5} 식으로 만들기.
		$arr = array ('afterMessage'=>$afterMessage,'afterWork'=>$afterWork,'afterAddress'=>$afterAddress);
			
		//json으로 변환.
		echo json_encode($arr);
	
}
?>