<?php
/* --------------------------------

module/member/logout_work.php
로그아웃 get방식의 ajax 페이지.

*ajax 오류 점검 :
1. form action에 정확한 주소가 입력 되었는가?
2. 전송하는 데이터가 잘 들어가는가?
3. 해당 주소의 페이지가 정당한 json 형식을 가지는가?

-------------------------------- */

//__CL__ 정의 되지 않았다면 false 를 return.
if(!defined('__CL__')) exit();

//로그아웃 설정.
if($_GET['logout']){
	
	session_unset($_SESSION["mb_rowid"]);
	
	gotoUrl(htmlspecialchars($_SERVER["PHP_SELF"])."?module=index&act=list.php");
	
}
?>