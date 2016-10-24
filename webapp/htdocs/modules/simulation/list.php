<?php
/* --------------------------------

module/simulation/list.php
시뮬레이션 첫화면 페이지.

-------------------------------- */

//__CL__ 정의 되지 않았다면 false 를 return.
if(!defined('__CL__')) exit();
?>
<div id="cl-content">
	<div id="cl-content-title">Simulation</div>
	<div class='cl-layout'>
		<div class='col-4'>
			<div class='cl-shadowbox-all'>
				Please select module
				<select id="cl-simul-module" class="cl-select" style="margin-bottom:1em;">
					<option value=''>--- Module ---</option>
					<option value='dream2015'>Dream2015</option>
					<option value='sfa'>SFA</option>
					<option value='attractor'>Attractor</option>
				</select>
				
				<div id="cl-simul-dream2015">
					Please select cell line and drugs
					<select id="cl-simul-dream2015-cellline" class="cl-select" style="margin-bottom:1em;">
					
						<option value=''>--- Cellline ---</option>
						
					</select>
					
					<select id="cl-simul-dream2015-drug1" class="cl-select" title="년도 선택" style="margin-bottom:1em; width:49%; float:left; margin-right:2%;">
						<option value=''>--- Drug 1 ---</option>
					</select>
					
					<select id="cl-simul-dream2015-drug2" class="cl-select" title="년도 선택" style="width:49%;">
						<option value=''>--- Drug 2 ---</option>
					</select>
				</div>
				
				<div id="cl-simul-sfa">
					2. SFA
				</div>
				
				<div id="cl-simul-attractor">
					2. Attractor
				</div>
				
			</div>
		</div>
<script type="text/javascript">
google.charts.load('current', {packages: ['corechart', 'bar']});
google.charts.setOnLoadCallback(drawBasic);
</script>
		<div class='col-8' style="padding-left: 1.5%;">
			<div id='cl-simul-dream2015-graph' class='cl-shadowbox-all'>

			</div>
		</div>
	</div>
</div>
