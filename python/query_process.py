# input is queries_in.txt, packet_info.txt
# output is queries.txt

# Input Format for queries_in.txt
# <query num> <keys> <attrs> <T_q>  (keys,attrs are comma-separated)
# For example:
# 1 dstIP srcIP 93
# 2 srcIP,dstIP dstPort 124

# Output Format:
# pnum and pden are the numerator and denominator of p
# <query num> <keys> <attrs> <T_q> <pnum> <-log(pden)> <m> <n> (keys,attrs are comma-separated)
# changes keys and attributes to integers representing subsets, according to packet_info.txt
# For exmaple:
# 1 2 1 93 10 11 1
# 2 3 8 124 7 14 9

import random
import math
# variables
MAX_MEMORY = 32 			# w = 32-bit
ERROR_TOLERANCE = 0.05
P_LIMIT = 30
NUM_TRIALS = 50			# for find_best_config_new

# order = 1 gives expectation, order = 2 gives squared variance
def moment_CC(m, inv_p, order):
	ret = [0]*m
	for j in range(m):
		val = inv_p/(m-j)
		if order == 2:
			val = val*val - val
		if j == 0:
			ret[j] = val
		else:
			ret[j] = ret[j-1] + val
	return ret

def relative_error(T, T_q):
	# print(abs(T - T_q)/T_q)
	return abs(T - T_q)/T_q

def CC_experiment(m, inv_p, T):
	MAX_TRY = 3*T				# 3 is arbitrary

	list_T = [MAX_TRY]*m
	collected = [0]*m
	num_collected = 0
	for it in range(1,MAX_TRY+1):				
		val = random.uniform(0,1)
		coupon = math.floor(val*inv_p)
		if coupon<m and collected[coupon] == 0:
			collected[coupon] = 1
			list_T[num_collected] = it
			num_collected += 1
			if num_collected == m:
				break
	return list_T


def CC_exp_rel_err(m, inv_p, T):
	list_error = [0]*m
	for trial in range(NUM_TRIALS):
		curr_list_T = CC_experiment(m, inv_p, T)
		# print(curr_list_T)
		for i in range(m):
			list_error[i] = list_error[i] + relative_error(curr_list_T[i], T)
	for i in range(m):
		list_error[i] = list_error[i]/NUM_TRIALS
	return list_error

def compute_error(m_q, inv_p_q, T_q, b):
	list_error = [0]*m_q
	list_exp = moment_CC(m_q, inv_p_q, 1)
	if b==0:
		list_error = CC_exp_rel_err(m_q, inv_p_q, T_q)
		bestind = 0
		for i in range(m_q):
			if relative_error(list_exp[i], T_q) > ERROR_TOLERANCE:		# relative error of the expectation here
				list_error[i] = math.inf
			if i!=0:
				if list_error[i] < list_error[bestind]:
					list_error[bestind] = math.inf
					bestind = i
				else:
					list_error[i] = math.inf	

	elif b==1:
		list_sqvar = moment_CC(m_q, inv_p_q, 2)
		for i in range(m_q):
			list_error[i] = (list_exp[i]-T_q)*(list_exp[i]-T_q)  + list_sqvar[i]

	return list_error

# This is forn iterating over powers of 2 for p
# b=0: minimizes the |T-T_q|/T_q for all possible things within 5% expectation range 
# actually run experiment and minimize average error
# b=1: minimizes the E[(T-T_q)^2] = Var[T]+(E[T]-T_q)^2
# ppow = 0 considers only p as powers of 2
def find_best_config(T_q, gamma_q, b, ppow):
	best_config = []
	smallest_error = float('inf')
	if ppow == 0:
		for i in range(P_LIMIT):
			inv_p_q = 2**i
			upperbound_m = int(min(MAX_MEMORY, gamma_q*inv_p_q))
			if upperbound_m < 1:
				continue
			for m_q in range(1,upperbound_m+1):
				list_curr_error = compute_error(m_q, inv_p_q, T_q, b) 	# value for each n_q in {1,...,m_q} 
				for n_q in range(1,m_q+1):
					curr_error = list_curr_error[n_q-1]
					if curr_error < smallest_error:
						best_config = [1, i, m_q, n_q]		# pnum = 1 in this case
						smallest_error = curr_error
	else:
		return []

	prob = best_config[0]/(2**best_config[1])
	inv_prob = 1/prob
	m_q = best_config[2]
	n_q = best_config[3]
	ind = n_q-1

	# Bias
	list_exp = moment_CC(m_q, inv_prob, 1)
	bias  = relative_error(list_exp[ind], T_q)
	# Relative error
	list_rel_error = CC_exp_rel_err(m_q, inv_prob, T_q)
	rel_error = list_rel_error[ind]
	# Square relative error
	list_sqvar = moment_CC(m_q, inv_p_q, 2)
	sq_rel_error = (list_exp[ind]-T_q)*(list_exp[ind]-T_q)  + list_sqvar[ind]
	l2_rel_error = (math.sqrt(sq_rel_error))/T_q
	return (best_config, bias, rel_error, l2_rel_error)
	# return (best_config,0,0,0)


# Simulations for a single query :

for T_q in range(100,123):
	print("T_q = "+str(T_q))
	curr_best_config, bias, rel_error, l2_rel_error = find_best_config(T_q, 1, 0, 0)
	# print(curr_best_config)
	val = curr_best_config[3]/curr_best_config[2]
	print("Paper Metric:")
	print("n/m = "+str(val))
	print("bias = "+str(bias))
	print("relative error = "+str(rel_error))
	print("l2 relative error = "+str(l2_rel_error))
	print("-------------------------------------------------")

	curr_best_config, bias, rel_error, l2_rel_error = find_best_config(T_q, 1, 1, 0)
	# print(curr_best_config)
	val = curr_best_config[3]/curr_best_config[2]
	print("Our Metric:")
	print("n/m = "+str(val))
	print("bias = "+str(bias))
	print("relative error = "+str(rel_error))
	print("l2 relative error = "+str(l2_rel_error))
	print("-------------------------------------------------")
	print("-------------------------------------------------")

exit()


# Running on queries_in.txt and packet_info.txt :

def run_on_files():
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
		curr_best_config, bias, rel_error, l2_rel_error = find_best_config(T_q, gamma_q, 1, 0)
		query[1] = subset_to_int(query[1])
		query[2] = subset_to_int(query[2])
		query = query + curr_best_config
		query = " ".join(str(x) for x in query)
		fout.write(query+"\n")
		# print(query)
	fout.close()

run_on_files()

