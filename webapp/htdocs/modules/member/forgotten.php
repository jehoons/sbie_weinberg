<?php
/* --------------------------------

module/member/forgotten.php
암호수정 페이지

-------------------------------- */

//__CL__ 정의 되지 않았다면 false 를 return.
if(!defined('__CL__')) exit();

?>
<div id="cl-content">
	<div id="cl-content-title">Account help</div>
	<div class='cl-shadowbox'>
<form action='<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>?module=member&act=forgotten_work.php' method='POST' target='_self' accept-charset='UTF-8' enctype='application/x-www-form-urlencoded' autocomplete='on' id="cl-form">	
		<input type='text' name="mb_email" placeholder='Email' class='cl-text'  data-formdata='email'  value="<?php echo $signinrow["mb_email"];?>">
		
		<input type='text' name="mb_name" placeholder='Full name' class='cl-text'  data-formdata='text'  value="<?php echo $signinrow["mb_name"];?>">
		
		<input type="submit" class="cl-btn" value="Request" />
		<span style="font-size:80%;">We will send you a random password through your email that you already registered .</span>
</form>			 
	</div>


</div>