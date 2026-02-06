from django.shortcuts import render,redirect
from django.views import View
from instructorApp.models import Course,Cart,Order
from instructorApp.forms import InstructorCreateForm
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator
from django.db.models import Sum
import razorpay
# Create your views here.
RZP_KEY_ID="rzp_test_RifDitkcb9Q5gl"
RZP_KEY_SECRET="jFvg655jJ2ixRc1FZovsZAAu"

class StudentHome(View):
    def get(self,request):
        courses=Course.objects.all()
        return render(request,'index.html',{'courses':courses})
    
class CourseDetail(View):
    def get(self,request,**kwargs):
        course=Course.objects.get(id=kwargs.get("id"))
        return render(request,'course_detail.html',{'course':course})
    
class StudentRegister(View):
    def get(self,request):
        form=InstructorCreateForm()
        return render(request,'student.html',{'form':form})
    def post(self,request):
        form_instance=InstructorCreateForm(request.POST)
        if form_instance.is_valid():
            form_instance.save()
            return redirect("student_login")
    
class StudentLogin(View):
    def get(self,request):
        form=InstructorCreateForm()
        return render(request,'student.html',{'form':form})
    def post(self,request):
        uname=request.POST.get("username")
        psw=request.POST.get("password")
        res=authenticate(request,username=uname,password=psw)
        if res:
            login(request,res)
            if res.role=="student":
                return redirect("student_home")
            else:
                return redirect("student_login")
            
def login_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect("student_login")
        else:
            return fn(request,*args,**kwargs)
    return wrapper

@method_decorator(login_required,name="dispatch")
class AddtoCartView(View):
    def get(self,request,*args,**kwargs):
        user=request.user
        course=Course.objects.get(id=kwargs.get("id"))
        Cart.objects.get_or_create(user_instance=user,course_instance=course)
        return redirect("student_home")

class ViewCart(View):
    def get(self,request):
        # carts=request.user.user_cart.all()
        carts=Cart.objects.filter(user_instance=request.user)
        # total=carts.aggregate(total=Sum("course_instance__price")).get("total")
        total=sum([cart.course_instance.price for cart in carts])
        return render(request,'cart_summary.html',{'carts':carts,'total':total})

class cartDelete(View):
    def get(self,request,*args,**kwargs):
        Cart.objects.get(id=kwargs.get("id")).delete()
        return redirect('cart_view')

class CheckoutView(View):
    def get(seld,request,*args,**kwargs):
        # carts=request.user.user_cart.all()
        carts=Cart.objects.filter(user_instance=request.user)
        user=request.user
        total=carts.aggregate(total=Sum("course_instance__price")).get("total")
        order_instance=Order.objects.create(user_instance=user,total=total)
        if carts:
            for cart in carts:
                order_instance.cart_instance.add(cart.course_instance)
                print("cart added")
                cart.delete()
            client = razorpay.Client(auth=(RZP_KEY_ID, RZP_KEY_SECRET))

            DATA = {
                "amount": 50000,
                "currency": "INR",
                "receipt": "receipt#1",
                "notes": {
                "key1": "value3",
                "key2": "value2"
             }
        }
            payment= client.order.create(data=DATA)
            print(payment)
            order_id=payment.get("id")
            order_instance.rzp_order_id=order_id
            order_instance.save()
            context={
                "total":float(total*100),
                "key_id":RZP_KEY_ID,
                "order_id":order_id
            }
            return render(request,'payment.html',context)