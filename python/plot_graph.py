import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter


plt.plot(list_gammas, list_rel_error_HLL, "x-", label="HyperLogLog")
plt.plot(list_gammas, list_rel_error_BC00, "+-", label="BeauCoup original")
plt.plot(list_gammas, list_rel_error_BC01, "2--", label="BeauCoup $p_q$ not power of 2")
plt.plot(list_gammas, list_rel_error_BC10, "-.", label="BeauCoup min variance")
plt.plot(list_gammas, list_rel_error_BC11, "*-", label="BeauCoup min variance, $p_q$ not power of 2")

plt.ylabel("Mean Relative Error")
plt.xscale('log', basex=10)
plt.xlabel('Average memory access per packet ($\gamma$)')
plt.legend()
plt.show()


# plot relative error
plt.plot(list_gammas, list_l2_rel_error_HLL, "x-", label="HyperLogLog")
plt.plot(list_gammas, list_l2_rel_error_BC00, "+-", label="BeauCoup original")
plt.plot(list_gammas, list_l2_rel_error_BC01, "2--", label="BeauCoup $p_q$ not power of 2")
plt.plot(list_gammas, list_l2_rel_error_BC10, "-.", label="BeauCoup min variance")
plt.plot(list_gammas, list_l2_rel_error_BC11, "*-", label="BeauCoup min variance, $p_q$ not power of 2")

plt.ylabel("Mean L2 Relative Error")
plt.xscale('log', basex=10)
plt.xlabel('Average memory access per packet ($\gamma$)')
plt.legend()
plt.show()