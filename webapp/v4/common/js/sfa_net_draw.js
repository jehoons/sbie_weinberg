var signal;
var network;
var cid;

function sfa_net_drawing(result, cancer_id) {


	
	//console.log("result: ", result);
//	fetch('./common/js/output_borisov_2009.json')
//	.then(readResponseAsJSON)
//	.then(createNetwork)
//	.then(cytoscape_drawing)
//	.catch(logError);

	//$.getJSON("./common/js/data/LUNG_sfv_output.json", function(data){
		
		
    cid = cancer_id;
    if (cancer_id == 1) coord_file = "./common/js/data/BREAST_node_coordinate.txt";
    else if (cancer_id == 2) coord_file = "./common/js/data/COAD_node_coordinate.txt";
    else if (cancer_id == 3) coord_file = "./common/js/data/LUNG_node_coordinate.txt";
	$.get(coord_file, function(coordi){
		var network = createNetwork(result, coordi);

		var cy = window.cy = cytoscape({
		container: document.getElementById('mynetwork_sfa'),
		elements: network,
		style: [{
			selector: 'node',
			style: {
			'label': 'data(label)',
			'text-halign': 'center',
			'text-valign': 'center',
			'width': 'label',
			'height': 'label',
			'padding':'10px',
//			shape: 'triangle',
			'border-style':'solid',
			'border-width':'1',
			'background-color':'data(color)',
//			'background-color': 'RosyBrown'
			'content':'data(id)'
			}
		}, {
			selector: 'edge',
			style: {
				'curve-style': 'bezier',
				//'width': 1,
				//'line-color': '#ccc',
				'target-arrow-shape': 'triangle',
				'target-arrow-color': 'data(color)',
//				'text-background-color': 'yellow',
//				'text-background-opacity': 0.4,
				'width': 'data(width)',
				'line-color':'data(color)',
				'control-point-step-size': '100px'
//				'control-point-weight':'0.2'
				}
			}, {
			selector: 'edge.inhibition',
			style: {
				'curve-style': 'bezier',
				'width': 'data(width)',
				'line-color': 'data(color)',
				'target-arrow-shape': 'tee',
				'arrow-scale':'1'

				}
			}],
		layout: {
//			name: 'dagre'
			name: 'preset'
			}

		});


	});
	//});


}



function logError(error){
	console.log("[JY LOG] Something wrong here ... \n", error);
}

function readResponseAsJSON(response){
	console.log("response: ", response);
	console.log("response.json()", response.json());
	return response.json();
}

function createNetwork(info, coordi){

	var positions = {};
	var nodes = {};
	var edges = {};

	var lines = coordi.split("\n");
	for (var i = 1 ; i < lines.length; i++){
		var token = lines[i].split("\t");
		
		positions[token[0]] = [parseFloat(token[1]), parseFloat(token[2])];
		
	}

	
	var index = 0;
	var node_color;
	var x_pos;
	var y_pos;
	$.each(info.nodes, function(){
//		node_color = this.FILL_COLOR;
//		node_color = node_color.substring(3,9);
		x_pos = positions[this.id][0];
		y_pos = positions[this.id][1];
		console.log("ID: ", this.id, ", x: ",x_pos,", y: ",y_pos);
		nodes[index] = {
			"data":{
				id: this.id,
				label: this.id,
//				color: "#"+node_color
				color: this.FILL_COLOR
			},
			position:{
//				x: this.POS_X,
//				y: this.POS_Y
				x: x_pos,
				y: y_pos
			}
		}
		index++;
	});

	var index = 0;
	var edge_color;
	$.each(info.links, function(){
		edge_color = this.FILL_COLOR;
		edge_color = edge_color.substring(3,9);
		edges[index] = {
			"data":{
//				id: this.ID,
				source: this.source,
				target: this.target,
				width: this.WIDTH,
				color: "#"+edge_color
			},
			classes: this.SIGN
		}
		index++;
	});

	var network = {};
	network.nodes = Object.values(nodes);
	network.edges = Object.values(edges);

	console.log("network: ", network);
	return network;
}

function cytoscape_drawing(network){
	var cy = cytoscape({
		container: document.getElementById('mynetwork_sfa'),
		elements: network,
		layout:{
//			name: 'dagre'
		},
		style: [
			{
				selector: 'node',
				style: {
					'label':'data(label)',
					shape: 'triangle',
					'background-color':'RosyBrown'
				}
			},
			{
				selector: 'edge',
				style: {
				}
			}
		]
	});

}

