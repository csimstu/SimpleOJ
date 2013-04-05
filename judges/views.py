from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from judges.judge import async_work
from judges.models import Submission
from problems.models import Problem
import datetime

@login_required
def submit_view(request, prob_id):
    if request.method == 'POST':
        problem = Problem.objects.get(id=request.POST['problem_id'])
        source_code = request.POST.get('source_code')
        language = request.POST.get('language')
        sub = Submission(problem=problem, source_code=source_code, 
                         user=request.user, status="Pending", datetime=datetime.datetime.now(),
                         language=language, time_cost=-1, memory_cost=-1)
        sub.save()
        async_work.delay(sub) #@UndefinedVariable
        return HttpResponseRedirect('/status/')
    else:
        return render(request, 'submit.html', {'prob_id':prob_id})

STATUS_TO_CLASS = {'Accepted':'ac', 'Wrong Answer':'wa', 'Compile Error':'ce',
                   'Runtime Error':'re', 'Time Limit Exceed':'tle',
                   'Memory Limit Exceed':'mle',
                   'Pending': 'pd', 'Running': 'rn'
                   }

def status_view(request):
    subs = Submission.objects.order_by('-id')
    wrap = []
    for x in subs:
        wrap.append({'id': x.id, 'name': x.user.get_profile().nick_name,'userid': x.user.id,
                     'language': x.language,
                     'probid': x.problem.id, 'cls': STATUS_TO_CLASS[x.status],
                     'status': x.status, 'code_len': len(x.source_code),
                     'time_cost': x.time_cost, 'memory_cost':x.memory_cost,
                     'datetime': x.datetime.strftime("%Y/%m/%d %H:%M:%S"),
                    })
    return render(request, 'status.html', {'info': wrap})