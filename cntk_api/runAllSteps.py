
import time
 
start_time = time.time()
import importlib
import shutil
import PARAMETERS
locals().update(importlib.import_module("PARAMETERS").__dict__)
print("INICIANDO PROCESSSAMENTO!")

#clear imdb cache and other files
if os.path.exists(procDir):
    assert(procDir.endswith(datasetName+"/"))
    shutil.rmtree(procDir)
    time.sleep(0.2) #avoid file access errors
if os.path.exists(resultsDir):    
    assert(resultsDir.endswith(datasetName+"/"))
    shutil.rmtree(resultsDir)
    time.sleep(0.2) #avoid file access errors

print("################# 1_computeRois ####################################################")
#exec(open("./cntk_api/1_computeRois.py").read())
exec(open("1_computeRois.py").read())

print("################# _2_cntkGenerateInputs #############################################")
#exec(open("./cntk_api/2_cntkGenerateInputs.py").read())
exec(open("2_cntkGenerateInputs.py").read())

print("################# _3_runCntk ########################################################")
#exec(open("./cntk_api/3_runCntk.py").read())
exec(open("3_runCntk.py").read())

print("################# 4_trainSvm #######################################################")
#exec(open("./cntk_api/4_trainSvm.py").read())
exec(open("4_trainSvm.py").read())

print("################# 5_evaluateResults ###############################################")
#exec(open("./cntk_api/5_evaluateResults.py").read())
exec(open("5_evaluateResults.py").read())

print("################# 5_visualizeResults ###############################################")
#exec(open("./cntk_api/5_visualizeResults.py").read())
exec(open("5_visualizeResults.py").read())

print("################# 6_scoreImage ###############################################")
#exec(open("./cntk_api/pj_Recursively_6_scoreImage.py").read())

print("FIM DO PROCESSAMENTO")

print("Levou %s segundos de processamento ---" % (time.time() - start_time))