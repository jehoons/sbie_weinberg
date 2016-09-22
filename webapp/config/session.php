<?php
/* --------------------------------

config/session.php
session 파일 설정.

-------------------------------- */

//__CL__ 정의 되지 않았다면 false 를 return.
if(!defined('__CL__')) exit();

// 세션 설정
@session_cache_limiter("no-cache, must-revalidate");
@session_save_path(_CL_PATH_."files/session");
ini_set("session.cache_expire", 180);
ini_set("session.gc_maxlifetime", 1440);
session_set_cookie_params(0, "/");
@session_start();

/*
// remove all session variables 예시
session_unset();

// destroy the session 예시
session_destroy();
*/
?>