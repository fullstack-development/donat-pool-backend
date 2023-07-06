from django.db import models

class SiteSettings(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "settings"
        verbose_name_plural = "settings"
         
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    background = models.ImageField(
        upload_to=("images/categories"), 
        blank=True, 
        null=True,
        )
    settings = models.ForeignKey(
        SiteSettings, 
        on_delete=models.SET_NULL, 
        related_name="categories", 
        related_query_name="categories",
        blank=True, 
        null=True,
        )

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    settings = models.ForeignKey(
        SiteSettings, 
        on_delete=models.SET_NULL, 
        related_name="tags", 
        related_query_name="tag",
        blank=True, 
        null=True,
        )
    
    class Meta:
        verbose_name = "tag"
        verbose_name_plural = "tags"
         
    def __str__(self):
        return self.name
