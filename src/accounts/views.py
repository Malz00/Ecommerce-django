from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import CreateView, FormView
from .forms import  LoginForm, RegisterForm, GuessForm
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.shortcuts import render,redirect
from is_safe_url import is_safe_url
from django.views.decorators.csrf import csrf_exempt

from .models import GuestEmail
from .signals import user_logged_in


def guest_register(request):
    form = GuessForm(request.POST or None)
    context = {
        "form": form
    }
 
    next_ =request.GET.get('next')
    next_post =request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        print (form.cleaned_data)
        email = form.cleaned_data.get("email")
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = new_guest_email
        
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
                return redirect("/register/")

    return redirect ("/register/")


class LoginView(FormView):
    form_class = LoginForm
    template_name = "acounts/login.html"
    success_url = '/'

    def form_valid(self, form, *args, **kwargs):
        request = self.request
        next_ =request.GET.get('next')
        next_post =request.POST.get('next')
        redirect_path = next_ or next_post or None
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
         
            login(request, user)
            user_logged_in.send(user.__class__, instance=user, request=request)
            try:
                del request.session['guest_email_id']
            except:
                pass
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
        else:
            print(" incorrect credentials ")
        return super(LoginView, self).form_valid(form)





# def login_page(request):
#     form = LoginForm(request.POST or None)
#     context = {
#         "form": form
#     }
 
#     next_ =request.GET.get('next')
#     next_post =request.POST.get('next')
#     redirect_path = next_ or next_post or None
#     if form.is_valid():
#         print (form.cleaned_data)
#         username = form.cleaned_data.get("username")
#         password = form.cleaned_data.get("password")
#         user = authenticate(request, username=username, password=password)
        
#         if user is not None:
         
#             login(request, user)
#             try:
#                 del request.session['guest_email_id']
#             except:
#                 pass
#             if is_safe_url(redirect_path, request.get_host()):
#                 return redirect(redirect_path)
#             else:
#                 return redirect("/")
#         else:
#             print(" incorrect credentials ")
#         context["form"] = LoginForm()
#     return render(request , "acounts/login.html", context)




User = get_user_model()
class RegisterView(CreateView):
    form_class = RegisterForm
    template_name='acounts/register.html'
    success_url= '/login'

# def register_page(request):
#     form = RegisterForm(request.POST or None)
#     context = {
#         "form": form
#     }
#     if form.is_valid():
#         form.save()
        # username = form.cleaned_data.get("username")
        # email = form.cleaned_data.get("email")
        # password = form.cleaned_data.get("password")
        # new_user = User.objects.create_user(username, email, password)
        # print(new_user)
        

#    return render(request , "acounts/register.html", context)


def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page or any other URL

