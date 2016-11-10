<?php
/* --------------------------------

config/handler.php
header, menu, footer 를 구성하고  main은  modules의 페이지가 차지하여 기능 하도록.

-------------------------------- */

//__CL__ 정의 되지 않았다면 false 를 return.
if(!defined('__CL__')) exit();

//세션값이 있다면 로그인한 상태이므로 회원정보 쿼리. $signinrow['mb_fullname'] 형식으로 사용.
if($_SESSION["mb_rowid"]){
	$mbrowid = $_SESSION['mb_rowid'];

	//회원 정보 쿼리
	$sql = "
	SELECT *
	FROM member
	WHERE mb_rowid = '$mbrowid'
	";
	$result = $conn->query($sql);
	$signinrow = $result->fetch_assoc();
	
	/*
	mb_code가  1이면 일반회원, 10이면 탈퇴회원, 100이면 괸리자.
	 */
}	

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

	<link href='http://fonts.googleapis.com/css?family=Open+Sans:300,400,600,700' rel='stylesheet' type='text/css'>

	<link rel="stylesheet" href="<?php echo _CL_PATH_HOST_;?>common/css/reset.css"> <!-- CSS reset -->
	<link rel="stylesheet" href="<?php echo _CL_PATH_HOST_;?>common/css/style.css"> <!-- Resource style -->
	<link rel="stylesheet" type="text/css" href="<?php echo _CL_PATH_HOST_;?>common/css/component.css" /> <!-- Form style -->
	<link rel="stylesheet" type="text/css" href="<?php echo _CL_PATH_HOST_;?>common/js/node_modules/vis/dist/vis.css" />
	<link rel="stylesheet" type="text/css" href="<?php echo _CL_PATH_HOST_;?>common/css/visNet.css" />
	<script src="<?php echo _CL_PATH_HOST_;?>common/js/modernizr.js"></script> <!-- Modernizr -->
	<script src="<?php echo _CL_PATH_HOST_;?>common/js/node_modules/vis/examples/network/exampleUtil.js"></script>
	<script src="<?php echo _CL_PATH_HOST_;?>common/js/node_modules/vis/dist/vis.js"></script>
	<script src="<?php echo _CL_PATH_HOST_;?>common/js/fumia.js"></script> 
	<script type="text/javascript" src="https://www.google.com/jsapi"></script>
	<script src='https://www.google.com/recaptcha/api.js'></script>
	<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
  	
	<title>Anti-cancer drug recommendation platform</title>
</head>


<body>
	<header>
		<div id="logo"><a href="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>?module=index&act=list.php" style="color:#FFFFFF;">SBiE</a><!-- <img src="<?php echo _CL_PATH_HOST_;?>common/img/cl-logo.svg" alt="Homepage"> --></div>

		<div id="cl-hamburger-menu"><a class="cl-img-replace" href="#0">Menu</a></div>
<?php 
if(!$mbrowid){
?>
		<div id="cl-cart-trigger"><a class="cl-lock" href="#0">Lock</a></div>
<?php
}else{
?>
		<div id="cl-cart-trigger"><a class="cl-user" href="#0">User</a></div>
<?php
}
?>
		
	</header>
<?php
// '_work.php'로 끝나지 않는 파일 호출. module 은 해당 폴더, act 는 해당 페이지.
if($_GET["module"] && $_GET["act"]){
	$url = _CL_PATH_.'modules/'.$_GET["module"].'/'.$_GET["act"];
}else{
	$url = _CL_PATH_.'modules/index/list.php';
}
?>
	<nav id="main-nav">
		<ul>
			<li><a <?php if(($_GET["module"] == "index" && $_GET["act"] == "list.php") || !$_GET["module"]){?>class="current"<?php }?> href="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>?module=index&act=list.php">Home</a></li>
			<li><a <?php if($_GET["module"] == "about" && $_GET["act"] == "list.php"){?>class="current"<?php }?> href="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>?module=about&act=list.php">About</a></li>
			<li><a <?php if($_GET["module"] == "services" && $_GET["act"] == "list.php"){?>class="current"<?php }?> href="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>?module=simulation&act=list.php">Simulation</a></li>
			<li><a <?php if($_GET["module"] == "board" && $_GET["act"] == "list.php"){?>class="current"<?php }?> href="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>?module=board&act=list.php">Board</a></li>
			<li><a <?php if($_GET["module"] == "contact" && $_GET["act"] == "list.php"){?>class="current"<?php }?> href="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>?module=contact&act=list.php">Contact</a></li>
		</ul>
	</nav>

	<main>
<?php
// url 을 require.
require $url;
?>
	</main>

	<div id="cl-shadow-layer"></div>

	<div id="cl-cart">
		<h2>Account <?php if($signinrow[mb_name]) echo "(".$signinrow[mb_name].")";?></h2>
		<ul class="cl-cart-items">
<?php 
if(!$mbrowid){
?>		
			<li>
				<a href="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>?module=member&act=login.php">Log in</a>
			</li>

			<li>
				<a href="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>?module=member&act=join.php">Join us</a>
			</li>	
<?php
}else{
?>
			<li>
				<a href="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>?module=member&act=edit.php">Your personal info</a>
			</li>
			
			<li>
				<a href="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>?module=member&act=logout_work.php&logout=true">Log out</a>
			</li>
	<?php
	//관리자만 볼 수 있도록
	if($signinrow[mb_code] >= 100){
	?>
			<li>
				<a href="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>?module=manage&act=member_list.php">Management</a>
			</li>
	<?php
	}
	?>	
<?php
}
?>				
		</ul> <!-- cl-cart-items -->
<?php 
if($mbrowid){
?>	
		<h2>My page</h2>
		
		<ul class="cl-cart-items">
			<li>
				Simulation Results
			</li>
		</ul>
<?php
}
?>		
	</div> <!-- cl-cart -->
	
	<footer>
		COPYRIGHT(C) LABORATORY FOR SYSTEMS BIOLOGY AND BIO-INSPIRED ENGINEERING. ALL RIHGT RESERVED<br />
		291 DAEHAK-RO, YUSEONG-GU, DAEJEON 305-701, REPUBLIC OF KOREA<br />
		<img src="<?php echo _CL_PATH_HOST_;?>common/img/kaist.jpg" alt="logo">
	</footer>
<input type="hidden"  id="clpathhost" value="<?php echo _CL_PATH_HOST_;?>">	
	
<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
<script src="<?php echo _CL_PATH_HOST_;?>common/js/main.js"></script> <!-- Gem jQuery -->
<script src="<?php echo _CL_PATH_HOST_;?>common/js/svgcheckbx.js"></script>
</body>
</html>
