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
				Please select cancer type<p>
                <div id="cl-simul-cancertype">
                    <input type="radio" id="colon" name="cancer_type" value="Colon cancer"> <label for ="colon">Colon cancer</label> <br>
                    <input type="radio" id="breast" name="cancer_type"  value="Breast cancer"> <label for="breast">Breast cancer</label> <br>
                    <input type="radio" id="lung" name="cancer_type" value="Lung cancer"> <label for="lung">Lung cancer</label>
                </div>
                
				
                <div id="cl-simul-patient-or-cellline">
                    <button id="cl-simul-select-patient" class="cl-btn", style="width:49%; float:left; margin-right:2%;">Patient</button>
                    <button id="cl-simul-select-cellline" class="cl-btn", style="width:49%;">Cell line</button>
                </div>
				<div id="cl-simul-condition">
                    <div id="cl-simul-cellline">
<form action='<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>?module=simulation&act=dream2015_graph_work.php' method='POST' target='_self' accept-charset='UTF-8' enctype='application/x-www-form-urlencoded' autocomplete='on' id="cl-simul-cellline-form">				
    					<br>Please select cell line & drugs
    					<select id="cl-simul-selected-cellline" name="cell" class="cl-select" style="margin-bottom:1em;">
    					
    						<option value=''>--- Cellline ---</option>
     					
    					</select>
                        <div>
                            <select id="cl-simul-dream2015-drug1" name="drug1" class="cl-select" title="약물 선택" style="margin-bottom:1em; width:49%; float:left; margin-right:2%;">
                                <option value=''>--- Drug 1 ---</option>
                            </select>
    
                            <select id="cl-simul-dream2015-drug2" name="drug2" class="cl-select" title="약물 선택" style="width:49%;">
                                <option value=''>--- Drug 2 ---</option>
                            </select>
                        </div>
                        <br>Single drug
                        <select id="cl-simul-selected-cellline-single" name="cell-single" class="cl-select" style="margin-bottom:1em;">

                            <option value=''>--- Cellline ---</option>

                        </select>
                        <div>
                            <select id="cl-simul-single-drug" name="drug-single" class="cl-select" title="약물 선택" style="margin-bottom:1em;">
                                <option value=''>--- Drug ---</option>
                            </select>
                        </div>
                        <input type="submit" class="cl-btn" value="Submit" />
</form>
                    </div>

                    <div id="cl-simul-patient">
<form action='<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>?module=simulation&act=patient_graph_work.php' method='POST' target='_self' accept-charset='UTF-8' enctype='application/x-www-form-urlencoded' autocomplete='on' id="cl-simul-patient-form">				
                        Mutation
                        <textarea id="cl-simul-mutation" name="mutation" class="cl-textarea"></textarea>
                        <div>
                            <select id="cl-simul-attractor-target1" name="target1" class="cl-select" style="margin-bottom:1em; width:49%; float:left; margin-right:2%;">
                                <option value=''>--- Target 1 ---</option>
                            </select>
                            <select id="cl-simul-attractor-target2" name="target2" class="cl-select" style="width:49%;">
                                <option value=''>--- Target 2 ---</option>
                            </select>
                        </div>
                        <input type="submit" class="cl-btn" value="Submit" />
</form>
                    </div>


				</div>
				
				<div id="cl-simul-sfa">
<form action='<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>?module=simulation&act=sfa_graph_work.php' method='POST' target='_self' accept-charset='UTF-8' enctype='application/x-www-form-urlencoded' autocomplete='on' id="cl-simul-sfa-form">				

					Please select cell lines<br />
                    <div id="cl-simul-sfa-cellline">
					    <input id="cl-simul-sfa-cell1" name="cell" type="radio" value="SW48"><label for='cl-simul-sfa-cell1' style="display: inline;">SW48</label>
    					<input id="cl-simul-sfa-cell2" name="cell" type="radio" value="COLO205"><label for='cl-simul-sfa-cell2' style="display: inline;">COLO205</label>
                    </div>
					Please select input nodes and targets<br />
					<input id="cl-simul-sfa-node1" name="node1" type="checkbox" value="1"><label for='cl-simul-sfa-node1' style="display: inline;">S_Mutagen</label>
					<input id="cl-simul-sfa-node2" name="node2" type="checkbox" value="1"><label for='cl-simul-sfa-node2' style="display: inline;">S_GFs</label>
					<input id="cl-simul-sfa-node3" name="node3" type="checkbox" value="1"><label for='cl-simul-sfa-node3' style="display: inline;">S_Nutrients</label>
					<input id="cl-simul-sfa-node4" name="node4" type="checkbox" value="1"><label for='cl-simul-sfa-node4' style="display: inline;">S_TNFalpha</label>
					<input id="cl-simul-sfa-node5" name="node5" type="checkbox" value="1"><label for='cl-simul-sfa-node5' style="display: inline;">S_Hypoxia</label>
					<br /><br />
					<div>
						<div style="height:60px;">
						<select id="cl-simul-sfa-target1" name="target1" class="cl-select" style="margin-bottom:1em; width:50%; float:left;">
							<option value=''>--- Target 1 ---</option>						
						</select>
						
						<input id="cl-simul-sfa-target1-on2" name="target1_on" value="1" type="radio" style=""><label for='cl-simul-sfa-target1-on2' style="display: inline;">On</label><input id="cl-simul-sfa-target1-on3" name="target1_on" value="0" type="radio" style=""><label for='cl-simul-sfa-target1-on3' style="display: inline;">Off</label>
						</div>
						
						
						<div style="height:70px;">
						<select id="cl-simul-sfa-target2" name="target2" class="cl-select" style="width:50%;">
							<option value=''>--- Target 2 ---</option>
						</select><input id="cl-simul-sfa-target2-on2" name="target2_on" value="1" type="radio" style=""><label for='cl-simul-sfa-target2-on2' style="display: inline;">On</label><input id="cl-simul-sfa-target2-on3" name="target2_on" value="0" type="radio" style=""><label for='cl-simul-sfa-target2-on3' style="display: inline;">Off</label>
						</div>	
					</div>
					<input type="submit" class="cl-btn" value="Submit" />
