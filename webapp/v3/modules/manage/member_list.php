<?php
/* --------------------------------

module/manage/member_list.php
관리자 회원관리 페이지.

-------------------------------- */

//__CL__ 정의 되지 않았다면 false 를 return.
if(!defined('__CL__')) exit();

//관리자인지 체크 : mb_code가 100이상일 때 관리자.
manageCheck($signinrow[mb_code]);
?>
<div id="cl-content">
	<div id="cl-content-title">Management</div>
	
	<table class="cl-manage-table">
		<colgroup>
			<col width='50px'>
			<col width='100px'>
			<col width='200px'>
			<col width='150px'>
			<col width='200px'>
			<col width='200px'>
			<col width='100px'>
			<col width='200px'>
			<col width='200px'>
			<col>
		</colgroup>
		<tr class="cl-manage-title">
			<td class="cl-manage-td">번호</td>
			
			<td class="cl-manage-td"><a href="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>?module=manage&act=member.php&pagenum=<?php echo $_GET["pagenum"];?>&searchColumn=<?php echo $_GET["searchColumn"];?>&searchStr=<?php echo $_GET["searchStr"];?>&orderby=mb.mb_fullname&orderopt=ASC">이름</a></td>
			
			<td class="cl-manage-td"><a href="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>?module=manage&act=member.php&pagenum=<?php echo $_GET["pagenum"];?>&searchColumn=<?php echo $_GET["searchColumn"];?>&searchStr=<?php echo $_GET["searchStr"];?>&orderby=mb.mb_id&orderopt=ASC">이메일(아이디)</a></td>
			
			<td class="cl-manage-td"><a href="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>?module=manage&act=member.php&pagenum=<?php echo $_GET["pagenum"];?>&searchColumn=<?php echo $_GET["searchColumn"];?>&searchStr=<?php echo $_GET["searchStr"];?>&orderby=mb.mb_code&orderopt=ASC">회원구분</a></td>
			
			<td class="cl-manage-td"><a href="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>?module=manage&act=member.php&pagenum=<?php echo $_GET["pagenum"];?>&searchColumn=<?php echo $_GET["searchColumn"];?>&searchStr=<?php echo $_GET["searchStr"];?>&orderby=mb.mb_writedatetime&orderopt=ASC">가입일</a></td>
			
			<td class="cl-manage-td"><a href="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>?module=manage&act=member.php&pagenum=<?php echo $_GET["pagenum"];?>&searchColumn=<?php echo $_GET["searchColumn"];?>&searchStr=<?php echo $_GET["searchStr"];?>&orderby=mb.mb_recentdatetime&orderopt=ASC">최근방문일</a></td>
			
			<td class="cl-manage-td"><a href="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>?module=manage&act=member.php&pagenum=<?php echo $_GET["pagenum"];?>&searchColumn=<?php echo $_GET["searchColumn"];?>&searchStr=<?php echo $_GET["searchStr"];?>&orderby=mb.mb_visitnum&orderopt=ASC">방문</a></td>
			
	<td class="cl-manage-td"><a href="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>?module=manage&act=member.php&pagenum=<?php echo $_GET["pagenum"];?>&searchColumn=<?php echo $_GET["searchColumn"];?>&searchStr=<?php echo $_GET["searchStr"];?>&orderby=mb.mb_writedatetime&orderopt=ASC">탈퇴일</a></td>
			
			<td class="cl-manage-td">기능</td>
		</tr>
<?php
// 검색어가 있다면 where 절 추가.
$where = "";
if($_GET["searchColumn"] && $_GET["searchStr"]){
	$where = "WHERE ".getSearch($_GET["searchColumn"], $_GET["searchStr"]);
}

if($_GET["orderby"]){
	$orderby = "ORDER BY ".$_GET["orderby"]." ".$_GET["orderopt"];
}else{
	$orderby = "ORDER BY mb_rowid DESC";
}

// choonlog_member, choonlog_book 쿼리
$sql = "
SELECT *
FROM member
$where
$orderby
";
$result = $conn->query($sql);

