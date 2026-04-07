import ROOT

def task_2_2():
    category = 0

    m   = ROOT.RooRealVar("m",   "", 5.0, 5.8)
    wgt = ROOT.RooRealVar("wgt", "", 1., 0., 1000.)
    rds_data = ROOT.RooDataSet("rds_data", "", ROOT.RooArgSet(m, wgt), "wgt")

    fin = ROOT.TFile("root://cmseos.fnal.gov//store/user/cmsdas/2025/long_exercises/long-ex-bs-mumu/bupsikData.root")
    tin = fin.Get("bupsikData")

    cate_t = ROOT.std.vector('unsigned int')(1)
    m_t    = ROOT.std.vector('float')(1)
    wgt_t  = ROOT.std.vector('float')(1)
    tin.SetBranchAddress("cate", cate_t.data())
    tin.SetBranchAddress("m",    m_t.data())
    tin.SetBranchAddress("wgt",  wgt_t.data())

    for evt in range(tin.GetEntries()):
        tin.GetEntry(evt)
        if cate_t[0] != category:
            continue
        if m_t[0] < 5.0 or m_t[0] >= 5.8:
            continue
        m.setVal(m_t[0])
        wgt.setVal(wgt_t[0])
        rds_data.add(ROOT.RooArgSet(m, wgt), wgt_t[0])

    fin.Close()

    # Signal PDF (fixed from MC)
    sig_mean1  = ROOT.RooRealVar("sig_mean1",  "", 5.27971)
    sig_mean2  = ROOT.RooRealVar("sig_mean2",  "", 5.26646)
    sig_sigma1 = ROOT.RooRealVar("sig_sigma1", "", 0.0156007)
    sig_sigma2 = ROOT.RooRealVar("sig_sigma2", "", 0.0627436)
    sig_frac   = ROOT.RooRealVar("sig_frac",   "", 0.926022)
    sig_g1  = ROOT.RooGaussian("sig_g1", "", m, sig_mean1, sig_sigma1)
    sig_g2  = ROOT.RooGaussian("sig_g2", "", m, sig_mean2, sig_sigma2)
    pdf_sig = ROOT.RooAddPdf("pdf_sig", "", ROOT.RooArgList(sig_g1, sig_g2), ROOT.RooArgList(sig_frac))
    n_sig   = ROOT.RooRealVar("n_sig", "", 100000, 0., 1E8)

    # Combinatorial background (exponential)
    comb_coeff = ROOT.RooRealVar("comb_coeff", "", -1.2, -10., 10.)
    pdf_comb   = ROOT.RooExponential("pdf_comb", "", m, comb_coeff)
    n_comb     = ROOT.RooRealVar("n_comb", "", 80000, 0., 1E6)

    # J/psi + X background (error function)
    jpsix_scale = ROOT.RooRealVar("jpsix_scale", "", 0.02, 0.001, 0.08)
    jpsix_shift = ROOT.RooRealVar("jpsix_shift", "", 5.13, 5.12, 5.16)
    pdf_jpsix   = ROOT.RooGenericPdf("pdf_jpsix", "", "TMath::Erfc((@0-@1)/@2)",
                                     ROOT.RooArgList(m, jpsix_shift, jpsix_scale))
    n_jpsix = ROOT.RooRealVar("n_jpsix", "", 20000, 0., 1E5)

    # Final model
    model = ROOT.RooAddPdf("model", "", ROOT.RooArgList(pdf_sig, pdf_comb, pdf_jpsix),
                           ROOT.RooArgList(n_sig, n_comb, n_jpsix))

    model.fitTo(rds_data, ROOT.RooFit.Extended(True), ROOT.RooFit.SumW2Error(True))

    # Plotting
    frame = m.frame(ROOT.RooFit.Title(" "), ROOT.RooFit.Bins(80))
    rds_data.plotOn(frame, ROOT.RooFit.Name("t_rds_data"))
    model.plotOn(frame, ROOT.RooFit.Name("t_model"), ROOT.RooFit.LineWidth(3))
    model.plotOn(frame, ROOT.RooFit.Name("t_pdf_comb"), ROOT.RooFit.Components("pdf_comb"),
                 ROOT.RooFit.LineWidth(3), ROOT.RooFit.LineStyle(2), ROOT.RooFit.LineColor(ROOT.kGray + 1))
    model.paramOn(frame, ROOT.RooFit.Layout(0.9, 0.6, 0.6))
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
    leg.SetHeader("Category %d" % category)
    leg.AddEntry(frame.findObject("t_rds_data"), "Real Data", "EP")
    leg.AddEntry(frame.findObject("t_pdf_sig"),  "Fit", "L")
    leg.AddEntry(frame.findObject("t_pdf_comb"), "Combinatorial bkg.", "L")
    leg.Draw()

    canvas.Print("task_2_2.pdf")
    canvas.Print("task_2_2.png")


if __name__ == "__main__":
    task_2_2()
