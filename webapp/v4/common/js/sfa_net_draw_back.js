var signal;
var network;

function sfa_net_drawing(result) {


	
	//console.log("result: ", result);
//	fetch('./common/js/output_borisov_2009.json')
//	.then(readResponseAsJSON)
//	.then(createNetwork)
//	.then(cytoscape_drawing)
//	.catch(logError);

		
		var network = createNetwork(result);

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
			'background-color':'data(color)'
//			'background-color': 'RosyBrown'
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
				'line-color':'data(color)'
//				'control-point-step-size': '140px'
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
			name: 'dagre'
			}

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
	var node_color;
	$.each(info.NODES, function(){
		node_color = this.FILL_COLOR;
		node_color = node_color.substring(3,9);
		nodes[index] = {
			"data":{
				id: this.ID,
				label: this.NAME,
				color: "#"+node_color
			}
		}
		index++;
	});

	var index = 0;
	var edge_color;
	$.each(info.LINKS, function(){
		edge_color = this.FILL_COLOR;
		edge_color = edge_color.substring(3,9);
		edges[index] = {
			"data":{
				id: this.ID,
				source: this.ID_SOURCE,
				target: this.ID_TARGET,
				width: this.WIDTH,
				color: "#"+edge_color
			},
			classes: this.HEADER.TYPE
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

