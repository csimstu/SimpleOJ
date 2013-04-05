from problems.models import Problem
from django.shortcuts import render

def show_problem_view(request, search_id):
    try:
        prob = Problem.objects.get(id=search_id)
    except Problem.DoesNotExist:
        return render(request, 'invalid_search_id.html', {'search_id': search_id})
    else:
        samples = []
        cnt = 0
        for x in prob.testcase_set.all():
            if x.is_sample:
                cnt += 1
                samples.append({'input':x.input, 'output':x.output, 'num':cnt})
        return render(request, 'show_problem.html', {'prob': prob, 'samples':samples})
    
def problemset_view(request):
    probs = Problem.objects.order_by('id')
    wrap = []
    odd = 1
    for x in probs:
        wrap.append({'id':x.id, 'title':x.title, 'solved_cnt':x.profile_set.count()
                     , 'odd':odd})
        odd = 3 - odd
    return render(request, 'problemset.html', {'info': wrap})