<?php
if(!defined('__CL__')) exit();
$start_time = array_sum(explode(' ', microtime()));
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
			<col width='100'>
			<col width='100'>
			<col width=''>
			<col width=''>
			<col width=''>
			<col width='100'>
			<col width='100'>
			<col>
		</colgroup>
		<tr style="background: #F2F2F2">
			<td class="supervisor-td"></td>
			<td class="supervisor-td">환자명</td>
			<td class="supervisor-td">암종</td>
			<td class="supervisor-td">Mutation (amino acid change)</td>
			<td class="supervisor-td">CNA (log fold change)</td>
			<td class="supervisor-td">mRNA expression (z-score)</td>
			<td class="supervisor-td">분석상태</td>
			<td class="supervisor-td">Work</td>
		</tr>
<?php
// 검색어가 있다면 where 절 추가.
$where = "";
if($_GET["searchStr"]){
	//searchColumn, searchStr 모두 띄어쓰기로 구분할 수 있다.
	$searchColumn = "P.NAME";
	$where = "WHERE ".getSearch($searchColumn, $_GET["searchStr"]);
}
$orderby = "ORDER BY PATIENT_ID DESC";

$sql = "
select P.ID as PATIENT_ID, P.NAME as PATIENT_NAME, C.NAME as CANCER_NAME, C.ID as CANCER_ID, A.STATUS as ANALYSIS_STATUS
from PATIENT as P inner join CANCER as C inner join ANALYSIS as A
on P.CANCER_ID = C.ID and P.ID = A.PATIENT_ID
$where
$orderby
";
$result = $conn->query($sql);

// 한 페이지당 수, 페이지 수 등등 페이징 기법 변수 global로 세팅
setPage($sql,20,10);

// 게시 번호 
$boardnum = $recordsu - $startpoint + 1;

//해당 페이지당 수 만큼 쿼리
while($row = $result->fetch_assoc()) {
	$boardnum--;
	$mutation_contents = "";
	$mutation_array = array('');
	$cna_array = array('');
	$mrna_array = array('');
	
	//분석상태
	if($row[ANALYSIS_STATUS]){
		$status = "<a href=".htmlspecialchars($_SERVER[PHP_SELF])."?module=analysis&act=analysis.php&PATIENT_ID=".$row[PATIENT_ID]." style='color:#000000;'>완료</a>";
	}else{
		$status = "<span style='color:#BCBCBC;'>진행중</span>";	
	}

	//Mutaion정보
	$sql_mutation = "
	select count(*) as MUTATION_COUNT
	from MUTATION
	where PATIENT_ID = $row[PATIENT_ID]
	";
	$result_mutation = $conn->query($sql_mutation);
	$row_mutation = $result_mutation->fetch_assoc();
	$mutation_count = $row_mutation[MUTATION_COUNT];
	
	$sql_mutation = "
	select M.ID as MUTATION_ID, M.AA as MUTATION_AA, G.SYMBOL as GENE_SYMBOL, T.NAME as MUTATIONTYPE_NAME
	from MUTATION as M inner join GENE as G inner join MUTATIONTYPE as T inner join (select * from DRIVER where CANCER_ID = $row[CANCER_ID]) as D
	on M.GENE_ID = G.ID and M.MUTATIONTYPE_ID = T.ID and M.GENE_ID = D.GENE_ID 
	where M.PATIENT_ID = $row[PATIENT_ID]
	LIMIT 3
	";
	$result_mutation = $conn->query($sql_mutation);
	while($row_mutation = $result_mutation->fetch_assoc()){
		array_push($mutation_array, "$row_mutation[GENE_SYMBOL]($row_mutation[MUTATION_AA])");
	}
	
	array_shift($mutation_array); //가장 앞에 있는 배열 값 제거
	$mutation_commaList = implode(', ', $mutation_array);
	if($mutation_commaList){
		$mutation_contents = "<span style='color:#D93131;'>".$mutation_count."개</span> - ".stringCut($mutation_commaList,200)."...";
	}else{
		$mutation_contents = "<span style='color:#D93131;'>".$mutation_count."개</span>";
	}
	
	
	//CNA정보
	$sql_cna = "
	select C.ID as CNA_ID, C.VALUE as CNA_VALUE, G.SYMBOL as GENE_SYMBOL
	from CNA as C inner join GENE as G inner join (select * from DRIVER where CANCER_ID = $row[CANCER_ID]) as D
	on C.GENE_ID = G.ID
	where C.PATIENT_ID = $row[PATIENT_ID]
	LIMIT 3
	";
	$result_cna = $conn->query($sql_cna);
	while($row_cna = $result_cna->fetch_assoc()){
		array_push($cna_array, "$row_cna[GENE_SYMBOL]($row_cna[CNA_VALUE])");
	}
	
	array_shift($cna_array); //가장 앞에 있는 배열 값 제거
	$cna_commaList = implode(', ', $cna_array);
	$cna_contents = stringCut($cna_commaList,200)."...";
	
	//MRNA정보
	$sql_mrna = "
	select M.ID as MRNA_ID, M.VALUE as MRNA_VALUE, G.SYMBOL as GENE_SYMBOL
	from MRNA as M inner join GENE as G
	on M.GENE_ID = G.ID
	where M.PATIENT_ID = $row[PATIENT_ID]
	LIMIT 3
	";
	$result_mrna = $conn->query($sql_mrna);
	while($row_mrna = $result_mrna->fetch_assoc()){
		$row_mrna[MRNA_VALUE] = round($row_mrna[MRNA_VALUE],5);
		array_push($mrna_array, "$row_mrna[GENE_SYMBOL]($row_mrna[MRNA_VALUE])");
	}
	
	array_shift($mrna_array); //가장 앞에 있는 배열 값 제거
	$mrna_commaList = implode(', ', $mrna_array);
	$mrna_contents = stringCut($mrna_commaList,200)."...";
?>
		<tr>
			<td class="supervisor-td"><input type="checkbox" id="myCheck"></td>
			<td class="supervisor-td"><?php echo $row[PATIENT_NAME]?></td>
			<td class="supervisor-td"><?php echo $row[CANCER_NAME]?></td>
			<td class="supervisor-td" style="text-align:left; padding-left:0.5em;"><?php echo $mutation_contents?></td>
			<td class="supervisor-td" style="text-align:left; padding-left:0.5em;"><?php echo $cna_contents?></td>
			<td class="supervisor-td" style="text-align:left; padding-left:0.5em;"><?php echo $mrna_contents?></td>
			<td class="supervisor-td"><?php echo $status?></td>
			<td class="supervisor-td">Edit / Delete
			<!--<a href="#0" class="delete-open" data-urldata="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>?module=analysis&act=patient_delete_work.php&pagenum=<?php echo $_GET["pagenum"];?>&searchColumn=<?php echo $_GET["searchColumn"];?>&searchStr=<?php echo $_GET["searchStr"];?>&orderby=<?php echo $_GET["orderby"];?>&orderopt=<?php echo $_GET["orderopt"];?>&pt_rowid=<?php echo $row["pt_rowid"]?>">Delete</a>  -->
			</td>
		</tr>
<?php
}

$end_time = array_sum(explode(' ', microtime()));
echo $end_time - $start_time;
?>					
		</table>
		
		<div style="margin-top:2.5em;"><?php echo getPage();?></div>
	</div>
</div>