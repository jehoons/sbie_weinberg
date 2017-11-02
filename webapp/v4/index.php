<?php
/*
 * --------------------------------
 *
 * index.php
 * 첫 화면.
 *
 * --------------------------------
 */

// require 시에만 열람할 수 있도록 제어.
define ( '__CL__', TRUE );

// 환경설정을 위해 config/config.inc.php 를 require.
require dirname ( __FILE__ ) . '/config/config.php';
?>