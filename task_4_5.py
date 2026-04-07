import ROOT
from common import (effyield, N_Categories,
                    N_bdmmMc, dN_bdmmMc,
                    N_bstohhMcBg, dN_bstohhMcBg,
                    N_bdtohhMcBg, dN_bdtohhMcBg,
                    N_bskmunuMcBg, dN_bskmunuMcBg,
                    N_bdpimunuMcBg, dN_bdpimunuMcBg,
                    N_bdpimumuMcBg, dN_bdpimumuMcBg,
                    N_bupimumuMcBg, dN_bupimumuMcBg,
                    Eff_bsmmMc, dEff_bsmmMc,
                    Eff_bupsikMc, dEff_bupsikMc)

BASE_URL = "root://cmseos.fnal.gov//store/user/cmsdas/2025/long_exercises/long-ex-bs-mumu/"


def build_pdf_peak(wspace, cate, bdt_min):
    ROOT.gROOT.SetBatch(True)

    decay     = []
    yield_    = []
    yield_err = []

    # B0 -> mu mu
    decay.append("bdmmMc");      yield_.append(effyield[cate][N_bdmmMc]);      yield_err.append(effyield[cate][dN_bdmmMc])
    # Bs -> hadron hadron
    decay.append("bstohhMcBg");  yield_.append(effyield[cate][N_bstohhMcBg]);  yield_err.append(effyield[cate][dN_bstohhMcBg])
    # B -> hadron hadron
    decay.append("bdtohhMcBg");  yield_.append(effyield[cate][N_bdtohhMcBg]);  yield_err.append(effyield[cate][dN_bdtohhMcBg])

    m   = ROOT.RooRealVar("m",   "", 4.9, 5.9)
    wgt = ROOT.RooRealVar("wgt", "", 1., 0., 1000.)
    rds = ROOT.RooDataSet("rds", "", ROOT.RooArgSet(m, wgt), "wgt")

    sum_weight     = 0.
    sum_weight_err = 0.
    rds.weightError(ROOT.RooAbsData.SumW2)

    weight_max = 0.
    for proc in range(len(decay)):
        fin = ROOT.TFile(BASE_URL + decay[proc] + ".root")
        tin = fin.Get(decay[proc])
        n_cate = tin.GetEntries("cate==%d" % cate)
        weight = yield_[proc] / float(n_cate)
        if weight > weight_max:
            weight_max = weight
        fin.Close()

    cate_t = ROOT.std.vector('unsigned int')(1)
    m_t    = ROOT.std.vector('float')(1)
    bdt_t  = ROOT.std.vector('float')(1)

    for proc in range(len(decay)):
        fin = ROOT.TFile(BASE_URL + decay[proc] + ".root")
        tin = fin.Get(decay[proc])

        n_cate     = tin.GetEntries("cate==%d" % cate)
        weight     = yield_[proc]    / float(n_cate)
        weight_err = yield_err[proc] / float(n_cate) / weight_max

        print("weight %g weight_err%g" % (weight, weight_err))

        tin.SetBranchAddress("cate", cate_t.data())
        tin.SetBranchAddress("m",    m_t.data())
        tin.SetBranchAddress("bdt",  bdt_t.data())

        for evt in range(tin.GetEntries()):
            tin.GetEntry(evt)
            if cate_t[0] != cate: continue
            if bdt_t[0] <= bdt_min: continue
            m.setVal(m_t[0])
            wgt.setVal(weight / weight_max)
            rds.add(ROOT.RooArgSet(m, wgt), weight / weight_max)

            sum_weight     += weight
            sum_weight_err += weight_err
        fin.Close()

    pdf = ROOT.RooKeysPdf("pdf_peak_%d" % cate, "", m, rds, ROOT.RooKeysPdf.NoMirror, 2.0)

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

    canvas.Print("task_4_5a_%d.pdf" % cate)

    print("Category:", cate)
    print("BDT min:", bdt_min)
    print("Sum of weights: %g +- %g" % (sum_weight, sum_weight_err))

    wspace.Import(pdf)
    wspace.Import(ROOT.RooRealVar("N_peak_%d" % cate, "", sum_weight))


