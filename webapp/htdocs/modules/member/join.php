<?php
/* --------------------------------

module/member/join.php
회원가입 페이지

-------------------------------- */

//__CL__ 정의 되지 않았다면 false 를 return.
if(!defined('__CL__')) exit();
?>
<div id="cl-content">
	<div id="cl-content-title">Join Us Today</div>
	<div class='cl-shadowbox'>
<form action='<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>?module=member&act=join_work.php' method='POST' target='_self' accept-charset='UTF-8' enctype='application/x-www-form-urlencoded' autocomplete='on' id="cl-form">	
		<input type='text' name="mb_email" placeholder='Email' class='cl-text'  data-formdata='email'  value="<?php echo $_POST["mb_id"];?>">
		
		<input type='password' name="mb_pwd1" placeholder='Password' class='cl-text'  data-formdata='password1'  value="<?php echo $_POST["mb_id"];?>">
		<input type='password' name="mb_pwd2" placeholder='Re-enter password' class='cl-text'  data-formdata='password2'  value="<?php echo $_POST["mb_id"];?>">
		<input type='text' name="mb_name" placeholder='Full name' class='cl-text'  data-formdata='text'  value="<?php echo $_POST["mb_id"];?>">
		<input type='text' name="mb_organization" placeholder='Organization' class='cl-text'  data-formdata='text'  value="<?php echo $_POST["mb_id"];?>">
		<input type="submit" class="cl-btn" value="Sign up" />
		<span style="font-size:80%;">By signing up, you agree to the <a href="#0">Terms of Service</a> and <a href="#0">Privacy Policy</a>.</span>
</form>			 
	</div>


</div>