import ROOT
import math
from common import N_Categories


def do_gen_and_fit():
    bdt_min = 0.8

    fin_wspace = ROOT.TFile("wspace.root")
    wspace     = fin_wspace.Get("wspace")

    m    = wspace.var("m")
    cate = ROOT.RooCategory("cate", "")
    for idx in range(N_Categories):
        cate.defineType("c%d" % idx, idx)

    model = ROOT.RooSimultaneous("model", "", cate)

    # Main POI: Bs->mumu branching fraction
    BF_bs = ROOT.RooRealVar("BF_bs", "", 3.57E-9, 0., 3E-8)

    # BF(B+ -> J/psi K+) = (1.010 +- 0.028) E-3 (PDG)
    # BF(J/psi -> mu+mu-) = (5.961 +- 0.033) E-2 (PDG)
    BF_bu = ROOT.RooRealVar("BF_bu", "", 1.010E-3 * 5.961E-2)

    # fs/fu = 0.252 +- 0.012 (PDG) +- 0.015 (energy/pt dependence)
    fs_over_fu = ROOT.RooRealVar("fs_over_fu", "", 0.252)

    N_bs_vars = []
    pdf_sum   = []
    for idx in range(N_Categories):
        Eff_bs = wspace.var("Eff_bs_%d" % idx)
        Eff_bu = wspace.var("Eff_bu_%d" % idx)
        N_bu   = wspace.var("N_bu_%d"   % idx)

        N_bs_i = ROOT.RooFormulaVar("N_bs_%d" % idx, "", "@0*@1*@2*@3/@4/@5",
                                    ROOT.RooArgList(BF_bs, N_bu, fs_over_fu, Eff_bs, Eff_bu, BF_bu))
        N_bs_vars.append(N_bs_i)

        N_peak = wspace.var("N_peak_%d" % idx)
        N_semi = wspace.var("N_semi_%d" % idx)
        N_comb = wspace.var("N_comb_%d" % idx)

        # fix the efficiencies
        Eff_bs.setConstant(True)
        Eff_bu.setConstant(True)

        # fix the semi/peak/bu yield
        N_bu.setConstant(True)
        N_peak.setConstant(True)
        N_semi.setConstant(True)

        pdf_list = ROOT.RooArgList()
        pdf_list.add(wspace.pdf("pdf_bs_%d"   % idx))
        pdf_list.add(wspace.pdf("pdf_peak_%d" % idx))
        pdf_list.add(wspace.pdf("pdf_semi_%d" % idx))
        pdf_list.add(wspace.pdf("pdf_comb_%d" % idx))

        N_list = ROOT.RooArgList()
        N_list.add(N_bs_i)
        N_list.add(N_peak)
        N_list.add(N_semi)
        N_list.add(N_comb)

        pdf_sum_i = ROOT.RooAddPdf("pdf_sum_%d" % idx, "", pdf_list, N_list)
        pdf_sum.append(pdf_sum_i)
        model.addPdf(pdf_sum_i, "c%d" % idx)

    rds_toy = model.generate(ROOT.RooArgSet(m, cate), ROOT.RooFit.Extended(True))

    res_best = model.fitTo(rds_toy, ROOT.RooFit.Save(True), ROOT.RooFit.Extended(True),
                           ROOT.RooFit.Minos(ROOT.RooArgSet(BF_bs)))

    res = [0.] * 5
    res[0] = BF_bs.getVal()
    res[1] = BF_bs.getError()
    res[2] = BF_bs.getErrorHi()
    res[3] = BF_bs.getErrorLo()

    BF_bs.setConstant(True)
    BF_bs.setVal(0.)
    res_null = model.fitTo(rds_toy, ROOT.RooFit.Save(True), ROOT.RooFit.Extended(True))

    res[4] = math.sqrt((res_null.minNll() - res_best.minNll()) * 2.)

    return res


def task_6_3():
    h_mean   = ROOT.TH1D("h_mean",   "", 50, 0.,   1E-8)
    h_error  = ROOT.TH1D("h_error",  "", 50, 0.,   2E-9)
    h_signif = ROOT.TH1D("h_signif", "", 50, 0.,   10.)
    h_pull   = ROOT.TH1D("h_pull",   "", 50, -5.,  5.)

    for iteration in range(1000):
        print("iteration:", iteration)
        res = do_gen_and_fit()

        h_mean.Fill(res[0])
        h_error.Fill(res[1])
        h_signif.Fill(res[4])

        pull = res[0] - 3.57E-9
        if pull > 0.:
            pull /= abs(res[3])
        if pull < 0.:
            pull /= abs(res[2])
        if abs(res[3]) > 0. and abs(res[2]) > 0.:
            h_pull.Fill(pull)

    canvas = ROOT.TCanvas("canvas", "", 800, 800)
    canvas.Divide(2, 2)

    for hist in [h_mean, h_error, h_signif, h_pull]:
        hist.GetYaxis().SetTitleOffset(1.50)
        hist.GetYaxis().SetTitle("# of toys")
        hist.GetXaxis().SetTitleOffset(1.15)
        hist.GetXaxis().SetLabelOffset(0.01)
        hist.GetXaxis().SetTitleSize(0.043)
        hist.GetYaxis().SetTitleSize(0.043)
        hist.SetStats(True)
        hist.SetFillColor(41)

    canvas.cd(1).SetMargin(0.15, 0.09, 0.13, 0.07)
    h_mean.GetXaxis().SetTitle("B(B_{s}#rightarrow#mu#mu) Mean")
    h_mean.Draw()
    canvas.cd(2).SetMargin(0.15, 0.09, 0.13, 0.07)
    h_error.GetXaxis().SetTitle("B(B_{s}#rightarrow#mu#mu) Error")
    h_error.Draw()
    canvas.cd(3).SetMargin(0.15, 0.09, 0.13, 0.07)
    h_signif.GetXaxis().SetTitle("Significance")
    h_signif.Draw()
    canvas.cd(4).SetMargin(0.15, 0.09, 0.13, 0.07)
    h_pull.GetXaxis().SetTitle("Pull")
    h_pull.Fit("gaus", "L")

    canvas.Print("task6_3.pdf")
    canvas.Print("task6_3.png")


if __name__ == "__main__":
    task_6_3()
