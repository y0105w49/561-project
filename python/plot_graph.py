import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter


plt.plot(list_gammas, list_rel_error_HLL, "x-", label="HyperLogLog")
plt.plot(list_gammas, list_rel_error_BC00, "+-", label="BeauCoup: Original metric, p power of 2")
plt.plot(list_gammas, list_rel_error_BC01, "2--", label="BeauCoup: Original metric, p arbitrary")
plt.plot(list_gammas, list_rel_error_BC10, "-.", label="BeauCoup: L2 metric, p power of 2")
plt.plot(list_gammas, list_rel_error_BC11, "*-", label="BeauCoup: L2 metric, p arbitrary")

plt.ylabel("Mean Relative Error")
plt.xscale('log', basex=10)
plt.xlabel('Average memory access per packet ($\gamma$)')
plt.legend()
plt.show()


# plot relative error
plt.plot(list_gammas, list_l2_rel_error_HLL, "x-", label="HyperLogLog")
plt.plot(list_gammas, list_l2_rel_error_BC00, "+-", label="BeauCoup: Original metric, p power of 2")
plt.plot(list_gammas, list_l2_rel_error_BC01, "2--", label="BeauCoup: Original metric, p arbitrary")
plt.plot(list_gammas, list_l2_rel_error_BC10, "-.", label="BeauCoup: L2 metric, p power of 2")
plt.plot(list_gammas, list_l2_rel_error_BC11, "*-", label="BeauCoup: L2 metric, p arbitrary")

plt.ylabel("Mean L2 Relative Error")
plt.xscale('log', basex=10)
plt.xlabel('Average memory access per packet ($\gamma$)')
plt.legend()
plt.show()