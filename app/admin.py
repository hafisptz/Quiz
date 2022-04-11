from django.contrib import admin
from .models import Quiz,Quiz_questions,Quiz_records
def mercy_pass(ModelAdmin,request,queryset):
	queryset.update(marks=12,result=True,completion_status=True)
mercy_pass.short_description='pass mark granted'	



class Quiz_recordsAdmin(admin.ModelAdmin):
    list_display=[
        'user','quiz_type','marks','result','completion_status',
        
        ]

    list_display_links =['user','result','marks']  


    list_filter=['result','user','completion_status',
        ]  

    
    search_fields=['user__username']  

    actions=[mercy_pass]  






# Register your models here.

admin.site.register(Quiz)
admin.site.register(Quiz_questions)
admin.site.register(Quiz_records,Quiz_recordsAdmin)
