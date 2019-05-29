#!/usr/bin/env python
import sys
import re
import os

ODIR=sys.argv[1]

#dowhat = "plots" 
#dowhat = "dumps" 
#dowhat = "yields" 
dowhat = "ntuple" # syntax: python ttH-multilepton/ttH_plots.py no 2lss_SR_extr outfile_{cname}.root --sP var1,var2,...

P0="/pool/cienciasrw/userstorage/sscruz/NanoAOD/"
if 'cmsco01'   in os.environ['HOSTNAME']: P0="/data/peruzzi"
if 'cmsphys10' in os.environ['HOSTNAME']: P0="/data1/g/gpetrucc"
if 'ucl.ac.be' in os.environ['HOSTNAME']: P0="/nfs/user/pvischia/tth/"
TREES = ""

#TREESONLYSKIM = "-P "+P0+"/NanoAODtest_v2 --Fs {P}/1_recleaner --Fs {P}/2_TauTightFlag --Fs {P}/3_triggerResult  --Fs {P}/4_eventVars "
#TREESONLYSKIM = "-P "+P0+"/ttH_EasterProduction/ --Fs {P}/1_triggerDecision --Fs {P}/2_countJets --Fs {P}/3_lepVars --FMCs {P}/4_bweight_new --Fs {P}/5_MET --Fs {P}/5_taus " 
TREESONLYSKIM = "-P "+P0+"/ttH_EasterProduction_2lss_3l/ --Fs {P}/1_triggerDecision --Fs {P}/2_countJets --Fs {P}/3_lepVars --FMCs {P}/4_bweight_new --Fs {P}/5_MET --Fs {P}/5_taus --Fs {P}/6_eventVars " 

TREESONLYSKIM  = "-P "+P0+"/synch_2016/ --Fs {P}/1_tight --Fs {P}/2_synch --Fs {P}/3_trigger --Fs {P}/4_mass "
TREESONLYFULL = TREESONLYSKIM

def base(selection, year):

    CORE=' '.join([TREES,TREESONLYSKIM])
    if   year == '2016': lumi = 35.9
    elif year == '2017': lumi = 41.4
    elif year == '2018': lumi = 59.7
    CORE+=" -f -j 88 -l {lumi} --s2v -L ttH-multilepton/functionsTTH.cc --tree nanoAODskim --mcc ttH-multilepton/lepchoice-ttH-FO.txt --split-factor=-1  ".format(lumi=lumi)# --neg"
    RATIO= " --maxRatioRange 0.0  1.99 --ratioYNDiv 505 "
    RATIO2=" --showRatio --attachRatioPanel --fixRatioRange "
    LEGEND=" --legendColumns 2 --legendWidth 0.25 "
    LEGEND2=" --legendFontSize 0.042 "
    SPAM=" --noCms --topSpamSize 1.1 --lspam '#scale[1.1]{#bf{CMS}} #scale[0.9]{#it{Preliminary}}' "
    if dowhat == "plots": CORE+=RATIO+RATIO2+LEGEND+LEGEND2+SPAM+"  --showMCError --rebin 4 --xP 'nT_.*' --xP 'debug_.*'"

    if selection=='2lss':
        GO="{CORE} ttH-multilepton/mca-2lss-mc-{year}.txt ttH-multilepton/2lss_tight.txt ".format(year=year,CORE=CORE)
        if dowhat != 'ntuple': GO="%s -W 'puWeight*leptonSF_ttH(LepFO_pdgId[0],LepFO_pt[0],LepFO_eta[0],2,year)*leptonSF_ttH(LepFO_pdgId[1],LepFO_pt[1],LepFO_eta[1],2,year)*triggerSF_ttH(LepFO_pdgId[0],LepFO_pt[0],LepFO_pdgId[1],LepFO_pt[1],nLepFO_isTight,year,0)'"%GO
        if dowhat in ["plots","ntuple"]: GO+=" ttH-multilepton/2lss_3l_plots.txt --xP '^lep(3|4)_.*' --xP '^(3|4)lep_.*' --xP 'kinMVA_3l_.*' "
        if dowhat == "plots": GO=GO.replace(LEGEND, " --legendColumns 3 --legendWidth 0.52 ")
        if dowhat == "plots": GO=GO.replace(RATIO,  " --maxRatioRange 0.6  1.99 --ratioYNDiv 210 ")
        GO += " --binname 2lss "
    elif selection=='3l':
        GO="{CORE} ttH-multilepton/mca-3l-mc-{year}.txt ttH-multilepton/3l_tight.txt ".format(year=year,CORE=CORE)
        if dowhat != 'ntuple': GO="%s -W 'puWeight*eventBTagSF*leptonSF_ttH(LepFO_pdgId[0],LepFO_pt[0],LepFO_eta[0],3,year)*leptonSF_ttH(LepFO_pdgId[1],LepFO_pt[1],LepFO_eta[1],3,year)*leptonSF_ttH(LepFO_pdgId[2],LepFO_pt[2],LepFO_eta[2],3,year)*triggerSF_ttH(LepFO_pdgId[0],LepFO_pt[0],LepFO_pdgId[1],LepFO_pt[1],nLepFO_isTight,year,0)'"%GO
        if dowhat in ["plots","ntuple"]: GO+=" ttH-multilepton/2lss_3l_plots.txt --xP '^(2|4)lep_.*' --xP '^lep4_.*' --xP 'kinMVA_2lss_.*' "
        if dowhat == "plots": GO=GO.replace(LEGEND, " --legendColumns 3 --legendWidth 0.42 ")
        GO += " --binname 3l "
    elif selection=='4l':
        GO="%s ttH-multilepton/mca-4l-mc.txt ttH-multilepton/4l_tight.txt "%CORE
        if dowhat != 'ntuple': GO="%s -W 'puWeight*eventBTagSF*leptonSF_ttH(LepFO_pdgId[0],LepFO_pt[0],LepFO_eta[0],3,year)*leptonSF_ttH(LepFO_pdgId[1],LepFO_pt[1],LepFO_eta[1],3,year)*leptonSF_ttH(LepFO_pdgId[2],LepFO_pt[2],LepFO_eta[2],3,year)*leptonSF_ttH(LepFO_pdgId[3],LepFO_pt[3],LepFO_eta[3],3,year)*triggerSF_ttH(LepFO_pdgId[0],LepFO_pt[0],LepFO_pdgId[1],LepFO_pt[1],nLepFO_isTight,year,0)'"%GO
        if dowhat in ["plots","ntuple"]: GO+=" ttH-multilepton/2lss_3l_plots.txt --xP '^(2|3)lep_.*' --xP '^lep(1|2|3|4)_.*' --xP 'kinMVA_.*' "
        if dowhat == "plots": GO=GO.replace(LEGEND, " --legendColumns 2 --legendWidth 0.3 ")
        if dowhat == "plots": GO=GO.replace(RATIO,  " --maxRatioRange 0.0  2.99 --ratioYNDiv 505 ")
        GO += " --binname 4l "
    else:
        raise RuntimeError, 'Unknown selection'

    if '_prescale' in torun:
        GO = doprescale3l(GO,torun)

    return GO

