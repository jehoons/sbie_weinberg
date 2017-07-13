<?php
/* --------------------------------

module/member/password.php
회원암호수정 페이지.

-------------------------------- */

//__CL__ 정의 되지 않았다면 false 를 return.
if(!defined('__CL__')) exit();

?>
<div id="cl-content">
	<div id="cl-content-title">Password Change</div>
	<div class='cl-shadowbox'>
<form action='<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>?module=member&act=password_work.php' method='POST' target='_self' accept-charset='UTF-8' enctype='application/x-www-form-urlencoded' autocomplete='on' id="cl-form">	
		<input type='text' name="mb_email" placeholder='Email' class='cl-text'  data-formdata='email'  value="<?php echo $signinrow["mb_email"];?>" readonly>
		
		<input type='password' name="mb_oldpwd" placeholder='Current password' class='cl-text'  data-formdata='pwd'>
		<input type='password' name="mb_pwd1" placeholder='New password' class='cl-text'  data-formdata='password1'>
		<input type='password' name="mb_pwd2" placeholder='Re-enter new password' class='cl-text'  data-formdata='password2'>
		
		<input type="submit" class="cl-btn" value="Update" />
</form>			 
	</div>


</div>