<?php
/* --------------------------------

module/member/edit.php
회원정보수정 페이지.

-------------------------------- */

//__CL__ 정의 되지 않았다면 false 를 return.
if(!defined('__CL__')) exit();

?>
<div id="cl-content">
	<div id="cl-content-title">Your Personal Info</div>
	<div class='cl-shadowbox'>
<form action='<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>?module=member&act=edit_work.php' method='POST' target='_self' accept-charset='UTF-8' enctype='application/x-www-form-urlencoded' autocomplete='on' id="cl-form">	
		<input type='text' name="mb_email" placeholder='Email' class='cl-text'  data-formdata='email'  value="<?php echo $signinrow["mb_email"];?>" readonly>
		
		<input type='text' name="mb_name" placeholder='Full name' class='cl-text'  data-formdata='text'  value="<?php echo $signinrow["mb_name"];?>">
		<input type='text' name="mb_organization" placeholder='Organization' class='cl-text'  data-formdata='text'  value="<?php echo $signinrow["mb_organization"];?>">
		
		<input type="submit" class="cl-btn" value="Update" />
		<span class="cl-form-span">If you want to chage your password, <a href="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>?module=member&act=password.php">Click here.</a> If you want to delete your account, <a href="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>?module=member&act=delete.php">Click here</a></span>
</form>			 
	</div>


</div>