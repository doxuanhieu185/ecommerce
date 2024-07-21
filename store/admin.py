from django.contrib import admin

# Register your models here.

from . models import Category, Products 



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    
    prepopolated_fields = {'slug': {'name',}}
    
    
@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    
    prepopolated_fields = {'slug': {'title',}}