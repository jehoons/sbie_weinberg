<?php
/* --------------------------------

module/member/delete.php
회원탈퇴 페이지

-------------------------------- */

//__CL__ 정의 되지 않았다면 false 를 return.
if(!defined('__CL__')) exit();

?>
<div id="cl-content">
	<div id="cl-content-title">Account Delete</div>
	<div class='cl-shadowbox'>
<form action='<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>?module=member&act=delete_work.php' method='POST' target='_self' accept-charset='UTF-8' enctype='application/x-www-form-urlencoded' autocomplete='on' id="cl-form">	
		<input type='text' name="mb_email" placeholder='Email' class='cl-text'  data-formdata='email'  value="<?php echo $signinrow["mb_email"];?>" readonly>
		
		<input type='password' name="mb_pwd" placeholder='New password' class='cl-text'  data-formdata='pwd'>
		<label class='cl-label' for='mboutreason'>Why do you leave here?</label>
		<textarea class='cl-textarea' name='mb_outreason' data-formdata='text' id='mboutreason'></textarea>
		
		<input type="submit" class="cl-btn" value="DELETE" />
		<span style="font-size:80%;">If you want to chage your password, <a href="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>?module=member&act=password.php">Click here.</a></span>
</form>			 
	</div>

</div>