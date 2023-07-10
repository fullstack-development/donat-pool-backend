from django.db import models

from django.conf import settings
from django.db import models
import donat_pool.core.models as core

class Author(models.Model):
    pkh = models.CharField(max_length=255, primary_key=True)  # TODO: rename to pkh 
    trusted = models.BooleanField(default=False)
    untrustworthy = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "author"
        verbose_name_plural = "authors"

    def __str__(self):
        return self.pkh

class Fundraising(models.Model):
    path = models.CharField(max_length=255, primary_key=True)
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE, 
        related_name="fundraisings", 
        related_query_name="fundraising",
        )
    category = models.ForeignKey(
        core.Category, 
        on_delete=models.SET_NULL, 
        related_name="fundraisings", 
        related_query_name="fundraising",
        blank=True,
        null=True,
        )
    description = models.CharField(
        max_length=1000, 
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
    tags = models.ManyToManyField(
        core.Tag, 
        related_name="fundraising", 
        related_query_name="fundraising",
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "fundraising"
        verbose_name_plural = "fundraising"

    def __str__(self):
        return self.path

class CompletedFundraising(models.Model):
    path = models.CharField(max_length=255)
    title = models.CharField(
        max_length=255, 
        blank=True,
        null=True,
        )
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE, 
        related_name="completed_fundraisings", 
        related_query_name="completed_fundraisings",
        )
    targetAmount = models.BigIntegerField()
    raisedAmount = models.BigIntegerField()
    completedAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "completed fundraising"
        verbose_name_plural = "completed fundraisings"

    def __str__(self):
        return self.title
