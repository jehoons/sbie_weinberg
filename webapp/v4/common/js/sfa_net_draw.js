var signal;
var network;

function sfa_net_drawing(result) {


	
	//console.log("result: ", result);
//	fetch('./common/js/output_borisov_2009.json')
//	.then(readResponseAsJSON)
//	.then(createNetwork)
//	.then(cytoscape_drawing)
//	.catch(logError);

	$.getJSON("./common/js/output_borisov_2009.json", function(data){
		
		var network = createNetwork(data);

		var cy = window.cy = cytoscape({
		container: document.getElementById('mynetwork_sfa'),
		elements: network,
		style: [{
			selector: 'node',
			style: {
			'label': 'data(label)',
			'width': '60px',
			'height': '60px',
			shape: 'triangle',
			'background-color': 'RosyBrown'
			}
		}, {
			selector: 'edge',
			style: {
				'curve-style': 'bezier',
				//'width': 1,
				//'line-color': '#ccc',
				'target-arrow-shape': 'triangle',
				'text-background-color': 'yellow',
				'text-background-opacity': 0.4,
				'width': '6px',
				'control-point-step-size': '140px'
				}
			}, {
			selector: 'edge.inhibition',
			style: {
				'curve-style': 'bezier',
				'width': '6px',
	//			'line-color': '#ccc',
				'target-arrow-shape': 'tee'
				}
			}],
		layout: {
			name: 'dagre'
			}

		});

	});


}

function logError(error){
	console.log("[JY LOG] Something wrong here ... \n", error);
}

function readResponseAsJSON(response){
	console.log("response: ", response);
	console.log("response.json()", response.json());
	return response.json();
}

function createNetwork(info){
	var nodes = {};
	var edges = {};
	
	var index = 0;
	$.each(info.NODES, function(){
		nodes[index] = {
			"data":{
				id: this.ID,
				label: this.NAME
			}
		}
		index++;
	});

	var index = 0;
	$.each(info.LINKS, function(){
		edges[index] = {
			"data":{
				id: this.ID,
				source: this.ID_SOURCE,
				target: this.ID_TARGET
			}
		}
		index++;
	});

	var network = {};
	network.nodes = Object.values(nodes);
	network.edges = Object.values(edges);

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

