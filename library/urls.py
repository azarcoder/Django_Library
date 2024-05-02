"""
URL configuration for library project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from main import views
urlpatterns = [
    path('a/', admin.site.urls),
    path('', views.home, name='Home'),
    path('student/', views.student, name='Student'),
    path('admin/', views.admin, name='Admin'),
    path('slogin/', views.slogin, name='studentLogin'),
    path('sregister/', views.sregister, name='studentRegister'),
    path('alogin/', views.alogin, name = 'adminLogin'),
    path('aregister/', views.aregister, name = 'adminRegister'),
    path('addbook/', views.addbook, name='addNewBook'),
    path('viewborrowed/', views.viewborrowed, name='viewBorrowed'),
    path('viewstudents/', views.viewstudents, name="viewAllStudents"),
    path('viewbooks/', views.viewbooks, name='viewAllBooks'),
    path('alogout/', views.alogout, name='adminLogout'),
    path('slogout/', views.slogout, name='studentLogout'),
    path('lendbook/', views.lendbook, name='lendBook'),
    path('returnbook/', views.returnbook, name='returnBook'),
    path('student_workPanel', views.student_workPanel, name='student_workPanel'),
    path('admin_workPanel', views.adminworkpanel, name='admin_workPanel'),
    path('updateBook/<int:id>', views.updatebook, name='updateBook'),
    path('deleteBook/<int:id>', views.deletebook, name='deleteBook'),
    path('updateStudent/<int:id>', views.updatestudent, name='updateStudent'),
    path('deleteStudent/<int:id>', views.deletestudent, name='deleteStudent'),
    path('lending/<int:id>/', views.lending, name='lending'),
    path('returning/<int:id>/', views.returning, name='returning'),
    
    


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
