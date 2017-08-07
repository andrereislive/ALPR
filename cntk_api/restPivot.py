import base64
from pj_6_scoreImage import *
import helpers
# Recebe uma cadeia de bytes, converte isso para uma imagem.
# pega a imagem e salva no diretorio onde o script 6 do cntk esta setado para reconhecimento


    # chamar esse metodo pelo WS, tem que passar a imagem em bytes e ele retorna string com json
def userRequest(imageJpgBytes):
    
    receiveImageJpgBytes(receiveImageJpgBytes)
    return getJSon()
####################################
def recognizeSavedImage(imageUUidName): # passar o nome da imagem somente, sem os diretorios superiores e sem o .jpg
    # boPrintLabel= False, boPrintScore = False = Argumentos para imprimir o label e o score na imagem
    boPrintLabel= True
    boPrintScore = False
    myJson =  generateJson(boPrintLabel, boPrintScore,imageUUidName)# gera o json do cntk 
    return myJson


def getShelfShareJSon_IntelligentPromoter(imageUuidName):
    
    myJson = json.loads(readTxtToString( recognizeDir+imageUuidName+".json"))


    # pega o tamanho da imagem
    im = imread(recognizeDir+imageUuidName+".jpg")
    width, height = np.shape(im[:,:,0])

    # calcula o share acumulando por nome do label, passa o json com os objetos reconhecidos + tamanho da imagem
    shelfShareObjects = calculateShareOfobjects(myJson,width,height)
   
    # Add os shares agrupado para cada produto
    myJson["shelf_share_objects"] = shelfShareObjects 
    
    
    
    return myJson  
 # calcula quanto ocupam de espaco em pixels
def calculateShareOfobjects(objectsJson, imageWidth , imageHeight):
   
    if(len(objectsJson["recognized_objects"])>0  ):
        imagePixelsSquared = imageWidth * imageHeight



        listOfProducts = getListOfProducts(objectsJson)
        # inicia array 
        share_first = getProductShare(listOfProducts[0],objectsJson["recognized_objects"] )
        
        
        share_first = ( share_first / imagePixelsSquared )  * 100
        
        # inicia array 
        objects_array =  {"share_percentage":  float("{0:.2f}".format(share_first)), "product": listOfProducts[0]}
        dataJson = [objects_array]
        for x in range(1, len(listOfProducts)):
            share = getProductShare(listOfProducts[x],objectsJson["recognized_objects"] )
            share = ( share / imagePixelsSquared )  * 100
            it = {"share_percentage": float("{0:.2f}".format(share)), "product": listOfProducts[x]}
            dataJson.append(it)
            
        return dataJson
    else:
        return None

def getProductShare(productName, listRecognizedObj):
    # calcula o share    
    shareHolder = 0
   
    for x in range(0,len(listRecognizedObj)):
        if(productName == listRecognizedObj[x]["label"]):
            left = listRecognizedObj[x]["left"]
            top =  listRecognizedObj[x]["top"]
            right = listRecognizedObj[x]["right"]
            bottom = listRecognizedObj[x]["bottom"]
            shareHolder = shareHolder + calculateShareSingleProduct(left,top,right,bottom)

    return shareHolder


def getListOfProducts(objectsJson):
    sizeObjects =len(objectsJson["recognized_objects"]) 
    if(sizeObjects > 0):
        sizeObjects =len(objectsJson["recognized_objects"]) 
        listOfLabels = [objectsJson["recognized_objects"][0]["label"]]
        for x in range(1,sizeObjects):
            listOfLabels.append(objectsJson["recognized_objects"][x]["label"])
        
        # remove os produtos duplicados, set() é uma lista que naoo pode ter duplicados    
        listOfLabels = list(set(listOfLabels))  

        return listOfLabels  

    # calcula os pixels quadrados de um unico objeto
def calculateShareSingleProduct(left,top,right,bottom):
    width = 0
    height = 0
    if int(right) > int(left):
        width = int(right) -  int(left) 
    else:
        width = int(left) -  int(right)  

    if int(bottom) > int(top):
        height = int(bottom) -  int(top) 
    else:
        height = int(top) -  int(bottom)       

    
    # importante usar abs para nao retornar valores negativos
    pixelsSquared = width * height
    
    return pixelsSquared   #  pixels quadrados

def getAgricuturaJson(imageUuidName):
   
    myJson = json.loads(readTxtToString( recognizeDir+imageUuidName+".json"))

       
    return myJson  

   




