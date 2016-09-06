% matlab -r "fumia_simulation('input.json', 'output.json'); exit"
function fumia_simulator(inputfilename, outputfilename, sample_size, time_length)
    
    if nargin == 0 
        inputfilename = 'test_input.json'; 
        outputfilename = 'test_output.json'; 
        time_length = 10;  % 1000
        sample_size = 5;  % 100
    end
    
    try
        output = struct();
        attractor_state=fumia_simulation(inputfilename,0,sample_size,time_length);
        output.before = make_output(attractor_state);
        attractor_state=fumia_simulation(inputfilename,1,sample_size,time_length);
        output.after = make_output(attractor_state);   
        savejson('output', output, outputfilename)
    catch err         
        disp(err.identifier)
        disp(err.message)        
    end

end

% time_length = 1000
% sample_size = 100
function attractor_state = fumia_simulation(filename,drugOK,sample_size,time_length)

    load fumia

    % Input
    ijon = loadjson(filename);
    idrugs = ijon.input.drugs;
    icelltype = ijon.input.celltype;

    idrugs 
    icelltype

    % Master table
    drug_master = readtable('drugs.txt', 'Delimiter', '\t');
    cell_master = readtable('cells.txt', 'Delimiter', '\t');

    % Mapping input to master table
    % cell line
    cellinfor = table2cell(cell_master(:,icelltype));

    alt_GOF = cell_master.Node(strcmpi(cellinfor, 'GOF'));
    alt_LOF = cell_master.Node(strcmpi(cellinfor, 'LOF'));

    [~, alt_GOF_index, ~] = intersect(node_name_list, alt_GOF);
    [~, alt_LOF_index, ~] = intersect(node_name_list, alt_LOF);

    for ii=1:length(alt_GOF_index)
        node_logic_list{alt_GOF_index(ii)}='1';
    end

    for ii=1:length(alt_GOF_index)
        node_logic_list{alt_GOF_index(ii)}='0';
    end
    if(drugOK==1)
        [~, ia, ~] = intersect(drug_master.name, idrugs);
        drug_names = drug_master.name(ia);
        drug_targets = drug_master.target(ia);

        [~, drug_targets_index, ~] = intersect(node_name_list, drug_targets);

        for i=1:length(drug_targets_index)
            node_logic_list{drug_targets_index(i)}='1';
        end
    end

    l = time_length;               % time length
    % sample_size = 100;      % http://www.surveysystem.com/sscalc.htm -> Sample Size Calculator
    node_number = 91;       % 총 node의 개수(96) - input node의 개수(5)    
    no_cycle = 20;          % limit cycle attractor가 되기 위한 최소 주기 반복 회수

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    S_total_node=cell(1,l);

    environmental_condition=[0 1 1 0 1];

    x=zeros(1,96);
    x(92:end)=environmental_condition;
    attractor_state{1,1}=zeros(1,node_number);
    attractor_state{1,2}=0;

    state_no=1;

    for kn=1:1:sample_size
        initial_state_random_sample{kn}=round(rand(1,node_number));
            for kk=1:91
                x(kk)=initial_state_random_sample{kn}(kk);
            end
        S_total_node{1}=x(1:91);
        
        % t=1 이후의 state를 구함
        for t=1:1:(l-1)
            
            for k=1:91
                x_next(k)=boolean(eval(node_logic_list{k}));
            end
            S_total_node{t+1}=x(1:91);
            x(1:91)=x_next;
            
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            %%%%%%%%%%%%%%%%%%%%%% fixed attractor에 수렴하는지 여부 검사 %%%%%%%%%%%%%%%%%%%%%%%%%%%
            fixed_attractor_decision=0;
            %         fixed_attractor_decision=zeros(1,sample_size);
            if t>=49
                s1=S_total_node{t+1}; s2=S_total_node{t}; s3=S_total_node{t-1}; s4=S_total_node{t-2}; s5=S_total_node{t-3}; s6=S_total_node{t-4}; s7=S_total_node{t-5};
                s8=S_total_node{t-6}; s9=S_total_node{t-7}; s10=S_total_node{t-8}; s11=S_total_node{t-9}; s12=S_total_node{t-10}; s13=S_total_node{t-11}; s14=S_total_node{t-12};
                s15=S_total_node{t-13}; s16=S_total_node{t-14}; s17=S_total_node{t-15}; s18=S_total_node{t-16}; s19=S_total_node{t-17}; s20=S_total_node{t-18}; s21=S_total_node{t-19};
                s22=S_total_node{t-20}; s23=S_total_node{t-21}; s24=S_total_node{t-22}; s25=S_total_node{t-23}; s26=S_total_node{t-24}; s27=S_total_node{t-25}; s28=S_total_node{t-26};
                s29=S_total_node{t-27}; s30=S_total_node{t-28}; s31=S_total_node{t-29}; s32=S_total_node{t-30}; s33=S_total_node{t-31}; s34=S_total_node{t-32}; s35=S_total_node{t-33};
                s36=S_total_node{t-34}; s37=S_total_node{t-35}; s38=S_total_node{t-36}; s39=S_total_node{t-37}; s40=S_total_node{t-38}; s41=S_total_node{t-39}; s42=S_total_node{t-40};
                s43=S_total_node{t-41}; s44=S_total_node{t-42}; s45=S_total_node{t-43}; s46=S_total_node{t-44}; s47=S_total_node{t-45}; s48=S_total_node{t-46}; s49=S_total_node{t-47};
                s50=S_total_node{t-48};
                %                 s51=S_total_node{t-49}; s52=S_total_node{t-50}; s53=S_total_node{t-51}; s54=S_total_node{t-52}; s55=S_total_node{t-53}; s56=S_total_node{t-54};
                %                 s57=S_total_node{t-55}; s58=S_total_node{t-56}; s59=S_total_node{t-57}; s60=S_total_node{t-58}; s61=S_total_node{t-59}; s62=S_total_node{t-60}; s63=S_total_node{t-61};
                
                fixed_attractor_decision=isequal(s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20, s21, s22, s23, s24, s25, s26,...,
                    s27, s28, s29, s30, s31, s32, s33, s34, s35, s36, s37, s38, s39, s40, s41, s42, s43, s44, s45, s46, s47, s48, s49, s50);
                %                     s51, s52, s53, s54, s55, s56,...,
                %                     s57, s58, s59, s60, s61, s62, s63, s64, s65, s66, s67, s68, s69, s70, s71, s72, s73, s74, s75, s76, s77, s78, s79, s80, s81, s82, s83, s84, s85, s86,...,
                %                     s87, s88, s89, s90, s91, s92, s93, s94, s95, s96, s97, s98, s99, s100);
                %                 , s101, s102, s103, s104, s105, s106, s107, s108, s109, s110, s111, s112, s113,...,
                %                     s114, s115, s116, s117, s118, s119, s120, s121, s122, s123, s124, s125, s126, s127, s128, s129, s130, s131, s132, s133, s134, s135, s136, s137, s138,...,
                %                     s139, s140, s141, s142, s143, s144, s145, s146, s147, s148, s149, s150, s151, s152, s153, s154, s155, s156, s157, s158, s159, s160, s161, s162, s163,...,
                %                     s164, s165, s166, s167, s168, s169, s170, s171, s172, s173, s174, s175, s176, s177, s178, s179, s180, s181, s182, s183, s184, s185, s186, s187, s188,...,
                %                     s189, s190, s191, s192, s193, s194, s195, s196, s197, s198, s199, s200);
                %                 s201, s202, s203, s204, s205, s206, s207, s208, s209, s210, s211, s212, s213,...,
                %                 s214, s215, s216, s217, s218, s219, s220, s221, s222, s223, s224, s225, s226, s227, s228, s229, s230, s231, s232, s233, s234, s235, s236, s237, s238,...,
                %                 s239, s240, s241, s242, s243, s244, s245, s246, s247, s248, s249, s250, s251, s252, s253, s254, s255, s256, s257, s258, s259, s260, s261, s262, s263,...,
                %                 s264, s265, s266, s267, s268, s269, s270, s271, s272, s273, s274, s275, s276, s277, s278, s279, s280, s281, s282, s283, s284, s285, s286, s287, s288,...,
                %                 s289, s290, s291, s292, s293, s294, s295, s296, s297, s298, s299, s300);
                % state가 200번 동일하게 반복되면 attractor state에 수렴한 것으로 간주된다.
            end
            %%%%%%%%%%%%%%%%%%%%%%%%%% fixed attractor에 수렴하는지 여부 검사 완료 %%%%%%%%%%%%%%%%%%%%%%%%%%%%
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            
            
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            %%%%%%%%%%%%%%%%%%%%%% cyclic attractor에 수렴하는지 여부 검사 %%%%%%%%%%%%%%%%%%%%%%%%%%%
            cyclic_attractor_decision=0;
            %         cyclic_attractor_decision=zeros(1,sample_size);
            temp=0;
            for b=t:-1:1
                equal_test=isequal(S_total_node{t+1},S_total_node{b});
                if (equal_test==1)&&(t+1-b>1)&&(t+1-no_cycle*(t+1-b)>=0)
                    % cyclic_period=t+1-b;  % b=t+1-cyclic_period  % no_cycle=20 -> limit cycle attractor가 되기 위한 최소 주기 반복 회수
                    % cyclic_period가 1이면 fixed attractor가 된다.
                    temp=1;
                    break
                end
            end
            all_cycle_test=0;
            if (temp==1)
                cyclic_period=t+1-b;
                cyclic_test=zeros(1,(cyclic_period-1));
                for c=0:1:(cyclic_period-1)
                    s1=S_total_node{t+1-c};
                    s2=S_total_node{t+1-cyclic_period-c};
                    s3=S_total_node{t+1-2*cyclic_period-c};
                    s4=S_total_node{t+1-3*cyclic_period-c};
                    s5=S_total_node{t+1-4*cyclic_period-c};
                    s6=S_total_node{t+1-5*cyclic_period-c};
                    s7=S_total_node{t+1-6*cyclic_period-c};
                    s8=S_total_node{t+1-7*cyclic_period-c};
                    s9=S_total_node{t+1-8*cyclic_period-c};
                    s10=S_total_node{t+1-9*cyclic_period-c};
                    s11=S_total_node{t+1-10*cyclic_period-c};
                    s12=S_total_node{t+1-11*cyclic_period-c};
                    s13=S_total_node{t+1-12*cyclic_period-c};
                    s14=S_total_node{t+1-13*cyclic_period-c};
                    s15=S_total_node{t+1-14*cyclic_period-c};
                    s16=S_total_node{t+1-15*cyclic_period-c};
                    s17=S_total_node{t+1-16*cyclic_period-c};
                    s18=S_total_node{t+1-17*cyclic_period-c};
                    s19=S_total_node{t+1-18*cyclic_period-c};
                    s20=S_total_node{t+1-19*cyclic_period-c};
                    cyclic_test(c+1)=isequal(s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12,s13,s14,s15,s16,s17,s18,s19,s20);
                end
                all_cycle_test=all(cyclic_test); % 한주기의 state sequence가 20회 반복되는지 체크한다.
                
                %%%%%%%%% fixed point attractor인지 check: fixed point attractor이면 제외 %%%%%%%%%
                one_cycle_states=cell(1,cyclic_period);
                for c=0:1:(cyclic_period-1)
                    one_cycle_states{cyclic_period-c}=S_total_node{t+1-c};
                end
                one_cycle_test=zeros(1,(cyclic_period-1));
                for d=1:1:(cyclic_period-1)
                    one_cycle_test(d)=isequal(one_cycle_states{d},one_cycle_states{d+1});  % 한주기 안에서 똑같은 state들이 반복되는지 확인한다.
                end
                all_one_cycle_test=all(one_cycle_test);
                %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                cyclic_attractor_decision=(all_cycle_test==1)&&(all_one_cycle_test==0);
            end
            %%%%%%%%%%%%%%%%%%%%%%%%%% cyclic attractor에 수렴하는지 여부 검사 완료 %%%%%%%%%%%%%%%%%%%%%%%%%%%%
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            
            
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            %%%%%%%%%%%%%%%%%%%%%%%%%% Table of attractors & basin sizes of attractors 갱신 %%%%%%%%%%%%%%%%%
            %         current_attractor_state=zeros(1,node_number);
            if fixed_attractor_decision==1
                % point attractor만 detection한다. cyclic attractor를 detection할 수 있는 criteria는 여기에 없다.
                current_attractor_state=s1;
                %             test2{k}=s1;
                if state_no==1
                    attractor_state{1,1}=current_attractor_state;
                    attractor_state{1,2}=attractor_state{1,2}+1;
                    state_no=state_no+1;   % 아직 생성되지 않은 새로운 attractor state에 대한 number를 부여한다.
                elseif state_no>=2
                    %                     while decision==0
                    % while 문이 있다면, "for p=1:1:(state_no-1) ~ end" 구문이 끝난 후에 decision==0이 최종적으로 나올 경우, while 문을 벗어나지 못하고 무한 루프가 형성된다.
                    overlap_decision=0;
                    for p=1:1:(state_no-1)   % 검토 부분
                        overlap_decision=isequal(attractor_state{p,1}, current_attractor_state);
                        if overlap_decision==1
                            attractor_state{p,2}=attractor_state{p,2}+1;   % break 문과 같이 있지 않으면 break 문이 수행되지 않았을 때, overlap_state_no 변수가 존재하지 않게 된다.
                            break   % "for p=1:1:(state_no-1) ~ end" 구문이 break 된다.
                        end
                    end
                    %                     end
                    %                     overlap_state_no=p;
                    %                     attractor_state{overlap_state_no,2}=attractor_state{overlap_state_no,2}+1;   % break 문과 같이 있지 않으면 break 문이 수행되지 않았을 때, overlap_state_no 변수가 존재하지 않게 된다.
                    if overlap_decision==0
                        attractor_state{state_no,1}=current_attractor_state;
                        attractor_state{state_no,2}=1;
                        state_no=state_no+1;
                    end
                end
    %             attractor_convergence_time(k)=t-48;
                break   % attractor_state 라는 cell에 current_attractor_state 정보를 추가하여 update한 후에 for loop를 break한다.
            end
            if cyclic_attractor_decision==1
                current_attractor_state=one_cycle_states;
                if state_no==1
                    attractor_state{1,1}=current_attractor_state;
                    attractor_state{1,2}=attractor_state{1,2}+1;
                    state_no=state_no+1;   % 아직 생성되지 않은 새로운 attractor state에 대한 number를 부여한다.
                elseif state_no>=2
                    overlap_decision=0;
                    for p=1:1:(state_no-1)
                        overlap_decision=isequal(attractor_state{p,1}, current_attractor_state);
                        % overlap_decision==0일 경우, attractor_state{p,1}의 첫번째 상태와 같은 상태가 current_attractor_state에 존재하는지 검사하는 script 작성
                        % attractor_state{p,1}의 첫번째 상태와 같은 상태가 current_attractor_state에 존재한다면, 시작 state만 다를 뿐 동일한 cyclic attractor인지 검사해야 한다.
                        % 즉, overlap_decision==1이 될 수 있는 기회를 다시 한번 준다.
                        % overlap_decision==1이 될 수 있는 기회를 attractor table에 저장된 기존의 cyclic attractor의 period와 current_attractor_state에 저장된 cyclic attractor의 period가 같은 경우에만 준다.
                        if (overlap_decision==0)&&(length(attractor_state{p,1})==length(current_attractor_state))
                            only_first_overlap=0;
                            for cn=1:1:length(attractor_state{p,1})
                                only_first_overlap=isequal(attractor_state{p,1}{1}, current_attractor_state{cn});
                                if only_first_overlap==1
                                    break
                                end
                            end
                            if only_first_overlap==1
                                current_attractor_state=circshift(current_attractor_state, [0,-(cn-1)]);
                                overlap_decision=isequal(attractor_state{p,1}, current_attractor_state);
                            end
                        end
                        if overlap_decision==1
                            attractor_state{p,2}=attractor_state{p,2}+1;   % break 문과 같이 있지 않으면 break 문이 수행되지 않았을 때, overlap_state_no 변수가 존재하지 않게 된다.
                            break   % "for p=1:1:(state_no-1) ~ end" 구문이 break 된다.
                        end
                    end
                    % overlap_decision==1이 될 수 있는 기회를 다시 한번 줬음에도 불구하고 실패한 경우
                    if overlap_decision==0
                        attractor_state{state_no,1}=current_attractor_state;
                        attractor_state{state_no,2}=1;
                        state_no=state_no+1;
                    end
                end
    %             attractor_convergence_time(k)=t+2-20*cyclic_period;    % t+1-19*cyclic_period-(cyclic_period-1)
                break   % attractor_state 라는 cell에 current_attractor_state 정보를 추가하여 update한 후에 for loop를 break한다.
            end
            %%%%%%%%%%%%%%%%%%%%%%%%%% Table of attractors & basin sizes of attractors 갱신 완료 %%%%%%%%%%%%%%%%%
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            
        end
    end
end

function atts = make_output(attractor_state)
    atts = struct();
    for i = 1 : size(attractor_state,1)
        attractor_id = strcat('att', num2str(i));
        attractor = [];
        if(iscell(attractor_state{i,1}))
            att_type = 'cyclic';
            attractor_state_test=attractor_state{i,1}{1};
            for j=1:length(attractor_state{i,1})
                attractor = [attractor; attractor_state{i,1}{j}];
            end
        else
            att_type = 'point';
            attractor =attractor_state{i,1};
            attractor_state_test=attractor_state{i,1};
        end
        att_size = size(attractor,1);
        basin_of_attraction = attractor_state{i,2};
        if(attractor_state_test(71)==1)
            phenotype='Apoptosis';
        elseif(attractor_state_test(50)==1)  %49 50 47 48 = DEAB
            phenotype='Proliferation';
        else
            phenotype='Quiescent';
        end

        a = struct( ...
            'attractor', attractor, ...
            'att_type', att_type, ...
            'att_size', att_size, ...
            'phenotype', phenotype, ...
            'basin_of_attraction', basin_of_attraction);
        atts.(attractor_id) = a;
    end
end

