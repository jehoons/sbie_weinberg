<?php
/* --------------------------------

module/member/logout_work.php
로그아웃 classic 페이지.

-------------------------------- */

//__CL__ 정의 되지 않았다면 false 를 return.
if(!defined('__CL__')) exit();

//로그아웃 설정.
if($_GET['logout']){
	
	session_unset($_SESSION["mb_rowid"]);
	
	gotoUrl(htmlspecialchars($_SERVER["PHP_SELF"])."?module=index&act=list.php");
	
}
?>