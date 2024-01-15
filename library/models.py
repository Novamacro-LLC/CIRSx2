from django.db import models
#from event.models import Event
from django.contrib.auth.models import Group


class Audience(models.Model):
    aud_name = models.CharField(max_length=50, unique=True, null=False)
    aud_desc = models.CharField(max_length=150, null=False)

    def __str__(self):
        return self.aud_name


class DocumentType(models.Model):
    doctyp_name = models.CharField(max_length=50, unique=True, null=False)
    doctyp_desc = models.CharField(max_length=150, null=False)

    def __str__(self):
        return self.doctyp_name


class DocumentRoute(models.Model):
    document_route = models.CharField(max_length=150, null=False)
    dr_description = models.TextField(null=True)

    def __str__(self):
        return self.document_route


class Curations(models.Model):
    cur_name = models.CharField(max_length=100)
    cat_name = models.CharField(max_length=100)
    subcat_name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.cat_name, " ", self.subcat_name


class Document(models.Model):
    doctyp_num = models.ForeignKey(DocumentType, null=True, on_delete=models.SET_NULL)
    aud_num = models.ForeignKey(Audience, null=True, on_delete=models.SET_NULL)
    doc_path = models.CharField(max_length=250)
    title = models.CharField(max_length=500, null=False)
    author = models.CharField(max_length=150, null=True, blank=True)
    keywords = models.CharField(max_length=250, null=True, blank=True)
    pub_dt = models.DateField(null=True, blank=True)
    doc_abs = models.TextField(null=True, blank=True)
    doc_txt = models.TextField(null=True, blank=True)
#   event = models.ForeignKey(Event, null=True, on_delete=models.SET_NULL, blank=True)
    tier = models.ForeignKey(Group, null=True, on_delete=models.SET_NULL, blank=True)
    doc_route = models.ForeignKey(DocumentRoute, null=True, on_delete=models.SET_NULL)
    curr_num = models.ForeignKey(Curations, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title
