import subprocess
from problems.models import Problem, TestCase
from judges.models import Submission
from celery import task

@task()
def async_work(submission):
    submission.result = "Running"
    submission.save()
    alreadySolved = submission.user.get_profile().problem_solved.filter(id=submission.problem.id)
    result, time_cost, memory_cost \
        = test(submission.problem, submission.source_code, submission.language)
    clean_up()
    
    submission.status = result
    submission.time_cost = time_cost
    submission.memory_cost = memory_cost
    if submission.status == "Accepted" and not alreadySolved:
        submission.user.get_profile().problem_solved.add(submission.problem)
    submission.save()

SUFFIX = {'C++': 'cpp', 'C': 'c', 'Pascal': 'pas'}
COMPILE_CODE = {'C++': 'g++ -o foo foo.cpp',
                'C': 'gcc -o foo foo.c',
                'Pascal': 'fpc foo.pas'}
import re, time

def clean_up():
    subprocess.call('rm foo t.in t2.in mem.log', shell=True)

def test(prob, source_code, language):
    src_name = 'foo' + '.' + SUFFIX[language]
    src_file = open(src_name, 'w')
    src_file.write(source_code)
    src_file.close()
    
    compile_return_code = subprocess.call(COMPILE_CODE[language], shell=True)
    subprocess.call('rm ' + src_name, shell=True)
    if compile_return_code != 0:
        return ('Compile Error', -1, -1)
    
    subprocess.call('size foo > mem.log', shell=True)
    mem_file = open('mem.log', 'r')
    mem_file.readline()
    mem_s = mem_file.readline()
    memory_cost = int(re.search(r'((\b\d+\b)\W+){3}(\b\d+\b)', mem_s).group(3)) / 1024
    
    test_cases = prob.testcase_set.all()
    time_cost = 0
    for single_test in test_cases:
        if single_test.is_for_judge:
            input_file = open('t.in', 'w')
            input_file.write(single_test.input)
            input_file.close()
            output_file = open('t2.out', 'w')
            output_file.write(single_test.output)
            output_file.close()
            
            start_time = time.time()
            
            run_return_code = subprocess.call('timeout ' + str((prob.time_limit*1.1)/1000) + ' ./foo < t.in > t.out', shell=True)
            
            time_cost += (time.time() - start_time) * 1000
            
            if run_return_code != 0:
                if run_return_code == 124:
                    return ('Time Limit Exceed', time_cost, memory_cost)
                else:
                    return ('Runtime Error', time_cost, memory_cost)
            diff_return_code = subprocess.call('diff -bc t.out t2.out', shell=True)
            if diff_return_code != 0:
                return ('Wrong Answer', time_cost, memory_cost)
    return ("Accepted", time_cost, memory_cost)