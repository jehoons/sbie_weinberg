var signal;
var network;
function sfa_net_drawing(result) {
    // load the JSON file containing the Gephi network.
    //var gephiJSON = loadJSON("./fumia.json"); // code in importing_from_gephi.
    var gephiJSON = netfile_sfa; // code in importing_from_gephi.

    // you can customize the result like with these options. These are explained below.
    // These are the default options.
    var parserOptions = {
        edges: {
            inheritColors: false
        },
        nodes: {
            fixed: true,
            parseColor: false
        }
    }

    // parse the gephi file to receive an object
    // containing nodes and edges in vis format.
    var parsed = vis.network.convertGephi(gephiJSON, parserOptions);

    // provide data in the normal fashion
    var data = {
        nodes: new vis.DataSet(parsed.nodes),
        edges: new vis.DataSet(parsed.edges)
    };

    // Node color
    nodeIds = data.nodes.getIds()
    for (var i = 0; i < nodeIds.length; i++) {
        var temp = data.nodes.get(nodeIds[i]);
        temp.color = {
            background: '#0011FF',
            border: '#0011FF'
        }
        data.nodes.update(temp);
    }

    if (result['drug1_target']!='') {
        S = result['drug1_target'];
        var selNode = data.nodes.get(String(S));
        selNode.color = {
            background: '#CC3333',
            border: '#CC3333'
        }
        data.nodes.update(selNode);
    }
    if (result['drug2_target']!='') {
        S = result['drug2_target'];
        var selNode = data.nodes.get(String(S));
        selNode.color = {
            background: '#CC3333',
            border: '#CC3333'
        }
        data.nodes.update(selNode);
    }
    //data.nodes[0]['color']['background'] = '#00ff00';
    //data.nodes[0]['color']['border'] = '#00ff00';

    //data.edges.update(selEdge);
    //data.edges[0]['color'] = '#ff0000';
    edgeIds = data.edges.getIds()
    for (var i = 0; i < edgeIds.length; i++) {
        var temp = data.edges.get(edgeIds[i]);
        temp.arrows = 'to';
        temp.width = 3;
        //temp.value = 1;
        if (temp.attributes.attribute == "-") {
            temp.color = '#0066FF';
        }
        data.edges.update(temp);
    }
    // Edge scaling
    signal_flow = result['signal'];
    signal_len = signal_flow.length;
    for (var i = 0; i < signal_len; i++) {
        for (var j = 0; j < edgeIds.length; j++) {
            var temp = data.edges.get(edgeIds[j]);
            if (temp.from == signal_flow[i][0] & temp.to == signal_flow[i][1]) {
                //temp.value = 2 * ((10**signal_flow[i][2])**5);
                temp.width = 3 * ((10**Math.abs(signal_flow[i][2]))**3);
                if (signal_flow[i][2] < 0) {
                    temp.color = '#0066FF';
                }
                data.edges.update(temp);
                break;
            }
        }
    }

    // create a network
    var options = {
        nodes: {
            font: {
                color: '#ffffff'
            },
            borderWidthSelected: 4
        },
        edges: {
            color: '#000000'
        },
        interaction: {
            // longheld click or control-click
            multiselect: true,
            hover: true
        }
    };
    var container = document.getElementById('mynetwork_sfa');
    var network = new vis.Network(container, data, options);

    // network load progress bar
    network.on("stabilizationProgress", function(params) {
        var maxWidth = 496;
        var minWidth = 20;
        var widthFactor = params.iterations/params.total;
        var width = Math.max(minWidth,maxWidth * widthFactor);
        document.getElementById('bar_sfa').style.width = width + 'px';
        document.getElementById('text_sfa').innerHTML = Math.round(widthFactor*100) + '%';
    });
    network.once("stabilizationIterationsDone", function() {
        document.getElementById('text_sfa').innerHTML = '100%';
        document.getElementById('bar_sfa').style.width = '496px';
        document.getElementById('loadingBar_sfa').style.opacity = 0;
        // really clean the dom element
        setTimeout(function () {document.getElementById('loadingBar_sfa').style.display = 'none';}, 500);
    });
    var selnodes = [];
    // event catch
    network.on("click", function (params) {
        //console.log(JSON.stringify(params));
        console.log(params['nodes']);
        selnodes = params['nodes'];
        //console.log(params['edges']);
    });
    this.signal = result['signal'];
    this.network = data;
}
