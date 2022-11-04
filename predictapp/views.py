from django.shortcuts import render
from django.http import FileResponse,Http404, HttpResponse, JsonResponse
import serializers
from django.views.decorators.csrf import csrf_exempt
from predictapp import models
from keras.models import load_model
from keras import backend as K
from keras.layers import Layer
import numpy as np
import json
from predictapp.utils import Position_Embedding,Self_Attention, get_accseq_accid, get_accsite_seq, getSiteIndexArr,\
htmlDisplay1, htmlDisplay2,selectModel,onehot_coding

# Create your views here.
loadSuccess = False

def runHome(request):
    return render(request,'home.html')

def runFuncPhosSEQ(request):
    return render(request,'seq.html')

def runDownload(request):
    return render(request,'download.html')

def runHelp(request):
    return render(request,'help.html')

def runContact(request):
    return render(request,'contact.html')

def downloadFile1(request):
    try:       
        file = open('static/files/human.fasta','rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="human.fasta"'
        return response
    except Exception:
        raise Http404

def downloadFile2(request):
    try:       
        file = open('static/files/1111.png','rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="1111.png"'
        return response
    except Exception:
        raise Http404

# @csrf_exempt
def predictPost(request):
    try:
        global features1,features2,loadSuccess
        if loadSuccess == False:
            features1 = np.load('./static/files/03add_pssm2d.npy')
            features2 = np.load('./static/files/03add_ppi500_enrich_evol_pssm.npy').astype(float)
            loadSuccess = True
        output = {}
        if request.POST:
            fastaSeq = request.POST.get('inputseq')
            modelStr = request.POST.get('model')
            acc_seq,ACC_ID = get_accseq_accid(fastaSeq)
            siteIndexArr = getSiteIndexArr(acc_seq,modelStr)
            for siteIndex in siteIndexArr:
                site = siteIndex + 1
                acc_site,sequence = get_accsite_seq(acc_seq,ACC_ID,site)
                one_hot_coding=np.expand_dims(onehot_coding(sequence),axis=0)
                try:
                    seqIdx = models.Sequence.objects.get(ACC_SITE=acc_site).index
                    feature1 = np.expand_dims(features1[seqIdx],axis=0)
                    feature2 = np.expand_dims(features2[seqIdx],axis=0)
                    
                    model = selectModel(modelStr)
                    functionScore = model.predict([one_hot_coding, feature1, feature2])[0][0]
                    output[str(siteIndex)] = float(functionScore)
                except:
                    modelStr = "Onehot_Only"
                    model = load_model('./static/models/one_hot21_1.h5',compile=False,
                        custom_objects={'Self_Attention': Self_Attention, 'Position_Embedding': Position_Embedding})
                    functionScore  = model.predict([one_hot_coding])[0][0]
                    output[str(siteIndex)] = float(functionScore)
                # output['html1'] = htmlDisplay1(acc_seq,site,modelStr,functionScore)
                # output['html2'] = htmlDisplay2(acc_site)
        return JsonResponse(output)
        # return render(request,'seq.html',{"data":output})
    except Exception:
        raise Http404



