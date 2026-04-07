import ROOT
from common import (effyield,
                    N_bskmunuMcBg, dN_bskmunuMcBg,
                    N_bdpimunuMcBg, dN_bdpimunuMcBg,
                    N_bdpimumuMcBg, dN_bdpimumuMcBg,
                    N_bupimumuMcBg, dN_bupimumuMcBg)

def task_4_2():
    cate    = 0
    bdt_min = 0.8

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
        fin = ROOT.TFile("root://cmseos.fnal.gov//store/user/cmsdas/2025/long_exercises/long-ex-bs-mumu/" + decay[proc] + ".root")
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

    pdf = ROOT.RooKeysPdf("pdf", "", m, rds, ROOT.RooKeysPdf.MirrorLeft, 2.0)

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

    canvas.Print("task_4_2.pdf")
    canvas.Print("task_4_2.png")

    print("Category:", cate)
    print("BDT min:", bdt_min)
    print("Sum of weights: %g +- %g" % (sum_weight, sum_weight_err))


if __name__ == "__main__":
    task_4_2()
