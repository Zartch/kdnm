# -*- coding: utf-8 -*-
from django.db import models

#esto sirve para que el texto se traduzca automaticamente en el idioma del navegador,
#pones un _('string') y esa palabra será traducida automaticamente por el framework
from django.utils.translation import ugettext as _


from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

TIPOS_COMIDA = (('DE',_('Desayuno')),
                ('AL',_('Almuerzo')),
                ('CO',_('Comida')),
                ('ME',_('Merienda')),
                ('CE',_('Cena')),
                ('RE',_('Resopón')),
                ('TE',_('Tentenpié')))

#Las familias podrian estar reducidas a Tags, las pongo para orientación
FAMILIAS_ALIMENTOS =(
    ('CE',_('Cereales')),
    ('LE',_('Legumbres')),
    ('LA',_('Lacticos')),
    ('VE',_('Verduras')),
    ('HO',_('Hortalizas')),
    ('FR',_('Fruta')),
    ('CA',_('Carne')),
    ('PE',_('Pescado')),
    ('HU',_('Huevos')),
    ('GR',_('Grasas')),
    ('FS',_('Frutos secos')),
    ('AZ',_('Azucares')),
)

#no se si algunas de estas deberian existir
UNIDAD_MEDIDA = (
    ('L', _('Litro')),
    ('K', _('Kilo')),
    ('G', _('Gramo')),
    ('P', _('Pizca')),
    ('C', _('Cucharada')),
    ('A', _('Al gusto')),
    ('T', _('Taza de café')),
    ('V', _('Vaso')),
)


class Tag(models.Model):
    tag = models.SlugField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.tag


class Dieta(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    comidas_diarias = models.ManyToManyField('ComidaDiaria')
    #para poder exportar dietas, deberiamos saber cuantas comidas hay en un mismo dia.
    #sin ser ese dia un dia concreto
    tags = GenericRelation(Tag)

    def __str__(self):
        return self.nombre

class TipoComida(models.Model):
    #Esta classe existe meramente para poderse relacionar con Comida, en una relación uno a uno
    #y la con plato como una relación de muchos a muchos, para que un pplato pueda ser cena y comida
    nombre = models.CharField(max_length=2, choices=TIPOS_COMIDA, unique=True)

    def __str__(self):
        return self.nombre


class ComidaDiaria(models.Model):
    fecha = models.DateField(null=True)
    comidas = models.ForeignKey(Comida)
    tags = GenericRelation(Tag)


class Comida(models.Model):
    tipo = models.ForeignKey(TipoComida)
    platos = models.ManyToManyField(Plato)
    h_inicio = models.DateTimeField()
    tags = GenericRelation(Tag)

    def __str__(self):
        return  str(self.h_inicio) + " (" + str(self.platos.count() or 0) + ")" + str(self.tags.all())


class Plato(models.Model):

    encaja_en = models.ManyToManyField(TipoComida, blank=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, default='')
    tiempo_elaboracion = models.FloatField(blank = True, default=0) #
    elaboracion = models.TextField() # esto podria ser otra classe que contara cosas como tiempo y fotos
    ingredientes = models.ManyToManyField(Ingrediente, through='IngCant')


class IngCant(models.Model):
    plato = models.ForeignKey(Plato)
    ingrediente = models.ForeignKey(Ingrediente)
    cantidad = models.FloatField()


class Ingrediente(models.Model):
    nombre = models.CharField(max_length=280)
    descripcion = models.TextField(blank=True,default='')
    inf_nutricional = models.ManyToManyField(InformacionNutricional, through='InfNu')


class InfNu(models.Model):
    ingrediente = models.ForeignKey(Ingrediente)
    informacion = models.ForeignKey(InformacionNutricional)
    cantidad = models.FloatField(default=0)
    unidad = models.CharField(max_length=1, choices=UNIDAD_MEDIDA)



class InformacionNutricional(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, default='')




