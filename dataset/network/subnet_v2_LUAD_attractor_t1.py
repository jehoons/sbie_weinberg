# edge & node list 만들기
import scipy as sp
import num2bin

edge = open('subnet_v2_edge.txt', 'r')
node = open('subnet_v2_node.txt', 'r')

n_node = 166
n_edge = 293
n_rep = 100000

node_list = [0] * n_node
edge_list = [0] * n_edge
i = 0
for line in node:
    node_list[i] = ''.join(line.strip().split())
    i += 1
j = 0
for line in edge:
    edge_list[j] = ''.join(line.strip()).split()
    j += 1


# STATE 메트릭스 만들기 x축의 node 들은 영향을 받고 y축 node 들은 영향을 줌 (x*STATE(=1*166)의 각 열은 x축에 해당하는 node 에 들어온 모든 input 의 합)
STATE_array = sp.array([[0] * n_node] * n_node)

for i in range((len(edge_list))):
    name1_index = node_list.index(edge_list[i][0])
    name2_index = node_list.index(edge_list[i][2])
    if edge_list[i][1] == '((activate))':
        STATE_array[name1_index][name2_index] = 1
    else:  # elif edge_list[i][1]=='((inhibit))':
        STATE_array[name1_index][name2_index] = -1


# initial state 정의 (중복 없음)
initial_state = num2bin.rand_bin_sampling(n_node, n_rep)

# initial state 에서 특정 node 의 값을 고정
f = open('lung_t1vst4.txt', 'r')
fixed_node_list = []
dic_fixed_node = {}
up_fixed_index = []
down_fixed_index = []
i = 0
for line in f:
    fixed_node_list.append(line.strip().split('\t')[0])
    dic_fixed_node[line.strip().split('\t')[0]] = line.strip().split('\t')[1]
    i += 1
for i in fixed_node_list:
    fixed_node_index = node_list.index(i)
   # print(fixed_node_index)
    if dic_fixed_node[i] == 'up':
        #print('up')
        up_fixed_index.append(fixed_node_index)
        for j in range(len(initial_state)):
            initial_state[j][fixed_node_index] = 0
    else:
        #print('down')
        down_fixed_index.append(fixed_node_index)
        for j in range(len(initial_state)):
            initial_state[j][fixed_node_index] = 1

# attractor 및 trajectory 만들기
dic_attractor = {}
dic_attractor_reverse = {}
counter2 = 0
for i in range(n_rep):
    x = initial_state[i]
    x_array = sp.array(x)
    dic_trajectory = dict()
    dic_trajectory[str(x)] = 0
    counter = 0
    while 1:
        x_sum = x_array.dot(STATE_array)
        # 특정 node 의 값을 고정
        for t in up_fixed_index:
            x_sum[t] = -1
        for h in down_fixed_index:
            x_sum[h] = 1

        x_next = [0] * n_node
        for i in range(len(x_sum)):
            if x_sum[i] > 0:
                x_next[i] = 1
            elif x_sum[i] == 0:
                x_next[i] = x[i]
            else:
                x_next[i] = 0
        x_next_string = str(x_next)
        if x_next_string in dic_trajectory:
            dic_attractor_reverse[counter2] = x_next
            counter2 += 1
            if x_next_string in dic_attractor:
                dic_attractor[x_next_string] += 1
            else:
                dic_attractor[x_next_string] = 1

            break
        else:
            counter += 1
            dic_trajectory[x_next_string] = counter
            x_array = sp.array(x_next)
print('attractor # : ',len(dic_attractor.keys()))
# 원하는 phenotype attractor 만 합계내서 저장
f = open('phenotype.txt', 'r')
dic_phenotype = dict()
for line in f:
    a = line.strip().split(' ')
    dic_phenotype[a[0]] = int(a[1])
phenotype_index = (sorted(dic_phenotype.values()))
print(dic_phenotype)
print(phenotype_index)
dic_attractor_phenotype = dict()
list_attractor = []
for i in dic_attractor_reverse.values():
    list_attractor.append(i)


for i in range(len(list_attractor)):
    phenotype_attractor = [0] * len(phenotype_index)
    for j in range(len(phenotype_index)):
        phenotype_attractor[j] = list_attractor[i][phenotype_index[j]]
    if str(phenotype_attractor) in dic_attractor_phenotype:
        dic_attractor_phenotype[str(phenotype_attractor)] += 1
    else:
        dic_attractor_phenotype[str(phenotype_attractor)] = 1


print(dic_attractor_phenotype)

f = open('subnet_v2_attractor_t1_size_%d(5).txt' % n_rep, 'w')
for i in dic_attractor_phenotype.keys():
    data = '%s\t%s\n' % (i, dic_attractor_phenotype[i])
    print(data)
    f.write(data)
f.close()
