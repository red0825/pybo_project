from django.shortcuts import render, get_object_or_404
from ..models import Question
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import Count


def index(request):
    sort = request.GET.get('sort', 'recent')  # 기본값: 최신순
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    question_list = Question.objects.order_by('-create_date')
    if sort == 'recommend':
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif sort == 'recent':  # 최신순
        question_list = Question.objects.order_by('-create_date')
    else: # 조회순
        question_list = Question.objects.order_by('-hits', '-create_date')
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(answer__content__icontains=kw) |  # 답변 내용 검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct()
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)  # 페이지 객체 생성
    context = {'question_list': page_obj, 'page': page, 'kw': kw, 'sort': sort}
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.hits += 1  # 조회수 증가
    question.save(update_fields=['hits'])  # hits 필드만 업데이트
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)