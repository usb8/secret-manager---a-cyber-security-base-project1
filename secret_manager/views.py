from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import Secret
import sqlite3
import pickle


# 🔴 Flaw A2:2017-Broken Authentication (Session fixation vulnerability)
@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # ❌ No session regeneration after login
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('secrets')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def secrets(request):
    # 🔴 Flaw A6:2017-Security Misconfiguration (Debug mode left on)
    # In settings.py we would have DEBUG = True in the vulnerable version

    secrets = Secret.objects.filter(user=request.user)
    return render(request, 'secrets.html', {'secrets': secrets})


# 🔴🔴 Flaw A1:2017-Injection (Raw SQL query without parameterization)
@login_required
def search_secrets(request):
    search_term = request.GET.get('q', '')

    # ❌ Vulnerable SQL query
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    query = f"""
    SELECT id, title, secret_header, created_at, user_id
    FROM secret_manager_secret 
    WHERE title LIKE '%{search_term}%' AND user_id = {request.user.id}
    """
    cursor.execute(query)
    results = cursor.fetchall()

    # Convert results to dictionary for template
    secrets = []
    for row in results:
        secrets.append(
            {
                'id': row[0],
                'title': row[1],
                'secret_header': row[2],
                'created_at': row[3],
                'user': request.user if request.user.id == row[4] else None,
            }
        )

    return render(request, 'secrets.html', {'secrets': secrets})


# 🟢🟢 Fixed for A1:2017 (Raw SQL query without parameterization)
@login_required
def search_secrets_fixed(request):
    search_term = request.GET.get('q', '')

    # ✔️ Safe ORM query
    secrets = Secret.objects.filter(
        title__icontains=search_term, user=request.user
    ).values('id', 'title', 'secret_header', 'created_at')

    return render(request, 'secrets.html', {'secrets': secrets})


# 🔴🔴 Flaw A3:2017-Sensitive Data Exposure (Showing decrypted secrets)
# 🔴🔴 Flaw A5:Security Misconfiguration (No proper authorization check)
@login_required
def secret_detail(request, secret_id):
    secret = Secret.objects.get(id=secret_id)

    # ❌ No proper authorization check (A5) and showing decrypted secret (A3)
    decrypted_key = secret.secret_key
    if secret.is_encrypted:
        decrypted_key = secret.get_decrypted_key()

    return render(
        request,
        'secret_detail.html',
        {'secret': secret, 'decrypted_key': decrypted_key},  # Dangerous!
    )


# 🟢🟢 Fixed for A5:2017 (No proper authorization check)
@login_required
def secret_detail_fixed(request, secret_id):
    secret = Secret.objects.get(id=secret_id, user=request.user)  # Proper authorization

    # Only show decrypted key if absolutely necessary
    # ✔️ In a real app, we might not show it at all or use temporary viewing
    return render(
        request,
        'secret_detail.html',
        {'secret': secret, 'show_decrypted': False},  # Safer approach
    )


# 🔴🔴 Flaw A5:2017-Broken Access Control (Missing user association)
@login_required
def create_secret(request):
    if request.method == 'POST':
        title = request.POST['title']
        secret_header = request.POST.get('secret_header', '')
        secret_key = request.POST['secret_key']

        # ❌ Vulnerable - no validation, accepts any data
        secret = Secret.objects.create(
            user=request.user,
            title=title,
            secret_header=secret_header,
            secret_key=secret_key,
        )
        return redirect('secrets')

    return render(request, 'create_secret.html')


# 🔴 Flaw A8:2017-Insecure Deserialization
@csrf_exempt
def import_secrets(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']

        try:
            # ❌ Dangerous deserialization
            data = pickle.load(uploaded_file)
            for item in data:
                Secret.objects.create(
                    user=request.user,
                    title=item['title'],
                    secret_key=item['content'],
                    is_encrypted=False,
                )
            return redirect('secrets')
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}", status=400)

    return render(request, 'import_secrets.html')


# 🟢 Fixed for A8:2017 (Dangerous deserialization)
@login_required
def import_secrets_fixed(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']

        # ✔️ Only accept JSON files
        if not uploaded_file.name.endswith('.json'):
            return HttpResponse("Only JSON files are allowed", status=400)

        try:
            import json

            # ✔️ Safe JSON parsing
            data = json.load(uploaded_file)
            for item in data:
                if not all(k in item for k in ['title', 'content']):
                    continue

                Secret.objects.create(
                    user=request.user,
                    title=item['title'],
                    secret_key=item['content'],
                    is_encrypted=True,  # Auto-encrypt
                )
            return redirect('secrets')
        except json.JSONDecodeError:
            return HttpResponse("Invalid JSON file", status=400)

    return render(request, 'import_secrets.html')


# Demo Flaw A6:2017-Security Misconfiguration
def vulnerable_view(request):
    # Intentionally create division by zero error
    result = 1 / 0
    return HttpResponse(result)
