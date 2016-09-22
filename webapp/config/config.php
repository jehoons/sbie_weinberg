<?php
/* --------------------------------

config/config.php
환경설정.

-------------------------------- */
// 페이지 상단
$start_time = array_sum(explode(' ', microtime()));

error_reporting(E_ALL ^ E_NOTICE ^ E_DEPRECATED);

//  __CL__ 정의 되지 않았다면 false 를 return.
if(!defined('__CL__')) exit();

// 쿠키 이외의 값에서도 세션을 인식할 수 있도록 함(파일업로드 등에서의 문제 수정)
ini_set('session.use_only_cookies', 0);

// css, js 파일을 들고오기 위한 파일 상대경로.
define('_CL_PATH_', str_replace('config/config.php', '', str_replace('\\', '/', __FILE__)));

// require 하기 위한 파일 절대경로.
define('_CL_PATH_HOST_', str_replace($_SERVER["DOCUMENT_ROOT"], '', _CL_PATH_));

// 필수 페이지 require
require _CL_PATH_.'config/function.php';
require _CL_PATH_.'config/database.php';
require _CL_PATH_.'config/session.php';
require _CL_PATH_.'config/page.php';
require _CL_PATH_.'config/handler.php';
?>