from rest_framework import viewsets
from .models import MonHoc
from .serializers import MonHocSerializer
from rest_framework.permissions import IsAuthenticated


class MonHocViewSet(viewsets.ModelViewSet):
    queryset = MonHoc.objects.all()
    serializer_class = MonHocSerializer
    permission_classes = [IsAuthenticated]

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import MonHoc
from .forms import MonHocForm

# Danh sách môn học
def monhoc_list(request):
    monhocs = MonHoc.objects.all()
    return render(request, "monhoc/monhoc_list.html", {"monhocs": monhocs})


# Thêm môn học
def monhoc_create(request):
    if request.method == "POST":
        form = MonHocForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("monhoc_list")
    else:
        form = MonHocForm()
    return render(request, "monhoc/monhoc_form.html", {"form": form})


# Sửa môn học
def monhoc_update(request, pk):
    monhoc = get_object_or_404(MonHoc, pk=pk)
    if request.method == "POST":
        form = MonHocForm(request.POST, instance=monhoc)
        if form.is_valid():
            form.save()
            return redirect("monhoc_list")
    else:
        form = MonHocForm(instance=monhoc)
    return render(request, "monhoc/monhoc_form.html", {"form": form})


# Xóa môn học
def monhoc_delete(request, pk):
    monhoc = get_object_or_404(MonHoc, pk=pk)
    if request.method == "POST":
        monhoc.delete()
        return redirect("monhoc_list")
    return render(request, "monhoc/monhoc_confirm_delete.html", {"monhoc": monhoc})
