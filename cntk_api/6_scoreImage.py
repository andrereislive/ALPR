# -*- coding: utf-8 -*-
import sys, os, importlib, random, json
import PARAMETERS
from helpers_cntk import *
from copy import deepcopy
locals().update(importlib.import_module("PARAMETERS").__dict__)

####################################
# Parameters
####################################

imgPath = recognizeDir+"1.jpg"
# Directory to save recognized images
outDir = recognizeDir

#choose which classifier to use
classifier = 'svm'
svm_experimentName = 'exp1'

# no need to change these parameters
boAddSelectiveSearchROIs = True
boAddGridROIs = True
boFilterROIs = True
boUseNonMaximaSurpression = True


####################################
# Main
####################################
random.seed(0)

# load cntk model
print("Loading DNN..")
tstart = datetime.datetime.now()
model_path = os.path.join(modelDir, "frcn_" + classifier + ".model")
model = load_model(model_path)
print("Time loading DNN [ms]: " + str((datetime.datetime.now() - tstart).total_seconds() * 1000))

# load trained svm
if classifier == "svm":
    print("Loading svm weights..")
    tstart = datetime.datetime.now()
    svmWeights, svmBias, svmFeatScale = loadSvm(trainedSvmDir, svm_experimentName)
    print("Time loading svm [ms]: " + str((datetime.datetime.now() - tstart).total_seconds() * 1000))
else:
    svmWeights, svmBias, svmFeatScale = (None, None, None)

# compute ROIs
tstart = datetime.datetime.now()
imgOrig = imread(imgPath)
currRois = computeRois(imgOrig, boAddSelectiveSearchROIs, boAddGridROIs, boFilterROIs, ss_kvals, ss_minSize,
                   ss_max_merging_iterations, ss_nmsThreshold,
                   roi_minDimRel, roi_maxDimRel, roi_maxImgDim, roi_maxAspectRatio, roi_minNrPixelsRel,
                   roi_maxNrPixelsRel, grid_nrScales, grid_aspectRatios, grid_downscaleRatioPerIteration)
currRois = currRois[:cntk_nrRois]  # only keep first cntk_nrRois rois
print("Time roi computation [ms]: " + str((datetime.datetime.now() - tstart).total_seconds() * 1000))

# prepare DNN inputs
tstart = datetime.datetime.now()
imgPadded = imresizeAndPad(imgOrig, cntk_padWidth, cntk_padHeight)
_, _, roisCntk = getCntkInputs(imgPath, currRois, None, train_posOverlapThres, nrClasses, cntk_nrRois, cntk_padWidth, cntk_padHeight)
arguments = {
    model.arguments[0]: [np.ascontiguousarray(np.array(imgPadded, dtype=np.float32).transpose(2, 0, 1))], # convert to CNTK's HWC format
    model.arguments[1]: [np.array(roisCntk, np.float32)]
}
print("Time cnkt input generation [ms]: " + str((datetime.datetime.now() - tstart).total_seconds() * 1000))

# run DNN model
print("Running model..")
tstart = datetime.datetime.now()
dnnOutputs = model.eval(arguments)[0][0]
dnnOutputs = dnnOutputs[:len(currRois)]  # remove the zero-padded rois
print("Time running model [ms]: " + str((datetime.datetime.now() - tstart).total_seconds() * 1000))

# score all ROIs
tstart = datetime.datetime.now()
labels, scores = scoreRois(classifier, dnnOutputs, svmWeights, svmBias, svmFeatScale, len(classes),
                           decisionThreshold = vis_decisionThresholds[classifier])
print("Time making prediction [ms]: " + str((datetime.datetime.now() - tstart).total_seconds() * 1000))

# perform non-maxima surpression
tstart = datetime.datetime.now()
nmsKeepIndices = []
if boUseNonMaximaSurpression:
    nmsKeepIndices = applyNonMaximaSuppression(nmsThreshold, labels, scores, currRois)
    print("Non-maxima surpression kept {:4} of {:4} rois (nmsThreshold={})".format(
        len(nmsKeepIndices), len(labels), nmsThreshold))
print("Time non-maxima surpression [ms]: " + str((datetime.datetime.now() - tstart).total_seconds() * 1000))


# visualize results
imgDebug = visualizeResults(imgPath, labels, scores, currRois, classes, nmsKeepIndices,
                            boDrawNegativeRois=False, boDrawNmsRejectedRois=False)

#imshow(imgDebug, waitDuration=5, maxDim=800)
imwrite(imgDebug, outDir +imageNameRecognizedPrefix +os.path.basename(imgPath))

#Troca o valor int de labels pelo valor correto da classe, uma string ex. 0 = __backgroun__, 1= coca_cola, 2 = azeite

mylabelsWithRealName = switchLabelIntToRealName(labels,classes)
# create json-encoded string of all detections
# carrega  outDic - Dicionario de Saida, com labels em String Ex. __background__, cocacola ...
outDict = [{"label": str(l), "score": str(s), "nms": str(False), "left": str(r[0]), "top": str(r[1]), "right": str(r[2]), "bottom": str(r[3])} for l,s, r in zip(mylabelsWithRealName, scores, currRois)]
for i in nmsKeepIndices:
    outDict[i]["nms"] = str(True)

#print("Json-encoded detections: " + outJsonString + "...")
   
outJsonString = json.dumps(outDict)



writeStringToFile(outDir+"requisition.json", outJsonString)



#--- optional code ---#

# write all detections to file, and show how to read in again to visualize
# carrega novamento o outDic - Dicionario de Saida, porem agora com labels em Int
outDict = [{"label": str(l), "score": str(s), "nms": str(False), "left": str(r[0]), "top": str(r[1]), "right": str(r[2]), "bottom": str(r[3])} for l,s, r in zip(labels, scores, currRois)]

writeDetectionsFile(outDir+"detections.tsv", outDict, classes)
labels2, scores2, currRois2, nmsKeepIndices2 = parseDetectionsFile(outDir+"detections.tsv", lutClass2Id)
    #imgDebug2 = visualizeResults(imgPath, labels2, scores2, currRois2, classes, nmsKeepIndices2,  # identical to imgDebug
                            # boDrawNegativeRois=False, boDrawNmsRejectedRois=False)
#imwrite(imgDebug2, outDir +"Recognized_image_" +os.path.basename(imgPath))
    #imshow(imgDebug2, waitDuration=5, maxDim=800)

#extract crop of the highest scored ROI
#maxScore = -float("inf")
#maxScoreRoi = []
#for index, (label,score) in enumerate(zip(labels,scores)):
#   if score > maxScore and label > 0: #and index in nmsKeepIndices:
#      maxScore = score
#      maxScoreRoi = currRois[index]
#if maxScoreRoi == []:
#   print("WARNING: not a single object detected")
#else:
#   imgCrop = imgOrig[maxScoreRoi[1]:maxScoreRoi[3], maxScoreRoi[0]:maxScoreRoi[2], :]
  # imwrite(imgCrop, outDir +"Best_Scored_object_" +os.path.basename(imgPath))
#   imshow(imgCrop, waitDuration=1, maxDim=800)
#print("DONE.")

    