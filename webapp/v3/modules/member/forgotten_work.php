<?php
/* --------------------------------

module/member/forgotten_work.php
암호찾기 ajax 페이지.

*ajax 오류 점검 :
1. form action에 정확한 주소가 입력 되었는가?
2. 전송하는 데이터가 잘 들어가는가?
3. 해당 주소의 페이지가 정당한 json 형식을 가지는가?

-------------------------------- */

//__CL__ 정의 되지 않았다면 false 를 return.
if(!defined('__CL__')) exit();

if($_POST["mb_email"] && $_POST["mb_name"]){
		
	//태그 있으면 제거 비밀번호는 특수문자를 인정하기 때문에 제거 하지 않는다.
	$mb_email = dataCheck($_POST["mb_email"]);
	$mb_name = dataCheck($_POST["mb_name"]);
		
	//데이터 이전.
	$mb_email = $mb_email;
	$mb_name = $mb_name;
		
	//개인정보 일치 하는지 확인
	$sql = "
	SELECT mb_rowid
	FROM member
	WHERE mb_email = '$mb_email' AND mb_name = '$mb_name'
	";
	$result = $conn->query($sql);
	$row = $result->fetch_assoc();
		
	//해당 이메일 있다면 메일방송.
	if($row['mb_rowid']){

		//난수 생성(문자가 입력된 변수는 문자 하나씩 배열을 갖게 되는 점을 이용).
		$pw = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
		$temp_pw = "";
		for($i=0;$i<30;$i++) {
			$temp_pw .= $pw[rand(0,61)];
		}

		//임의 암호로 수정 시행.
		$sql = "UPDATE member

		SET

		mb_pwd = password('$temp_pw')

		WHERE

		mb_email = '$mb_email'";

		//수정 성공.
		if ($conn->query($sql) === TRUE) {
				
			$to = $mb_id;
			$subject = "SBIE에서 임의 암호를 발송했습니다.";
				
			$message = "
			<html>
			<head>
			<title>SBIE</title>
			</head>
			<body>
			이메일 : $mb_email <br />
			임의 암호 : $temp_pw <br />
			<br /><br /><a href='http://weinberg.kaist.ac.kr'>
			</body>
			</html>
			";
				
			// Always set content-type when sending HTML email
			$headers = "MIME-Version: 1.0" . "\r\n";
			$headers .= "Content-type:text/html;charset=UTF-8" . "\r\n";
				
			// More headers
			$headers .= 'From: <choonlog@outlook.com>' . "\r\n";
				
			$mailOk = mail($to,$subject,$message,$headers);
				
			if($mailOk){

				$afterMessage = "입력하신 주소(".$mb_email.")로 임의 암호를 발송하였습니다.<br />로그인 후 새로운 암호로 변경하여 주십시오. ";
				$afterWork = "move";
				$afterAddress = htmlspecialchars($_SERVER["PHP_SELF"])."?module=index&act=list.php";

			}else{

				$afterMessage = ("메일발송이 실패하였습니다.<br />다시 시도해 주십시오.");
				$afterWork = "close";
				$afterAddress = "empty";

			}
				
		}else{
			$afterMessage = "데이터베이스에 문제가 발생하여<br />데이터가 정상적으로 등록되지 않았습니다.<br />다시 시도해 주십시오.<br /><br />불편을 끼쳐 드려 죄송합니다.";
			$afterWork = "close";
			$afterAddress = "empty";
		}



	//해당 이메일 없다면 취소. 
	}else{

		$afterMessage = ("일치하는 정보가 없습니다.<br />다시 시도해 주십시오.");
		$afterWork = "close";
		$afterAddress = "empty";

	}
	
	//{"a":1,"b":2,"c":3,"d":4,"e":5} 식으로 만들기.
	$arr = array ('afterMessage'=>$afterMessage,'afterWork'=>$afterWork,'afterAddress'=>$afterAddress);
	
	//json으로 변환.
	echo json_encode($arr);
	
}
?>