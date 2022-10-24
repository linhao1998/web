from keras.models import load_model
from keras import backend as K
from keras.layers import Layer
from predictapp import models
import numpy as np
import re

class Position_Embedding(Layer):

    def __init__(self, size=None, mode='concat', **kwargs):

        self.size = size

        self.mode = mode

        super(Position_Embedding, self).__init__(**kwargs)

    def call(self, x):

        if (self.size == None) or (self.mode == 'concat'):
            self.size = int(x.shape[-1])

        position_j = 1. / K.pow(10000., 2 * K.arange(self.size / 2, dtype='float32') / self.size)

        position_j = K.expand_dims(position_j, 0)

        position_i = K.cumsum(K.ones_like(x[:, :, 0]), 1) - 1

        position_i = K.expand_dims(position_i, 2)

        position_ij = K.dot(position_i, position_j)

        position_ij = K.concatenate([K.cos(position_ij), K.sin(position_ij)], 2)

        if self.mode == 'sum':

            return position_ij + x

        elif self.mode == 'concat':

            return K.concatenate([position_ij, x], 2)

    def compute_output_shape(self, input_shape):

        if self.mode == 'sum':

            return input_shape

        elif self.mode == 'concat':

            return (input_shape[0], input_shape[1], input_shape[2] + self.size)
class Self_Attention(Layer):
    def __init__(self, output_dim=128, **kwargs):
        self.output_dim = output_dim
        super(Self_Attention, self).__init__(**kwargs)

    def build(self, input_shape):
        self.kernel = self.add_weight(name='kernel',
                                      shape=(3, input_shape[2], self.output_dim),
                                      initializer='uniform',
                                      trainable=True)

        super(Self_Attention, self).build(input_shape)

    def call(self, x):
        WQ = K.dot(x, self.kernel[0])
        WK = K.dot(x, self.kernel[1])
        WV = K.dot(x, self.kernel[2])
        QK = K.batch_dot(WQ, K.permute_dimensions(WK, [0, 2, 1]))
        QK = QK / (self.output_dim ** 0.5)
        QK = K.softmax(QK)
        V = K.batch_dot(QK, WV)
        return V

    def compute_output_shape(self, input_shape):
        return (input_shape[0], input_shape[1], self.output_dim)

def selectModel(modelStr):
    if modelStr == "Activity":
        model = load_model('./static/models/Activity.h5',compile=False,
                            custom_objects={'Self_Attention': Self_Attention, 'Position_Embedding': Position_Embedding})
    elif modelStr == "Activity(Y)":
        model = load_model('./static/models/Activity(Y).h5',compile=False,
                           custom_objects={'Self_Attention': Self_Attention, 'Position_Embedding': Position_Embedding})
    elif modelStr == "Activity(ST)":
        model = load_model('./static/models/Activity(ST).h5',compile=False,
                           custom_objects={'Self_Attention': Self_Attention, 'Position_Embedding': Position_Embedding})
    elif modelStr == "PPI":
        model = load_model('./static/models/PPI.h5',compile=False,
                           custom_objects={'Self_Attention': Self_Attention, 'Position_Embedding': Position_Embedding})
    elif modelStr == "PPI(Y)":
        model = load_model('./static/models/PPI(Y).h5',compile=False,
                           custom_objects={'Self_Attention': Self_Attention, 'Position_Embedding': Position_Embedding})
    elif modelStr == "PPI(ST)":
        model = load_model('./static/models/PPI(ST).h5',compile=False,
                           custom_objects={'Self_Attention': Self_Attention, 'Position_Embedding': Position_Embedding})
    elif modelStr == "Regulation":
        model = load_model('./static/models/Regulation.h5',compile=False,
                           custom_objects={'Self_Attention': Self_Attention, 'Position_Embedding': Position_Embedding})
    elif modelStr == "Regulation(Y)":
        model = load_model('./static/models/Regulation(Y).h5',compile=False,
                           custom_objects={'Self_Attention': Self_Attention, 'Position_Embedding': Position_Embedding})
    elif modelStr == "Regulation(ST)":
        model = load_model('./static/models/Regulation(ST).h5',compile=False,
                           custom_objects={'Self_Attention': Self_Attention, 'Position_Embedding': Position_Embedding})
    return model
    
