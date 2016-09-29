<?php
/* --------------------------------

module/member/login_work.php
로그인 ajax 페이지.

-------------------------------- */

//__CL__ 정의 되지 않았다면 false 를 return.
if(!defined('__CL__')) exit();

//로그인 설정.
if($_POST['signinemail'] && $_POST['signinpwd']){
	$signinemail = $_POST['signinemail'];
	$signinpwd = $_POST['signinpwd'];

	$sql = "
	SELECT mb_rowid, mb_name
	FROM member
	WHERE mb_email = '$signinemail' AND mb_pwd = password('$signinpwd')
	";
	$result = $conn->query($sql);
	$loginrow = $result->fetch_assoc();

	if($loginrow['mb_rowid']){
		//session 설정
		$_SESSION["mb_rowid"] = $loginrow['mb_rowid'];
		
		$afterMessage = "<span style='font-size:140%;'>".$loginrow['mb_name']."</span> 님 안녕하세요.<br />로그인에 성공 하였습니다.";
		$afterWork = "move";
		$afterAddress = $_SERVER["PHP_SELF"]."?module=index&act=list.php";
		
		//방문숫자 수정
		$sql = "
		SELECT DATE_FORMAT(mb_recentdatetime, '%Y%m%d') AS mb_recentdatetime
		FROM member
		WHERE mb_email = '$signinemail' AND mb_pwd = password('$signinpwd')
		";
		$result = $conn->query($sql);
		$visitrow = $result->fetch_assoc();
		
			//최근방문일자와 오늘이 같지 않다면 +1
			if(date("Ymd") != $visitrow['mb_recentdatetime']){
				
				//방문숫자 수정
				$sql = "UPDATE member
				
				SET
				
				mb_visitnum = mb_visitnum + 1
				,mb_score = mb_score + 1
				
				WHERE mb_email = '$signinemail' AND mb_pwd = password('$signinpwd')";
				$conn->query($sql);
			
			}
		
		//최근 방문일 수정
		$sql = "UPDATE member
		
		SET
		
		mb_recentdatetime = now()
		
		WHERE mb_email = '$signinemail' AND mb_pwd = password('$signinpwd')";
		$conn->query($sql);

		
	}else{
		$afterMessage = "이메일 혹은 암호를 잘못 입력하였습니다.";
		$afterWork = "close";
		$afterAddress = "empty";
	}
	
	//{"a":1,"b":2,"c":3,"d":4,"e":5} 식으로 만들기.
	$arr = array ('afterMessage'=>$afterMessage,'afterWork'=>$afterWork,'afterAddress'=>$afterAddress);
	
	//json으로 변환.
	echo json_encode($arr);
}
?>