def build_pdf_semi(wspace, cate, bdt_min):
    decay     = []
    yield_    = []
    yield_err = []

    decay.append("bskmunuMcBg");  yield_.append(effyield[cate][N_bskmunuMcBg]);  yield_err.append(effyield[cate][dN_bskmunuMcBg])
    decay.append("bdpimunuMcBg"); yield_.append(effyield[cate][N_bdpimunuMcBg]); yield_err.append(effyield[cate][dN_bdpimunuMcBg])
    decay.append("bdpimumuMcBg"); yield_.append(effyield[cate][N_bdpimumuMcBg]); yield_err.append(effyield[cate][dN_bdpimumuMcBg])
    decay.append("bupimumuMcBg"); yield_.append(effyield[cate][N_bupimumuMcBg]); yield_err.append(effyield[cate][dN_bupimumuMcBg])

    m   = ROOT.RooRealVar("m",   "", 4.9, 5.9)
    wgt = ROOT.RooRealVar("wgt", "", 1., 0., 1000.)
    rds = ROOT.RooDataSet("rds", "", ROOT.RooArgSet(m, wgt), "wgt")

    sum_weight     = 0.
    sum_weight_err = 0.

    cate_t = ROOT.std.vector('unsigned int')(1)
    m_t    = ROOT.std.vector('float')(1)
    bdt_t  = ROOT.std.vector('float')(1)

    for proc in range(len(decay)):
        fin = ROOT.TFile(BASE_URL + decay[proc] + ".root")
        tin = fin.Get(decay[proc])

        n_cate     = tin.GetEntries("cate==%d" % cate)
        weight     = yield_[proc]    / float(n_cate)
        weight_err = yield_err[proc] / float(n_cate)

        tin.SetBranchAddress("cate", cate_t.data())
        tin.SetBranchAddress("m",    m_t.data())
        tin.SetBranchAddress("bdt",  bdt_t.data())

        for evt in range(tin.GetEntries()):
            tin.GetEntry(evt)
            if cate_t[0] != cate: continue
            if bdt_t[0] <= bdt_min: continue
            m.setVal(m_t[0])
            wgt.setVal(weight)
            rds.add(ROOT.RooArgSet(m, wgt), weight)

            sum_weight     += weight
            sum_weight_err += weight_err
        fin.Close()

    pdf = ROOT.RooKeysPdf("pdf_semi_%d" % cate, "", m, rds, ROOT.RooKeysPdf.MirrorLeft, 2.0)

    frame = m.frame(ROOT.RooFit.Title(" "), ROOT.RooFit.Bins(50))
    rds.plotOn(frame, ROOT.RooFit.Name("t_rds"))
    pdf.plotOn(frame, ROOT.RooFit.Name("t_pdf"), ROOT.RooFit.LineWidth(3))

    canvas = ROOT.TCanvas("canvas", "", 600, 600)
    canvas.SetMargin(0.15, 0.06, 0.13, 0.07)

    frame.GetYaxis().SetTitleOffset(1.50)
    frame.GetYaxis().SetTitle("Entries / 0.02 GeV")
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

    canvas.Print("task_4_5b_%d.pdf" % cate)

    print("Category:", cate)
    print("BDT min:", bdt_min)
    print("Sum of weights: %g +- %g" % (sum_weight, sum_weight_err))

    wspace.Import(pdf)
    wspace.Import(ROOT.RooRealVar("N_semi_%d" % cate, "", sum_weight))


