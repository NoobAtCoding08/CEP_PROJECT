from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Department, Tender, Vendor
from django.contrib.auth.models import User

# Login View
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("select_department")
        else:
            return render(request, "tenders/login.html", {"error": "Invalid credentials"})
    return render(request, "tenders/login.html")

# Logout View
def logout_view(request):
    logout(request)
    return redirect("login")

# Step 1: Select Department
@login_required
def select_department(request):
    departments = Department.objects.all()
    return render(request, "tenders/select_department.html", {"departments": departments})

# Step 2: Show Tenders for Selected Department
@login_required
def department_tenders(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    tenders = Tender.objects.filter(department=department)
    return render(request, "tenders/department_tenders.html", {"department": department, "tenders": tenders})

# Step 3: Show Tender Details
@login_required
def tender_details(request, tender_id):
    tender = get_object_or_404(Tender, id=tender_id)
    vendors = Vendor.objects.filter(tender=tender).prefetch_related('documents','shortfall_documents')
    context = {
        "tender": tender,
        "vendors": vendors,
        "shortfall_stages": [1, 2, 3],  # ✅ Pass this list to the template
    }
    
    return render(request, "tenders/tender_details.html",context)

@login_required
def shortfall_details(request, vendor_id, stage):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    shortfall_documents = vendor.shortfall_documents.filter(shortfall_stage=stage)
    
    return render(request, "tenders/shortfall_details.html", {
        "vendor": vendor,
        "shortfall_documents": shortfall_documents,
        "stage": stage,
    })
    