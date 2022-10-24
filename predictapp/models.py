from django.db import models

# Create your models here.

class Sequence(models.Model):
    ACC_SITE = models.CharField(max_length=32)
    index = models.IntegerField()

class Information(models.Model):
    ACC_ID_RES = models.CharField(max_length=32)
    GENE = models.CharField(max_length=32)
    PROTEIN = models.CharField(max_length=32)
    Database = models.CharField(max_length=32)
    KIN_ACC_ID = models.CharField(max_length=300)
    KIN_GENE = models.CharField(max_length=300)
    source = models.CharField(max_length=300)
    disease_PSP = models.CharField(max_length=800)
    disease_ptmd = models.CharField(max_length=800)
    ON_FUNCTION = models.CharField(max_length=300)
    ON_PROCESS = models.CharField(max_length=300)
    ON_PROT_INTERACT = models.CharField(max_length=300)
    ON_OTHER_INTERACT = models.CharField(max_length=300)

