<?php
/* --------------------------------

module/manage/member_edit_list.php
관리자 회원정보 수정  페이지.

-------------------------------- */

//__CL__ 정의 되지 않았다면 false 를 return.
if(!defined('__CL__')) exit();

//관리자인지 체크 : mb_code가 100이상일 때 관리자.
manageCheck($signinrow[mb_code]);

//mb_rowid 받아오기
if($_GET["mb_rowid"]){
	$mb_rowid = $_GET['mb_rowid'];

	//회원 정보 쿼리
	$sql = "
	SELECT *
	FROM member
	WHERE mb_rowid = '$mb_rowid'
	";
	$result = $conn->query($sql);
	$editrow = $result->fetch_assoc();
}else{
	exit();
}
?>
<div id="cl-content">
	<div id="cl-content-title">Personal Info Update</div>
	<div class='cl-shadowbox'>
<form action='<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>?module=manage&act=member_edit_work.php' method='POST' target='_self' accept-charset='UTF-8' enctype='application/x-www-form-urlencoded' autocomplete='on' id="cl-form">	
		<input type='text' name="mb_email" placeholder='Email' class='cl-text'  data-formdata='email'  value="<?php echo $editrow["mb_email"];?>" readonly>
		
		<input type='text' name="mb_name" placeholder='Full name' class='cl-text'  data-formdata='text'  value="<?php echo $editrow["mb_name"];?>">
		<input type='text' name="mb_organization" placeholder='Organization' class='cl-text'  data-formdata='text'  value="<?php echo $signinrow["mb_organization"];?>">
		
		<div class="cl-select-wrapper" style='width: 100%;'>
		<select name="mb_code" class="cl-select" title="선택"  data-formdata='select' >
			<option value=''>회원구분</option>
			<option value='1'  <?php if($editrow["mb_code"] == '1'){?>selected<?php }?>>일반회원 - 1</option>
			<option value='10'  <?php if($editrow["mb_code"] == '10'){?>selected<?php }?>>탈퇴회원 - 10</option>
			<option value='100'  <?php if($editrow["mb_code"] == '100'){?>selected<?php }?>>관리자 - 100</option>
		</select>
		</div>
		
		<input type="submit" class="cl-btn" value="Update" />
		
		<input type="hidden" name="mb_rowid" value="<?php echo $mb_rowid;?>">
		<input type="hidden" name="module" value="<?php echo $_GET["module"];?>">
		<input type="hidden" name="act" value="<?php echo $_GET["act"];?>">
		<input type="hidden" name="orderby" value="<?php echo $_GET["orderby"];?>">
		<input type="hidden" name="orderopt" value="<?php echo $_GET["orderopt"];?>">
		<input type="hidden" name="searchStr" value="<?php echo $_GET["searchStr"];?>">
		<input type="hidden" name="searchColumn" value="<?php echo $_GET["searchColumn"];?>">
		<input type="hidden" name="pagenum" value="<?php echo $_GET["pagenum"];?>">
		
</form>			 
	</div>


</div>