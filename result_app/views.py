from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Result, Prescription
from django.db.models import Q
from .forms import PresForm
from datetime import datetime
from django.contrib import messages

# Create your views here.

# 내담자 ID 받아서 나의 ID와 해당하는 내담자 ID로 결과 리스트 뽑기
def result_view(request, cse_id):
    results = Result.objects.filter(counselor_id=request.user, counselee_id=cse_id).all().order_by('-date')
    return render(request, 'result_app/results.html', {"results":results})

# 결과 ID 받아서 해당 결과의 처방전 보여주기
def pres_view(request, result_id):
    # 처방전 있으면 보여주기
    pres = get_object_or_404(Prescription, result_id=result_id)
    return render(request, 'result_app/prescription.html', context={'pres':pres})

# 결과 ID 받아서 해당 결과의 처방전 작성하기
def add_pres(request, result_id):
    result = get_object_or_404(Result, id=result_id)
    if request.method == 'POST':
        form = PresForm(request.POST)

        if form.is_valid():  # 유효하면 처방전 내용 추가
            comment = form.save(commit=False)
            comment.result_id = result
            comment.save()
            return redirect("result_app:pres_view", result_id)  
    else:
        form = PresForm()
    return render(request, 'result_app/pres_form.html', context={'result':result, 'form':form})

# 처방전 ID 받아서 처방전 수정하기
def update_pres(request, pres_id):
    pres = get_object_or_404(Prescription, id=pres_id)

    if request.method == "POST":
        form = PresForm(request.POST, instance=pres)
        if form.is_valid():
            form.save()
            return redirect('result_app:pres_view', pres.result_id)
    else:
        form = PresForm(instance=pres)
    return render(request, 'result_app/pres_form', context={'pres':pres, 'form':form})

# 처방전 ID 받아서 처방전 삭제하기
def delete_pres(request, pres_id):
    pres = get_object_or_404(Prescription, id=pres_id)
    pres.delete()
    return redirect('result_app:pres_view', pres.result_id)