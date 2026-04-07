import ROOT
from common import effyield, Eff_bsmmMc, dEff_bsmmMc

def task_4_3():
    cate    = 0
    bdt_min = 0.8

    m   = ROOT.RooRealVar("m", "", 4.9, 5.9)
    rds = ROOT.RooDataSet("rds", "", ROOT.RooArgSet(m))

    fin = ROOT.TFile("root://cmseos.fnal.gov//store/user/cmsdas/2025/long_exercises/long-ex-bs-mumu/bsmmMc.root")
    tin = fin.Get("bsmmMc")

    cate_t = ROOT.std.vector('unsigned int')(1)
    m_t    = ROOT.std.vector('float')(1)
    bdt_t  = ROOT.std.vector('float')(1)
    tin.SetBranchAddress("cate", cate_t.data())
    tin.SetBranchAddress("m",    m_t.data())
    tin.SetBranchAddress("bdt",  bdt_t.data())

    evtcount = [0, 0]
    for evt in range(tin.GetEntries()):
        tin.GetEntry(evt)
        if cate_t[0] != cate: continue
        evtcount[0] += 1
        if bdt_t[0] <= bdt_min: continue
        evtcount[1] += 1
        m.setVal(m_t[0])
        rds.add(ROOT.RooArgSet(m))

    eff       = float(evtcount[1]) / float(evtcount[0]) * effyield[cate][Eff_bsmmMc]
    eff_error = effyield[cate][dEff_bsmmMc] / effyield[cate][Eff_bsmmMc] * eff  # ignore MC statistical error
    fin.Close()

    bs_mean1   = ROOT.RooRealVar("bs_mean1",   "", 5.37, 5.2, 5.5)
    bs_mean2   = ROOT.RooRealVar("bs_mean2",   "", 5.37, 5.2, 5.5)
    bs_sigma1  = ROOT.RooRealVar("bs_sigma1",  "", 0.030, 0.005, 0.060)
    bs_sigma2  = ROOT.RooRealVar("bs_sigma2",  "", 0.080, 0.040, 0.200)
    bs_cbalpha = ROOT.RooRealVar("bs_cbalpha", "", 1., 0., 4.)
    bs_cbn     = ROOT.RooRealVar("bs_cbn",     "", 1., 0., 4.)
    bs_frac    = ROOT.RooRealVar("bs_frac",    "", 0.7, 0., 1.)
    bs_gaus    = ROOT.RooGaussian("bs_gaus",   "", m, bs_mean1, bs_sigma1)
    bs_cbline  = ROOT.RooCBShape("bs_cbline",  "", m, bs_mean2, bs_sigma2, bs_cbalpha, bs_cbn)
    pdf        = ROOT.RooAddPdf("pdf", "", ROOT.RooArgList(bs_gaus, bs_cbline), ROOT.RooArgList(bs_frac))
    pdf.fitTo(rds)

    frame = m.frame(ROOT.RooFit.Title(" "), ROOT.RooFit.Bins(100))
    rds.plotOn(frame, ROOT.RooFit.Name("t_rds"))
    pdf.plotOn(frame, ROOT.RooFit.Name("t_pdf"), ROOT.RooFit.LineWidth(3))

    canvas = ROOT.TCanvas("canvas", "", 600, 600)
    canvas.SetMargin(0.15, 0.06, 0.13, 0.07)

    frame.GetYaxis().SetTitleOffset(1.50)
    frame.GetYaxis().SetTitle("Entries / 0.01 GeV")
    frame.GetXaxis().SetTitleOffset(1.15)
    frame.GetXaxis().SetLabelOffset(0.01)
    frame.GetXaxis().SetTitle("M(#mu#mu) [GeV]")
    frame.GetXaxis().SetTitleSize(0.043)
    frame.GetYaxis().SetTitleSize(0.043)
    frame.Draw()

    leg = ROOT.TLegend(0.58, 0.77, 0.93, 0.92)
    leg.SetFillStyle(0)
    leg.SetLineWidth(0)
    leg.SetHeader("Category %d" % cate)
    leg.AddEntry(frame.findObject("t_rds"), "Simluation", "EP")
    leg.AddEntry(frame.findObject("t_pdf"), "PDF",        "L")
    leg.Draw()

    canvas.Print("task_4_3.pdf")
    canvas.Print("task_4_3.png")

    print("Category:", cate)
    print("BDT min:", bdt_min)
    print("Selection efficiency: %g +- %g" % (eff, eff_error))


if __name__ == "__main__":
    task_4_3()