def onehot_coding(sequence):
    ONE_HOT_SIZE = 21
    # _aminos = 'ACDEFGHIKLMNPQRSTVWY*'
    letterDict = {}
    letterDict["A"] = 0
    letterDict["C"] = 1
    letterDict["D"] = 2
    letterDict["E"] = 3
    letterDict["F"] = 4
    letterDict["G"] = 5
    letterDict["H"] = 6
    letterDict["I"] = 7
    letterDict["K"] = 8
    letterDict["L"] = 9
    letterDict["M"] = 10
    letterDict["N"] = 11
    letterDict["P"] = 12
    letterDict["Q"] = 13
    letterDict["R"] = 14
    letterDict["S"] = 15
    letterDict["T"] = 16
    letterDict["V"] = 17
    letterDict["W"] = 18
    letterDict["Y"] = 19
    letterDict["#"] = 20

    Matr = np.zeros((21, ONE_HOT_SIZE))

    AANo = 0
    for AA in sequence:
        index = letterDict[AA]
        Matr[AANo][index] = 1
        AANo = AANo+1
    return Matr

def get_site_sequence(sequence,site):
    acc_seq = ''
    lines=sequence.split('\n')
    for line in lines:
        if line[0] == '>':
            ACC_ID=line.rstrip().split('|')[1]
            continue
        acc_seq = acc_seq + line.strip()
    acc_seq = re.sub('\s','',acc_seq)
    fasta = [s for s in acc_seq.strip()]
    seq = ['#' for i in range(21)]
    i = 10
    ab = site - 1
    RES=fasta[ab]
    ACC_SITE = ACC_ID + '_' + RES+str(site)
    while ab < len(fasta) and i < 21:
        seq[i] = fasta[ab]
        i = i + 1
        ab = ab + 1
    i = 10
    ab = site - 1
    while ab >= 0 and i >= 0:
        seq[i] = fasta[ab]
        i = i - 1
        ab = ab - 1
    return acc_seq,ACC_SITE,seq

def htmlDisplay1(acc_seq,site,modelStr,functionScore):
    acc_seq_len = len(acc_seq)
    insertTimes = acc_seq_len//10
    acc_seq_list = list(acc_seq)
    acc_seq_list[site-1] = '<b style="background-color:red">' + acc_seq[site - 1] + '</b>'
    for i in range(1,insertTimes+1):      
        acc_seq_list.insert(10*i+i-1,'&emsp;')
    acc_seq_html = ''.join(acc_seq_list)
    html1 = '<h4 style="padding-top: 30px;">Phosphorylation site Function Score</h4>\
            <div class="container mt-3 bg-light"\
                style="overflow: hidden;\
                word-wrap: break-word;\
                word-break: break-all;\
                padding: 20px 20px;\
                ">\
                <div class="row">\
                    <div class="col">\
                        <h5>Length&emsp;'+str(acc_seq_len)+'</h5>\
                        <h5>Site&emsp;'+str(site)+'</h5>\
                    </div>\
                    <div class="col">\
                        <h5>Model_Name&emsp;'+modelStr+'</h5>\
                        <h5>Predict_Score&emsp;<b style="color:red">'+str(functionScore)+'</b></h5>\
                    </div>\
                </div>\
            <p style="letter-spacing: 2px;">' + acc_seq_html + '</p>\
            </div>'
    return html1

