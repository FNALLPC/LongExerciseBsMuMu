import math

def task_3_3():
    cate    = 2
    pt_min  = 20.0
    pt_max  = 30.0
    eta_min = 0.
    eta_max = 2.5

    # From task3_1.cc
    # Category: 2
    # pt range: 20, 30
    # |eta| range: 0, 2.5
    # Selection efficiency: 0.32762 +- 0.0014842
    # Observed yield: 106740 +- 782.594

    # From task3_2.cc
    # Category: 2
    # pt range: 20, 30
    # |eta| range: 0, 2.5
    # Selection efficiency: 0.39079 +- 0.00154296
    # Observed yield: 7593.83 +- 207.071

    ret_bupsik   = [0.] * 4
    ret_bspsiphi = [0.] * 4

    ret_bupsik[0] = 0.32762
    ret_bupsik[1] = 0.0014842 / ret_bupsik[0]
    ret_bupsik[2] = 106740
    ret_bupsik[3] = 782.594 / ret_bupsik[2]

    ret_bspsiphi[0] = 0.39079
    ret_bspsiphi[1] = 0.00154296 / ret_bspsiphi[0]
    ret_bspsiphi[2] = 7593.83
    ret_bspsiphi[3] = 207.071 / ret_bspsiphi[2]

    baseeff_bupsik   = 0.001267
    baseeff_bspsiphi = 0.0005476

    BF_bupsik     = 1.010E-3
    BF_bupsik_err = 0.028 / 1.010

    BF_bspsiphi     = 1.08E-3 * 0.492
    BF_bspsiphi_err = math.sqrt((0.08 / 1.08)**2 + (0.5 / 49.2)**2)

    fs = ret_bspsiphi[2] / ret_bspsiphi[0] / baseeff_bspsiphi / BF_bspsiphi
    fu = ret_bupsik[2]   / ret_bupsik[0]   / baseeff_bupsik   / BF_bupsik

    fs_over_fu            = fs / fu
    fs_over_fu_err        = fs_over_fu * math.sqrt(ret_bspsiphi[1]**2 + ret_bspsiphi[3]**2 +
                                                    ret_bupsik[1]**2   + ret_bupsik[3]**2)
    fs_over_fu_err_common = fs_over_fu * math.sqrt(BF_bupsik_err**2 + BF_bspsiphi_err**2)

    print("Category:", cate)
    print("pt range: %g, %g" % (pt_min, pt_max))
    print("|eta| range: %g, %g" % (eta_min, eta_max))
    print("fs_over_fu: %g +- %g +- %g" % (fs_over_fu, fs_over_fu_err, fs_over_fu_err_common))


if __name__ == "__main__":
    task_3_3()
