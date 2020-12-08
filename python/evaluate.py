from query_process import *

list_gammas = [2**(-i) for i in range(10)]
T_q = 10


# Simulations for a single query :

for b in range(1):
	for ppow in range(2):
		filename = "Beaucoup"+str(b)+str(ppow)+"_errors.txt"
		f = open(filename, "w+")
		for gamma in list_gammas:
			curr_best_config, bias, rel_error, l2_rel_error = find_best_config(T_q, gamma, b, ppow)
			ind = b + 2*ppow
			arr = [gamma, rel_error, l2_rel_error, bias]+curr_best_config
			strtoprint = ",".join(str(x) for x in arr)
			f.write(strtoprint+"\n")
		f.close()


# plot for HLL
filename = "HLL_errors.txt"
f = open(filename, "w+")
for gamma in list_gammas:
    p = gamma
    rel_error, l2_rel_error = HLL_error_experiment(p, T_q)
    arr = [gamma, rel_error, l2_rel_error]
    strtoprint = ",".join(str(x) for x in arr)
    f.write(strtoprint+"\n")
f.close()



# run_on_files()