import ROOT

def task_2_1():
    cate_t = 0

    m = ROOT.RooRealVar("m", "", 5.0, 5.8)
    cate = ROOT.RooRealVar("cate", "", -1, 20)

    # B -> J/psi K MC
    fin = ROOT.TFile("root://cmseos.fnal.gov//store/user/cmsdas/2025/long_exercises/long-ex-bs-mumu/bupsikMc.root")
    tin = fin.Get("bupsikMc")

    rds_mc = ROOT.RooDataSet("rds_mc", "rds_mc", tin, ROOT.RooArgSet(cate, m))
    rds_mc = rds_mc.reduce(m, "m >= 5.0 && m <= 5.8 && cate==%d" % cate_t)

    # Construct Double Gaussian Model
    sig_mean1  = ROOT.RooRealVar("sig_mean1",  "", 5.28, 5.2, 5.4)
    sig_mean2  = ROOT.RooRealVar("sig_mean2",  "", 5.28, 5.2, 5.4)
    sig_sigma1 = ROOT.RooRealVar("sig_sigma1", "", 0.030, 0.005, 0.060)
    sig_sigma2 = ROOT.RooRealVar("sig_sigma2", "", 0.080, 0.040, 0.200)
    sig_frac   = ROOT.RooRealVar("sig_frac",   "", 0.9, 0.5, 1.0)

    sig_g1 = ROOT.RooGaussian("sig_g1", "", m, sig_mean1, sig_sigma1)
    sig_g2 = ROOT.RooGaussian("sig_g2", "", m, sig_mean2, sig_sigma2)
    pdf_sig = ROOT.RooAddPdf("pdf_sig", "", ROOT.RooArgList(sig_g1, sig_g2), ROOT.RooArgList(sig_frac))

    # Fit
    pdf_sig.fitTo(rds_mc)

    # Plotting
    frame = m.frame(ROOT.RooFit.Title(" "), ROOT.RooFit.Bins(80))
    rds_mc.plotOn(frame, ROOT.RooFit.Name("t_rds_mc"))
    pdf_sig.plotOn(frame, ROOT.RooFit.Name("t_pdf_sig"), ROOT.RooFit.LineWidth(3))
    pdf_sig.plotOn(frame, ROOT.RooFit.Name("sig_g1"), ROOT.RooFit.Components(ROOT.RooArgList(sig_g1)),
                   ROOT.RooFit.LineColor(ROOT.kRed), ROOT.RooFit.LineStyle(2), ROOT.RooFit.LineWidth(2))
    pdf_sig.plotOn(frame, ROOT.RooFit.Name("sig_g2"), ROOT.RooFit.Components(ROOT.RooArgList(sig_g2)),
                   ROOT.RooFit.LineColor(ROOT.kGreen), ROOT.RooFit.LineStyle(2), ROOT.RooFit.LineWidth(3))

    pdf_sig.paramOn(frame, ROOT.RooFit.Layout(0.9, 0.6, 0.5))
    frame.getAttText().SetTextSize(0.02)

    canvas = ROOT.TCanvas("canvas", "", 600, 600)
    canvas.SetMargin(0.15, 0.06, 0.13, 0.07)

    frame.GetYaxis().SetTitleOffset(1.50)
    frame.GetYaxis().SetTitle("Entries / 0.01 GeV")
    frame.GetXaxis().SetTitleOffset(1.15)
    frame.GetXaxis().SetLabelOffset(0.01)
    frame.GetXaxis().SetTitle("M(#mu#muK) [GeV]")
    frame.GetXaxis().SetTitleSize(0.043)
    frame.GetYaxis().SetTitleSize(0.043)
    frame.Draw()

    leg = ROOT.TLegend(0.58, 0.77, 0.93, 0.92)
    leg.SetFillStyle(0)
    leg.SetLineWidth(0)
    leg.SetHeader("Category %d" % cate_t)
    leg.AddEntry(frame.findObject("t_rds_mc"), "Simluation", "EP")
    leg.AddEntry(frame.findObject("t_pdf_sig"), "Fit", "L")
    leg.Draw()

    canvas.Print("task_2_1.pdf")
    canvas.Print("task_2_1.png")


if __name__ == "__main__":
    task_2_1()
