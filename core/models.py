from django.db import models
from django.utils.text import slugify

# Create your models here.
from atributes.models import Collection, Taille, Pointure, Couleur
from django.db import models
from django.urls import reverse
from tinymce.widgets import TinyMCE
from tinymce import models as tinymce_models
# Create your models here.
from django.utils.translation import gettext_lazy as _

STATUS_PRODUIT = (
    ('N', _('Nouveau')),
    ('R', _('Rupture')),
    ('P', _('Promotion')),
)

class Category(models.Model):
    name = models.CharField( max_length=150, verbose_name='Nom')
    slug = models.SlugField( max_length=150, unique= True, verbose_name='URL')
    # pixel = models.TextField(verbose_name='Facebook Pixel', blank=True, null=True)
    actif  = models.BooleanField(verbose_name='actif', default=True)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Catégorie'
        verbose_name_plural = '1. Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name +'-'+str(self.id))
        return super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("core:prod-by-cat", args=[self.slug])


class SubCategory(models.Model):
    name = models.CharField( max_length=150, verbose_name='Nom')
    slug = models.SlugField( max_length=150, unique= True, verbose_name='URL')
    actif  = models.BooleanField(verbose_name='actif', default=True)
    category = models.ForeignKey(Category, verbose_name="Catégorie",related_name="sub_categories" ,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('id',)
        verbose_name = 'Sous Catégorie'
        verbose_name_plural = '2. Sous Catégorie'
    
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name +'-'+str(self.id))
        return super(SubCategory, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("core:prod-by-sub-cat", args=[self.slug])


class Product(models.Model):
    name            = models.CharField( max_length=150, verbose_name='Nom')
    slug            = models.SlugField( max_length=150, unique= True, verbose_name='URL')
    sous_category   = models.ForeignKey(SubCategory, verbose_name="Sous Catégorie",related_name="products" ,on_delete=models.CASCADE)
    description     = tinymce_models.HTMLField(verbose_name='Déscription', blank=True, null=True)
    price           = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    old_price       = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ancien prix",blank=True, null=True)
   
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name="collections", blank=True, null=True)
    taille     = models.ManyToManyField(Taille, blank=True, related_name="tailles")
    pointure   = models.ManyToManyField(Pointure, blank=True, related_name="pointures")
    couleur    = models.ManyToManyField(Couleur, related_name="couleurs")

    actif      = models.BooleanField(verbose_name='actif', default=True)
    new        = models.BooleanField(verbose_name='Nouveau', default=True)
    top        = models.BooleanField(verbose_name='Meilleur vente', default=True)

    status     = models.CharField(choices=STATUS_PRODUIT, max_length=1, default='N', blank=True, null=True, verbose_name='Status')

    photo1  = models.ImageField(upload_to='images/produits', blank=True, null=True)
    photo2  = models.ImageField(upload_to='images/produits', blank=True, null=True)
    photo3  = models.ImageField(upload_to='images/produits', blank=True, null=True)
    photo4  = models.ImageField(upload_to='images/produits', blank=True, null=True)
    photo6  = models.ImageField(upload_to='images/produits', blank=True, null=True)
    photo7  = models.ImageField(upload_to='images/produits', blank=True, null=True)
    photo8  = models.ImageField(upload_to='images/produits', blank=True, null=True)
    photo9  = models.ImageField(upload_to='images/produits', blank=True, null=True)
    photo10 = models.ImageField(upload_to='images/produits', blank=True, null=True) 
    
    created = models.DateTimeField(verbose_name='Date de Création', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Date de dernière mise à jour', auto_now=True)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)
        verbose_name = 'Produit'
        verbose_name_plural = '3. Produits'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name +'-'+str(self.id))
        return super(Product, self).save(*args, **kwargs)    

    def get_absolute_url(self):
        return reverse("core:productDetail", args=[self.slug])

class ContactForm(models.Model):
    name        = models.CharField(verbose_name=_('Nom complet'), max_length=100)
    phone       = models.CharField(verbose_name=_("Téléphone") , max_length=25)
    email       = models.EmailField(verbose_name=_("Email"), null=True, blank = True)
    subject     = models.CharField(verbose_name=_("Sujet"), max_length=50, blank=True)
    message     = models.TextField(verbose_name=_("Message"), blank=True, null=True)
    date_sent = models.DateTimeField(verbose_name=_("Date"), auto_now_add=True)

    def __str__(self):
        return self.name


class Photos(models.Model):
    big_slide = models.ImageField(upload_to='images/slides', height_field=None, width_field=None, max_length=None, verbose_name='URL image ')
    actif  = models.BooleanField(verbose_name='Active', default=False)
    is_big  = models.BooleanField(verbose_name='Grande photo (1920 x 570)', default=False)
    is_small  = models.BooleanField(verbose_name='Medium photo (720 x 540)', default=False)

