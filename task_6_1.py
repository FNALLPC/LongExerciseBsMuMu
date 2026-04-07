import ROOT
from common import N_Categories

def task_6_1():
    bdt_min = 0.80

    fin_wspace = ROOT.TFile("wspace.root")
    wspace     = fin_wspace.Get("wspace")

    m    = wspace.var("m")
    nset = ROOT.RooArgSet(m)
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

    model.fitTo(rds_data, ROOT.RooFit.Extended(True), ROOT.RooFit.Minos(ROOT.RooArgSet(BF_bs)))

    canvas = ROOT.TCanvas("canvas", "", 1200, 600)
    canvas.Divide(4, 2)

    frames = []
    for idx in range(N_Categories):
        pad = canvas.cd(idx + 1)
        pad.SetMargin(0.15, 0.06, 0.13, 0.07)

        frame_i = m.frame(ROOT.RooFit.Title(" "), ROOT.RooFit.Bins(25))
        frames.append(frame_i)
        rds_data.plotOn(frame_i, ROOT.RooFit.Cut("cate==%d" % idx), ROOT.RooFit.MarkerSize(0.8))

        norm = pdf_sum[idx].expectedEvents(nset)
        pdf_sum[idx].plotOn(frame_i, ROOT.RooFit.Normalization(norm, ROOT.RooAbsReal.NumEvent), ROOT.RooFit.LineWidth(3))
        pdf_sum[idx].plotOn(frame_i, ROOT.RooFit.Normalization(norm, ROOT.RooAbsReal.NumEvent),
                            ROOT.RooFit.Components(ROOT.RooArgSet(wspace.pdf("pdf_bs_%d"   % idx))),
                            ROOT.RooFit.DrawOption("F"), ROOT.RooFit.FillColor(ROOT.kRed),       ROOT.RooFit.FillStyle(3365))
        pdf_sum[idx].plotOn(frame_i, ROOT.RooFit.Normalization(norm, ROOT.RooAbsReal.NumEvent),
                            ROOT.RooFit.Components(ROOT.RooArgSet(wspace.pdf("pdf_peak_%d" % idx))),
                            ROOT.RooFit.DrawOption("F"), ROOT.RooFit.FillColor(ROOT.kViolet - 4), ROOT.RooFit.FillStyle(3344))
        pdf_sum[idx].plotOn(frame_i, ROOT.RooFit.Normalization(norm, ROOT.RooAbsReal.NumEvent),
                            ROOT.RooFit.Components(ROOT.RooArgSet(wspace.pdf("pdf_semi_%d" % idx))),
                            ROOT.RooFit.DrawOption("L"), ROOT.RooFit.LineColor(ROOT.kGreen - 3),  ROOT.RooFit.LineStyle(2))

        frame_i.GetYaxis().SetTitleOffset(1.50)
        frame_i.GetYaxis().SetTitle("Entries / 0.04 GeV")
        frame_i.GetXaxis().SetTitleOffset(1.15)
        frame_i.GetXaxis().SetLabelOffset(0.01)
        frame_i.GetXaxis().SetTitle("M(#mu#mu) [GeV]")
        frame_i.GetXaxis().SetTitleSize(0.043)
        frame_i.GetYaxis().SetTitleSize(0.043)
        frame_i.Draw()

    canvas.Print("task_6_1.pdf")
    canvas.Print("task_6_1.png")


if __name__ == "__main__":
    task_6_1()