</form>
				</div>
				
				<div id="cl-simul-attractor">
<form action='<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>?module=simulation&act=attractor_graph_work.php' method='POST' target='_self' accept-charset='UTF-8' enctype='application/x-www-form-urlencoded' autocomplete='on' id="cl-simul-attractor-form">				
					Please select input nodes and targets<br />
					<input id="cl-simul-attractor-node1" name="node1" type="checkbox" value="1"><label for='cl-simul-attractor-node1' style="display: inline;">S_Mutagen</label>
					<input id="cl-simul-attractor-node2" name="node2" type="checkbox" value="1"><label for='cl-simul-attractor-node2' style="display: inline;">S_GFs</label>
					<input id="cl-simul-attractor-node3" name="node3" type="checkbox" value="1"><label for='cl-simul-attractor-node3' style="display: inline;">S_Nutrients</label>
					<input id="cl-simul-attractor-node4" name="node4" type="checkbox" value="1"><label for='cl-simul-attractor-node4' style="display: inline;">S_TNFalpha</label>
					<input id="cl-simul-attractor-node5" name="node5" type="checkbox" value="1"><label for='cl-simul-attractor-node5' style="display: inline;">S_Hypoxia</label>
					<br />
                    Please select mutation (default : normal)<br />
                    <div id="cl-simul-attractor-mutation">
                        <input id="cl-simul-attractor-normal" name="mutation" type="radio" value="normal"><label for='cl-simul-attractor-normal' style="display: inline;">normal</label>
                        <input id="cl-simul-attractor-apc" name="mutation" type="radio" value="apc"><label for='cl-simul-attractor-apc' style="display: inline;">APC</label>
                    </div>
					<br />
					<div>
						<div style="height:60px;">
						<select id="cl-simul-attractor-target1" name="target1" class="cl-select" style="margin-bottom:1em; width:50%; float:left;">
							<option value=''>--- Target 1 ---</option>						
						</select>
						
						<input id="cl-simul-attractor-target1-on2" name="target1_on" value="1" type="radio" style=""><label for='cl-simul-attractor-target1-on2' style="display: inline;">On</label><input id="cl-simul-attractor-target1-on3" name="target1_on" value="" type="radio" style=""><label for='cl-simul-attractor-target1-on3' style="display: inline;">Off</label>
						</div>
						
						
						<div style="height:70px;">
						<select id="cl-simul-attractor-target2" name="target2" class="cl-select" style="width:50%;">
							<option value=''>--- Target 2 ---</option>
						</select><input id="cl-simul-attractor-target2-on2" name="target2_on" value="1" type="radio" style=""><label for='cl-simul-attractor-target2-on2' style="display: inline;">On</label><input id="cl-simul-attractor-target2-on3" name="target2_on" value="" type="radio" style=""><label for='cl-simul-attractor-target2-on3' style="display: inline;">Off</label>
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

            <div id='cl-simul-single-graph' class='cl-shadowbox-all'>
                <div id="single-inner" style="width: 100%; height: 700px"></div>
                <div id="single-inner-plot" style="width: 100%; height: 700px"></div>
                <div id="selected-ic50"></div>
            </div>

            <div id='cl-simul-sfa-graph' class='cl-shadowbox-all'>
                <div id="wrapper_sfa" style="width: 100%; height: 700px">
                    <div id="mynetwork_sfa" style="width: 100%; height: 700px"></div>
                    <div id="loadingBar_sfa">
                         <div class="outerBorder_sfa">
                             <div id="text_sfa">0%</div>
                             <div id="border_sfa">
                                <div id="bar_sfa"></div>
                            </div>
                         </div>
                    </div>
                </div>
                <div id="optimal_sfa"></div>
            </div>

			
			<div id='cl-simul-attractor-graph' class='cl-shadowbox-all'>
                <div id="wrapper" style="width: 100%; height: 700px">
                    <div id="mynetwork" style="width: 100%; height: 700px"></div>
                    <div id="loadingBar">
                         <div class="outerBorder">
                             <div id="text">0%</div>
                             <div id="border">
                                <div id="bar"></div>
                            </div>
                         </div>
                    </div>
                </div>
                <div id="atthist_control" style="width: 100%; height: 300px"></div>
                <div id="atthist_exp" style="width: 100%; height: 300px"></div>
                <div id="optimal_att"></div>
			</div>
		</div>
	</div>
</div>
