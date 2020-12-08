from query_process import *

list_gammas = [2**(-i) for i in range(10)]
T_q = 1000

# plot for HLL
list_rel_error_HLL = []
list_l2_rel_error_HLL = []
for gamma in list_gammas:
    p = gamma
    curr_rel_error_HLL, curr_l2_rel_error_HLL = HLL_error_experiment(p, T_q)
    list_rel_error_HLL.append(curr_rel_error_HLL)
    list_l2_rel_error_HLL.append(curr_l2_rel_error_HLL)

# plot for BC b=0 (minimize relative error) ppow=0 (only power of 2)
list_rel_error_BC00 = []
list_l2_rel_error_BC00 = []
b = 0
ppow = 0
for gamma in list_gammas:
    curr_best_config, bias, rel_error, l2_rel_error = find_best_config(T_q, gamma, b, ppow)
    list_rel_error_BC00.append(rel_error)
    list_l2_rel_error_BC00.append(l2_rel_error)

# plot for BC b=0 (minimize relative error) ppow=1 
list_rel_error_BC01 = []
list_l2_rel_error_BC01 = []
b = 0
ppow = 1
for gamma in list_gammas:
    curr_best_config, bias, rel_error, l2_rel_error = find_best_config(T_q, gamma, b, ppow)
    list_rel_error_BC01.append(rel_error)
    list_l2_rel_error_BC01.append(l2_rel_error)

# plot for BC b=1 (minimize variance) ppow=0 (only power of 2)
list_rel_error_BC10 = []
list_l2_rel_error_BC10 = []
b = 1
ppow = 0
for gamma in list_gammas:
    curr_best_config, bias, rel_error, l2_rel_error = find_best_config(T_q, gamma, b, ppow)
    list_rel_error_BC10.append(rel_error)
    list_l2_rel_error_BC10.append(l2_rel_error)

# plot for BC b=1 (minimize variance) ppow=1
list_rel_error_BC11 = []
list_l2_rel_error_BC11 = []
b = 1
ppow = 1
for gamma in list_gammas:
    curr_best_config, bias, rel_error, l2_rel_error = find_best_config(T_q, gamma, b, ppow)
    list_rel_error_BC11.append(rel_error)
    list_l2_rel_error_BC11.append(l2_rel_error)



# Simulations for a single query :

for T_q in range(1000,1001):
	print("T_q = "+str(T_q))

	for b in range(2):
		for ppow in range(2):
			curr_best_config, bias, rel_error, l2_rel_error = find_best_config(T_q, 1, b, ppow)
			val = curr_best_config[3]/curr_best_config[2]
			# curr_best_config.append(curr_best_config[0]/(2**curr_best_config[1]))
			if b==0:
				currstr = "Paper Metric"
			else:
				currstr = "Our Metric:"

			if ppow == 0:
				currstr += "; p powers of 2"
			else:
				currstr += "; p arbitrary"

			print(currstr)
			print(curr_best_config)
			print("n/m = "+str(val))
			print("bias = "+str(bias))
			print("relative error = "+str(rel_error))
			print("l2 relative error = "+str(l2_rel_error))
			print("-------------------------------------------------")
			
	print("-------------------------------------------------")

exit()


# run_on_files()