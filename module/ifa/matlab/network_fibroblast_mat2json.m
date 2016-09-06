%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% This code is a part of information-processing-network
% Je-Hoon Song email: song.jehoon@gmail.com

% in this module, matlab variable network_fibroblast is translated into json 
% format.

clear all

startup; 

load network_fibroblast

% in network_fibroblast, you can find following variables: 
% Name                     Size              Bytes  Class     Attributes

%  adj                    139x139            154568  double              
%  initial_condition      139x1                1112  double              
%  input_list             139x1               19088  cell                
%  inputnode_list           9x1                  72  double              
%  logic_list             139x1              135096  cell                
%  node_list              139x1               16968  cell                
%  outputnode_list          1x4                  32  double 

% input_list

num_input_list = length(input_list);
strt_input_list = struct();
for i = 1 : num_input_list
    data = input_list{i};
    strt_input_list = setfield(strt_input_list, ['i' num2str(i)], data);
end

% logic_list

num_logic_list = length(logic_list);
strt_logic_list = struct();
for i = 1 : num_logic_list
    data = logic_list{i};
    strt_logic_list = setfield(strt_logic_list, ['i' num2str(i)], data);
end

% node_list

num_node_list = length(node_list);
strt_node_list = struct();
for i = 1 : num_node_list
    data = node_list{i};
    strt_node_list = setfield(strt_node_list, ['i' num2str(i)], data);
end

outputdata = struct(); 

outputdata.input_list = strt_input_list;

outputdata.logic_list = strt_logic_list;

outputdata.node_list = strt_node_list;

outputdata.adj = adj;

outputdata.initial_condition = initial_condition;

outputdata.inputnode_list = inputnode_list;

outputdata.outputnode_list = outputnode_list;

outputfile = fullfile(result_dir, 'helikar2008.json'); 
savejson('', outputdata, 'ArrayIndent', 0, 'FloatFormat', '\t%.5g', ...
    'FileName', outputfile, 'SingletArray', 0);

fprintf('output: %s\n', outputfile)

