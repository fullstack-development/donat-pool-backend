from django.db import models

from django.conf import settings
from django.db import models

class Author(models.Model):
    address = models.CharField(max_length=255, primary_key=True)
    trusted = models.BooleanField(default=False)
    untrustworthy = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "author"
        verbose_name_plural = "authors"

    def __str__(self):
        return self.pkh

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    background = models.ImageField(
        upload_to=("images/categories"), 
        blank=True, 
        null=True,
        )

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

class Fundraising(models.Model):
    path = models.CharField(max_length=255, primary_key=True)
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE, 
        related_name="fundraisings", 
        related_query_name="fundraising",
        )
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        related_name="fundraisings", 
        related_query_name="fundraising",
        blank=True,
        null=True,
        )
    description = models.CharField(
        max_length=255, 
        blank=True,
        null=True,
        )
    image = models.ImageField(
        upload_to=("images/fundraisings"), 
        blank=True, 
        null=True,
        )
    verified = models.BooleanField(default=False)
    promoted = models.BooleanField(default=False)
    main = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "fundraising"
        verbose_name_plural = "fundraisings"

    def __str__(self):
        return self.path

class CompletedFundraising(models.Model):
    fundraising = models.OneToOneField(
        Fundraising,
        on_delete=models.CASCADE,
        related_name="info",
        related_query_name="info"
        )
    targetAmount = models.BigIntegerField()
    raisedAmount = models.BigIntegerField()
    completedAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "completed fundraising"
        verbose_name_plural = "completed fundraisings"

    def __str__(self):
        return self.fundraising.path


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    fundraisings = models.ManyToManyField(
        Fundraising, 
        related_name="tags", 
        related_query_name="tag",
        blank=True
    )

    class Meta:
        verbose_name = "tag"
        verbose_name_plural = "tags"
         
    def __str__(self):
        return self.name