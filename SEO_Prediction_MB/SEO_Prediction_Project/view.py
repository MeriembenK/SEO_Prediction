from django.shortcuts import render
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SEO_Prediction_Project.settings')
django.setup() 


def my_view(request):
    if request.user.is_authenticated:
        user_name = request.user.username
        context = {
            'user_name': user_name
        }
        print(user_name)
        return render(request, 'templates/layout/center.html', context)

   
   