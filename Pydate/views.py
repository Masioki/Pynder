from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth import logout
from Pydate.forms import RegisterForm, PersonalQuestionsForm
from Pydate.models import UserData, PersonalQuestionUser, PersonalQuestionContent, PersonalQuestionAnswer, Match
from django.forms import formset_factory


def base(request):
    if request.user.is_authenticated:
        return render(request, 'html_pages/view_people.html', {})
    return render(request, 'html_pages/base.html', {})


# W register.html wystarczy wstawić {{form}} albo samemu rozłożyć
# za pomocą notacji {{ }} {% %}
@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            profile = UserData(user=user)
            profile.birth = form.cleaned_data.get('birth_date')
            profile.sex = form.cleaned_data.get('sex')
            profile.searching_for = form.cleaned_data.get('searching_for')
            profile.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'html_pages/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            return redirect('html_pages/login.html')
    return render(request, 'html_pages/login')


def logout_view(request):
    logout(request)
    return render(request, 'html_pages/base.html', {})


@login_required
def personal_questionnaire(request, username):
    question_user = User.objects.get(username=username)
    match = Match.objects.filter(user1=request.user, user2=question_user)
    if not match:
        match = Match.objects.filter(user1=question_user, user2=request.user)
        if not match:
            return redirect("/")
        # question_user = request.user  # to replace with the upper line
    questions = []
    questions_ids = []
    personal_questions_user = PersonalQuestionUser.objects.filter(user=question_user)
    if personal_questions_user:
        for p in personal_questions_user:
            answer = PersonalQuestionAnswer.objects.filter(user=request.user)
            if answer:
                return redirect('/')
            queryset = PersonalQuestionContent.objects.filter(questionID=str(p.id)).values("content").all()
            if queryset:
                questions += [q["content"] for q in queryset]
                questions_ids.append(str(p.id))
    formset_form = formset_factory(PersonalQuestionsForm, extra=len(questions_ids))
    if request.method == "POST":
        formset = formset_form(request.POST)
        if formset.is_valid():
            for i, form in enumerate(formset):
                if form.is_valid():
                    answer = form.save(commit=False)
                    answer.user = request.user
                    answer.questionID = PersonalQuestionContent.objects.get(pk=i+1)
                    answer.save()
            return redirect('/')
    else:
        formset = formset_form()
    return render(request, 'html_pages/personal_questionnaire.html', {"formset": formset, "questions": questions})


@login_required
def my_matches(request):
    matches_data = []
    # search matches for user1=request.user
    matches = Match.objects.filter(user1=request.user)
    if matches:
        for match in matches:
            if match.personal_questions_match == "11":
                u = UserData.objects.get(user=match.user2)
                # matches_data.append({"username": u.user.username, "description": u.description, "photo": u.photo})
                matches_data.append({"username": u.user.username, "description": u.description})
    # search matches for user2=request.user
    matches = Match.objects.filter(user2=request.user)
    if matches:
        for match in matches:
            if match.personal_questions_match == "11":
                u = UserData.objects.get(user=match.user1)
                # matches_data.append({"username": u.user.username, "description": u.description, "photo": u.photo})
                matches_data.append({"username": u.user.username, "description": u.description})
    if len(matches_data) == 0:
        display_no_matches_info = True
    else:
        info = ""
        display_no_matches_info = False

    return render(request, 'html_pages/my_matches.html',
                  {"matches_data": matches_data, "display_no_matches_info": display_no_matches_info})
