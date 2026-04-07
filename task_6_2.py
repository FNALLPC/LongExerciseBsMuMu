import ROOT
import math
from common import N_Categories

def task_6_2():
    bdt_min = 0.8

    fin_wspace = ROOT.TFile("wspace.root")
    wspace     = fin_wspace.Get("wspace")

    m    = wspace.var("m")
    cate = ROOT.RooCategory("cate", "")
    for idx in range(N_Categories):
        cate.defineType("c%d" % idx, idx)

    model = ROOT.RooSimultaneous("model", "", cate)

    # Main POI: Bs->mumu branching fraction
    BF_bs = ROOT.RooRealVar("BF_bs", "", 3.57E-9, 0., 2E-8)

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

    rds_data = ROOT.RooDataSet("rds_data", "", ROOT.RooArgSet(m, cate))

    fin_data = ROOT.TFile("root://cmseos.fnal.gov//store/user/cmsdas/2025/long_exercises/long-ex-bs-mumu/bmmSoup10.root")
    tin      = fin_data.Get("bmmSoup10_100")

    cate_t = ROOT.std.vector('unsigned int')(1)
    m_t    = ROOT.std.vector('float')(1)
    bdt_t  = ROOT.std.vector('float')(1)
    tin.SetBranchAddress("cate", cate_t.data())
    tin.SetBranchAddress("m",    m_t.data())
    tin.SetBranchAddress("bdt",  bdt_t.data())

    for evt in range(tin.GetEntries()):
        tin.GetEntry(evt)
        if bdt_t[0] <= bdt_min: continue
        cate.setIndex(cate_t[0])
        m.setVal(m_t[0])
        rds_data.add(ROOT.RooArgSet(m, cate))

    res_best = model.fitTo(rds_data, ROOT.RooFit.Extended(True), ROOT.RooFit.Save(True),
                           ROOT.RooFit.Minos(ROOT.RooArgSet(BF_bs)))
    nll = model.createNLL(rds_data, ROOT.RooFit.Extended(True))

    frame = ROOT.TH1D("frame", "", 101, -0.5E-10, 100.5E-10)
    for bin_i in range(1, frame.GetNbinsX() + 1):
        BF_bs.setVal(frame.GetBinCenter(bin_i))
        BF_bs.setConstant(True)
        model.fitTo(rds_data, ROOT.RooFit.Extended(True))
        frame.SetBinContent(bin_i, (nll.getVal() - res_best.minNll()) * 2.)

    canvas = ROOT.TCanvas("canvas", "", 600, 600)
    canvas.SetMargin(0.15, 0.09, 0.13, 0.07)
    canvas.SetGrid()

    frame.GetYaxis().SetTitleOffset(1.50)
    frame.GetYaxis().SetTitle("-2log(L/L_{max})")
    frame.GetXaxis().SetTitleOffset(1.15)
    frame.GetXaxis().SetLabelOffset(0.01)
    frame.GetXaxis().SetTitle("B(B_{s}#rightarrow#mu#mu)")
    frame.GetXaxis().SetTitleSize(0.043)
    frame.GetYaxis().SetTitleSize(0.043)
    frame.SetLineWidth(4)
    frame.SetStats(False)
    frame.Draw("c")

    canvas.Print("task_6_2.pdf")
    canvas.Print("task_6_2.png")

    print("Observed significance: %g sigma." % math.sqrt(frame.GetBinContent(1)))


if __name__ == "__main__":
    task_6_2()
