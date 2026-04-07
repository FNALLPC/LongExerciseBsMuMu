import ROOT

def task_2_4():
    cate = 1

    m   = ROOT.RooRealVar("m",   "", 5.0, 5.8)
    wgt = ROOT.RooRealVar("wgt", "", 1., 0., 1000.)
    rds_data = ROOT.RooDataSet("rds_data", "", ROOT.RooArgSet(m, wgt), "wgt")
    rds_mc   = ROOT.RooDataSet("rds_mc",   "", ROOT.RooArgSet(m))

    # --- Read data ---
    fin = ROOT.TFile("root://cmseos.fnal.gov//store/user/cmsdas/2025/long_exercises/long-ex-bs-mumu/bupsikData.root")
    tin = fin.Get("bupsikData")

    cate_t = ROOT.std.vector('unsigned int')(1)
    m_t    = ROOT.std.vector('float')(1)
    wgt_t  = ROOT.std.vector('float')(1)
    tin.SetBranchAddress("cate", cate_t.data())
    tin.SetBranchAddress("wgt",  wgt_t.data())
    tin.SetBranchAddress("m",    m_t.data())

    for evt in range(tin.GetEntries()):
        tin.GetEntry(evt)
        if cate_t[0] != cate:
            continue
        if m_t[0] < 5.0 or m_t[0] >= 5.8:
            continue
        m.setVal(m_t[0])
        wgt.setVal(wgt_t[0])
        rds_data.add(ROOT.RooArgSet(m, wgt), wgt_t[0])
    fin.Close()

    # --- Read MC ---
    fin = ROOT.TFile("root://cmseos.fnal.gov//store/user/cmsdas/2025/long_exercises/long-ex-bs-mumu/bupsikMc.root")
    tin = fin.Get("bupsikMc")

    tin.SetBranchAddress("cate", cate_t.data())
    tin.SetBranchAddress("m",    m_t.data())

    for evt in range(tin.GetEntries()):
        tin.GetEntry(evt)
        if cate_t[0] != cate:
            continue
        if m_t[0] < 5.0 or m_t[0] >= 5.8:
            continue
        m.setVal(m_t[0])
        rds_mc.add(ROOT.RooArgSet(m))
    fin.Close()

    # --- MC PDF fit ---
    sigmc_mean1  = ROOT.RooRealVar("sigmc_mean1",  "", 5.28, 5.2, 5.4)
    sigmc_mean2  = ROOT.RooRealVar("sigmc_mean2",  "", 5.28, 5.2, 5.4)
    sigmc_sigma1 = ROOT.RooRealVar("sigmc_sigma1", "", 0.030, 0.005, 0.060)
    sigmc_sigma2 = ROOT.RooRealVar("sigmc_sigma2", "", 0.080, 0.040, 0.200)
    sig_frac     = ROOT.RooRealVar("sig_frac",     "", 0.9, 0.5, 1.0)
    sigmc_g1  = ROOT.RooGaussian("sig_g1",   "", m, sigmc_mean1, sigmc_sigma1)
    sigmc_g2  = ROOT.RooGaussian("sig_g2",   "", m, sigmc_mean2, sigmc_sigma2)
    pdf_sigmc = ROOT.RooAddPdf("pdf_sigmc",  "", ROOT.RooArgList(sigmc_g1, sigmc_g2), ROOT.RooArgList(sig_frac))

    pdf_sigmc.fitTo(rds_mc)

    frame1 = m.frame(ROOT.RooFit.Title(" "), ROOT.RooFit.Bins(80))
    rds_mc.plotOn(frame1, ROOT.RooFit.Name("t_rds_mc"))
    pdf_sigmc.plotOn(frame1, ROOT.RooFit.Name("t_pdf_sigmc"), ROOT.RooFit.LineWidth(3))

    canvas1 = ROOT.TCanvas("canvas1", "", 600, 600)
    canvas1.SetMargin(0.15, 0.06, 0.13, 0.07)

    frame1.GetYaxis().SetTitleOffset(1.50)
    frame1.GetYaxis().SetTitle("Entries / 0.01 GeV")
    frame1.GetXaxis().SetTitleOffset(1.15)
    frame1.GetXaxis().SetLabelOffset(0.01)
    frame1.GetXaxis().SetTitle("M(#mu#muK) [GeV]")
    frame1.GetXaxis().SetTitleSize(0.043)
    frame1.GetYaxis().SetTitleSize(0.043)
    frame1.Draw()

    leg1 = ROOT.TLegend(0.58, 0.77, 0.93, 0.92)
    leg1.SetFillStyle(0)
    leg1.SetLineWidth(0)
    leg1.SetHeader("Category %d" % cate)
    leg1.AddEntry(frame1.findObject("t_rds_mc"),    "Simluation", "EP")
    leg1.AddEntry(frame1.findObject("t_pdf_sigmc"), "Fit",        "L")
    leg1.Draw()

    canvas1.Print("task_2_4a.pdf")
    canvas1.Print("task_2_4a.png")

    # Fix MC parameters
    sigmc_mean1.setConstant(True)
    sigmc_mean2.setConstant(True)
    sigmc_sigma1.setConstant(True)
    sigmc_sigma2.setConstant(True)
    sig_frac.setConstant(True)

    # Data fit with MC-constrained signal + corrections
    sig_shift = ROOT.RooRealVar("sig_shift", "", 0., -0.02, 0.02)
    sig_scale = ROOT.RooRealVar("sig_scale", "", 1., 0.8, 1.2)

    sig_mean1  = ROOT.RooAddition("sig_mean1",  "", ROOT.RooArgList(sigmc_mean1, sig_shift))
    sig_mean2  = ROOT.RooAddition("sig_mean2",  "", ROOT.RooArgList(sigmc_mean2, sig_shift))
    sig_sigma1 = ROOT.RooProduct("sig_sigma1",  "", ROOT.RooArgList(sigmc_sigma1, sig_scale))
    sig_sigma2 = ROOT.RooProduct("sig_sigma2",  "", ROOT.RooArgList(sigmc_sigma2, sig_scale))
    sig_g1  = ROOT.RooGaussian("sig_g1d", "", m, sig_mean1, sig_sigma1)
    sig_g2  = ROOT.RooGaussian("sig_g2d", "", m, sig_mean2, sig_sigma2)
    pdf_sig = ROOT.RooAddPdf("pdf_sig", "", ROOT.RooArgList(sig_g1, sig_g2), ROOT.RooArgList(sig_frac))

    comb_coeff = ROOT.RooRealVar("comb_coeff", "", -1.2, -10., 10.)
    pdf_comb   = ROOT.RooExponential("pdf_comb", "", m, comb_coeff)

    jpsix_scale = ROOT.RooRealVar("jpsix_scale", "", 0.02, 0.001, 0.08)
    jpsix_shift = ROOT.RooRealVar("jpsix_shift", "", 5.13, 5.12, 5.16)
    pdf_jpsix   = ROOT.RooGenericPdf("pdf_jpsix", "", "TMath::Erfc((@0-@1)/@2)",
                                     ROOT.RooArgList(m, jpsix_shift, jpsix_scale))

    n_comb_guess  = rds_data.sumEntries("m>5.4") * 2.
    n_sig_guess   = rds_data.sumEntries("m>5.18&&m<5.38") - n_comb_guess / 4.
    n_jpsix_guess = rds_data.sumEntries("m<5.18") - n_comb_guess * 0.18 / 0.8

    n_sig   = ROOT.RooRealVar("n_sig",   "", n_sig_guess,   0., rds_data.sumEntries())
    n_comb  = ROOT.RooRealVar("n_comb",  "", n_comb_guess,  0., rds_data.sumEntries())
    n_jpsix = ROOT.RooRealVar("n_jpsix", "", n_jpsix_guess, 0., rds_data.sumEntries())
    model   = ROOT.RooAddPdf("model", "", ROOT.RooArgList(pdf_sig, pdf_comb, pdf_jpsix),
                             ROOT.RooArgList(n_sig, n_comb, n_jpsix))

    model.fitTo(rds_data, ROOT.RooFit.Extended(True), ROOT.RooFit.SumW2Error(True))

    frame2 = m.frame(ROOT.RooFit.Title(" "), ROOT.RooFit.Bins(80))
    rds_data.plotOn(frame2, ROOT.RooFit.Name("t_rds_data"))
    model.plotOn(frame2, ROOT.RooFit.Name("t_model"), ROOT.RooFit.LineWidth(3))
    model.plotOn(frame2, ROOT.RooFit.Name("t_pdf_comb"), ROOT.RooFit.Components("pdf_comb"),
                 ROOT.RooFit.LineWidth(3), ROOT.RooFit.LineStyle(2), ROOT.RooFit.LineColor(ROOT.kGray + 1))

    canvas2 = ROOT.TCanvas("canvas2", "", 600, 600)
    canvas2.SetMargin(0.15, 0.06, 0.13, 0.07)

    frame2.GetYaxis().SetTitleOffset(1.50)
    frame2.GetYaxis().SetTitle("Entries / 0.01 GeV")
    frame2.GetXaxis().SetTitleOffset(1.15)
    frame2.GetXaxis().SetLabelOffset(0.01)
    frame2.GetXaxis().SetTitle("M(#mu#muK) [GeV]")
    frame2.GetXaxis().SetTitleSize(0.043)
    frame2.GetYaxis().SetTitleSize(0.043)
    frame2.Draw()

    leg2 = ROOT.TLegend(0.58, 0.77, 0.93, 0.92)
    leg2.SetFillStyle(0)
    leg2.SetLineWidth(0)
    leg2.SetHeader("Category %d" % cate)
    leg2.AddEntry(frame2.findObject("t_rds_data"), "Data",               "EP")
    leg2.AddEntry(frame2.findObject("t_model"),    "Fit",                "L")
    leg2.AddEntry(frame2.findObject("t_pdf_comb"), "Combinatorial bkg.", "L")
    leg2.Draw()

    canvas2.Print("task_2_4b.pdf")
    canvas2.Print("task_2_4b.png")


if __name__ == "__main__":
    task_2_4()
