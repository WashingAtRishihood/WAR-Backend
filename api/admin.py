from django.contrib import admin
from .models import Student, Washerman, Order

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'enrollment_no', 'bag_no', 'phone_no', 'residency_no', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'enrollment_no', 'bag_no', 'phone_no')
    ordering = ('name',)
    readonly_fields = ('bag_no', 'created_at', 'updated_at')

@admin.register(Washerman)
class WashermanAdmin(admin.ModelAdmin):
    list_display = ('username', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('username',)
    ordering = ('username',)
    readonly_fields = ('created_at',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'bag_no', 'number_of_clothes', 'status', 'submission_date', 'created_at')
    list_filter = ('status', 'created_at', 'submission_date')
    search_fields = ('bag_no', 'id')
    ordering = ('-created_at',)
    readonly_fields = ('submission_date', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Order Information', {
            'fields': ('bag_no', 'number_of_clothes', 'status')
        }),
        ('Timestamps', {
            'fields': ('submission_date', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
