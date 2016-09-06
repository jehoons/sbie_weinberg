% 한 입력만 랜덤 하고 모든 노드 비교
% 나머지 입력에는 1010 이 반복됨

tic;
clc; clear;
load network_fibroblast

D=distance_bin(adj');
n_node=length(node_list);
for k=1:9
            input_sequence(:,k)=round(rand(1,100));
end
    for i=1:1
%         input_vector_list=50*ones(1,9);
%         input_sequence=zeros(100,9);
%         for j=1:9
%             temp1=zeros(1,100/input_vector_list(i,j));
%             temp1(1)=1;
%             input_sequence(:,j)=repmat(temp1,[1 input_vector_list(i,j)])';
%         end
  

        
        %     initial_condition(inputnode_list)=input_sequence(1,:);
        initial_condition(:)=0;
        output_sequence_list = input2outputSeq(inputnode_list,outputnode_list,input_list,logic_list,initial_condition,input_sequence);
    end
for k=1:9    
    for i=1:n_node
        d=D(inputnode_list(k),i);
        if(~isinf(d))
            mi_list(i,k)=mutInfo(output_sequence_list(end-100+1:end,i),output_sequence_list(end-100+1-d:end-d,inputnode_list(k)));
        end
        mi_list(inputnode_list(k),k)=0;
    end
    
end
toc

a=log10(mi_list);
% a(isinf(a))=-5;
a(a<-5)=-5;

% tic
% for i=1:n_node
%     i
%     data=[output_sequence_list(1:99,input_list{i}) output_sequence_list(2:100,i)];
%     mi_inOut_list(i)=mi_inOut(data);
% end
% toc