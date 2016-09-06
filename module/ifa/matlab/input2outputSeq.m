function ouput_sequence = input2outputSeq( ...
    inputnode_list, ...
    ouputnode_list, ...
    input_list, ...
    logic_list, ...
    start_state, ...
    input_sequence)

    next_state = start_state';
    
    for i = 1 : 100
        now_state = next_state;
        tt = 0;
        for j = inputnode_list'
            tt = tt + 1;
            next_state(j) = input_sequence(mod(i - 1, 100) + 1, tt);
        end
        for j = setdiff(1:139, inputnode_list)
            next_state(j)=logic_list{j}(bin2dec(num2str(now_state(input_list{j}))) + 1);            
        end
    end
    
    ouput_sequence = zeros(100, 139);

    for i = 1 : 120
        now_state = next_state;
        tt = 0;
        for j = inputnode_list'
            tt = tt + 1;
            next_state(j) = input_sequence(mod(i - 1, 100) + 1, tt);
        end
        for j = setdiff(1 : 139, inputnode_list)
            next_state(j) = logic_list{j}(bin2dec(num2str(now_state(input_list{j}))) + 1);
        end
        ouput_sequence(i, :) = next_state;
    end

end

