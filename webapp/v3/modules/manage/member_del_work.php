<?php
/* --------------------------------

module/manage/member_del_work.php
관리자 회원삭제 get방식의 ajax 페이지.

*ajax 오류 점검 :
1. form action에 정확한 주소가 입력 되었는가?
2. 전송하는 데이터가 잘 들어가는가?
3. 해당 주소의 페이지가 정당한 json 형식을 가지는가?

-------------------------------- */

//__CL__ 정의 되지 않았다면 false 를 return.
if(!defined('__CL__')) exit();

//관리자인지 체크 : mb_code가 100이상일 때 관리자.
manageCheck($signinrow[mb_code]);

//데이터가 넘어왔는지 확인.
if($_GET["mb_rowid"]){

	//데이터 이전
	$mb_rowid = $_GET["mb_rowid"];

	//DELETE 실행.
	$sql = "DELETE FROM member WHERE mb_rowid = '$mb_rowid'";

	//책 업데이트 성공.
	if ($conn->query($sql) === TRUE) {
			
		$afterMessage = "회원 삭제를 완료하였습니다.";
		$afterWork = "move";
		$afterAddress = htmlspecialchars($_SERVER["PHP_SELF"])."?module=manage&act=member_list.php&pagenum=".$_GET["pagenum"]."&searchColumn=".$_GET["searchColumn"]."&searchStr=".$_GET["searchStr"]."&orderby=".$_GET["orderby"]."&orderopt=".$_GET["orderopt"];
			
		//책 업데이트 실패.
	} else {
		$afterMessage = "데이터베이스에 문제가 발생하여<br />데이터가 정상적으로 등록되지 않았습니다.<br />다시 시도해 주십시오.<br /><br />불편을 끼쳐 드려 죄송합니다.";
		$afterWork = "close";
		$afterAddress = "empty";

	}
	
	//{"a":1,"b":2,"c":3,"d":4,"e":5} 식으로 만들기.
	$arr = array ('afterMessage'=>$afterMessage,'afterWork'=>$afterWork,'afterAddress'=>$afterAddress);
	
	//json으로 변환.
	echo json_encode($arr);
	
}	
?>