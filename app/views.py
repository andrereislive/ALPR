from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from restPivot import *


####################### INDEX
@csrf_exempt
def index(request):
   
  
    #return render(request, 'index/index.html')
    return JsonResponse({"response": "Hello World"}, safe=False)

 
####################### Check if server is online
def online(request):
    return HttpResponse('<h1>SERVER IS ONLINE</h1>',status=200)

###################################################
# INICIO Funcoes - Projeto Intelligent Promoter
@csrf_exempt
def supermercado(request):

    if request.method == 'POST':
      
## algoritmo OK INICIO #### Descomentar depois que terminar
       data = JSONParser().parse(request)
       imageUUidName = data["clean_image_uuid_name"]
       # Salva a img no diretorio 
       receiveImageJpgBytes(data["clean_image"], recognizeDir+imageUUidName+".jpg")
       # faz o processo de reconhecimento
       # passa somente o nome da imagem sem .jpg nem diretorios superiores
      
       recognizeSavedImage(imageUUidName)
       # retorna o json reconhecido  p dispositivo
       serializer = getShelfShareJSon_IntelligentPromoter(imageUUidName)

     

       # remove o .json - Joga para pasta historic storage
       fileSource = recognizeDir + imageUUidName + ".json"
       fileDest = historicStorageDir 
       deleteFromSource = True
       copyFileToHistoricStorage(fileSource,fileDest, deleteFromSource)

         # remove o .jpg - Joga para pasta historic storage
       fileSource = recognizeDir + imageUUidName + ".jpg"
       fileDest = historicStorageDir 
       deleteFromSource = True
       copyFileToHistoricStorage(fileSource,fileDest, deleteFromSource)

       # remove a imagem reconhecida - Joga para pasta historic storage
       fileSource = recognizeDir + imageNameRecognizedPrefix +imageUUidName + ".jpg"
       fileDest = historicStorageDir 
       deleteFromSource = True
       copyFileToHistoricStorage(fileSource,fileDest, deleteFromSource)
       return JsonResponse(serializer,  safe=False)   
#### Algoritmo OK Fim DESCOMENTAR

    
   
# Fim Funcoes - Intelligent Promoter        
###############################################


###################################################
# INICIO Funcoes - Projeto dos Fungos


@csrf_exempt
def agricultura(request):
     if request.method == 'POST':
       
## algoritmo OK INICIO #### Descomentar depois que terminar
       data = JSONParser().parse(request)
       imageUUidName = data["clean_image_uuid_name"]
       # Salva a img no diretorio 
       receiveImageJpgBytes(data["clean_image"], recognizeDir+imageUUidName+".jpg")
       # faz o processo de reconhecimento
       # passa somente o nome da imagem sem .jpg nem diretorios superiores
       recognizeSavedImage(imageUUidName)
       # retorna o json reconhecido  p dispositivo
       serializer = getAgricuturaJson(imageUUidName)

       # remove o .json - Joga para pasta historic storage
       fileSource = recognizeDir + imageUUidName + ".json"
       fileDest = historicStorageDir 
       deleteFromSource = True
       copyFileToHistoricStorage(fileSource,fileDest, deleteFromSource)

         # remove o .jpg - Joga para pasta historic storage
       fileSource = recognizeDir + imageUUidName + ".jpg"
       fileDest = historicStorageDir 
       deleteFromSource = True
       copyFileToHistoricStorage(fileSource,fileDest, deleteFromSource)

       # remove a imagem reconhecida - Joga para pasta historic storage
       fileSource = recognizeDir + imageNameRecognizedPrefix +imageUUidName + ".jpg"
       fileDest = historicStorageDir 
       deleteFromSource = True
       copyFileToHistoricStorage(fileSource,fileDest, deleteFromSource)
       return JsonResponse(serializer,  safe=False)   
#### Algoritmo OK Fim DESCOMENTAR
    

# Fim Funcoes - Projeto dos Fungos        
###############################################