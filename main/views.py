from django.shortcuts import render,HttpResponse, redirect, get_object_or_404
from .forms import studentRegisterForm, UserRegistrationForm, bookCreationForm
from django.contrib import messages
from .models import Students,Books
from django.contrib.auth.models import User, auth
from django.contrib.auth import logout
from django.views.decorators.cache import never_cache
import os
from django.conf import settings

# Create your views here.


def home(request):
    return render(request, 'main.html')

def student(request):
    return render(request, 'student.html')

def admin(request):
    return render(request, 'admin.html')

############# STUDENTS ##################
@never_cache
def slogin(request):
    if request.method == 'POST':
        username = request.POST.get('username') 
        password = request.POST.get('password')
        try:
            student = Students.objects.get(name=username, password=password)
            if student:
                # Store student ID in session
                request.session['student_id'] = student.id
                messages.success(request, 'Welcome %s' % student.name)
                return redirect('student_workPanel')
        except Students.DoesNotExist:
            messages.error(request, 'Invalid username or password. Please try again.')
            return redirect('Student')  
    else:
        return render(request, 'student_login.html')
    
def student_workPanel(request):

    # Retrieve student object from session
    student_id = request.session.get('student_id')
    if student_id:
        student = Students.objects.get(id=student_id)
        return render(request, 'student_workPanel.html', {'student': student})
    else:
        # Redirect to login if student ID is not in session
        return redirect('studentLogin')

def sregister(request):
    if request.method == 'POST':
        form = studentRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Registered Successfully')
                return redirect('Home')
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")

    else:
        form = studentRegisterForm()

    return render(request, 'student_register.html', {'form': form})


def slogout(request):
    request.session.clear()
    messages.success(request, 'Logout Successfully')
    return redirect('Home')

def viewstudents(request):
    data = Students.objects.all()
    if data:
        return render(request, 'view_allStudents.html', {'data' : data})

def updatestudent(request, id):
    student = Students.objects.get(id = id)
    if request.method == 'POST':
        name = request.POST.get('name')
        city = request.POST.get('city')
        contact = request.POST.get('contact')
        email = request.POST.get('email')

        if 'image' in request.FILES:
            image = request.FILES['image']
            student.photo = image
    
        student.name = name
        student.city = city
        student.contact = contact
        student.email = email

        student.save()
        messages.success(request, 'Updated successfully')
        return redirect('student_workPanel')
    
    return render(request, 'studentUpdate.html', {'data': student})
        
    





def deletestudent(request, id):
    try:
        student = Students.objects.get(id = id)
        if student.photo:
            photo_path = os.path.join(settings.MEDIA_ROOT, str(student.photo))
            if os.path.exists(photo_path):
                os.remove(photo_path)
        student.delete()
        messages.success(request, 'Student deleted successfullly')
    except Students.DoesNotExist:
        messages.error(request, 'Student not found')
    
    return redirect('admin_workPanel')
    



########### Admin ############

def alogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password = password)
        if user is not None:

            #session for admin
            request.session['admin_id'] = user.id

            auth.login(request, user)
            messages.success(request, 'Login Successful')
            return render(request, 'admin_workPanel.html', {'username' : username})
        else:
            messages.error(request, 'Invalid credentials.')
            return redirect('Admin')
    else:
        return render(request, 'admin_login.html')

def alogout(request):
    logout(request)
    messages.success(request, 'logout successfully')
    return redirect('Home')

def aregister(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Registered Successfully')
                return redirect('Admin')
            
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")
    else:
        form = UserRegistrationForm()
    return render(request, 'admin_register.html', {'form': form})

def adminworkpanel(request):
    admin_id = request.session.get('admin_id')
    print(admin_id)
    if admin_id:
        try:
            admin = User.objects.get(id=admin_id)
            return render(request, 'admin_workPanel.html', {'username': admin.username})
        except User.DoesNotExist:
            messages.error(request, 'Session error.')
    # If admin_id is not found or an error occurs, return a default HttpResponse
    return HttpResponse("An error occurred or admin session is invalid.")


############### BOOKS ####################
def addbook(request):
    if request.method == 'POST':
        form = bookCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book Added Successfully')
            return redirect('admin_workPanel')
    else:
        form = bookCreationForm()
    return render(request, 'add_books.html', {'form': form})

def viewborrowed(request):
    book = Books.objects.all()
    return render(request, 'borrowedBooks.html', {'book':book})

def viewbooks(request):
    data = Books.objects.all()
    if data != ' ':
        return render(request, 'view_allBooks.html', {'data':data})

def lendbook(request):
    book = Books.objects.all()
    if book:
        return render(request, 'lendingPage.html', {'book':book})

def lending(request, id):
    book = get_object_or_404(Books, id=id)

    if book.bookTaken:
        messages.error(request, 'Book not available!')
    else:
        if book.bookCount > 0:
            student_id = student_id = request.session.get('student_id')
            student = Students.objects.get(id = student_id)
            if student:
                lending_info = {
                    'student_name' : student.name,
                    'book_id' : book.id
                }
                book.lending_info = lending_info
            else:
                messages.error(request, 'Student id not retrieved by session')
            book.bookCount -= 1
            if book.bookCount == 0:
                book.bookTaken = True
            book.save() 
            messages.success(request, 'Book lent successfully!')
        else:
            messages.error(request, 'Book count is already zero!')
    
    return redirect('student_workPanel')


def returning(request, id):
    book = get_object_or_404(Books, id=id)
    student_id = request.session.get('student_id')
    
    if student_id:
        student = Students.objects.get(id=student_id)
        if student:
            lending_info = book.lending_info
            if lending_info and lending_info.get('student_name') == student.name:
                if book.bookCount < 3:
                    book.bookCount += 1
                if book.bookCount == 3:
                    book.bookTaken = False
                book.lending_info = None  # Or set it to a default value as needed
                book.save()
                messages.success(request, 'Book returned successfully!')
            else:
                messages.error(request, 'This book was not borrowed by the current student!')
        else:
            messages.error(request, 'Student not found!')
    else:
        messages.error(request, 'Student ID not retrieved from session!')
    
    return redirect('student_workPanel')
    


def returnbook(request):
    book = Books.objects.all()
    if book:
        return render(request, 'returningBook.html', {'book':book})

def updatebook(request,id):
    book = Books.objects.get(id = id)
    if request.method == 'POST':
        bookid = request.POST.get('bookid')
        bookname = request.POST.get('bookname')
        authorname = request.POST.get('authorname')
        count = request.POST.get('bookcount')
        
        # Check if a new file is uploaded
        if 'image' in request.FILES:
            image = request.FILES['image']
            book.images = image

        book.bookId = bookid
        book.bookName = bookname
        book.authorName = authorname
        book.bookCount = count
        
        book.save()
        messages.success(request, 'Updated successfully')
        return redirect('admin_workPanel')

    return render(request, 'bookUpdate.html', {'data': book})

def deletebook(request, id):
    try:
        book = Books.objects.get(id=id)
        # Delete associated photo
        if book.images:
            photo_path = os.path.join(settings.MEDIA_ROOT, str(book.images))
            if os.path.exists(photo_path):
                os.remove(photo_path)
        # Delete book object
        book.delete()
        messages.success(request, 'Book deleted successfully')
    except Books.DoesNotExist:
        messages.error(request, 'Book not found')
    return redirect('admin_workPanel')


