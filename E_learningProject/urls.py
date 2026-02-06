"""
URL configuration for E_learningProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from instructorApp import views as instructorView
from studentApp import views as studentView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('instructor/register',instructorView.InstructorCreateView.as_view(),name="instructor_view"),
    path('',studentView.StudentHome.as_view(),name="student_home"),
    path('course/detail/<int:id>',studentView.CourseDetail.as_view(),name="course_detail"),
    path('student/register',studentView.StudentRegister.as_view(),name="student_register"),
    path('student/login',studentView.StudentLogin.as_view(),name="student_login"),
    path('addcart/<int:id>',studentView.AddtoCartView.as_view(),name="add_to_cart"),
    path('cartview',studentView.ViewCart.as_view(),name="cart_view"),
    path('delete/<int:id>',studentView.cartDelete.as_view(),name="cart_delete"),
    path('chekout',studentView.CheckoutView.as_view(),name="checkout_view"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
