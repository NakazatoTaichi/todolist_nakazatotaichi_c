from django.shortcuts import render
# from .models import MyModel

def home(request):
    # objects = MyModel.objects.all()
    # return render(request, 'myapp/template.html', {'objects': objects})
    return render(request, 'home.html')


