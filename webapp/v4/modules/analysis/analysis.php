<?php
if(!defined('__CL__')) exit();

$sql = "
SELECT *
FROM patient
WHERE pt_rowid = '$_GET[pt_rowid]' 
";
$result = $conn->query($sql);
$row = $result->fetch_assoc();

?>
<div class="module-upspace"></div>

<div class="module-content">
	<div class='layout'>
		<div class='col-4'>
				<div style="margin-bottom:1em; font-size:120%;"><span style="font-weight: bold;"><?php echo $row[pt_name];?> 환자</span> 분석결과(<?php echo $row[pt_cancertype];?>, <?php echo $row[pt_expression];?>, <?php echo $row[pt_mutation];?>, <?php echo $row[pt_cnv];?>)</div>
				<table class="supervisor-table">
					<colgroup>
						<col width='70'>
						<col width='100'>
						<col width='100'>
						<col width='100'>
						<col width='100'>
						<col width='100'>
						<col>
					</colgroup>
					<tr style="background: #F2F2F2">
						<td class="supervisor-td">Number</td>
						<td class="supervisor-td">약물이름</td>
						<td class="supervisor-td">약물타겟</td>
						<td class="supervisor-td">Attractor</td>
						<td class="supervisor-td">SFA</td>
						<td class="supervisor-td">ML</td>
					</tr>
					
					<tr>
						<td class="supervisor-td"></td>
						<td class="supervisor-td">FTI-227</td>
						<td class="supervisor-td">AKT1<br />AKT2</td>
						<td class="supervisor-td">5.32</td>
						<td class="supervisor-td">12.8</td>
						<td class="supervisor-td">11.99</td>
					</tr>
					
					<tr>
						<td class="supervisor-td"></td>
						<td class="supervisor-td">FTI-227</td>
						<td class="supervisor-td">AKT1<br />AKT2</td>
						<td class="supervisor-td">5.32</td>
						<td class="supervisor-td">12.8</td>
						<td class="supervisor-td">11.99</td>
					</tr>
					
					<tr>
						<td class="supervisor-td"></td>
						<td class="supervisor-td">FTI-227</td>
						<td class="supervisor-td">AKT1<br />AKT2</td>
						<td class="supervisor-td">5.32</td>
						<td class="supervisor-td">12.8</td>
						<td class="supervisor-td">11.99</td>
					</tr>
				</table>
		</div>
		
		<div class='col-8' style="padding-left: 1.5%;">탭 화면 출력 예정..
		</div>
	</div>
</div>	