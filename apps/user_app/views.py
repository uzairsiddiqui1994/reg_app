from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import * 
# Create your views here.

'''
1. Show them the page with the form - registration
2. Route/Function that handles the form submission - POST 
    a. Validations
    b. Hash the password
    c. Add the data to the database
    d. Redirect to somewhere

3. Show them the login form 
4. Route/Function that handles login POST 
    a. Validation
    b. Check password against the database 
    c. Log them in using session 
    d. Redirect
'''

def index(request):
    return render(request, 'user_app/index.html')

def register(request):
    valid = True
    form = request.POST

    if len(form['first_name']) < 3:
        valid = False
        messages.error(request, 'First name must be at least 3 characters.')
    if len(form['last_name']) < 3:
        valid = False
        messages.error(request, 'Last name must be at least 3 characters.')
    if len(form['email']) < 3:
        valid = False
        messages.error(request, 'Email name must be at least 3 characters.')
    if len(form['password']) < 8:
        valid = False
        messages.error(request, 'Password must be at least 8 characters.')
    if not form['password'] == form['password_confirmation']:
        valid = False
        messages.error(request, 'Password and password confirmation do not match')

    if valid: 
        hashed_pw = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt())
        User.objects.create(first_name=form['first_name'], last_name=form['last_name'], email = form['email'], password = hashed_pw)
        messages.success(request, 'You have succesfully registered. Please login.')

    return redirect('/')

def login(request):
    valid = True
    form = request.POST

    if len(form['email']) < 3:
        valid = False
        messages.error(request, 'Email name must be at least 3 characters.')
    if len(form['password']) < 8:
        valid = False
        messages.error(request, 'Password must be at least 8 characters.')

    if valid:
        try:
            user = User.objects.get(email = form['email'])
            if bcrypt.checkpw(form['password'].encode(), user.password.encode()):
                request.session['user_id'] = user.id 
                return redirect('/home')

            else:
                messages.error(request, "Email and password did not match.")
                return redirect('/')

        except User.DoesNotExist:
            messages.error(request, 'A user with this email does not exist. Please register.')
            return redirect('/')

    return redirect('/')

def home(request):
    if not 'user_id' in request.session:
        messages.error(request, 'You need to login')
        return redirect('/')

    else:
        user = User.objects.get(id = request.session['user_id'])
        quotes = Quote.objects.all()


        context = {
            'user' : user, 
            'all_quotes': quotes,
        }
        return render(request, 'user_app/home.html', context)


def logout(request):
    request.session.clear()
    return redirect('/')

#Quote Dash App

def my_account(request, account_id):

    context={
        'user' : User.objects.get(id=account_id)
    }
    return render(request, 'user_app/edit_account.html', context)

def added_quotes_index(request):
    valid =True
    if len(request.POST['author']) < 3:
        messages.error(request, 'Enter Author name more then 3 charactors')
        valid=False

    if len(request.POST['quote']) < 10:
        messages.error(request, 'Enter Author name more then 10 charactors')
        valid=False

    if valid: #add job to database 
        user = User.objects.get(id=request.session['user_id'])      
        Quote.objects.create(author= request.POST['author'],quote_description= request.POST['quote'],quote_created_by_author=user)
    return redirect('/home')


def my_updated_account(request,updated_account_id):

    process= User.objects.get(id=updated_account_id)
    process.first_name= request.POST['first_name']
    process.last_name= request.POST['last_name']
    process.email= request.POST['email']
    process.save()

    return redirect('/home')

def quote_view(request, quote_view_id):
    context={
        "all_quotes": Quote.objects.all(),
        'user' : User.objects.get(id=quote_view_id)
    }
    return render(request, "user_app/view_quote.html", context)