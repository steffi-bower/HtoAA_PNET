
import datetime
import os

def init():
    global test
    global SameSign 
    global isMC 
    global Analysis_Region
    global reversedBID
    global reversedTauID
    global reversedEIso

    global BIDCut
    global EleUncertainty
    global muUncertainty

    test=False #if true we run over a local file read in on the main script, else we look for all .root files transferred during running
    isMC = False # Basically, determining how we handle our gen info

    #Analysis_Region= "SR" #take the values for our control regions Un comment the line you want

    #Analysis_Region= "SR_V" 
    #Analysis_Region= "SR_V_eMu" 
    #Analysis_Region= "AR" 
    #Analysis_Region= "AR_V" 
    #Analysis_Region= "AR_V_eMu" 
    Analysis_Region= "DRNom" 
    #Analysis_Region= "DRNom_V" 
    #Analysis_Region= "DRNom_V_eMu" 
    #Analysis_Region= "DRAlt" 
    #Analysis_Region= "DRAlt_V" 
    #Analysis_Region= "DRAlt_V_eMu" 
    
    if "SR" in Analysis_Region or "AR" in Analysis_Region:
        SameSign=False
    else:
        SameSign=True
    if "Alt" in Analysis_Region or "AR" in Analysis_Region:

        reversedBID=True
    else:
        reversedBID=False
    reversedEIso=False
    reversedTauID=False
    if "V" in Analysis_Region:
        if "eMu" in Analysis_Region:
            reversedEIso=True
        else:
            reversedTauID=True



    ###uncertainties
    EleUncertainty = 0 #For Computing SF Errors 1 is for the upper bound -1 is for the nominal bound
    muUncertainty = "nominal"
    #muUncertainty = "systup"
    #muUncertainty = "systdown"
    '''
    Working points for DeepFlavour:
    80=0.919;
    85=0.863;
    90=0.744;
    95=0.502

    Working points for PNet:
    80=0.733;
    85=0.605;
    90=0.408;
    95=0.174
    '''
    BIDCut= 0.78  
    #BIDCut= 0.863  

if __name__ == '__main__':

    Sample_List=os.environ.get('INSAMPS')
    FileName=os.environ.get('ANA_LABEL')
    init()

    location = os.getcwd() 
    logdir = location+"/AnalysisLogs/"
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    print (Sample_List)
    print (FileName)
    with open(logdir+FileName+".txt", "w") as f:
        f.write("Analysis Run: " +FileName+" at "+ datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")+"\n")
        f.write("Input files " +Sample_List+"\n"+
                "Parameters:"+"\n"+
                "Test (running over singal local file) = "+str(test)+"\n"+
                "\n=====Analysis Region "+(Analysis_Region)+"=====\n"+
                "Same Sign Leptons = "+str(SameSign)+"\n"+
                "Reversed PNet ID = "+str(reversedBID)+"\n"+
                "Reversed Electron Isolation (Does not pass Medium iso) = "+str(reversedEIso)+"\n"+
                "Reversed Tau MVAID (Passes VVloose but Medium)= "+str(reversedTauID)+"\n"+
                "\n\n"+
                "=====Scale Factor Uncertainty Tags=====\n"+
                "Electron Uncertainty (1 is for the upper bound, -1 is for the Lower Bound, 0 is Nominal) = "+ str(EleUncertainty)+"\n"+
                "Muon Uncertainty = "+str(muUncertainty)+"\n\n"+
                "Pnet ID Cut = "+ str(BIDCut)               
                )