// 한 페이지당 수, 페이지 수 등등 페이징 기법 변수 global로 세팅
setPage($sql,10,5);

// 게시 번호 
$boardnum = $recordsu - $startpoint + 1;

//해당 페이지당 수 만큼 쿼리
while($row = $result->fetch_assoc()) {
$boardnum--;
?>
		<tr class="cl-manage-tr">
			<td class="cl-manage-td"><?php echo $boardnum;?></td>
			<td class="cl-manage-td"><?php echo $row[mb_name];?></td>
			<td class="cl-manage-td"><?php echo $row[mb_email];?></td>
			<td class="cl-manage-td"><?php echo $row[mb_code];?></td>
			<td class="cl-manage-td"><?php echo $row[mb_writedatetime];?></td>
			<td class="cl-manage-td"><?php echo $row[mb_recentdatetime];?></td>
			<td class="cl-manage-td"><?php echo $row[mb_visitnum];?></td>
			<td class="cl-manage-td"><?php echo $row[mb_outdatetime];?></td>
			<td class="cl-manage-td">
			
			<a href="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>?module=manage&act=member_edit_list.php&pagenum=<?php echo $_GET["pagenum"];?>&searchColumn=<?php echo $_GET["searchColumn"];?>&searchStr=<?php echo $_GET["searchStr"];?>&orderby=<?php echo $_GET["orderby"];?>&orderopt=<?php echo $_GET["orderopt"];?>&mb_rowid=<?php echo $row["mb_rowid"]?>" class="cl-btn-small">수정</a>&nbsp;/
<?php 
if($row[mb_code] < 100){
?>			
			<a href="#" class="cl-btn-small delete-open" data-urldata="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>?module=manage&act=member_del_work.php&pagenum=<?php echo $_GET["pagenum"];?>&searchColumn=<?php echo $_GET["searchColumn"];?>&searchStr=<?php echo $_GET["searchStr"];?>&orderby=<?php echo $_GET["orderby"];?>&orderopt=<?php echo $_GET["orderopt"];?>&mb_rowid=<?php echo $row["mb_rowid"]?>">삭제</a>
<?php } else {?>
			삭제불가(관리자)
<?php }?>					
			
			</td>
		</tr>
<?php }?>		
		
		
	</table>
	
	<div><?php echo getPage();?></div>
	
	<div>
	<form action='<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>?module=<?php echo $_GET["module"];?>&act=<?php echo $_GET["act"];?>'  method='GET' target='_self' accept-charset='UTF-8' enctype='application/x-www-form-urlencoded' autocomplete='on' id="booklistsearchform">
	<input type="hidden" name="module" value="<?php echo $_GET["module"];?>">
	<input type="hidden" name="act" value="<?php echo $_GET["act"];?>">
	<input type="hidden" name="orderby" value="<?php echo $_GET["orderby"];?>">
	<input type="hidden" name="orderopt" value="<?php echo $_GET["orderopt"];?>">			
				<div style="width:320px; margin:auto;">
					<div class="cl-select-wrapper" style="float:left;">
					<select name="searchColumn" class="cl-select-search" title="년도 선택" style="width:100px; float:left;">
						<option value='mb_name' <?php if($_GET["searchColumn"] == "mb_name"){?>selected<?php }?>>이름</option>
						<option value='mb_email' <?php if($_GET["searchColumn"] == "mb_email"){?>selected<?php }?>>이메일</option>
						<option value='mb_code' <?php if($_GET["searchColumn"] == "mb_code"){?>selected<?php }?>>코드</option>
					</select>
					</div>
					
				    <div style="width:150px; float:left;"><input type='text' name="searchStr" placeholder='검색어' class='cl-text-search' value="<?php echo $_GET["searchStr"];?>"></div>
				    <div style="width:70px; float:left;"><input type="submit" class="cl-btn-search" value="조회"></div>
				</div>
	</form>			
	</div>			
</div>