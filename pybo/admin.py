from django.contrib import admin
from .models import Question

# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']  # 검색 필드 설정
    list_display = ('id', 'subject', 'create_date')  # 목록에 표시할 필드 설정
    list_filter = ('create_date',)  # 필터링 옵션 설정

admin.site.register(Question, QuestionAdmin)  # Question 모델을 관리자 사이트에 등록