def htmlDisplay2(acc_site):
    acc_site_list = acc_site.split('_')
    ACC_ID = acc_site_list[0]
    MOD_RES = acc_site_list[1]
    try:
        information = models.Information.objects.get(ACC_ID_RES=acc_site)
        GENE = information.GENE
        PROTEIN = information.PROTEIN
        Database = information.Database
        KIN_ACC_ID = information.KIN_ACC_ID
        KIN_GENE = information.KIN_GENE
        source = information.source
        disease_PSP = information.disease_PSP
        disease_ptmd = information.disease_ptmd
        ON_FUNCTION = information.ON_FUNCTION
        ON_PROCESS = information.ON_PROCESS
        ON_PROT_INTERACT = information.ON_PROT_INTERACT
        ON_OTHER_INTERACT = information.ON_OTHER_INTERACT
    except:
        GENE = '-'
        PROTEIN = '-'
        Database = '-'
        KIN_ACC_ID = '-'
        KIN_GENE = '-'
        source = '-'
        disease_PSP = '-'
        disease_ptmd = '-'
        ON_FUNCTION = '-'
        ON_PROCESS = '-'
        ON_PROT_INTERACT = '-'
        ON_OTHER_INTERACT = '-'
    html2 ='<h4 style="padding-top: 30px;">Phosphorylation site information</h4>\
            <div class="container"\
                style="overflow: hidden;\
                word-wrap: break-word;\
                word-break: break-all;\
                padding: 20px 20px">\
            <h5>Protein</h4>\
            <table class="table" style="table-layout:fixed">\
                <thead class="table-light">\
                    <tr>\
                        <th>ACC_ID</th>\
                        <th>MOD_RES</th>\
                        <th>GENE</th>\
                        <th>PROTEIN</th>\
                        <th>Database</th>\
                    </tr>\
                </thead>\
                <tbody>\
                    <tr>\
                        <td>' + ACC_ID + '</td>\
                        <td>' + MOD_RES + '</td>\
                        <td>' + GENE + '</td>\
                        <td>' + PROTEIN + '</td>\
                        <td>' + Database + '</td>\
                    </tr>\
                </tbody>\
            </table>\
            <h5 style="padding-top: 10px;">Kinas</h4>\
            <table class="table" style="table-layout:fixed">\
                <thead class="table-light">\
                    <tr>\
                        <th>KIN_ACC_ID</th>\
                        <th>KIN_GENE</th>\
                        <th>source</th>\
                    </tr>\
                </thead>\
                <tbody>\
                    <tr>\
                        <td>' + KIN_ACC_ID + '</td>\
                        <td>' + KIN_GENE + '</td>\
                        <td>' + source + '</td>\
                    </tr>\
                </tbody>\
            </table>\
            <h5 style="padding-top: 10px;">Disease</h4>\
            <table class="table" style="table-layout:fixed">\
                <thead class="table-light">\
                    <tr>\
                        <th>DISEASE_PSP</th>\
                        <th>DISEASE_PTMD</th>\
                    </tr>\
                </thead>\
                <tbody>\
                    <tr>\
                        <td>' + disease_PSP + '</td>\
                        <td>' + disease_ptmd + '</td>\
                    </tr>\
                </tbody>\
            </table>\
            <h5 style="padding-top: 10px;">Reconciliation information in the PSP database</h4>\
            <table class="table" style="table-layout:fixed">\
                <thead class="table-light">\
                    <tr>\
                        <th>ON_FUNCTION</th>\
                        <th>ON_PROCESS</th>\
                        <th>ON_PROT_INTERACT</th>\
                        <th>ON_OTHER_INTERACT</th>\
                    </tr>\
                </thead>\
                <tbody>\
                    <tr>\
                        <td>' + ON_FUNCTION + '</td>\
                        <td>' + ON_PROCESS + '</td>\
                        <td>' + ON_PROT_INTERACT + '</td>\
                        <td>' + ON_OTHER_INTERACT + '</td>\
                    </tr>\
                </tbody>\
            </table>\
            </div>'
    return html2