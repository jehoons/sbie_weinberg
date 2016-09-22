<?php
/* --------------------------------

config/handler.php
header, menu, footer 를 구성하고  main은  modules의 페이지가 차지하여 기능 하도록.

-------------------------------- */
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
	<script src="<?php echo _CL_PATH_HOST_;?>common/js/modernizr.js"></script> <!-- Modernizr -->
	<script type="text/javascript" src="https://www.google.com/jsapi"></script>
  	
	<title>Anti-cancer drug recommendation platform</title>
</head>


<body>
	<header>
		<div id="logo">SBIE<!-- <img src="<?php echo _CL_PATH_HOST_;?>common/img/cl-logo.svg" alt="Homepage"> --></div>

		<div id="cl-hamburger-menu"><a class="cl-img-replace" href="#0">Menu</a></div>
		<div id="cl-cart-trigger"><a class="cl-img-replace" href="#0">Cart</a></div>
	</header>
<?php
// module 은 해당 폴더, act 는 해당 페이지.
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
			<li><a <?php if($_GET["module"] == "services" && $_GET["act"] == "list.php"){?>class="current"<?php }?> href="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>?module=services&act=list.php">Services</a></li>
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
		<h2>Account</h2>
		<ul class="cl-cart-items">
			<li>
				Login
			</li>

			<li>
				Join us
			</li>
		</ul> <!-- cl-cart-items -->
		
		<h2>Search</h2>
		
		<ul class="cl-cart-items">
			<li>
				search
			</li>
		</ul>

		<a href="#0" class="checkout-btn">Search</a>
	</div> <!-- cl-cart -->
	
	<footer>
		COPYRIGHT(C) LABORATORY FOR SYSTEMS BIOLOGY AND BIO-INSPIRED ENGINEERING. ALL RIHGT RESERVED<br />
		291 DAEHAK-RO, YUSEONG-GU, DAEJEON 305-701, REPUBLIC OF KOREA<br />
		<img src="<?php echo _CL_PATH_HOST_;?>common/img/kaist.jpg" alt="logo">
	</footer>
<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
<script src="<?php echo _CL_PATH_HOST_;?>common/js/main.js"></script> <!-- Gem jQuery -->
<script src="<?php echo _CL_PATH_HOST_;?>common/js/svgcheckbx.js"></script>
</body>
</html>