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
        related_query_name="category",
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

class Feedback(models.Model):
    contact = models.CharField(max_length=255, blank=False, null=False)
    name = models.CharField(max_length=255, blank=False, null=False)
    message = models.TextField(blank=False, null=False)
    processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Contact us request"
        verbose_name_plural = "Contact us requests"
         
    def __str__(self):
        return self.name

class UnwantedWord(models.Model):
    word = models.CharField(max_length=500, blank=False, null=False)

    class Meta:
        verbose_name = "Unwanted word"
        verbose_name_plural = "Unwanted words"
         
    def __str__(self):
        return self.word
