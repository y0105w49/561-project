import matplotlib.pyplot as plt

# plot relative error
f = open("Beaucoup00_errors.txt", "r")
list_gammas = []
list_rel_error_BC00 = []
list_l2_rel_error_BC00 = []
list_bias_BC00 = []
for line in f:
    gamma, rel_error, l2_rel_error, bias, numer_p, denom_p, m_q, n_q = [float(x) for x in line.split(",")]
    list_gammas.append(gamma)
    list_rel_error_BC00.append(rel_error)
    list_l2_rel_error_BC00.append(l2_rel_error)
    list_bias_BC00.append(bias)
f.close()

f = open("Beaucoup01_errors.txt", "r")
list_gammas = []
list_rel_error_BC01 = []
list_l2_rel_error_BC01 = []
list_bias_BC01 = []
for line in f:
    gamma, rel_error, l2_rel_error, bias, numer_p, denom_p, m_q, n_q = [float(x) for x in line.split(",")]
    list_gammas.append(gamma)
    list_rel_error_BC01.append(rel_error)
    list_l2_rel_error_BC01.append(l2_rel_error)
    list_bias_BC01.append(bias)
f.close()

f = open("Beaucoup10_errors.txt", "r")
list_gammas = []
list_rel_error_BC10 = []
list_l2_rel_error_BC10 = []
list_bias_BC10 = []
for line in f:
    gamma, rel_error, l2_rel_error, bias, numer_p, denom_p, m_q, n_q = [float(x) for x in line.split(",")]
    list_gammas.append(gamma)
    list_rel_error_BC10.append(rel_error)
    list_l2_rel_error_BC10.append(l2_rel_error)
    list_bias_BC10.append(bias)
f.close()

f = open("Beaucoup11_errors.txt", "r")
list_gammas = []
list_rel_error_BC11 = []
list_l2_rel_error_BC11 = []
list_bias_BC11 = []
for line in f:
    gamma, rel_error, l2_rel_error, bias, numer_p, denom_p, m_q, n_q = [float(x) for x in line.split(",")]
    list_gammas.append(gamma)
    list_rel_error_BC11.append(rel_error)
    list_l2_rel_error_BC11.append(l2_rel_error)
    list_bias_BC11.append(bias)
f.close()

f = open("HLL_errors.txt", "r")
list_gammas = []
list_rel_error_HLL = []
list_l2_rel_error_HLL = []
for line in f:
    gamma, rel_error, l2_rel_error = [float(x) for x in line.split(",")]
    list_gammas.append(gamma)
    list_rel_error_HLL.append(rel_error)
    list_l2_rel_error_HLL.append(l2_rel_error)
f.close()


# plot relative error

plt.plot(list_gammas, list_rel_error_HLL, "x-", label="HyperLogLog")
plt.plot(list_gammas, list_rel_error_BC00, "+-", label="BeauCoup: Original metric, p power of 2")
plt.plot(list_gammas, list_rel_error_BC01, "2--", label="BeauCoup: Original metric, p arbitrary")
plt.plot(list_gammas, list_rel_error_BC10, "-.", label="BeauCoup: L2 metric, p power of 2")
plt.plot(list_gammas, list_rel_error_BC11, "*-", label="BeauCoup: L2 metric, p arbitrary")

plt.ylabel("Mean Relative Error")
plt.xscale('log', basex=10)
plt.xlabel('Average memory access per packet ($\gamma$)')
plt.legend()
plt.savefig("figures/rel_error.png")
plt.close()


# plot l2 relative error
plt.plot(list_gammas, list_l2_rel_error_HLL, "x-", label="HyperLogLog")
plt.plot(list_gammas, list_l2_rel_error_BC00, "+-", label="BeauCoup: Original metric, p power of 2")
plt.plot(list_gammas, list_l2_rel_error_BC01, "2--", label="BeauCoup: Original metric, p arbitrary")
plt.plot(list_gammas, list_l2_rel_error_BC10, "-.", label="BeauCoup: L2 metric, p power of 2")
plt.plot(list_gammas, list_l2_rel_error_BC11, "*-", label="BeauCoup: L2 metric, p arbitrary")

plt.ylabel("Mean L2 Relative Error")
plt.xscale('log', basex=10)
plt.xlabel('Average memory access per packet ($\gamma$)')
plt.legend()
plt.savefig("figures/l2_rel_error.png")
plt.close()

plt.plot(list_gammas, list_bias_BC10, "-.", label="BeauCoup: L2 metric, p power of 2")
plt.plot(list_gammas, list_bias_BC11, "*-", label="BeauCoup: L2 metric, p arbitrary")
plt.ylabel("Mean Bias")
plt.xscale('log', basex=10)
plt.xlabel('Average memory access per packet ($\gamma$)')
plt.legend()
plt.savefig("figures/bias.png")
plt.close()