def promptsub(x):
    procs = [ '' ]
    if dowhat == "cards": procs += ['_FRe_norm_Up','_FRe_norm_Dn','_FRe_pt_Up','_FRe_pt_Dn','_FRe_be_Up','_FRe_be_Dn','_FRm_norm_Up','_FRm_norm_Dn','_FRm_pt_Up','_FRm_pt_Dn','_FRm_be_Up','_FRm_be_Dn']
    return x + ' '.join(["--plotgroup data_fakes%s+='.*_promptsub%s'"%(x,x) for x in procs])+" --neglist '.*_promptsub.*' "
def procs(GO,mylist):
    return GO+' '+" ".join([ '-p %s'%l for l in mylist ])
def sigprocs(GO,mylist):
    return procs(GO,mylist)+' --showIndivSigs --noStackSig'
def runIt(GO,name,plots=[],noplots=[]):
    if '_74vs76' in name: GO = prep74vs76(GO)
    if dowhat == "plots":  
        if not ('forcePlotChoice' in sys.argv[3:]): print 'python mcPlots.py',"--pdir %s/%s"%(ODIR,name),GO,' '.join(['--sP %s'%p for p in plots]),' '.join(['--xP %s'%p for p in noplots]),' '.join(sys.argv[3:])
        else: print 'python mcPlots.py',"--pdir %s/%s"%(ODIR,name),GO,' '.join([x for x in sys.argv[3:] if x!='forcePlotChoice'])
    elif dowhat == "yields": print 'echo %s; python mcAnalysis.py'%name,GO,' '.join(sys.argv[3:])
    elif dowhat == "dumps":  print 'echo %s; python mcDump.py'%name,GO,' '.join(sys.argv[3:])
    elif dowhat == "ntuple": print 'echo %s; python mcNtuple.py'%name,GO,' '.join(sys.argv[3:])
def add(GO,opt):
    return '%s %s'%(GO,opt)
def setwide(x):
    x2 = add(x,'--wide')
    x2 = x2.replace('--legendWidth 0.35','--legendWidth 0.20')
    return x2
