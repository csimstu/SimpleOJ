from django.contrib import auth
from django.shortcuts import render
from django.http import HttpResponseRedirect
from accounts.models import Profile
from django.contrib.auth.models import User

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect('/problemset/')
        else:
            return render(request, 'login.html', {'errors':True})
    else:
        return render(request, 'login.html', {'errors':False})
    
def logout_view(request):
    auth.logout(request)
    return HttpResponseRedirect('/problemset/')

def ceil_div(a, b):
    if a % b == 0:
        return a // b
    return a // b + 1

def userdata_view(request, user_id_str):
    """

    :param request:
    :param user_id_str:
    :return:
    """
    error = False
    user_id = int(user_id_str)
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        error = True
    if not error:
        sub_set = user.submission_set.all()
        solved_list = list(user.get_profile().problem_solved.all())
        problem_solved = len(solved_list)
        ac_cnt, wa_cnt, re_cnt, ce_cnt, tle_cnt, mle_cnt = 0, 0, 0, 0, 0, 0
        for sub in sub_set:
            if sub.status == 'Accepted':
                ac_cnt += 1
            elif sub.status == 'Wrong Answer':
                wa_cnt += 1
            elif sub.status == 'Compile Error':
                ce_cnt += 1
            elif sub.status == 'Runtime Error':
                re_cnt += 1
            elif sub.status == 'Time Limit Exceed':
                tle_cnt += 1
            elif sub.status == 'Memory Limit Exceed':
                mle_cnt += 1
        
        current_rank = 1
        for rival in Profile.objects.all():
            if len(rival.problem_solved.all()) > problem_solved:
                current_rank += 1
        rows = []
        
        for i in range(0, ceil_div(problem_solved, 8)):
            col = []
            for j in range(0, 8):
                if i*8+j < problem_solved:
                    col.append(solved_list[i*8+j].id)
                else:
                    col.append('')
            rows.append(col)
        
        return render(request, 'userdata.html',
                                      {'error':False, 'current_rank':current_rank,
                                       'problem_solved': problem_solved,
                                       'total_submission':len(sub_set),
                                       'ac_cnt':ac_cnt, 'wa_cnt':wa_cnt,
                                       're_cnt':re_cnt, 'ce_cnt':ce_cnt,
                                       'tle_cnt':tle_cnt, 'mle_cnt':mle_cnt,
                                       'rows':rows, 'curuser':user})
    return render(request, 'userdata.html', {'error':True})

from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from django.shortcuts import render
@login_required
def update_profile_view(request):
    errors = False
    if request.method == 'POST':
        user = request.user
        try:
            profile = user.get_profile()
        except Exception:
            profile = Profile.objects.create(user=user, nick_name=user.username)
        if user.check_password(request.POST['old_password']):
            user.set_password(request.POST['new_password'])
            user.email = request.POST['email']
            user.save()
            profile.nick_name = request.POST['nickname']
            profile.school = request.POST['school']
            profile.motto = request.POST['motto']
            profile.save()
            return HttpResponseRedirect('/problemset/')
        else:
            errors = True
 
    return render(request, 'update_profile.html', {'errors':errors})


def registration_view(request):
    if request.method == 'POST':
        user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
        user.save()
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        profile = Profile.objects.create(user=user, nick_name=user.username)
        profile.save()
        auth.login(request, user)
        return HttpResponseRedirect('/update_profile/')
    else:
        return render(request, 'register.html')
    
def ranklist_view(request):
    def rank_cmp(x, y):
        return -(x['solved_cnt'] - y['solved_cnt'])
    ranklist = []
    for x in User.objects.all():
        ranklist.append({'nick_name': x.get_profile().nick_name,
                         'motto': x.get_profile().motto,
                         'solved_cnt': len(x.get_profile().problem_solved.all())})
    ranklist.sort(cmp=rank_cmp)
    cnt = 0
    for x in ranklist:
        cnt += 1
        x.update({'rank':cnt})
    
    return render(request, 'ranklist.html', {'ranklist':ranklist})