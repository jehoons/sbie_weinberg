<?php
/* --------------------------------

module/member/login.php
로그인 페이지

-------------------------------- */

//__CL__ 정의 되지 않았다면 false 를 return.
if(!defined('__CL__')) exit();
?>
<div id="cl-content">
	<div id="cl-content-title">Log in</div>
	<div class='cl-shadowbox'>
<form action='<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>?module=member&act=login_work.php' method='POST' target='_self' accept-charset='UTF-8' enctype='application/x-www-form-urlencoded' autocomplete='on' id="cl-form">	
		<input type='text' name="signinemail" placeholder='Email' class='cl-text'  data-formdata='id'  value="<?php echo $_POST["mb_id"];?>">
		
		<input type='password' name="signinpwd" placeholder='Password' class='cl-text'  data-formdata='pwd'  value="<?php echo $_POST["mb_id"];?>">
		
		<input type="submit" class="cl-btn" value="Log in" />
		<span class="cl-form-span"><a href="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>?module=member&act=forgotten.php">Forgot account?</a></span>
</form>			 
	</div>


</div>