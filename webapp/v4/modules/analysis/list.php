<?php
if(!defined('__CL__')) exit();
?>
<div class="module-upspace"></div>

<div class="module-content-wraper">
	<div class="module-content">
	<button class="board-button" id="paitent-add" style="float:right; margin-left:5px;">추가</button>
	<form action='<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>?module=<?php echo $_GET["module"];?>&act=<?php echo $_GET["act"];?>'  method='GET' target='_self' accept-charset='UTF-8' enctype='application/x-www-form-urlencoded' autocomplete='on' id="booklistsearchform">	
	<input type="submit" class="board-button" value="검색" style="float:right;">
	<input type="text" name="searchStr" class="search-text" style="float:right;" placeholder="Search"  value="<?php echo $_GET["searchStr"];?>">
	<input type="hidden" name="module" value="<?php echo $_GET["module"];?>">
	<input type="hidden" name="act" value="<?php echo $_GET["act"];?>">
	</form>
	<table class="supervisor-table">
		<colgroup>
			<col width='50'>
			<col width='70'>
			<col width='100'>
			<col width='100'>
			<col width='100'>
			<col width='100'>
			<col width='100'>
			<col width=''>
			<col width='150'>
			<col width='150'>
			<col>
		</colgroup>
		<tr style="background: #F2F2F2">
			<td class="supervisor-td"></td>
			<td class="supervisor-td">Number</td>
			<td class="supervisor-td">Patient</td>
			<td class="supervisor-td">Cancer type</td>
			<td class="supervisor-td">Expression</td>
			<td class="supervisor-td">Mutation</td>
			<td class="supervisor-td">CNV</td>
			<td class="supervisor-td">Contents</td>
			<td class="supervisor-td">Analysis</td>
			<td class="supervisor-td">Work</td>
		</tr>
<?php
// 검색어가 있다면 where 절 추가.
$where = "";
if($_GET["searchStr"]){
	//searchColumn, searchStr 모두 띄어쓰기로 구분할 수 있다.
	$searchColumn = "pt_name";
	$where = "WHERE ".getSearch($searchColumn, $_GET["searchStr"]);
}
$orderby = "ORDER BY pt_rowid DESC";

$sql = "
SELECT *
FROM patient
$where
$orderby
";
$result = $conn->query($sql);

// 한 페이지당 수, 페이지 수 등등 페이징 기법 변수 global로 세팅
setPage($sql,20,5);

// 게시 번호 
$boardnum = $recordsu - $startpoint + 1;

//해당 페이지당 수 만큼 쿼리
while($row = $result->fetch_assoc()) {
$boardnum--;
?>
		<tr>
			<td class="supervisor-td"><input type="checkbox" id="myCheck"></td>
			<td class="supervisor-td"><?php echo $boardnum?></td>
			<td class="supervisor-td"><?php echo $row[pt_name]?></td>
			<td class="supervisor-td"><?php echo $row[pt_cancertype]?></td>
			<td class="supervisor-td"><?php echo $row[pt_expression]?></td>
			<td class="supervisor-td"><?php echo $row[pt_mutation]?></td>
			<td class="supervisor-td"><?php echo $row[pt_cnv]?></td>
			<td class="supervisor-td"></td>
			<td class="supervisor-td"><a href="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>?module=analysis&act=analysis.php&pt_rowid=<?php echo $row["pt_rowid"]?>">분석완료</a></td>
			<td class="supervisor-td">Edit / <a href="#0" class="delete-open" data-urldata="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>?module=analysis&act=patient_delete_work.php&pagenum=<?php echo $_GET["pagenum"];?>&searchColumn=<?php echo $_GET["searchColumn"];?>&searchStr=<?php echo $_GET["searchStr"];?>&orderby=<?php echo $_GET["orderby"];?>&orderopt=<?php echo $_GET["orderopt"];?>&pt_rowid=<?php echo $row["pt_rowid"]?>">Delete</a></td>
		</tr>
<?php
}
?>					
		</table>
		
		<div style="margin-top:2.5em;"><?php echo getPage();?></div>
	</div>
</div>