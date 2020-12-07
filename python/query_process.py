# input is queries_in.txt, packet_info.txt
# output is queries.txt

# Input Format for queries_in.txt
# <query num> <keys> <attrs> <T_q>  (keys,attrs are comma-separated)
# For example:
# 1 dstIP srcIP 93
# 2 srcIP,dstIP dstPort 124

# Output Format:
# <query num> <keys> <attrs> <T_q> <-log(p)> <m> <n> (keys,attrs are comma-separated)
# changes keys and attributes to integers representing subsets, according to packet_info.txt
# For exmaple:
# 1 2 1 93 10 11 1
# 2 3 8 124 7 14 9

import random
# variables
MAX_MEMORY = 32 			# w = 32-bit
ERROR_TOLERANCE = 0.05

def expected_CC(m,inv_p,n):
	ret = 0
	for j in range(n):
		ret += inv_p/(m-j)
	return ret

def relative_error(T, T_q):
	# print(abs(T - T_q)/T_q)
	return abs(T - T_q)/T_q


def find_best_config(T_q, gamma_q, p_limit=20):
	best_config = []
	smallest_error = float('inf')
	for i in range(p_limit):
		inv_p_q = 2**i
		upperbound_m = int(min(MAX_MEMORY, gamma_q*inv_p_q))
		if upperbound_m < 1:
			continue
		for m_q in range(1,upperbound_m+1):
			for n_q in range(1,m_q+1):
				curr_expected_CC = expected_CC(m_q, inv_p_q, n_q)
				curr_error = relative_error(curr_expected_CC, T_q)
				if curr_error < smallest_error:
					best_config = [i, m_q, n_q]
					smallest_error = curr_error

	if smallest_error > ERROR_TOLERANCE:
		print("Relative error greater than 0.05")
	
	return best_config

# actually run experiment and minimize average error
# def find_best_config_new(T_q, gamma_q, p_limit=20):
# 	best_config = []
# 	smallest_error = float('inf')
# 	for i in range(p_limit):
# 		inv_p_q = 2**i
# 		upperbound_m = int(min(MAX_MEMORY, gamma_q*inv_p_q))
# 		if upperbound_m < 1:
# 			continue
# 		for m_q in range(1,upperbound_m+1):
# 			for n_q in range(1,m_q+1):
# 				curr_expected_CC = expected_CC(m_q, inv_p_q, n_q)
# 				curr_error = relative_error(curr_expected_CC, T_q)
# 				if curr_error < smallest_error:
# 					best_config = [i, m_q, n_q]
# 					smallest_error = curr_error

# 	if smallest_error > ERROR_TOLERANCE:
# 		print("Relative error greater than 0.05")
	
# 	return best_config

fin = open("packet_info.txt", "r")
packet_info = fin.read()
fin.close()
packet_info = packet_info.split("\n")
if packet_info[len(packet_info)-1] == '':
	packet_info.pop()
# print(packet_info)
num_pack = len(packet_info)
pack_dict = {}
for i in range(num_pack):
	pack_dict[packet_info[i]] = i

def subset_to_int(sub):
	sub = sub.split(',')
	sublist = [0]*num_pack
	for i in range(len(sub)):
		sublist[pack_dict[sub[i]]] = 1
	sublist = "".join(str(x) for x in sublist)
	ret = int(sublist[::-1],2)
	# print(sub)
	# print(sublist)
	# print(ret)
	return ret
	

fin = open("queries_in.txt", "r")
queries_in = fin.read()
fin.close()
queries_in = queries_in.split("\n")
if queries_in[len(queries_in)-1] == '':
	queries_in.pop()
# print(queries_in)
number_queries = len(queries_in)
gamma_q = 1/number_queries

fout = open("queries.txt","w+")

for i in range(number_queries):
	query = queries_in[i].split(" ")
	T_q = int(query[3])
	curr_best_config = find_best_config(T_q, gamma_q, p_limit=20)
	query[1] = subset_to_int(query[1])
	query[2] = subset_to_int(query[2])
	query = query+ curr_best_config
	query = " ".join(str(x) for x in query)
	fout.write(query+"\n")
	# print(query)
	
fout.close()
