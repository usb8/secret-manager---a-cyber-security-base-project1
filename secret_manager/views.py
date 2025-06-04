from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import Secret
import sqlite3
import pickle

# Flaw A2:2017-Broken Authentication (Session fixation vulnerability)
@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # No session regeneration after login
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('secrets')
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

# Flaw A1:2017-Injection (Raw SQL query without parameterization)
@login_required
def search_secrets(request):
    search_term = request.GET.get('q', '')
    
    # Vulnerable SQL query
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    query = f"SELECT * FROM secret_manager_secret WHERE title LIKE '%{search_term}%' AND user_id = {request.user.id}"
    cursor.execute(query)
    results = cursor.fetchall()
    
    # Convert results to Secret objects for template
    secrets = []
    for row in results:
        secret = Secret(id=row[0], user=request.user, title=row[2], content=row[3])
        secrets.append(secret)
    
    return render(request, 'secrets.html', {'secrets': secrets})

# Flaw A3:2017-Sensitive Data Exposure (Secrets stored in plaintext)
@login_required
def secret_detail(request, secret_id):
    secret = Secret.objects.get(id=secret_id, user=request.user)
    # No encryption of sensitive data
    return render(request, 'secret_detail.html', {'secret': secret})

# Flaw A5:2017-Broken Access Control (Missing authorization check)
@login_required
def create_secret(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        
        # No validation that the user owns this secret
        Secret.objects.create(
            user=request.user,
            title=title,
            content=content
        )
        return redirect('secrets')
    
    return render(request, 'create_secret.html')

# Flaw A8:2017-Insecure Deserialization
@csrf_exempt
def import_secrets(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        
        # Dangerous deserialization
        data = pickle.load(uploaded_file)
        for item in data:
            Secret.objects.create(
                user=request.user,
                title=item['title'],
                content=item['content']
            )
        return redirect('secrets')
    
    return render(request, 'import_secrets.html')

@login_required
def secrets(request):
    # Flaw A6:2017-Security Misconfiguration (Debug mode left on)
    # In settings.py we would have DEBUG = True in the vulnerable version
    
    secrets = Secret.objects.filter(user=request.user)
    return render(request, 'secrets.html', {'secrets': secrets})