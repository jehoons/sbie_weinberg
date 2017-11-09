<?php
if(!defined('__CL__')) exit();

//작업모드('_work.php'로 끝나는 파일은 디자인이 필요없는 백그라운드 작업페이지이다)이면 작업 페이지 호출.
if(substr($_GET["act"],-9,9) == "_work.php"){
	$url = _CL_PATH_.'modules/'.$_GET["module"].'/'.$_GET["act"];
	require $url;
	$conn->close();
	exit();
}
?>
<!doctype html>
<html lang="en" class="no-js">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">

	<link href='http://fonts.googleapis.com/css?family=Roboto:400,700,300' rel='stylesheet' type='text/css'>

	<link rel="stylesheet" href="<?php echo _CL_PATH_HOST_;?>common/css/reset.css"> <!-- CSS reset -->
	<link rel="stylesheet" href="<?php echo _CL_PATH_HOST_;?>common/css/style.css"> <!-- Resource style -->
	<link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css"> 
	<script src="<?php echo _CL_PATH_HOST_;?>common/js/modernizr.js"></script> <!-- Modernizr -->
	
  	
	<title>Alternate Fixed And Scroll Backgrounds</title>
</head>
<body>
	<header class="header">
		<div id="logo"><a href="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">SBiE</a></div>

		<nav class="main-nav">
			<ul>
				<!-- inser more links here -->
				<li><a href="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">Home</a></li>
				<li><a href="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>?module=analysis&act=list.php">Anaylsis</a></li>
				<li><a href="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>?module=about&act=list.php">About</a></li>
				<li><a href="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>?module=contact&act=list.php">Contact</a></li>
				<li><a href="#0">Account</a></li>
			</ul>
		</nav> <!-- main-nav -->
	</header>
<?php
// 해당 페이지 require. 형식 : module 은 'first' , act 는 'list.php'
if($_GET["module"] && $_GET["act"]){
	$url = _CL_PATH_.'modules/'.$_GET["module"].'/'.$_GET["act"];
}else{
	$url = _CL_PATH_.'modules/index/list.php';
}

// url 을 require.
require $url;
?>
	<footer>
		<img src="<?php echo _CL_PATH_HOST_;?>common/img/kaist.jpg" alt="logo"><br /><br />
		COPYRIGHT© LABORATORY FOR SYSTEMS BIOLOGY AND BIO-INSPIRED ENGINEERING. ALL RIHGT RESERVED.<br />
		291 DAEHAK-RO, YUSEONG-GU, DAEJEON 305-701, REPUBLIC OF KOREA
	</footer> <!-- main-content -->
	<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
	<script src="<?php echo _CL_PATH_HOST_;?>common/js/main.js"></script> <!-- Resource jQuery -->
	<script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
	<script>                                                                                                                                                  
        $( function() {                                                                                                                                       
            $("#simul-tab").tabs();                                                                                                                           
        } );                                                                                                                                                  
    </script> 
	
	<input type="hidden"  id="phpself" value="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">
	<input type="hidden"  id="clpathhost" value="<?php echo _CL_PATH_HOST_;?>">	
</body>
</html>