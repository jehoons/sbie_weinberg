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
<form action='<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>?module=simulation&act=attractor_graph_work.php' method='POST' target='_self' accept-charset='UTF-8' enctype='application/x-www-form-urlencoded' autocomplete='on' id="cl-simul-attractor-form">				
					Please select input nodes and targets<br />
					<input id="cl-simul-attractor-node1" name="node1" type="checkbox" value="1"><label for='cl-simul-attractor-node1' style="display: inline;">S_Mutagen</label>
					<input id="cl-simul-attractor-node2" name="node2" type="checkbox" value="1"><label for='cl-simul-attractor-node2' style="display: inline;">S_GFs</label>
					<input id="cl-simul-attractor-node3" name="node3" type="checkbox" value="1"><label for='cl-simul-attractor-node3' style="display: inline;">S_Nutrients</label>
					<input id="cl-simul-attractor-node4" name="node4" type="checkbox" value="1"><label for='cl-simul-attractor-node4' style="display: inline;">S_TNFalpha</label>
					<input id="cl-simul-attractor-node5" name="node5" type="checkbox" value="1"><label for='cl-simul-attractor-node5' style="display: inline;">S_Hypoxia</label>
					<br /><br />
					<div>
						<div style="height:60px;">
						<select id="cl-simul-attractor-target1" name="target1" class="cl-select" style="margin-bottom:1em; width:30%; float:left;">
							<option value=''>--- Target 1 ---</option>						
						</select>
						
						<input id="cl-simul-attractor-target1-on1" name="target1_on" value="free" type="radio" style=""><label for='cl-simul-attractor-target1-on1' style="display: inline;">Free</label><input id="cl-simul-attractor-target1-on2" name="target1_on" value="1" type="radio" style=""><label for='cl-simul-attractor-target1-on2' style="display: inline;">On</label><input id="cl-simul-attractor-target1-on3" name="target1_on" value="0" type="radio" style=""><label for='cl-simul-attractor-target1-on3' style="display: inline;">Off</label>
						</div>
						
						
						<div style="height:70px;">
						<select id="cl-simul-attractor-target2" name="target2" class="cl-select" style="width:30%;">
							<option value=''>--- Target 2 ---</option>
						</select><input id="cl-simul-attractor-target2-on1" name="target2_on" value="free" type="radio" style=""><label for='cl-simul-attractor-target2-on1' style="display: inline;">Free</label><input id="cl-simul-attractor-target2-on2" name="target2_on" value="1" type="radio" style=""><label for='cl-simul-attractor-target2-on2' style="display: inline;">On</label><input id="cl-simul-attractor-target2-on3" name="target2_on" value="0" type="radio" style=""><label for='cl-simul-attractor-target2-on3' style="display: inline;">Off</label>
						</div>	
					</div>
					<input type="submit" class="cl-btn" value="Submit" />
</form>						
				</div>
				
			</div>
		</div>

		<div class='col-8' style="padding-left: 1.5%;">
			<div id='cl-simul-dream2015-graph' class='cl-shadowbox-all'>
				<div id="example1" style="width: 100%; height: 700px"></div>
				<div id="meandeviation"></div>
			</div>
			
			<div id='cl-simul-attractor-graph' class='cl-shadowbox-all'>
			</div>
		</div>
	</div>
</div>