def build_pdf_bs(wspace, cate, bdt_min):
    m   = ROOT.RooRealVar("m", "", 4.9, 5.9)
    rds = ROOT.RooDataSet("rds", "", ROOT.RooArgSet(m))

    fin = ROOT.TFile(BASE_URL + "bsmmMc.root")
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

    bs_mean1   = ROOT.RooRealVar("bs_%d_mean1"   % cate, "", 5.37, 5.2, 5.5)
    bs_mean2   = ROOT.RooRealVar("bs_%d_mean2"   % cate, "", 5.37, 5.2, 5.5)
    bs_sigma1  = ROOT.RooRealVar("bs_%d_sigma1"  % cate, "", 0.030, 0.005, 0.060)
    bs_sigma2  = ROOT.RooRealVar("bs_%d_sigma2"  % cate, "", 0.080, 0.040, 0.200)
    bs_cbalpha = ROOT.RooRealVar("bs_%d_cbalpha" % cate, "", 1., 0., 4.)
    bs_cbn     = ROOT.RooRealVar("bs_%d_cbn"     % cate, "", 1., 0., 4.)
    bs_frac    = ROOT.RooRealVar("bs_%d_frac"    % cate, "", 0.7, 0., 1.)
    bs_gaus    = ROOT.RooGaussian("bs_%d_gaus"   % cate, "", m, bs_mean1, bs_sigma1)
    bs_cbline  = ROOT.RooCBShape("bs_%d_cbline"  % cate, "", m, bs_mean2, bs_sigma2, bs_cbalpha, bs_cbn)
    pdf        = ROOT.RooAddPdf("pdf_bs_%d"      % cate, "", ROOT.RooArgList(bs_gaus, bs_cbline), ROOT.RooArgList(bs_frac))
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

    canvas.Print("task_4_5c_%d.pdf" % cate)

    print("Category:", cate)
    print("BDT min:", bdt_min)

    bs_mean1.setConstant(True)
    bs_mean2.setConstant(True)
    bs_sigma1.setConstant(True)
    bs_sigma2.setConstant(True)
    bs_cbalpha.setConstant(True)
    bs_cbn.setConstant(True)
    bs_frac.setConstant(True)
    wspace.Import(pdf)
    wspace.Import(ROOT.RooRealVar("Eff_bs_%d" % cate, "", eff))


def fit_bupsik(wspace, cate, bdt_min):
    m   = ROOT.RooRealVar("m",   "", 5.0, 5.8)
    wgt = ROOT.RooRealVar("wgt", "", 1., 0., 1000.)
    rds_data = ROOT.RooDataSet("rds_data", "", ROOT.RooArgSet(m, wgt), "wgt")
    rds_mc   = ROOT.RooDataSet("rds_mc",   "", ROOT.RooArgSet(m))

    fin = ROOT.TFile(BASE_URL + "bupsikData.root")
    tin = fin.Get("bupsikData")

    cate_t = ROOT.std.vector('unsigned int')(1)
    m_t    = ROOT.std.vector('float')(1)
    wgt_t  = ROOT.std.vector('float')(1)
    bdt_t  = ROOT.std.vector('float')(1)
    tin.SetBranchAddress("cate", cate_t.data())
    tin.SetBranchAddress("wgt",  wgt_t.data())
    tin.SetBranchAddress("m",    m_t.data())

    for evt in range(tin.GetEntries()):
        tin.GetEntry(evt)
        if cate_t[0] != cate: continue
        if m_t[0] < 5.0 or m_t[0] >= 5.8: continue
        m.setVal(m_t[0])
        wgt.setVal(wgt_t[0])
        rds_data.add(ROOT.RooArgSet(m, wgt), wgt_t[0])
    fin.Close()

    fin = ROOT.TFile(BASE_URL + "bupsikMc.root")
    tin = fin.Get("bupsikMc")

    tin.SetBranchAddress("cate", cate_t.data())
    tin.SetBranchAddress("m",    m_t.data())

    evtcount = [0, 0]
    for evt in range(tin.GetEntries()):
        tin.GetEntry(evt)
        if cate_t[0] != cate: continue
        evtcount[0] += 1
        if m_t[0] < 5.0 or m_t[0] >= 5.8: continue
        evtcount[1] += 1
        m.setVal(m_t[0])
        rds_mc.add(ROOT.RooArgSet(m))
    eff       = float(evtcount[1]) / float(evtcount[0]) * effyield[cate][Eff_bupsikMc]
    eff_error = effyield[cate][dEff_bupsikMc] / effyield[cate][Eff_bupsikMc] * eff  # ignore MC statistics error
    fin.Close()

    sigmc_mean1  = ROOT.RooRealVar("sigmc_mean1",  "", 5.28, 5.2, 5.4)
    sigmc_mean2  = ROOT.RooRealVar("sigmc_mean2",  "", 5.28, 5.2, 5.4)
    sigmc_sigma1 = ROOT.RooRealVar("sigmc_sigma1", "", 0.030, 0.005, 0.060)
    sigmc_sigma2 = ROOT.RooRealVar("sigmc_sigma2", "", 0.080, 0.040, 0.200)
    sig_frac     = ROOT.RooRealVar("sig_frac",     "", 0.9, 0.5, 1.0)
    sigmc_g1  = ROOT.RooGaussian("sig_g1",  "", m, sigmc_mean1, sigmc_sigma1)
    sigmc_g2  = ROOT.RooGaussian("sig_g2",  "", m, sigmc_mean2, sigmc_sigma2)
    pdf_sigmc = ROOT.RooAddPdf("pdf_sigmc", "", ROOT.RooArgList(sigmc_g1, sigmc_g2), ROOT.RooArgList(sig_frac))

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
    leg1.AddEntry(frame1.findObject("t_rds_mc"),   "Simluation", "EP")
    leg1.AddEntry(frame1.findObject("t_pdf_sigmc"), "Fit",       "L")
    leg1.Draw()

    canvas1.Print("task_4_5d_%d.pdf" % cate)

    sigmc_mean1.setConstant(True)
    sigmc_mean2.setConstant(True)
    sigmc_sigma1.setConstant(True)
    sigmc_sigma2.setConstant(True)
    sig_frac.setConstant(True)

    sig_shift  = ROOT.RooRealVar("sig_shift", "", 0., -0.02, 0.02)
    sig_scale  = ROOT.RooRealVar("sig_scale", "", 1., 0.8, 1.2)

    sig_mean1  = ROOT.RooAddition("sig_mean1",  "", ROOT.RooArgList(sigmc_mean1, sig_shift))
    sig_mean2  = ROOT.RooAddition("sig_mean2",  "", ROOT.RooArgList(sigmc_mean2, sig_shift))
    sig_sigma1 = ROOT.RooProduct("sig_sigma1",  "", ROOT.RooArgList(sigmc_sigma1, sig_scale))
    sig_sigma2 = ROOT.RooProduct("sig_sigma2",  "", ROOT.RooArgList(sigmc_sigma2, sig_scale))
    sig_g1     = ROOT.RooGaussian("sig_g1",     "", m, sig_mean1, sig_sigma1)
    sig_g2     = ROOT.RooGaussian("sig_g2",     "", m, sig_mean2, sig_sigma2)
    pdf_sig    = ROOT.RooAddPdf("pdf_sig", "", ROOT.RooArgList(sig_g1, sig_g2), ROOT.RooArgList(sig_frac))

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

    model.fitTo(rds_data, ROOT.RooFit.SumW2Error(True))

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

    canvas2.Print("task_4_5e_%d.pdf" % cate)

    print("Category:", cate)
    print("Selection efficiency: %g +- %g" % (eff, eff_error))
    print("Observed yield: %g +- %g" % (n_sig.getVal(), n_sig.getError()))

    wspace.Import(ROOT.RooRealVar("N_bu_%d"   % cate, "", n_sig.getVal()))
    wspace.Import(ROOT.RooRealVar("Eff_bu_%d" % cate, "", eff))


