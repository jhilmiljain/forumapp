from django.contrib.auth import authenticate,login
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.template import loader
from django.urls import reverse

from forum.models import Question, Answer, Topic

# Create your views here.
from django.http.response import HttpResponse,HttpResponseRedirect


def forum(request):
   return render(request,"forum.html")


def Question_List_View(request):
    question_list = Question.objects.select_related('created_by').order_by('-pub_date')
    paginator = Paginator(question_list, 10)
    page = request.GET.get('page')
    try:
        question_list=paginator.page(page)
    except PageNotAnInteger:
        question_list=paginator.page(1)
    except EmptyPage:
        question_list=paginator.page(paginator.num_pages)
    template = loader.get_template('forum/question_list.html')
    context = {
        'question_list': question_list, 'page': page,
    }
    return HttpResponse(template.render(context, request))

def addquestion(request):
    if request.method == "POST":
     q = request.POST.get('question_text')
     t = request.POST.get('topics_text')
     question=Question.objects.create(question_text=q, Topic_id=t)
     return HttpResponseRedirect(reverse('question_page', args=(question.id,)))
    else :
        return render(request, "forum/forum.html")

def question_page(request, question_id):
    question = Question.objects.get(id=question_id)
    return render(request, 'forum/question.html', {'question': question})




def login_page(request):
    _message = 'Please sign in'
    if request.method == 'POST':
        _username = request.POST['username']
        _password = request.POST['password']
        user = authenticate(username=_username, password=_password)
        if user is not None:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('Question_List_View'))
            else:
                _message = 'Your account is not activated'
        else:
            _message = 'Invalid login, please try again.'
    context = {'message': _message}
    return render(request, 'forum/login.html', context)


def signup_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        pass_1 = request.POST.get('password1')
        pass_2 = request.POST.get('password2')
        if pass_1 == pass_2:
             user = authenticate(
                                email=email,
                                password=pass_1,
                                )
             return HttpResponseRedirect(reverse('Question_List_View'))
        else:
             error = " Password Mismatch "
             return render(request, 'forum/signup.html',{"error":error})
    else:
         return render(request, 'forum/signup.html')


def answer(request):
    if request.method == "POST":
        a = request.POST.get('answer_text')
        q = request.POST.get('question_text_id')
        print(q)
        answer = Answer.objects.create(answer_text=a,question_text_id=q)
        return HttpResponseRedirect(reverse('answer_page', args=(answer.id,)))
    else:
        return render(request, "forum/answer.html")



def answer_page(request, answer_id):
    answer = Answer.objects.get(id=answer_id)
    return render(request, 'forum/answer.html', {'answer': answer})


def search(request):
    query = request.GET.get('q')
    if query:
        results = Topic.objects.create(topics_text=query)
    else:
        results = Topic.objects.all()
    return render(request, 'forum/search.html', {'results': results})


def topic_list(request):
    topic_list = Topic.objects.order_by('-pub_date')
    template = loader.get_template('forum/search.html')
    context = {
        'topic_list': topic_list,
    }
    return HttpResponse(template.render(context, request))


def home_page(request):
    if request.method == "POST":
      return HttpResponseRedirect(reverse('login_page'))
    else:
      return render(request,"forum/home.html")