var att;
var att_con;
var network;
function att_net_drawing(result) {
    // load the JSON file containing the Gephi network.
    //var gephiJSON = loadJSON("./fumia.json"); // code in importing_from_gephi.
    var gephiJSON = netfile; // code in importing_from_gephi.

    // you can customize the result like with these options. These are explaine d below.
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
            background: '#3333FF',
            border: '#3333FF'
        }
        data.nodes.update(temp);
    }

    if (result['target1']!='') {
        S = result['target1'].slice(2);
        var selNode = data.nodes.get(String(S));
        selNode.color = {
            background: '#CC3333',
            border: '#CC3333'
        }
        data.nodes.update(selNode);
    }
    if (result['target2']!='') {
        S = result['target2'].slice(2);
        var selNode = data.nodes.get(String(S));
        selNode.color = {
            background: '#CC3333',
            border: '#CC3333'
        }
        data.nodes.update(selNode);
    }
    //data.nodes[0]['color']['background'] = '#00ff00';
    //data.nodes[0]['color']['border'] = '#00ff00';


    // Edge color
    //var selEdge = data.edges.get('134');
    //selEdge.color = '#ff0000';
    //data.edges.update(selEdge);
    //data.edges[0]['color'] = '#ff0000';
    edgeIds = data.edges.getIds()
    for (var i = 0; i < edgeIds.length; i++) {
        var temp = data.edges.get(edgeIds[i]);
        temp.arrows = 'to';
        data.edges.update(temp);
    }
    // Edge scaling
    temp = data.edges.get(0);
    //temp.from == 'node1' & temp.to == 'node2';
    temp.value = 0.3;
    //data.edges.update(temp);

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
    var container = document.getElementById('mynetwork');
    var network = new vis.Network(container, data, options);

    // network load progress bar
    network.on("stabilizationProgress", function(params) {
        var maxWidth = 496;
        var minWidth = 20;
        var widthFactor = params.iterations/params.total;
        var width = Math.max(minWidth,maxWidth * widthFactor);
        document.getElementById('bar').style.width = width + 'px';
        document.getElementById('text').innerHTML = Math.round(widthFactor*100) + '%';
    });
    network.once("stabilizationIterationsDone", function() {
        document.getElementById('text').innerHTML = '100%';
        document.getElementById('bar').style.width = '496px';
        document.getElementById('loadingBar').style.opacity = 0;
        // really clean the dom element
        setTimeout(function () {document.getElementById('loadingBar').style.display = 'none';}, 500);
    });

    var selnodes = [];
    // event catch
    network.on("click", function (params) {
        //console.log(JSON.stringify(params));
        console.log(params['nodes']);
        selnodes = params['nodes'];
        //console.log(params['edges']);
    });
    this.att = result['att_exp'];
    this.att_con = result['att_control'];
    this.network = data;
}
