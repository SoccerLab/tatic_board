from django.contrib import admin

# Register your models here.
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ['username', 'email']  # 검색 가능한 필드 추가
    list_display = ['username', 'email', 'date_joined']  # 표시할 필드 설정