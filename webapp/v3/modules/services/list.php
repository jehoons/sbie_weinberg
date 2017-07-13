<?php
/* --------------------------------

module/Services/list.php
플랫폼 페이지

-------------------------------- */

//__CL__ 정의 되지 않았다면 false 를 return.
if(!defined('__CL__')) exit();
?>
<div id="cl-content">
	<div id="cl-content-title">Services</div>Step 2. Combination drug
	<form class="ac-custom ac-checkbox ac-checkmark" autocomplete="off">
		<ul>

<?php
$where = "";
if($_GET["searchColumn"] && $_GET["searchStr"]){
	$where = "AND ".getSearch($_GET["searchColumn"], $_GET["searchStr"]);
}

// sql to select the information
$sql = "
SELECT *
FROM drugs";
$result = $conn->query($sql);
$li_num == 0;
while($row = $result->fetch_assoc()) {
$li_num++;
?>
<li><input id="<?php echo $li_num?>" name="<?php echo $li_num?>" type="checkbox"><label for="<?php echo $li_num?>"><?php echo $row["sbie_id"]?>processes</label></li>
<?php 
}
?>
		</ul>
		<input type="button" class="cl-btn-inner" value="SAVE" />
	</form>
</div>