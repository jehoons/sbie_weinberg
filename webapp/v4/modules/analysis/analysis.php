<?php
if(!defined('__CL__')) exit();

$sql = "
SELECT P.ID as PATIENT_ID, P.NAME as PATIENT_NAME, C.NAME as CANCER_NAME
FROM PATIENT as P inner join CANCER as C
on P.CANCER_ID = C.ID
WHERE P.ID = '$_GET[PATIENT_ID]' 
";
$result = $conn->query($sql);
$row = $result->fetch_assoc();

?>
<div class="module-upspace"></div>

<div class="module-content">
	<div class='layout'>
		<div class='col-8'>
			<div style="margin-bottom:1em; font-size:120%;"><span style="font-weight: bold;"><?php echo $row[PATIENT_NAME];?> 환자</span> 분석결과(<?php echo $row[CANCER_NAME];?> CANCER)</div>
			<div id="simul-tab">                                                                                                                              
                <ul>                                                                                                                                          
                    <li><a href="#att-tab">Attractor</a></li>                                                                                                
                    <li><a href="modules/analysis/analysis_sfa_tab.php">SFA</a></li>
                    <!--<li><a href="#sfa-tab">SFA</a></li>-->                                                                                                      
                    <li><a href="#ml-tab">ML</a></li>                                                                                                         
                </ul>                                                                                                                                         
                <div id="att-tab">                                                                                                                            
                    <p>Attractor</p>                                                                                                                          
                </div>                                                                                                                                        

                <div id="ml-tab">                                                                                                                             
                    <p>ML</p>                                                                                                                                 
                </div>                                                                                                                                        
            </div>
		</div>
		
		<div class='col-4' style="padding-left: 1.5%;">
			<div style="height:32px;"></div>
			<table class="supervisor-table">
				<colgroup>
					<col width='130'>
					<col width='130'>
					<col width='80'>
					<col width='80'>
					<col width='80'>
					<col>
				</colgroup>
				<tr style="background: #F2F2F2">
					<td class="supervisor-td" rowspan="2" style="vertical-align: middle;">약물이름</td>
					<td class="supervisor-td" rowspan="2" style="vertical-align: middle;">약물타겟</td>
					<td class="supervisor-td" colspan="3">Resistance score</td>
				</tr>
				
				<tr style="background: #F2F2F2">
					
					<td class="supervisor-td">Attractor</td>
					<td class="supervisor-td">SFA</td>
					<td class="supervisor-td">ML</td>
				</tr>
<?php 
$sql = "
select T.DRUG_ID1, T.DRUG_ID2, T.DRUG_ID3, AR.ATT_SUMMARY_SCORE as ATTRACTOR, AR.SFA_SUMMARY_SCORE as SFA, AR.ML_SUMMARY_SCORE as ML
from ANALYSIS_RESULT as AR inner join TREATMENT as T
on AR.ANALYSIS_ID=1 and	AR.TREATMENT_ID = T.ID
";
$result = $conn->query($sql);

// 한 페이지당 수, 페이지 수 등등 페이징 기법 변수 global로 세팅
setPage($sql,20,5);

// 게시 번호
$boardnum = $recordsu - $startpoint + 1;

//해당 페이지당 수 만큼 쿼리
while($row = $result->fetch_assoc()) {
	$target_array = array('');
	
	if($row[DRUG_ID1]){
		$sql_drug1 = "
		select *
		from DRUG
		where ID = $row[DRUG_ID1]
		";
		$result_drug1 = $conn->query($sql_drug1);
		$row_drug1 = $result_drug1->fetch_assoc();
		$drug = $row_drug1[NAME];
		
		$sql_drug1_target = "
		select G.SYMBOL as GENE_SYMBOL
		from DRUG_TARGET as D inner join GENE as G
		on D.GENE_ID = G.ID
		where D.DRUG_ID = $row[DRUG_ID1]
		";
		$result_drug1_target = $conn->query($sql_drug1_target);
		while($row_drug1_target = $result_drug1_target->fetch_assoc()){
			array_push($target_array, "$row_drug1_target[GENE_SYMBOL]");
		}
	}
	
	if($row[DRUG_ID2]){
		$sql_drug2 = "
		select *
		from DRUG
		where ID = $row[DRUG_ID2]
		";
		$result_drug2 = $conn->query($sql_drug2);
		$row_drug2 = $result_drug2->fetch_assoc();
		$drug .= ", ".$row_drug2[NAME];
		
		$sql_drug2_target = "
		select G.SYMBOL as GENE_SYMBOL
		from DRUG_TARGET as D inner join GENE as G
		on D.GENE_ID = G.ID
		where D.DRUG_ID = $row[DRUG_ID1]
		";
		$result_drug2_target = $conn->query($sql_drug2_target);
		while($row_drug2_target = $result_drug2_target->fetch_assoc()){
			array_push($target_array, "$row_drug2_target[GENE_SYMBOL]");
		}
	}
	
	if($row[DRUG_ID3]){
		$sql_drug3 = "
		select *
		from DRUG
		where ID = $row[DRUG_ID3]
		";
		$result_drug3 = $conn->query($sql_drug3);
		$row_drug3 = $result_drug3->fetch_assoc();
		$drug .= ", ".$row_drug3[NAME];
		
		$sql_drug3_target = "
		select G.SYMBOL as GENE_SYMBOL
		from DRUG_TARGET as D inner join GENE as G
		on D.GENE_ID = G.ID
		where D.DRUG_ID = $row[DRUG_ID1]
		";
		$result_drug3_target = $conn->query($sql_drug3_target);
		while($row_drug3_target = $result_drug3_target->fetch_assoc()){
			array_push($target_array, "$row_drug3_target[GENE_SYMBOL]");
		}
	}
	
	array_shift($target_array); //가장 앞에 있는 배열 값 제거
	$commaList = implode(', ', $target_array);
?>					
				<tr>
					<td class="supervisor-td"><?php echo $drug?></td>
					<td class="supervisor-td"><?php echo $commaList;?></td>
					<td class="supervisor-td"><?php echo round($row[ATTRACTOR],3);?></td>
					<td class="supervisor-td"><?php echo round($row[SFA],3);?></td>
					<td class="supervisor-td"><?php echo round($row[ML],3);?></td>
				</tr>
<?php
}?>					
			</table>
			<div style="margin-top:2.5em; margin-bottom:1.5em;"><?php echo getPage();?></div>
		</div>
	</div>
</div>	
