from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponseForbidden


from fb.models import (
    UserPost, UserPostComment, UserProfile, Questionnaire, Answer,
    Question, Interest, User
)

from fb.forms import (
    UserPostForm, UserPostCommentForm, UserLogin, UserProfileForm,
    QuestionFrom, AddAnswerForm,
)


@login_required
def index(request):
    posts = UserPost.objects.all()
    if request.method == 'GET':
        form = UserPostForm()
    elif request.method == 'POST':
        form = UserPostForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            post = UserPost(text=text, author=request.user)
            post.save()

    context = {
        'posts': posts,
        'form': form,
    }
    return render(request, 'index.html', context)


@login_required
def post_details(request, pk):
    post = UserPost.objects.get(pk=pk)

    if request.method == 'GET':
        form = UserPostCommentForm()
    elif request.method == 'POST':
        form = UserPostCommentForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            comment = UserPostComment(text=cleaned_data['text'],
                                      post=post,
                                      author=request.user)
            comment.save()

    comments = UserPostComment.objects.filter(post=post)

    context = {
        'post': post,
        'comments': comments,
        'form': form,
    }

    return render(request, 'post_details.html', context)


def login_view(request):
    if request.method == 'GET':
        login_form = UserLogin()
        context = {
            'form': login_form,
        }
        return render(request, 'login.html', context)
    if request.method == 'POST':
        login_form = UserLogin(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            context = {
                'form': login_form,
                'message': 'Wrong user and/or password!',
            }
            return render(request, 'login.html', context)


@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse('login'))


@login_required
def profile_view(request, user):
    profile = UserProfile.objects.get(user__username=user)
    interests = Interest.objects.filter(users__username=user)
    context = {
        'profile': profile,
        'interests': interests
    }
    return render(request, 'profile.html', context)


@login_required
def edit_profile_view(request, user):
    profile = UserProfile.objects.get(user__username=user)
    if not request.user == profile.user:
        return HttpResponseForbidden()
    if request.method == 'GET':
        data = {
            'first_name': profile.user.first_name,
            'last_name': profile.user.last_name,
            'gender': profile.gender,
            'date_of_birth': profile.date_of_birth,
            'interests': profile.user.interests.all(),
        }
        avatar = SimpleUploadedFile(
            profile.avatar.name, profile.avatar.file.read()) \
            if profile.avatar else None
        file_data = {'avatar': avatar}
        form = UserProfileForm(data, file_data)
    elif request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile.user.first_name = form.cleaned_data['first_name']
            profile.user.last_name = form.cleaned_data['last_name']
            profile.user.save()

            profile.gender = form.cleaned_data['gender']
            profile.date_of_birth = form.cleaned_data['date_of_birth']
            if form.cleaned_data['avatar']:
                profile.avatar = form.cleaned_data['avatar']

            interests = form.cleaned_data['interests']
            request.user.interests.clear()
            for interest in interests:
                i = Interest.objects.get(name=interest)
                i.users.add(request.user)

            profile.save()

            return redirect(reverse('profile', args=[profile.user.username]))
    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'edit_profile.html', context)

@login_required
def edit_questionnaire_view(request, user):
    if request.method == 'GET':
        items = list()
        questionnaire = Questionnaire.objects.get(owner__username=user)
        questions = Question.objects.filter(questionnaire_id=questionnaire.id)
        for q in questions:
            answers = Answer.objects.filter(question=q)
            items.append({"question": q, "answers": answers})

        context = {
            'questionnaire': questionnaire,
            'items': items,
        }
    return render(request, 'edit_questionnaire.html', context)


@login_required
def add_question(request, q_id):
    if request.method == 'GET':
        form = QuestionFrom()
        context = {
            'form': form
        }
        return render(request, 'add_question.html', context)

    elif request.method == 'POST':
        form = QuestionFrom(request.POST)
        if form.is_valid():
            q = Question()
            q.questionnaire_id = q_id
            q.quesiton_description = form.cleaned_data['question_description']
            q.points = form.cleaned_data['points']

            q.save()

        return redirect(reverse('edit_questionnaire', args=[request.user.username]))

@login_required
def add_answer(request, quesiton_id):
    if request.method == 'GET':
        form = AddAnswerForm()
        context = {
            'form': form
        }

        return render(request, 'add_answer.html', context)
    elif request.method == 'POST':
        form = AddAnswerForm(request.POST)
        if form.is_valid():
            a = Answer()
            a.question = Question.objects.get(pk=quesiton_id)
            a.answer_description = form.cleaned_data['answer_description']
            a.correct_answer = form.cleaned_data['correct_answer']

            a.save()
        return redirect(reverse('edit_questionnaire', args=[request.user.username]))


@login_required
def remove_question(request, quesiton_id):
    if request.method == 'GET':
        q = Question.objects.get(pk=quesiton_id)
        q.delete()

        return redirect(reverse('edit_questionnaire', args=[request.user.username]))

@login_required
def like_view(request, pk):
    post = UserPost.objects.get(pk=pk)
    post.likers.add(request.user)
    post.save()
    return redirect(reverse('post_details', args=[post.pk]))


@login_required
def discover_view(request):
    user = request.user
    users = User.objects.all()
    user_list = []

    for u in users:
        if u != user:
            for interest in u.interests.all():
                if interest in user.interests.all() and u not in user_list:
                    user_list.append(u)

    return render(request, 'discover.html', { 'user_list': user_list })