def fulltrees(x):
    return x.replace(TREESONLYSKIM,TREESONLYFULL)
def doprescale3l(x,torun):
    return x.replace(TREESONLYSKIM,TREESONLYMEMZPEAK if any([(_y in torun) for _y in ['cr_wz','cr_ttz','cr_fourlep_onZ','_Zpeak']]) else TREESONLYMEMZVETO)

allow_unblinding = True

if __name__ == '__main__':

    torun = sys.argv[2]
    
    if '2016' in torun: year='2016'
    if '2017' in torun: year='2017'
    if '2018' in torun: year='2018'

    if (not allow_unblinding) and '_data' in torun and (not any([re.match(x.strip()+'$',torun) for x in ['.*_appl.*','cr_.*','3l.*_Zpeak.*']])): raise RuntimeError, 'You are trying to unblind!'

    if '2lss_' in torun:
        x = base('2lss',year)
        if '_appl' in torun: x = add(x,'-I ^TT ')
        if '_flip' in torun: x = add(x,'-I ^same-sign')
        if '_1fo' in torun:
            x = add(x,"-A alwaystrue 1FO 'LepFO_isTight[0]+LepGood_isTight[1]==1'")
            x = x.replace("--xP 'nT_.*'","")
        if '_2fo' in torun: x = add(x,"-A alwaystrue 2FO 'LepFO_isTight[0]+LepFO_isTight[1]==0'")
        if '_relax' in torun: x = add(x,'-X ^TT ')
        if '_extr' in torun:
            x = x.replace('mca-2lss-mc-{year}.txt'.format(year=year),'mca-2lss-mc-sigextr.txt').replace('--showRatio --maxRatioRange 0 2','--showRatio --maxRatioRange 0 1 --ratioYLabel "S/B"')
        if '_data' in torun: x = x.replace('mca-2lss-mc.txt','mca-2lss-mcdata.txt')
        if '_table' in torun:
            x = x.replace('mca-2lss-mc.txt','mca-2lss-mc-table.txt')
        if '_frdata' in torun:
            x = promptsub(x)
            if '_blinddata' in torun:
                x = x.replace('mca-2lss-mc.txt','mca-2lss-mcdata.txt')
                x = add(x,'--xp data')
            elif not '_data' in torun: raise RuntimeError
            x = x.replace('mca-2lss-mcdata.txt','mca-2lss-mcdata-frdata.txt')
            if '_table' in torun:
                x = x.replace('mca-2lss-mcdata-frdata.txt','mca-2lss-mcdata-frdata-table.txt')

        if '_mll200' in torun:
            x = add(x,"-E ^mll200 ")

        if '_synch' in torun:
            x = x.replace('ttH-multilepton/2lss_3l_plots.txt','ttH-multilepton/synchTuple.txt')
            x = x.replace('ttH-multilepton/mca-2lss-mc-sigextr.txt','ttH-multilepton/mca-synch.txt')



        if '_splitfakes' in torun:
            x = x.replace('mca-2lss-mc.txt','mca-2lss-mc-flavsplit.txt')
            
        if '_closuretest' in torun:
            x = x.replace('mca-2lss-mc.txt','mca-2lss-mc-closuretest.txt')
            x = x.replace("--maxRatioRange 0.6  1.99 --ratioYNDiv 210", "--maxRatioRange 0.0 1.99 --fixRatioRange ")
            x = x.replace("--legendColumns 3", "--legendColumns 2")
            x = add(x,"--AP --plotmode nostack --sP 2lep_catIndex_nosign --sP 2lep_catIndex --sP kinMVA_2lss_ttbar --sP kinMVA_2lss_ttV --sP nBJetCentralMedium25 --sP 2lep_nJet25_from4")
            x = add(x,"-p TT_FR_QCD -p TT_FR_TT -p TT_fake --ratioDen TT_FR_QCD --ratioNums TT_fake,TT_FR_TT --errors ")
            if '_closuretest_norm' in torun:
                x = x.replace("--plotmode nostack","--plotmode norm")
                x = x.replace("--ratioNums TT_fake,TT_FR_TT","--ratioNums TT_fake")
                x = add(x,"--fitRatio 1")
                if '_unc' in torun:
                    x = add(x,"--su CMS_ttHl16_Clos_[em]_norm")
            else:
                if '_uncfull' in torun:
                    x = add(x,"--su 'CMS_ttHl16_FR.*' ")
                elif '_unc' in torun:
                    x = add(x,"--su 'CMS_ttHl16_Clos_[em].*_norm' ")
            if '_mufake' in torun: x = add(x,"-A alwaystrue mufake '(abs(LepFO_pdgId[0])==13 && LepFO_mcMatchId[0]==0) || (abs(LepFO_pdgId[1])==13 && LepFO_mcMatchId[1]==0)'")
            if '_elfake' in torun: x = add(x,"-A alwaystrue elfake '(abs(LepFO_pdgId[0])==11 && LepFO_mcMatchId[0]==0) || (abs(LepFO_pdgId[1])==11 && LepFO_mcMatchId[1]==0)'")
            if '_bloose' in torun: x = add(x,'-E ^BLoose ')
            if '_btight' in torun: x = add(x,'-E ^BTight ')
            if '_nobcut' in torun: x = add(x,'-X ^2b1B ')
            if '_notrigger' in torun: x = add(x,'-X ^trigger ' )

        if '_unc' in torun:
            x = add(x,"--unc ttH-multilepton/systsUnc.txt")

        if '_varsFR' in torun:
            x = x.replace('mca-2lss-mc.txt','mca-2lss-data-frdata-vars.txt')
            x = add(x,"--plotmode nostack --xP '.*Binning' --sP 'kinMVA_.*' --sP 2lep_catIndex")
            x = add(x,"--ratioDen data_fakes --ratioNums 'data_fakes_.*'")
            if '_norm' in torun:
                x = x.replace("--plotmode nostack","--plotmode norm")
            if '_fit' in torun:
                x = add(x,"--fitRatio 1")
            if '_varsFR_e' in torun: x = add(x,"--xp 'data_fakes_m_.*'")
            if '_varsFR_m' in torun: x = add(x,"--xp 'data_fakes_e_.*'")

        if '_Xh' in torun:
            x = x.replace('4_BDTv8_Hj_230217_v6','4_BDTv8_Hj_Xmass_bkg')
            x = x.replace('mca-2lss-mc.txt','mca-2lss-mc-sigextr-Xh.txt').replace('--showRatio','')
            x = x.replace('--legendColumns 3 --legendWidth 0.46','--legendWidth 0.30')
            x = x.replace('--showMCError','')
            x = add(x,'--plotmode norm')
            x = add(x,"--sP kinMVA_input_BDTv8_eventReco_X_mass --sP kinMVA_2lss_ttbar_withBDTv8 --sP kinMVA_input_BDTv8_eventReco_MT_HadLepTop_MET")

        runIt(x,'%s'%torun)
        if '_flav' in torun:
            for flav in ['mm','ee','em']: 
                runIt(add(x,'-E ^%s'%flav).replace("--binname 2lss","--binname 2lss_"+flav),'%s/%s'%(torun,flav))
        if '_catnosign' in torun:
            for flav in ['mm','ee','em']: 
                runIt(add(x,'-E ^%s'%flav).replace("--binname 2lss","--binname 2lss_"+flav),'%s/%s'%(torun,flav))
            for flav in ['mm_bt','mm_bl','em_bt','em_bl']: 
                runIt(add(x,'-E ^%s -E ^B%s'%(flav[:2], ("Tight" if "bt" in flav else "Loose"))).replace("--binname 2lss","--binname 2lss_"+flav),'%s/%s'%(torun,flav))
            for flav in ['btight','bloose']: 
                runIt(add(x,' -E ^B%s'%("Tight" if "bt" in flav else "Loose")),'%s/%s'%(torun,flav))
        if '_cats' in torun:
            for cat in ['b2lss_ee_neg','b2lss_ee_pos',\
                            'b2lss_em_bl_neg','b2lss_em_bl_pos','b2lss_em_bt_neg','b2lss_em_bt_pos',\
                            'b2lss_mm_bl_neg','b2lss_mm_bl_pos','b2lss_mm_bt_neg','b2lss_mm_bt_pos']:
                runIt(add(x,'-E ^%s'%cat).replace("--binname 2lss","--binname %s" % cat[1:-4]),'%s/%s'%(torun,cat))


    if '3l_' in torun:
        x = base('3l',year)
        if '_appl' in torun: x = add(x,'-I ^TTT ')
        if '_synch' in torun: 
            x = x.replace('ttH-multilepton/2lss_3l_plots.txt','ttH-multilepton/synchTuple.txt')
            x = x.replace('ttH-multilepton/mca-3l-mc-{year}.txt'.format(year=year),'ttH-multilepton/mca-synch-3l.txt' )

        if '_1fo' in torun:
            x = add(x,"-A alwaystrue 1FO 'LepFO_isTight[0]+LepFO_isTight[1]+LepFO_isTight[2]==2'")
            x = x.replace("--xP 'nT_.*'","")
        if '_relax' in torun: x = add(x,'-X ^TTT ')
        if '_extr' in torun:
            x = x.replace('mca-3l-mc-{year}.txt'.format(year=year),'mca-3l-mc-sigextr.txt').replace('--showRatio --maxRatioRange 0 2','--showRatio --maxRatioRange 0 1 --ratioYLabel "S/B"')
        if '_data' in torun: x = x.replace('mca-3l-mc.txt','mca-3l-mcdata.txt')
        if '_frdata' in torun:
            x = promptsub(x)
            if '_blinddata' in torun:
                x = x.replace('mca-3l-mc.txt','mca-3l-mcdata.txt')
                x = add(x,'--xp data')
            elif not '_data' in torun: raise RuntimeError
            x = x.replace('mca-3l-mcdata.txt','mca-3l-mcdata-frdata.txt')
            if '_table' in torun:
                x = x.replace('mca-3l-mcdata-frdata.txt','mca-3l-mcdata-frdata-table.txt')
        if '_table' in torun:
            x = x.replace('mca-3l-mc.txt','mca-3l-mc-table.txt')

        if '_closuretest' in torun:
            x = x.replace('mca-3l-mc.txt','mca-3l-mc-closuretest.txt')
            #x = x.replace("--maxRatioRange 0 3","--maxRatioRange 0.5 1.5")
            x = add(x,"--AP --plotmode nostack --sP kinMVA_3l_ttbar --sP kinMVA_3l_ttV --sP --sP 3lep_catIndex --sP nBJetCentralMedium25 --sP 3lep_nJet25 --sP 3lep_n_ele")
            x = add(x,"-p TT_FR_QCD -p TT_FR_TT -p TT_fake --ratioDen TT_FR_QCD --ratioNums TT_fake,TT_FR_TT --errors ")
            x = x.replace('--showMCError','')
            x = x.replace('--legendWidth 0.42','--legendWidth 0.60')
            if '_closuretest_norm' in torun:
                x = x.replace("--plotmode nostack","--plotmode norm")
                x = x.replace("--ratioNums TT_fake,TT_FR_TT","--ratioNums TT_fake")
                x = add(x,"--fitRatio 1")
                if '_unc' in torun:
                    x = add(x,"--su CMS_ttHl16_Clos_[em]_norm")
            else:
                if '_uncfull' in torun:
                    x = add(x,"--su 'CMS_ttHl16_FR.*' ")
                elif '_unc' in torun:
                    x = add(x,"--su 'CMS_ttHl16_Clos_[em].*_norm' ")
            if '_mufake' in torun: x = add(x,"-A alwaystrue mufake '(abs(LepFO_pdgId[0])==13 && LepFO_mcMatchId[0]==0) || (abs(LepFO_pdgId[1])==13 && LepFO_mcMatchId[1]==0) || (abs(LepFO_pdgId[2])==13 && LepFO_mcMatchId[2]==0)'")
            if '_elfake' in torun: x = add(x,"-A alwaystrue elfake '(abs(LepFO_pdgId[0])==11 && LepFO_mcMatchId[0]==0) || (abs(LepFO_pdgId[1])==11 && LepFO_mcMatchId[1]==0) || (abs(LepFO_pdgId[2])==11 && LepFO_mcMatchId[2]==0)'")
            if '_bloose' in torun: x = add(x,'-E ^BLoose ')
            if '_btight' in torun: x = add(x,'-E ^BTight ')
            if '_nobcut' in torun: x = add(x,'-X ^2b1B ')
            if '_notrigger' in torun: x = add(x,'-X ^trigger ')

        if '_unc' in torun:
            x = add(x,"--unc ttH-multilepton/systsUnc.txt")

        if '_varsFR' in torun:
            torun += "_"+sys.argv[-1]
            x = x.replace('mca-3l-mc.txt','mca-3l-data-frdata-%s.txt'%sys.argv[-1])
            x = x.replace("--maxRatioRange 0 3","--maxRatioRange 0 2")
            x = add(x,"--plotmode nostack --sP kinMVA_3l_ttbar --sP kinMVA_3l_ttV_withMEM --sP kinMVA_3l_ttV")
            x = add(x,"--ratioDen fakes_data --ratioNums fakes_data_%s --errors"%sys.argv[-1])
            if '_varsFR_norm' in torun:
                x = x.replace("--plotmode nostack","--plotmode norm")
                x = add(x,"--fitRatio 1")
        if '_x2j' in torun:
            x = add(x,"-E ^x2j ")
        if '_Zpeak' in torun:
            x = add(x,'-I ^Zveto')
        runIt(x,'%s'%torun)
        if '_cats' in torun:
            for cat in ['b3l_bl_neg','b3l_bl_pos','b3l_bt_neg','b3l_bt_pos']:
                runIt(add(x,'-E ^%s'%cat).replace("--binname 3l","--binname %s" % cat[1:-4]),'%s/%s'%(torun,cat))
        if '_catnosign' in torun:
            for flav in ['btight','bloose']: 
                runIt(add(x,' -E ^B%s'%("Tight" if "bt" in flav else "Loose")).replace("--binname 3l","--binname 3l_%s" % flav[:2]),'%s/%s'%(torun,flav))


    if '4l_' in torun:
        x = base('4l')
        if '_appl' in torun: x = add(x,'-I ^TTTT ')
        if '_relax' in torun: x = add(x,'-X ^TTTT ')
        if '_data' in torun: x = x.replace('mca-4l-mc.txt','mca-4l-mcdata.txt')
        if '_extr' in torun: x = x.replace('mca-4l-mc.txt','mca-4l-mc-sigextr.txt')
        if '_synch' in torun: 
            x = x.replace('ttH-multilepton/2lss_3l_plots.txt','ttH-multilepton/synchTuple.txt')
            x = add(x, ' --Fs {P}/8_synch')

        if '_frdata' in torun:
            x = promptsub(x)
            raise RuntimeError, 'Fakes estimation not implemented for 4l'
        if '_unc' in torun:
            x = add(x,"--unc ttH-multilepton/systsUnc.txt")
        runIt(x,'%s'%torun)

    if 'cr_3j' in torun:
        x = base('2lss',year)
        if '_data' in torun: x = x.replace('mca-2lss-mc-{year}.txt'.format(year=year),'mca-2lss-mcdata-{year}.txt'.format(year=year))
        if '_appl' in torun: x = add(x,'-I ^TT ')
        if '_relax' in torun: x = add(x,'-X ^TT ')
        if '_flip' in torun: x = add(x,'-I ^same-sign')
        if '_synch' in torun: 
            x = x.replace('ttH-multilepton/2lss_3l_plots.txt','ttH-multilepton/synchTuple.txt')
            x = add(x, ' --Fs {P}/8_synch')
        if '_extr' in torun:
            x = x.replace('mca-2lss-mc.txt','mca-2lss-mc-sigextr.txt').replace('--showRatio --maxRatioRange 0 2','--showRatio --maxRatioRange 0 1 --ratioYLabel "S/B"')

        if '_frdata' in torun:
            x = promptsub(x)
            if not '_data' in torun: raise RuntimeError
            x = x.replace('mca-2lss-mcdata.txt','mca-2lss-mcdata-frdata.txt')
        x = add(x,"-R ^4j 3j 'nJetCentral25==3'")
        if '_unc' in torun:
            x = add(x,"--unc ttH-multilepton/systsUnc.txt")

        plots = ['2lep_.*','nJet25','nBJetLoose25','nBJetCentralMedium25','met','metLD','htJet25j','mhtJet25','mtWmin','htllv','kinMVA_2lss_ttbar.*','kinMVA_2lss_ttV.*','kinMVA_2lss_bins7','kinMVA_input.*','era']
        runIt(x,'%s'%torun,plots)
        if '_flav' in torun:
            for flav in ['mm','ee','em']:
                runIt(add(x,'-E ^%s'%flav).replace("--binname 2lss","--binname 2lss_"+flav),'%s/%s'%(torun,flav))

    if 'cr_ttbar' in torun:
        x = base('2lss',year)
        x = fulltrees(x) # for mc same-sign

        x = x.replace('mca-2lss-mc.txt','mca-2lss-mcdata-ttbar-{year}.txt'.format(year=year))
        if '_data' not in torun: x = add(x,'--xp data')
        if '_appl' in torun: x = add(x,'-I ^TT ')
        if '_1fo' in torun: x = add(x,"-A alwaystrue 1FO 'LepFO_isTight[0]+LepFO_isTight[0]==1'")
        if '_leadmupt25' in torun: x = add(x,"-A 'entry point' leadmupt25 'abs(LepFO_pdgId[0])==13 && LepFO_pt[0]>25'")
        if '_norm' in torun:
            x = add(x,"--sp '.*' --scaleSigToData")
        x = add(x,"-I same-sign -X ^4j -X ^2b1B -E ^2j -E ^em ")
        if '_highMetNoBCut' in torun: x = add(x,"-A 'entry point' highMET 'met_pt>60'")
        else: x = add(x,"-E ^1B ")
        if '_unc' in torun:
            x = add(x,"--unc ttH-multilepton/systsUnc.txt")
        plots = ['2lep_.*','met','metLD','nVert','nJet25','nBJetCentralMedium25','nBJetLoose25','nBJetLoose40','nBJetMedium40','era']
        runIt(x,'%s'%torun)#,plots)


    if 'cr_ttbar' in torun:
        x = base('2lss',year)
        x = fulltrees(x) # for mc same-sign

        x = x.replace('mca-2lss-mc.txt','mca-2lss-mcdata-ttbar-{year}.txt'.format(year=year))
        if '_data' not in torun: x = add(x,'--xp data')
        if '_appl' in torun: x = add(x,'-I ^TT ')
        if '_1fo' in torun: x = add(x,"-A alwaystrue 1FO 'LepFO_isTight[0]+LepFO_isTight[0]==1'")
        if '_leadmupt25' in torun: x = add(x,"-A 'entry point' leadmupt25 'abs(LepFO_pdgId[0])==13 && LepFO_pt[0]>25'")
        if '_norm' in torun:
            x = add(x,"--sp '.*' --scaleSigToData")
        x = add(x,"-I same-sign -X ^4j -X ^2b1B -E ^2j -E ^em ")
        if '_highMetNoBCut' in torun: x = add(x,"-A 'entry point' highMET 'met_pt>60'")
        else: x = add(x,"-E ^1B ")
        if '_unc' in torun:
            x = add(x,"--unc ttH-multilepton/systsUnc.txt")
        plots = ['2lep_.*','met','metLD','nVert','nJet25','nBJetCentralMedium25','nBJetLoose25','nBJetLoose40','nBJetMedium40','era']
        runIt(x,'%s'%torun)#,plots)

    if 'cr_dileptonic' in torun:
        x = base('2lss',year)
        x = x.replace('mca-2lss-mc-{year}.txt'.format(year=year),'mca-2lss-mcdata-ttbar-{year}.txt'.format(year=year))
        x = x.replace('--maxRatioRange 0.6  1.99','--maxRatioRange 0.6 1.4')
        x = x.replace('--rebin 4',' ')
        if '_data' not in torun: x = add(x,'--xp data')
        x = add(x,"-I same-sign -X Zee_veto -X metLDee -X 4j -X 2b1B -X tauveto ")
        if '_norm' in torun: x = add(x, ' --scaleBkgToData TT2L --scaleBkgToData DY  --scaleBkgToData SingleTop --scaleBkgToData WW ')
        if '_unc' in torun:
            x = add(x,"--unc ttH-multilepton/systsUnc.txt")
        for flav in ['em','mm','ee']:
            plots =   ['mZ1','nVert','nJet.*_from0', 'tot_weight','lep1_.*', 'lep2_.*','nBJet.*','met','nJnB_Central25Medium'] # 'jet1_.*','jet2_.*','jet3_.*','jet4_.*', ]
            runIt(add(x,'-E ^%s '%flav),'%s/%s'%(torun,flav),plots)

    if 'cr_wz' in torun:
        x = base('3l',year)
        if '_appl' in torun: x = add(x,'-I ^TTT ')
        if '_synch' in torun:
            x = x.replace('ttH-multilepton/2lss_3l_plots.txt','ttH-multilepton/synchTuple.txt')
            x = add(x, ' --Fs {P}/8_synch')
        if '_extr' in torun:
            x = x.replace('mca-3l-mc.txt','mca-3l-mc-sigextr.txt').replace('--showRatio --maxRatioRange 0 2','--showRatio --maxRatioRange 0 1 --ratioYLabel "S/B"')
        if '_relax' in torun: x = add(x,'-X ^TTT ')

        x = x.replace("--binname 3l","--binname 3l_crwz")
        x = add(x,"-I 'Zveto' -I ^2b1B ")
        #x = add(x, " --Fs {P}/7_bestMTW3l_v1 ")
        if '_data' in torun: x = x.replace('mca-3l-mc.txt','mca-3l-mcdata.txt')
        if '_frdata' in torun:
            x = promptsub(x)
            if not '_data' in torun: raise RuntimeError
            x = x.replace('mca-3l-mcdata.txt','mca-3l-mcdata-frdata.txt')
        else: 
            print "ERROR: cr_wz with MC backgrounds does not work."
        if '_unc' in torun:
            x = add(x,"--unc ttH-multilepton/systsUnc.txt")
        if '_fit' in torun:
            if not '_data' in torun: raise RuntimeError
            x = add(x,"--sP tot_weight --preFitData tot_weight --sp WZ ")
            x = add(x,"--xu CMS_ttHl_ZZ_lnU ") # otherwise here we fit as ZZ
            if '_unc' not in torun:
                print "Will just float WZ freely"
                x = add(x,"--flp WZ")
        plots = ['3lep_mtW','3lep_nJet25','tot_weight','met','metLD','htJet25j','nBJetLoose25']
        if '_more' in torun:
            plots += ['lep3_pt','metLD','nBJetLoose25','3lep_worseIso','minMllAFAS','3lep_worseMVA','3lep_mtW','kinMVA.*','htJet25j','nJet25','era']
            plots += ['3lep_.*','nJet25','nBJetLoose25','nBJetCentralMedium25','met','metLD','htJet25j','mhtJet25','mtWmin','htllv','kinMVA_3l_ttbar','kinMVA_3l_ttV','kinMVA_3l_ttV_withMEM']
        runIt(x,'%s'%torun,plots)

    if 'cr_ttz' in torun:
        x = base('3l')
        if '_appl' in torun: x = add(x,'-I ^TTT ')

        if '_synch' in torun:
            x = x.replace('ttH-multilepton/2lss_3l_plots.txt','ttH-multilepton/synchTuple.txt')
            x = add(x, ' --Fs {P}/8_synch')
        if '_extr' in torun:
            x = x.replace('mca-3l-mc.txt','mca-3l-mc-sigextr.txt').replace('--showRatio --maxRatioRange 0 2','--showRatio --maxRatioRange 0 1 --ratioYLabel "S/B"')

        if '_relax' in torun: x = add(x,'-X ^TTT ')

        if '_data' in torun: x = x.replace('mca-3l-mc.txt','mca-3l-mcdata.txt')
        if '_frdata' in torun:
            x = promptsub(x)
            if not '_data' in torun: raise RuntimeError
            x = x.replace('mca-3l-mcdata.txt','mca-3l-mcdata-frdata.txt')
        plots = ['lep2_pt','met','nJet25','mZ1']
        plots += ['3lep_.*','nJet25','nBJetLoose25','nBJetCentralMedium25','met','metLD','htJet25j','mhtJet25','mtWmin','htllv','kinMVA_3l_ttbar','kinMVA_3l_ttV','kinMVA_3l_ttV_withMEM','era']
        x = add(x,"-I 'Zveto'  ")
        if '_tight' in torun:
            x = add(x,'-X ^2b1B -E ^gt2b -E ^1B')

        if '_unc' in torun:
            x = add(x,"--unc ttH-multilepton/systsUnc.txt")
        if '_4j' in torun:
            x = add(x,"-E ^4j ")
            runIt(x,'%s/4j'%torun,plots)
        else:
            runIt(x,'%s'%torun,plots)

    if 'cr_fourlep_onZ' in torun:
        x = base('4l').replace('mca-4l-mc.txt','mca-4l-mcdata.txt')
        if '_data' not in torun: x = add(x, "--xp data ")
        if '_frdata' in torun:
            x = promptsub(x)
            raise RuntimeError, 'Fakes estimation not implemented for 4l'
        if '_unc' in torun:
            x = add(x,"--unc ttH-multilepton/systsUnc.txt")
        x = add(x,"-I ^Zveto")
        plots = ['lep4_pt','met','mZ1','4lep_m4l_noRecl','4lep_mZ2_noRecl','minMllAFAS','tot_weight','4lep_nJet25','nBJetCentralMedium25']
        runIt(x,'%s'%torun,plots)
    if 'cr_zz' in torun:
        x = base('4l')
        x = x.replace('mca-4l-mc.txt','mca-4l-mcdata.txt')
        x = x.replace("--binname 4l","--binname 4l_crzz")
        if '_extr' in torun: x = x.replace('mca-4l-mc.txt','mca-4l-mc-sigextr.txt')
        if '_synch' in torun: 
            x = x.replace('ttH-multilepton/2lss_3l_plots.txt','ttH-multilepton/synchTuple.txt')
            x = add(x, ' --Fs {P}/8_synch')

        x = add(x,"-I ^Zveto -I ^2b1B")
        if '_data' not in torun: x = add(x, "--xp data ")
        if '_frdata' in torun:
            x = promptsub(x)
            raise RuntimeError, 'Fakes estimation not implemented for 4l'
        if '_unc' in torun:
            x = add(x,"--unc ttH-multilepton/systsUnc.txt")
        if '_fit' in torun:
            if not '_data' in torun: raise RuntimeError
            x = add(x,"--sP tot_weight --preFitData tot_weight --sp ZZ ")
            x = add(x,"--xu CMS_ttHl_WZ_lnU ") # otherwise here we fit as WZ
            if '_unc' not in torun:
                print "Will just float WZ freely"
                x = add(x,"--flp WZ")
        plots = ['lep4_pt','met','mZ1','4lep_m4l_noRecl','4lep_mZ2_noRecl','minMllAFAS','tot_weight','4lep_nJet25']
        runIt(x,'%s'%torun,plots)

        
