import random
import time


def num2bin(num, dim):
    # """
    # num: number to be converted
    # dim: dimension of array
    # This function takes the avg., 0.00260 sec.
    # """
    fstr = '{0:0%db}' % dim
    str_bin = fstr.format(num)
    return [int(elem) for elem in str_bin]


# def num2bin_str(num, dim):
# 	"""
# 	num: number to be converted
# 	dim: dimension of array
# 	This function takes the avg., 0.0237 sec.
# 	"""
# 	arr = np.zeros((dim,), dtype=np.float)
# 	quo = num
# 	for i in range(dim):
# 		quo, rem = divmod(quo, 2)
# 		arr[-(i+1)] = rem
# 		if quo == 0:
# 			break
#
# 	return arr
#
# def time_num2bin(num_samp, dim, func):
#     start =  time.time()
#     for i in range(num_samp):
#         res = func(random.randint(0, 2**dim-1), dim)
#     end = time.time()
#     return (end - start)/num_samp
#
# if __name__ == "__main__":
#     # Check functionality
#     res = num2bin(7, 5)
#     print(res)
#     assert( (res == np.array([0, 0, 1, 1, 1])).all() )
#
#     # Test performance
#     num_samp = 10**3
#     dim = 10000
#     print ("num2bin: ", time_num2bin(num_samp, dim, num2bin))
#     print ("num2bin_str: ", time_num2bin(num_samp, dim, num2bin_str))


def rand_bin_sampling(n_node, n_rep):
    """
    :param n_node: number of node
    :param n_rep: number of repetition / sampling
    :return: random binary initial input(len : n_node) * n_rep
    """
    initial_state_num = {}
    initial_state_bin = []
    while True:
        if len(initial_state_bin) == n_rep:
            break
        else:
            num = random.randint(0, 2**n_node-1)  # 0 <= random_int <= 2**n_node-1
            if num not in initial_state_num:
                initial_state_num[num] = 0
                initial_state_bin.append(num2bin(num, n_node))
            else:
                continue
    return initial_state_bin


# def rand_bin_sampling2(n_node, n_rep):
# # n_node shouldn't bigger than 64. if not, it does'not work.
#     rand_num_list = [0]* n_node
#     rand_bin_list = [0]*n_rep
#     rand_num_list = random.sample(range(int(2**n_node-1)), n_rep)
#     for i in range(n_rep):
#         rand_bin_list[i] = num2bin(rand_num_list[i], n_node)
#     return rand_bin_list

# def time_random(n_node, n_rep, func):
#     start =  time.time()
#     res = func(n_node, n_rep)
#     end = time.time()
#     return (end - start)/n_rep
#
# if __name__ == "__main__":
#     # Check functionality
#     list_rand = rand_bin_sampling(50, 100)
#     print(list_rand)
#     a = rand_bin_sampling(50, 100)
#     print(a)
#     # Test performance
#     n_node = 60
#     n_rep = 1000
#     print("v1 : ", time_random(n_node, n_rep, rand_bin_sampling))
#     print("v2 : ", time_random(n_node, n_rep, rand_bin_sampling2))
#   """
#   the time test result
#   v1 :  2.300119400024414e-05
#   v2 :  3.1001806259155275e-05
#   """




