import ROOT
import math

def task_3_2():
    cate = 2
    pt_min = 20.0
    pt_max = 30.0
    eta_min = 0.
    eta_max = 2.5
    
    m = ROOT.RooRealVar("m", "", 5.0, 5.8)
    wgt = ROOT.RooRealVar("wgt", "", 1., 0., 1000.)
    rds_data = ROOT.RooDataSet("rds_data", "", ROOT.RooArgSet(m, wgt), "wgt")
    rds_mc = ROOT.RooDataSet("rds_mc", "", ROOT.RooArgSet(m))
    
    # --- Process Data Tree ---
    fin_data = ROOT.TFile("root://cmseos.fnal.gov//store/user/cmsdas/2025/long_exercises/long-ex-bs-mumu/bspsiphiData.root")
    tin_data = fin_data.Get("bspsiphiData")
    
    for evt in tin_data:
        if evt.cate != cate: continue
        if evt.m < 5.0 or evt.m >= 5.8: continue
        if evt.pt < pt_min or evt.pt >= pt_max: continue
        if abs(evt.eta) < eta_min or abs(evt.eta) >= eta_max: continue
        
        m.setVal(evt.m)
        wgt.setVal(evt.wgt)
        rds_data.add(ROOT.RooArgSet(m, wgt), evt.wgt)
        
    fin_data.Close()
    
    # --- Process MC Tree ---
    fin_mc = ROOT.TFile("root://cmseos.fnal.gov//store/user/cmsdas/2025/long_exercises/long-ex-bs-mumu/bspsiphiMc.root")
    tin_mc = fin_mc.Get("bspsiphiMc")
    
    evtcount = [0, 0]
    for evt in tin_mc:
        if evt.cate != cate: continue
        evtcount[0] += 1
        if evt.m < 5.0 or evt.m >= 5.8: continue
        if evt.pt < pt_min or evt.pt >= pt_max: continue
        if abs(evt.eta) < eta_min or abs(evt.eta) >= eta_max: continue
        
        evtcount[1] += 1
        m.setVal(evt.m)
        rds_mc.add(ROOT.RooArgSet(m))
        
    eff = float(evtcount[1]) / float(evtcount[0]) if evtcount[0] > 0 else 0.0
    eff_error = math.sqrt(eff * (1. - eff) / float(evtcount[0])) if evtcount[0] > 0 else 0.0
    
    fin_mc.Close()
    
    # --- Fit MC ---
    sigmc_mean1 = ROOT.RooRealVar("sigmc_mean1", "", 5.37, 5.2, 5.5)
    sigmc_mean2 = ROOT.RooRealVar("sigmc_mean2", "", 5.37, 5.2, 5.5)
    sigmc_sigma1 = ROOT.RooRealVar("sigmc_sigma1", "", 0.030, 0.005, 0.060)
    sigmc_sigma2 = ROOT.RooRealVar("sigmc_sigma2", "", 0.080, 0.040, 0.200)
    sig_frac = ROOT.RooRealVar("sig_frac", "", 0.9, 0.5, 1.0)
    
    sigmc_g1 = ROOT.RooGaussian("sig_g1", "", m, sigmc_mean1, sigmc_sigma1)
    sigmc_g2 = ROOT.RooGaussian("sig_g2", "", m, sigmc_mean2, sigmc_sigma2)
    pdf_sigmc = ROOT.RooAddPdf("pdf_sigmc", "", ROOT.RooArgList(sigmc_g1, sigmc_g2), ROOT.RooArgList(sig_frac))
    
    pdf_sigmc.fitTo(rds_mc)
    
    # --- Plot MC ---
    frame1 = m.frame(ROOT.RooFit.Title(" "), ROOT.RooFit.Bins(80))
    rds_mc.plotOn(frame1, ROOT.RooFit.Name("t_rds_mc"))
    pdf_sigmc.plotOn(frame1, ROOT.RooFit.Name("t_pdf_sigmc"), ROOT.RooFit.LineWidth(3))
    
    canvas1 = ROOT.TCanvas("canvas1", "", 600, 600)
    canvas1.SetMargin(0.15, 0.06, 0.13, 0.07)
    
    frame1.GetYaxis().SetTitleOffset(1.50)
    frame1.GetYaxis().SetTitle("Entries / 0.01 GeV")
    frame1.GetXaxis().SetTitleOffset(1.15)
    frame1.GetXaxis().SetLabelOffset(0.01)
    frame1.GetXaxis().SetTitle("M(#mu#muKK) [GeV]")
    frame1.GetXaxis().SetTitleSize(0.043)
    frame1.GetYaxis().SetTitleSize(0.043)
    frame1.Draw()
    
    leg1 = ROOT.TLegend(0.58, 0.77, 0.93, 0.92)
    leg1.SetFillStyle(0)
    leg1.SetLineWidth(0)
    leg1.SetHeader(f"Category {cate}")
    leg1.AddEntry(frame1.findObject("t_rds_mc"), "Simulation", "EP")
    leg1.AddEntry(frame1.findObject("t_pdf_sigmc"), "Fit", "L")
    leg1.Draw()
    
    canvas1.Print("task3_2a.pdf")
    
    # --- Fix parameters and Setup Data Fit ---
    sigmc_mean1.setConstant(True)
    sigmc_mean2.setConstant(True)
    sigmc_sigma1.setConstant(True)
    sigmc_sigma2.setConstant(True)
    sig_frac.setConstant(True)
    
    sig_shift = ROOT.RooRealVar("sig_shift", "", 0., -0.02, 0.02)
    sig_scale = ROOT.RooRealVar("sig_scale", "", 1., 0.8, 1.2)
    
    sig_mean1 = ROOT.RooAddition("sig_mean1", "", ROOT.RooArgList(sigmc_mean1, sig_shift))
    sig_mean2 = ROOT.RooAddition("sig_mean2", "", ROOT.RooArgList(sigmc_mean2, sig_shift))
    sig_sigma1 = ROOT.RooProduct("sig_sigma1", "", ROOT.RooArgList(sigmc_sigma1, sig_scale))
    sig_sigma2 = ROOT.RooProduct("sig_sigma2", "", ROOT.RooArgList(sigmc_sigma2, sig_scale))
    
    sig_g1 = ROOT.RooGaussian("sig_g1", "", m, sig_mean1, sig_sigma1)
    sig_g2 = ROOT.RooGaussian("sig_g2", "", m, sig_mean2, sig_sigma2)
    pdf_sig = ROOT.RooAddPdf("pdf_sig", "", ROOT.RooArgList(sig_g1, sig_g2), ROOT.RooArgList(sig_frac))
    
    comb_coeff = ROOT.RooRealVar("comb_coeff", "", -1.2, -10., 10.)
    pdf_comb = ROOT.RooExponential("pdf_comb", "", m, comb_coeff)
    
    n_comb_guess = rds_data.sumEntries("m>5.46||m<5.26") * 0.8 / 0.6
    n_sig_guess = rds_data.sumEntries("m>5.26&&m<5.46") - n_comb_guess / 4.
    
    n_sig = ROOT.RooRealVar("n_sig", "", n_sig_guess, 0., rds_data.sumEntries())
    n_comb = ROOT.RooRealVar("n_comb", "", n_comb_guess, 0., rds_data.sumEntries())
    model = ROOT.RooAddPdf("model", "", ROOT.RooArgList(pdf_sig, pdf_comb), ROOT.RooArgList(n_sig, n_comb))
    
    model.fitTo(rds_data, ROOT.RooFit.SumW2Error(True))
    
    # --- Plot Data ---
    frame2 = m.frame(ROOT.RooFit.Title(" "), ROOT.RooFit.Bins(80))
    rds_data.plotOn(frame2, ROOT.RooFit.Name("t_rds_data"))
    model.plotOn(frame2, ROOT.RooFit.Name("t_model"), ROOT.RooFit.LineWidth(3))
    model.plotOn(frame2, ROOT.RooFit.Name("t_pdf_comb"), ROOT.RooFit.Components("pdf_comb"), 
                 ROOT.RooFit.LineWidth(3), ROOT.RooFit.LineStyle(2), ROOT.RooFit.LineColor(ROOT.kGray+1))
    
    canvas2 = ROOT.TCanvas("canvas2", "", 600, 600)
    canvas2.SetMargin(0.15, 0.06, 0.13, 0.07)
    
    frame2.GetYaxis().SetTitleOffset(1.50)
    frame2.GetYaxis().SetTitle("Entries / 0.01 GeV")
    frame2.GetXaxis().SetTitleOffset(1.15)
    frame2.GetXaxis().SetLabelOffset(0.01)
    frame2.GetXaxis().SetTitle("M(#mu#muKK) [GeV]")
    frame2.GetXaxis().SetTitleSize(0.043)
    frame2.GetYaxis().SetTitleSize(0.043)
    frame2.Draw()
    
    leg2 = ROOT.TLegend(0.58, 0.77, 0.93, 0.92)
    leg2.SetFillStyle(0)
    leg2.SetLineWidth(0)
    leg2.SetHeader(f"Category {cate}")
    leg2.AddEntry(frame2.findObject("t_rds_data"), "Data", "EP")
    leg2.AddEntry(frame2.findObject("t_model"), "Fit", "L")
    leg2.AddEntry(frame2.findObject("t_pdf_comb"), "Combinatorial bkg.", "L")
    leg2.Draw()
    
    canvas2.Print("task3_2b.pdf")
    
    print(f"Category: {cate}")
    print(f"pt range: {pt_min}, {pt_max}")
    print(f"|eta| range: {eta_min}, {eta_max}")
    print(f"Selection efficiency: {eff} +- {eff_error}")
    print(f"Observed yield: {n_sig.getVal()} +- {n_sig.getError()}")

if __name__ == "__main__":
    task_3_2()