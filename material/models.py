from django.db import models

# Create your models here.

class Source(models.Model):
    title = models.CharField(max_length=200, verbose_name = "Kaynak")
    slug = models.SlugField(unique=True)

    class Meta:
        unique_together = ('slug',)    
        verbose_name_plural = "sources"

    def __str__(self):
        return self.title

MATERIAL_TYPES = (("diger", "Diğer"), ("mentese", "Menteşe"), ("ray", "Ray"), ("mese_kereste", "Meşe Kereste"),
                  ("kayin_kereste", "Kayın Kereste"), ("kaplamali_mdf_18", "Kaplamalı MDF 18"), ("kaplamali_mdf_25", "Kaplamalı MDF 25"),
                  ("ham_mdf_18", "Ham MDF 18"), ("cekmece_mdf", "Çekmece MDF"), ("aralik", "Aralık"), ("tutkal", "Tutkal"),
                  ("kenar_bandi", "Kenar Bandı"), ("maxifix", "Maxifix"), ("l_baglanti", "L Bağlantı"), ("minifix", "Minifix"),
                  ("aski_takimi", "Askı Takımı"), ("ayna", "Ayna"), ("raf_pimi", "Raf Pimi"), ("cnc", "CNC"),
                  ("boya", "Boya"), ("kulp", "Kulp"), ("lata", "Lata"), ("doseme", "Döşeme"),
                  ("hazeran", "Hazeran"), ("torna", "Torna"), ("paketleme", "Paketleme"), ("nakliye", "Nakliye"),
                  ("google", "Google"))
QUANTITY_TYPES = (("adet", "Adet"), ("kilogram", "Kg"), ("gram", "Gr"), ("litre", "Litre"), ("metre", "Metre"), ("metrekare", "m2"), ("desimetrekup", "dm3"))

class Material(models.Model):
    source = models.ForeignKey(Source, on_delete = models.CASCADE, verbose_name = "Kaynak")
    type = models.CharField(choices = MATERIAL_TYPES, default = "diger", verbose_name = "Malzeme Tipi", max_length = 30)
    title = models.CharField(max_length=200, verbose_name = "Malzeme İsmi")
    quantity_type = models.CharField(choices = QUANTITY_TYPES, default = "adet", verbose_name = "Birim", max_length = 30)
    quantity = models.FloatField(verbose_name = "Miktar", default = 1)
    price = models.FloatField(verbose_name = "Birim Fiyat", default = 0.00)
    
    
    def __str__(self):
        return self.title