def build_pdf_comb(wspace, cate, bdt_min):
    m = ROOT.RooRealVar("m", "", 4.9, 5.9)

    comb_B1 = ROOT.RooRealVar("comb_B1_%d" % cate, "", 0.5, 0., 1.)
    comb_B2 = ROOT.RooFormulaVar("comb_B2_%d" % cate, "", "1.-@0", ROOT.RooArgList(comb_B1))
    pdf     = ROOT.RooBernstein("pdf_comb_%d" % cate, "", m, ROOT.RooArgList(comb_B1, comb_B2))

    fin = ROOT.TFile(BASE_URL + "bmmData-blind.root")
    tin = fin.Get("bmmData")

    N_comb_guess = float(tin.GetEntries("cate==%d&&bdt>%g&&m>5.45" % (cate, bdt_min)))
    N_comb_guess *= 1.0 / 0.45  # scale to full mass region
    fin.Close()

    print("Category:", cate)
    wspace.Import(pdf)
    wspace.Import(ROOT.RooRealVar("N_comb_%d" % cate, "", N_comb_guess, 0., N_comb_guess * 10.))


def task_4_5():
    wspace = ROOT.RooWorkspace("wspace")

    for cate in range(N_Categories):
        bdt_min = 0.80
        build_pdf_peak(wspace, cate, bdt_min)
        build_pdf_semi(wspace, cate, bdt_min)
        build_pdf_bs(wspace, cate, bdt_min)
        build_pdf_comb(wspace, cate, bdt_min)
        fit_bupsik(wspace, cate, bdt_min)

    wspace.writeToFile("wspace.root")


if __name__ == "__main__":
    task_4_5()
