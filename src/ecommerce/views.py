from django.http import HttpResponse,JsonResponse,HttpRequest

from django.shortcuts import render
from .forms import ContactForm

def is_ajax(self):
    return self.headers.get('x-requested-with') == 'XMLHttpRequest'

HttpRequest.is_ajax = is_ajax

def home_page(request):
    #print(request.session.get('first_name', "unkown"))
    context ={
        "title":"homey page",
        "content":"welcome to the home page",
        
    }
    if request.user.is_authenticated:
        context['Premium_content'] = "this content is explicit"

    return render(request, "home_page.html", context)


def about_page(request):
    context = {
        "title":"helo my world",
        "content":"welcome to the about page"

    }
    return render(request, "home_page.html", context)


def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context={
        "title":"contact page",
        "content":"welcome to the contact page",
        "form":contact_form,

    }
    if contact_form.is_valid():
        print(contact_form.cleaned_data)

        if request.is_ajax():
            return JsonResponse({"message": "thank you for your submission"})

    if contact_form.errors:
        errors = contact_form.errors.as_json()
        if request.is_ajax():
            return HttpResponse(errors, status=400, content_type ="application/json")

   
    # if request.method == 'POST':
    #     print(request.POST)
    #     print(request.POST.get('fullname'))
    #     print(request.POST.get('EMAIL'))
    #     print(request.POST.get('content'))
    return render(request, "contact/view.html", context)



