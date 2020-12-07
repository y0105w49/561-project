# input is queries_in.txt, packet_info.txt
# output is queries.txt

# Input Format for queries_in.txt
# <query num> <keys> <attrs> <T_q>  (keys,attrs are comma-separated)
# For example:
# 1 dstIP srcIP 93
# 2 srcIP,dstIP dstPort 124

# Output Format:
# <query num> <keys> <attrs> <T_q> <-log(p)> <m> <n> (keys,attrs are comma-separated)
# For exmaple:
# 1 1 0 6 30 20
# 2 0,1 2 5 10 10


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


fin = open("queries_in.txt", "r")
queries_in = fin.read()
fin.close()

queries_in = queries_in.split("\n")
queries_in.pop()
# print(queries_in)
number_queries = len(queries_in)
gamma_q = 1/number_queries

fout = open("queries.txt","w+")

for i in range(number_queries):
	query = queries_in[i].split(" ")
	T_q = int(query[3])
	curr_best_config = find_best_config(T_q, gamma_q, p_limit=20)
	query = query+ curr_best_config
	query = " ".join(str(x) for x in query)
	fout.write(query+"\n")
	# print(query)
	# print(T_q)
	# list_T_q.append(int(queries_in[i][3]))

fout.close()
