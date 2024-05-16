from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.http.response import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from . import test
from .models import Data, Test, MinMaxValue
from Predictive.train_Models import TrainModels
from Predictive.response_Builder import ResponseBuilder
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Max
from django.contrib.auth import get_user_model
from django.utils.functional import SimpleLazyObject
from django.http import JsonResponse
import plotly.express as px
import pandas as pd
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


# Create your views here.
#-------------------------General(Dashboards,Widgets & Layout)---------------------------------------

#---------------Dashboards
@login_required(login_url="/login_home")
def index(request):
    message = "Ceci est un message à afficher dans le modèle centre.html"
    user_name = request.user.username if request.user.is_authenticated else None
    print("j'affiche le user_name", user_name)
    context = {
        'message': message,
        'user_name': user_name
    }
    return render(request, "general/dashboard/default/index.html", context)

@login_required(login_url="/login_home")
def centre(request):
    message = "Ceci est un message à afficher dans le modèle centre.html"
    user_name = request.user.username if request.user.is_authenticated else None
    print("j'affiche le user_name", user_name)
    context = {
        'message': message,
        'user_name': user_name
    }
    return render(request, "general/dashboard/default/centre.html", context)

@login_required(login_url="/login_home")
def url(request):
    message = "Ceci est un message à afficher dans le modèle centre.html"
    text = "Ceci est un message à afficher dans le modèle url.html"
    user_name = request.user.username if request.user.is_authenticated else None
   
    context = {
        'message': message,
        'text': text,
        'user_name': user_name
    }
    return render(request, 'general/dashboard/default/url.html', context)



User = get_user_model()
def handle_keyword(request):
    if request.method == 'POST':
        keyword_searched = request.POST.get('keyword')
        email = request.POST.get('email')
        
        user_instance = request.user

        print(user_instance)
        user_instance = request.user

        # Si user_instance est un SimpleLazyObject, déballez-le
        if isinstance(user_instance, SimpleLazyObject):
            user_instance = user_instance._wrapped

        # Assurez-vous que user_instance est bien une instance de User
        if not isinstance(user_instance, User):
            return HttpResponse("Utilisateur non valide", status=400)



        # Stocker les valeurs dans la session Django
        request.session['keyword'] = keyword_searched
        request.session['email'] = email
        
        expediteur = 'damienhernandez0@gmail.com'
        mot_de_passe = 'ceeeiennsmzyuhfg'
        destinataire = email
        objet = 'Analyse predictive ranking'
        corps_message = f"""Bonjour, une analyse sur le prédictive ranking a été créée.\n
                            Bien cordialemment"""

        message = MIMEMultipart()
        message['From'] = expediteur
        message['To'] = destinataire
        message['Subject'] = objet
        message.attach(MIMEText(corps_message, 'plain'))
        serveur_smtp = smtplib.SMTP('smtp.gmail.com', 587)
        serveur_smtp.starttls()
        serveur_smtp.login(expediteur, mot_de_passe)
        serveur_smtp.send_message(message)
        serveur_smtp.quit()

        test.run_script_with_keyword(keyword_searched)
        
        # Initialisation de la classe TrainModels
        trainer = TrainModels()
        response_builder = ResponseBuilder()
        trainer.keyword = keyword_searched
        print("****************************Trainer.keyword is ***********************", trainer.keyword)

        # Read data from Data Base
        trainer.read_my_data()
        trainer.df = trainer.data_to_drop(trainer.df)
        trainer.preprocessing()

        trained_models, X_train, y_train, X_test, y_test=trainer.Final_get_importance(user_instance)
        response_builder.trainedModels= trained_models
        response_builder.df = trainer.df
        response_builder.trainedModels.X = X_train
        response_builder.trainedModels.y = y_train

        min_max = response_builder.get_min_max()
        
        
        # Récupérer l'ID du test le plus récent pour le mot-clé spécifié
        latest_test_id = Test.objects.filter(Keyword=keyword_searched).aggregate(latest_id=Max('id'))['latest_id']

        #Récupération des données pour les graphs en courbe
        if latest_test_id:
            # Récupérer le test correspondant à l'ID le plus récent
            test_instance = Test.objects.get(id=latest_test_id)

            # Obtenez les noms de champs et leurs valeurs depuis la base de données
            fields_and_values = {}
            for field in Test._meta.get_fields():
                field_name = field.name
                field_value = getattr(test_instance, field_name)
                # Supprimer '_score' du nom de champ et remplacer '_' par un espace
                display_field_name = field_name.replace('_score', '').replace('_', ' ')
                if isinstance(field_value, (int, float)):
                    field_value = round(field_value, 2)
                fields_and_values[display_field_name] = field_value


            # Filtrer les champs qui sont des entiers ou des flottants et ont une valeur supérieure à 0
            results = [(field_name, field_value) for field_name, field_value in fields_and_values.items() if isinstance(field_value, (int, float)) and field_value > 0.0]
            results = sorted(results, key=lambda x: x[1], reverse=True)[:15]

            # Récupérer tous les noms de champ à partir de results
            champs = [field_name for field_name, _ in results]
          
            # Récupérer les valeurs de l'attribut à partir du quatrième champ pour chaque objet dans la base de données filtrés par keyword_searched
            valeurs_attributs_a_partir_de_4_yes = [] 
            valeurs_attributs_a_partir_de_4_no = [] 

            # Restaurer les noms de champ en supprimant les remplacements précédents
            champs_restaurés = [field_name.replace(' ', '_').replace('_score', '_') for field_name in champs]
            # Liste des colonnes à exclure
            columns_to_exclude = ["id", "nb_url", "precision"]
            # Déterminer les colonnes à conserver
            set_champs = set(champs_restaurés)
            set_exclude = set(columns_to_exclude)
            set_min_max = set(min_max)

            columns_to_keep = list(set_champs - set_exclude & set_min_max)
            # Alternativement, vous pouvez utiliser une compréhension de liste si vous préférez rester avec des listes
            columns_to_keep = [field for field in champs_restaurés if field not in columns_to_exclude and field in min_max]

            print(columns_to_keep)

            # Filtrer min_max pour ne conserver que les clés de columns_to_keepzs
            min_max_filtered = {key: min_max[key] for key in columns_to_keep}

            print("min_max_filtered:", min_max_filtered)
            
            results_with_min_max = []
            for field_name, field_value in results:
                # Obtenir les valeurs min-max en tant que chaîne
                min_max_series = min_max_filtered.get(field_name.replace(' ', '_'), None)
                min_max_str = str(min_max_series.values[0]) if min_max_series is not None else "N/A"  # Exclure les métadonnées comme index
                results_with_min_max.append((field_name, field_value, min_max_str))
           
            print("j'affiche results_with_min_wmax, afin d'envoyer vers le front-end et les afficher",results_with_min_max)  

            # Boucle à travers les résultats pour créer et enregistrer les valeurs min_max
            for attribute_name, attribute_value, min_max_value in results_with_min_max:
                # Créez une instance de MinMaxValue associée à l'instance de Test
                min_max_instance = MinMaxValue.objects.create(
                    test_instance=test_instance,
                    attribute_name=attribute_name,
                    attribute_value=attribute_value,
                    min_max=min_max_value  # Utilisez le champ 'min_max' au lieu de 'min_max_value'
                )
                # Enregistrez l'instance dans la base de données
                min_max_instance.save()
            
            #print("DataFrame filtré avec les colonnes de 'results':", min_max_filtered)
            for objet in Data.objects.filter(Keyword=keyword_searched, Top10=True):
                # Récupérer les valeurs de tous les attributs à partir du quatrième champ
                valeurs_attributs = [getattr(objet, field_name) for field_name in champs_restaurés[4:]]  # Utilisez tous les champs à partir du quatrième
                valeurs_attributs_a_partir_de_4_yes.append(valeurs_attributs)

            # Parcourir les huit premiers attributs à partir du 4eme
            for index, attribut in enumerate(champs_restaurés[4:15], start=4):
                #print(f"Valeurs de l'attribut '{attribut}' pour Top10 = Yes:")
                for valeurs in valeurs_attributs_a_partir_de_4_yes:
                    if len(valeurs) > index - 4:  # Index relatif à la position dans champs_restaurés
                        print(valeurs[index - 4])
                    else:
                        print("Aucune valeur disponible")
                print("\n")


            for objet in Data.objects.filter(Keyword=keyword_searched, Top10=False):
                # Récupérer les valeurs de tous les attributs à partir du quatrième champ
                valeurs_attributs = [getattr(objet, field_name) for field_name in champs_restaurés[4:]]  # Utilisez tous les champs à partir du quatrième
                valeurs_attributs_a_partir_de_4_no.append(valeurs_attributs)

            # Parcourir les huit premiers attributs à partir du 4eme
            for index, attribut in enumerate(champs_restaurés[4:15], start=4):
                #print(f"Valeurs de l'attribut '{attribut}' pour Top10 = No:")
                for valeurs in valeurs_attributs_a_partir_de_4_no:
                    if len(valeurs) > index - 4:  # Index relatif à la position dans champs_restaurés
                        print("valeurs[index - 4]")
                    else:
                        print("Aucune valeur disponible")
                print("\n")


              # Organiser les données
            data_for_charts = []
            for index, attribut in enumerate(champs_restaurés[3:15], start=3):
                values_yes = [v[index - 4] for v in valeurs_attributs_a_partir_de_4_yes if v[index - 4] is not None]
                values_no = [v[index - 4] for v in valeurs_attributs_a_partir_de_4_no if v[index - 4] is not None]
                data_for_charts.append({'attribut': attribut, 'yes': values_yes, 'no': values_no})


                #print("What im going to send",data_for_charts)

           
            data_for_charts_json = json.dumps(data_for_charts)        
  
        
        objet_terminer = "Analyse predictive ranking terminée"
        corps_message_terminer = f"L'analyse pour le mot-clé '{keyword_searched}' est terminée. Vous pouvez maintenant consulter les résultats."
       
        message = MIMEMultipart()
        message['From'] = expediteur
        message['To'] = destinataire
        message['Subject'] = objet_terminer
        message.attach(MIMEText(corps_message_terminer, 'plain'))
        serveur_smtp = smtplib.SMTP('smtp.gmail.com', 587)
        serveur_smtp.starttls()
        serveur_smtp.login(expediteur, mot_de_passe)
        serveur_smtp.send_message(message)
        serveur_smtp.quit()

        return render(request, 'general/dashboard/default/index.html', {'results': results, 'data_for_charts_json': data_for_charts_json, 'results_with_min_max': results_with_min_max})
    return HttpResponse()
    
    
    
def general_widget(request):
    # Assurez-vous que l'utilisateur est authentifié
    if request.user.is_authenticated:
        # Récupérez l'utilisateur connecté
        user = request.user

        # Récupérez tous les tests de l'utilisateur connecté avec leurs valeurs min/max associées
        all_tests = Test.objects.filter(user=user).prefetch_related('min_max_values')

        # Créez une liste pour stocker les tests avec leurs valeurs min/max associées
        tests_with_min_max_values = []

        # Bouclez à travers chaque test et formatez les données
        for test in all_tests:
            test_data = {
                'id': test.id,
                'keyword': test.Keyword,
                'nb_url': test.nb_url,
                'precision': test.precision,
                'Ttfb_babbar_score': test.Ttfb_babbar_score,
                'min_max_values': []
            }

            # Ajoutez les valeurs min/max associées à ce test
            for min_max_value in test.min_max_values.all():
                test_data['min_max_values'].append({
                    'attribute_name': min_max_value.attribute_name,
                    'attribute_value': min_max_value.attribute_value,
                    'min_max': min_max_value.min_max
                })

            # Ajoutez le test formaté à la liste des tests
            tests_with_min_max_values.append(test_data)

        # Envoyez les données formatées au frontend
        context = {
            "breadcrumb": {
                "parent": "Widgets",
                "child": "General"
            },
            "tests_with_min_max_values": tests_with_min_max_values
        }

        return render(request, "general/widget/general-widget/general-widget.html", context)
    else:
        # Gérez le cas où l'utilisateur n'est pas authentifié
        # Redirigez l'utilisateur vers la page de connexion ou affichez un message d'erreur
        return render(request, "login_required_error.html")

@login_required(login_url="/login_home")
def dashboard_02(request):
    context = { "breadcrumb":{"parent":"Dashboard", "child":"Ecommerce"}} 
    return render(request,"general/dashboard/ecommerce/dashboard-02.html",context)

@login_required(login_url="/login_home")
def online_course(request):
    context = { "breadcrumb":{"parent":"Dashboard", "child":"Online Course"}}
    return render(request,"general/dashboard/online-course/online-course.html",context)

@login_required(login_url="/login_home")
def crypto(request):
    context = { "breadcrumb":{"parent":"Dashboard", "child":"Crypto"}}
    return render(request,"general/dashboard/crypto/crypto.html",context)

    

@login_required(login_url="/login_home")
def chart_widget(request):
    context = { "breadcrumb":{"parent":"Widgets", "child":"Chart"}}
    return render(request,"general/widget/chart-widget/chart-widget.html",context)


# #-----------------Layout

@login_required(login_url="/login_home")
def box_layout(request):
    context = {'layout':'box-layout', "breadcrumb":{"parent":"Page Layout", "child":"Box Layout"}}
    return render(request,"general/page-layout/box-layout.html",context)
    


@login_required(login_url="/login_home")
def layout_rtl(request):
    context = {'layout':'rtl', "breadcrumb":{"parent":"Page Layout", "child":"RTL"}}
    return render(request,"general/page-layout/layout-rtl.html",context)
    

@login_required(login_url="/login_home")
def layout_dark(request):
    context = {'layout':'dark-only', "breadcrumb":{"parent":"Page Layout", "child":"Layout Dark"}}
    return render(request,"general/page-layout/layout-dark.html",context)

@login_required(login_url="/login_home")
def hide_on_scroll(request):
    context = { "breadcrumb":{"parent":"Page Layout", "child":"Hide Menu On Scroll"}}
    return render(request,"general/page-layout/hide-on-scroll.html",context)
    

@login_required(login_url="/login_home")
def footer_light(request):
    context = { "breadcrumb":{"parent":"Page Layout", "child":"footer light"}}
    return render(request,"general/page-layout/footer-light.html",context)
    

@login_required(login_url="/login_home")
def footer_dark(request):
    context = { "footer": "footer-dark", "breadcrumb":{"parent":"Page Layout", "child":"footer dark"}}
    return render(request,"general/page-layout/footer-dark.html",context)
    

@login_required(login_url="/login_home")
def footer_fixed(request):
    context = { "footer": "footer-fix", "breadcrumb":{"parent":"Page Layout", "child":"footer fixed"}}
    return render(request,"general/page-layout/footer-fixed.html",context)


#--------------------------------Applications---------------------------------

#---------------------Project 

@login_required(login_url="/login_home")
def projects(request):
    context = { "breadcrumb":{"parent":"Apps", "child":"Project List"}}
    return render(request,"applications/projects/projects-list/projects.html",context)
    

@login_required(login_url="/login_home")
def projectcreate(request):
    context = { "breadcrumb":{"parent":"Apps", "child":"Project Create"}}
    return render(request,"applications/projects/projectcreate/projectcreate.html",context)

#-------------------File Manager
@login_required(login_url="/login_home")
def file_manager(request):
    context = { "breadcrumb":{"parent":"Apps", "child":"File Manager"}}
    return render(request,"applications/file-manager/file-manager.html",context)
       


#------------------Kanban Board
@login_required(login_url="/login_home")
def kanban(request):
    context = { "breadcrumb":{"parent":"Apps", "child":"Kanban Board"}}
    return render(request,"applications/kanban/kanban.html",context)
    




#--------------------ecommerce
@login_required(login_url="/login_home")
def product_cards(request):
    context = { "breadcrumb":{"parent":"Ecommerce", "child":"Product"}}
    return render(request,"applications/ecommerce/product/product.html",context)
      
  
@login_required(login_url="/login_home")
def product_page(request):
    context = { "breadcrumb":{"parent":"Ecommerce", "child":"Product Page"}}
    return render(request,"applications/ecommerce/product-page/product-page.html",context)
           

@login_required(login_url="/login_home")
def list_products(request):
    context = { "breadcrumb":{"parent":"Ecommerce", "child":"Product List"}}
    return render(request,"applications/ecommerce/list-products/list-products.html",context)
           
    

@login_required(login_url="/login_home")
def payment_details(request):
    context = { "breadcrumb":{"parent":"Ecommerce", "child":"Payment Details"}}
    return render(request,"applications/ecommerce/payment-details/payment-details.html",context)
           

@login_required(login_url="/login_home")
def order_history(request):
    context = { "breadcrumb":{"parent":"Ecommerce", "child":"Recent Orders"}}
    return render(request,"applications/ecommerce/order-history/order-history.html",context)
           
    

@login_required(login_url="/login_home")
def invoice_template(request):
    context = { "breadcrumb":{"parent":"Ecommerce", "child":"Invoice"}}
    return render(request,"applications/ecommerce/invoice-template/invoice-template.html",context)
           


@login_required(login_url="/login_home")
def cart(request):
    context = { "breadcrumb":{"parent":"Ecommerce", "child":"Cart"}}
    return render(request,"applications/ecommerce/cart/cart.html",context)
      

@login_required(login_url="/login_home")
def list_wish(request):
    context = { "breadcrumb":{"parent":"Ecommerce", "child":"Wishlist"}}
    return render(request,"applications/ecommerce/list-wish/list-wish.html",context)
     

@login_required(login_url="/login_home")
def checkout(request):
    context = { "breadcrumb":{"parent":"Ecommerce", "child":"Checkout"}}
    return render(request,"applications/ecommerce/checkout/checkout.html",context)
    


@login_required(login_url="/login_home")
def pricing(request):
    context = { "breadcrumb":{"parent":"Ecommerce", "child":"Pricing"}}
    return render(request,"applications/ecommerce/pricing/pricing.html",context)
    
#--------------------------emails

@login_required(login_url="/login_home")
def email_application(request):
    context = { "breadcrumb":{"parent":"Email", "child":"Email Application"}}
    return render(request,"applications/email/email-application/email-application.html",context)
     
  
@login_required(login_url="/login_home")
def email_compose(request):
    context = { "breadcrumb":{"parent":"Email", "child":"Email Compose"}}
    return render(request,"applications/email/email-compose/email-compose.html",context)
    

#--------------------------------chat
@login_required(login_url="/login_home")
def chat_app(request):
    context = { "breadcrumb":{"parent":"Chat", "child":"Chat App"}}
    return render(request,"applications/chat/chat/chat.html",context)
     

@login_required(login_url="/login_home")
def chat_video(request):
    context = { "breadcrumb":{"parent":"Chat", "child":"Video Chat"}}
    return render(request,"applications/chat/chat-video/chat-video.html",context)
    


#---------------------------------user
@login_required(login_url="/login_home")
def user_profile(request):
    context = { "breadcrumb":{"parent":"Users", "child":"User Profile"}}
    return render(request,"applications/user/user-profile/user-profile.html",context)
    


@login_required(login_url="/login_home")
def edit_profile(request):
    context = { "breadcrumb":{"parent":"Users", "child":"User Profile"}}
    return render(request,"applications/user/edit-profile/edit-profile.html",context)
       

@login_required(login_url="/login_home")
def user_cards(request):
    context = { "breadcrumb":{"parent":"Users", "child":"User Cards"}}
    return render(request,"applications/user/user-cards/user-cards.html",context)
       

#------------------------bookmark
@login_required(login_url="/login_home")
def bookmark(request):
    context = { "breadcrumb":{"parent":"Apps", "child":"Bookmark"}}
    return render(request,"applications/bookmark/bookmark.html",context)
       

#------------------------contacts
@login_required(login_url="/login_home")
def contacts(request):
    context = { "breadcrumb":{"parent":"Apps", "child":"Contacts"}}
    return render(request,"applications/contacts/contacts.html",context)
    
#------------------------task
@login_required(login_url="/login_home")
def task(request):
    context = { "breadcrumb":{"parent":"Apps", "child":"Tasks"}}
    return render(request,"applications/task/task.html",context)
    

#------------------------calendar
@login_required(login_url="/login_home")
def calendar_basic(request):
    context = { "breadcrumb":{"parent":"Apps", "child":"Calender Basic"}}
    return render(request,"applications/calendar/calendar-basic.html",context)
    

#------------------------social-app
@login_required(login_url="/login_home")
def social_app(request):
    context = { "breadcrumb":{"parent":"Apps", "child":"Social App"}}
    return render(request,"applications/social-app/social-app.html",context)
    

#------------------------search
@login_required(login_url="/login_home")
def search(request):
    context = { "breadcrumb":{"parent":"Search Pages", "child":"Search Website"}}
    return render(request,"applications/search/search.html",context)
    
#--------------------------------Forms & Table-----------------------------------------------
#--------------------------------Forms------------------------------------
#------------------------form-controls
@login_required(login_url="/login_home")
def form_validation(request):
    context = { "breadcrumb":{"parent":"Form Controls", "child":"Validation Forms"}}
    return render(request,"forms-table/forms/form-controls/form-validation/form-validation.html",context)
    

@login_required(login_url="/login_home")
def base_input(request):
    context = { "breadcrumb":{"parent":"Form Controls", "child":"Base Inputs"}}
    return render(request,"forms-table/forms/form-controls/base-input/base-input.html",context)
     

@login_required(login_url="/login_home")
def radio_checkbox_control(request):
    context = { "breadcrumb":{"parent":"Form Controls", "child":"Checkbox & Radio"}}
    return render(request,"forms-table/forms/form-controls/radio-checkbox-control/radio-checkbox-control.html",context)
    

@login_required(login_url="/login_home")
def input_group(request):
    context = { "breadcrumb":{"parent":"Form Controls", "child":"Input Groups"}}
    return render(request,"forms-table/forms/form-controls/input-group/input-group.html",context)
    

@login_required(login_url="/login_home")
def megaoptions(request):
    context = { "breadcrumb":{"parent":"Form control", "child":"Mega Options"}}
    return render(request,"forms-table/forms/form-controls/megaoptions/megaoptions.html",context)
    

#---------------------------form widgets

@login_required(login_url="/login_home")
def datepicker(request):
    context = { "breadcrumb":{"parent":"Form Widgets", "child":"Date Picker"}}
    return render(request,"forms-table/forms/form-widgets/datepicker/datepicker.html",context)
    

@login_required(login_url="/login_home")
def time_picker(request):
    context = { "breadcrumb":{"parent":"Form Widgets", "child":"Time Picker"}}
    return render(request,"forms-table/forms/form-widgets/time-picker/time-picker.html",context)
    


@login_required(login_url="/login_home")
def datetimepicker(request):
    context = { "breadcrumb":{"parent":"Form Widgets", "child":"Date Time Picker"}}
    return render(request,'forms-table/forms/form-widgets/datetimepicker/datetimepicker.html',context)
     
    
@login_required(login_url="/login_home")
def daterangepicker(request):
    context = { "breadcrumb":{"parent":"Form Widgets", "child":"Date Range Picker"}}
    return render(request,'forms-table/forms/form-widgets/daterangepicker/daterangepicker.html',context)
     

@login_required(login_url="/login_home")
def touchspin(request):
    context = { "breadcrumb":{"parent":"Form Widgets", "child":"Touchspin"}}
    return render(request,'forms-table/forms/form-widgets/touchspin/touchspin.html',context)
      

@login_required(login_url="/login_home")
def select2(request):
    context = { "breadcrumb":{"parent":"Form Widgets", "child":"Select2"}}
    return render(request,'forms-table/forms/form-widgets/select2/select2.html',context)
      

@login_required(login_url="/login_home")
def switch(request):
    context = { "breadcrumb":{"parent":"Form Widgets", "child":"Switch"}}
    return render(request,'forms-table/forms/form-widgets/switch/switch.html',context)
      
    
@login_required(login_url="/login_home")
def typeahead(request):
    context = { "breadcrumb":{"parent":"Form Widgets", "child":"Typeahead"}}
    return render(request,'forms-table/forms/form-widgets/typeahead/typeahead.html',context)
      
    
@login_required(login_url="/login_home")
def clipboard(request):
    context = { "breadcrumb":{"parent":"Form Widgets", "child":"Clipboard"}}
    return render(request,'forms-table/forms/form-widgets/clipboard/clipboard.html',context)


#-----------------------form layout
@login_required(login_url="/login_home")
def default_form(request):
    context = { "breadcrumb":{"parent":"Form Layout", "child":"Default Forms"}}
    return render(request,'forms-table/forms/form-layout/default-form/default-form.html',context)
    

@login_required(login_url="/login_home")
def form_wizard_one(request):
    context = { "breadcrumb":{"parent":"Form Layout", "child":"Form Wizard"}}
    return render(request,'forms-table/forms/form-layout/form-wizard/form-wizard.html',context) 
    

@login_required(login_url="/login_home")
def form_wizard_two(request):
    context = { "breadcrumb":{"parent":"Form Layout", "child":"Step Form Wizard"}}
    return render(request,'forms-table/forms/form-layout/form-wizard-two/form-wizard-two.html',context) 
    

@login_required(login_url="/login_home")
def form_wizard_three(request):
    context = { "breadcrumb":{"parent":"Form Layout", "child":"Form Wizard With Icon"}}
    return render(request,'forms-table/forms/form-layout/form-wizard-three/form-wizard-three.html',context)
    

#----------------------------------------------------Table------------------------------------------
#------------------------bootstrap table
@login_required(login_url="/login_home")
def basic_table(request):
    context = { "breadcrumb":{"parent":"Bootstrap Tables", "child":"Bootstrap Basic Tables"}}
    return render(request,'forms-table/table/bootstrap-table/basic-table/bootstrap-basic-table.html',context)
    


@login_required(login_url="/login_home")
def sizing_table(request):
    context = { "breadcrumb":{"parent":"Bootstrap Tables", "child":"Bootstrap Table Sizes"}}
    return render(request,'forms-table/table/bootstrap-table/sizing-table/bootstrap-sizing-table.html',context)
    


@login_required(login_url="/login_home")
def border_table(request):
    context = { "breadcrumb":{"parent":"Bootstrap Tables", "child":"Bootstrap Border Table"}}
    return render(request,'forms-table/table/bootstrap-table/border-table/bootstrap-border-table.html',context)
    

@login_required(login_url="/login_home")
def styling_table(request):
    context = { "breadcrumb":{"parent":"Bootstrap Tables", "child":"Bootstrap Styling Tables"}}
    return render(request,'forms-table/table/bootstrap-table/styling-table/bootstrap-styling-table.html',context)
    


@login_required(login_url="/login_home")
def table_components(request):
    context = { "breadcrumb":{"parent":"Bootstrap Tables", "child":"Table Components"}}
    return render(request,'forms-table/table/bootstrap-table/table-components/table-components.html',context)
    

#------------------------data table
@login_required(login_url="/login_home")
def datatable_basic_init(request):
    context = { "breadcrumb":{"parent":"Data Tables", "child":"Basic DataTables"}}
    return render(request,'forms-table/table/data-table/datatable-basic/datatable-basic-init.html',context)
    

@login_required(login_url="/login_home")
def datatable_advance(request):
    context = { "breadcrumb":{"parent":"Data Tables", "child":"Advanced DataTables"}}
    return render(request,'forms-table/table/data-table/datatable-advance/datatable-advance.html',context)
    

@login_required(login_url="/login_home")
def datatable_styling(request):
    context = { "breadcrumb":{"parent":"Data Tables", "child":"Styling DataTables"}}
    return render(request,'forms-table/table/data-table/datatable-styling/datatable-styling.html',context)
    

@login_required(login_url="/login_home")
def datatable_AJAX(request):
    context = { "breadcrumb":{"parent":"Data Tables", "child":"Ajax DataTables"}}
    return render(request,'forms-table/table/data-table/datatable-AJAX/datatable-AJAX.html',context)
    

@login_required(login_url="/login_home")
def datatable_server_side(request):
    context = { "breadcrumb":{"parent":"Data Tables", "child":"Datatables Server Side"}}
    return render(request,'forms-table/table/data-table/datatable-server/datatable-server-side.html',context)
    

@login_required(login_url="/login_home")
def datatable_plugin(request):
    context = { "breadcrumb":{"parent":"Data Tables", "child":"Plugin DataTable"}}
    return render(request,'forms-table/table/data-table/datatable-plugin/datatable-plugin.html',context)
    

@login_required(login_url="/login_home")
def datatable_API(request):
    context = { "breadcrumb":{"parent":"Data Tables", "child":"API DataTables"}}
    return render(request,'forms-table/table/data-table/datatable-API/datatable-API.html',context)
    

@login_required(login_url="/login_home")
def datatable_data_source(request):
    context = { "breadcrumb":{"parent":"Data Tables", "child":"DATA Source DataTables"}}
    return render(request,'forms-table/table/data-table/data-source/datatable-data-source.html',context)


#-------------------------------EX.data-table
@login_required(login_url="/login_home")
def ext_autofill(request):
    context = { "breadcrumb":{"parent":"Extension Data Tables", "child":"Autofill Datatables"}}
    return render(request,'forms-table/table/Ex-data-table/ext-autofill/datatable-ext-autofill.html',context)
    

@login_required(login_url="/login_home")
def ext_basic_button(request):
    context = { "breadcrumb":{"parent":"Extension Data Tables", "child":"Basic button"}}
    return render(request,'forms-table/table/Ex-data-table/basic-button/datatable-ext-basic-button.html',context)
    

@login_required(login_url="/login_home")
def ext_col_reorder(request):
    context = { "breadcrumb":{"parent":"Extension Data Tables", "child":"Columns Reorder"}}
    return render(request,'forms-table/table/Ex-data-table/col-reorder/datatable-ext-col-reorder.html',context)
    

@login_required(login_url="/login_home")
def ext_fixed_header(request):
    context = { "breadcrumb":{"parent":"Extension Data Tables", "child":"Fixed Header"}}
    return render(request,'forms-table/table/Ex-data-table/fixed-header/datatable-ext-fixed-header.html',context)
    

@login_required(login_url="/login_home")
def ext_html_5_data_export(request):
    context = { "breadcrumb":{"parent":"Extension Data Tables", "child":"HTML 5 Data Export"}}
    return render(request,'forms-table/table/Ex-data-table/html-export/datatable-ext-html-5-data-export.html',context)
    

@login_required(login_url="/login_home")
def ext_key_table(request):
    context = { "breadcrumb":{"parent":"Extension Data Tables", "child":"Key Table"}}
    return render(request,'forms-table/table/Ex-data-table/key-table/datatable-ext-key-table.html',context)
    

@login_required(login_url="/login_home")
def ext_responsive(request):
    context = { "breadcrumb":{"parent":"Extension Data Tables", "child":"Responsive Datatables"}}
    return render(request,'forms-table/table/Ex-data-table/ext-responsive/datatable-ext-responsive.html',context)
    

@login_required(login_url="/login_home")
def ext_row_reorder(request):
    context = {"breadcrumb":{"parent":"Extension Data Tables", "child":"Rows Reorder"}}    
    return render(request,'forms-table/table/Ex-data-table/row-reorder/datatable-ext-row-reorder.html',context)
    

@login_required(login_url="/login_home")
def ext_scroller(request):
    context = { "breadcrumb":{"parent":"Extension Data Tables", "child":"Scroller"}}
    return render(request,'forms-table/table/Ex-data-table/ext-scroller/datatable-ext-scroller.html',context)


#--------------------------------jsgrid_table

@login_required(login_url="/login_home")
def jsgrid_table(request):
    context = { "breadcrumb":{"parent":"Tables", "child":"JS Grid Tables"}}
    return render(request,'forms-table/table/js-grid-table/jsgrid-table.html',context) 
       


#------------------Components------UI Components-----Elements ----------->

#-----------------------------Ui kits
@login_required(login_url="/login_home")
def statecolor(request):
    context = { "breadcrumb":{"parent":"Ui Kits", "child":"State Color"}}
    return render(request,'components/ui-kits/state-color.html', context)
     

@login_required(login_url="/login_home")
def typography(request):
    context = { "breadcrumb":{"parent":"Ui Kits", "child":"Typography"}}
    return render(request,'components/ui-kits/typography.html', context)
     


@login_required(login_url="/login_home")
def avatars(request):
    context = { "breadcrumb":{"parent":"Ui Kits", "child":"Avatars"}}
    return render(request,'components/ui-kits/avatars.html', context)
     

@login_required(login_url="/login_home")
def helper(request):
    context = { "breadcrumb":{"parent":"Ui Kits", "child":"Helper Classes"}}
    return render(request,'components/ui-kits/helper.html', context)
     


@login_required(login_url="/login_home")
def grid(request):
    context = { "breadcrumb":{"parent":"Ui Kits", "child":"grid"}}
    return render(request,'components/ui-kits/grid.html', context)
      

@login_required(login_url="/login_home")
def tagpills(request):
    context = { "breadcrumb":{"parent":"Ui Kits", "child":"Tag & Pills"}}
    return render(request,'components/ui-kits/tag-pills.html', context)
      

@login_required(login_url="/login_home")
def progressbar(request):
    context = { "breadcrumb":{"parent":"Ui Kits", "child":"Progress"}}
    return render(request,'components/ui-kits/progressbar.html', context)
         

@login_required(login_url="/login_home")
def modal(request):
    context = { "breadcrumb":{"parent":"Ui Kits", "child":"modal"}}
    return render(request,'components/ui-kits/modal.html', context)  
    

@login_required(login_url="/login_home")
def alert(request):
    context = { "breadcrumb":{"parent":"Ui Kits", "child":"alert"}}
    return render(request,'components/ui-kits/alert.html', context)
    
      

@login_required(login_url="/login_home")
def popover(request):
    context = { "breadcrumb":{"parent":"Ui Kits", "child":"popover"}}
    return render(request,'components/ui-kits/popover.html', context) 
    

@login_required(login_url="/login_home")
def tooltip(request):
    context = { "breadcrumb":{"parent":"Ui Kits", "child":"tooltip"}}
    return render(request,'components/ui-kits/tooltip.html', context)
    

@login_required(login_url="/login_home")
def spiners(request):
    context = { "breadcrumb":{"parent":"Ui Kits", "child":"Spinners"}}
    return render(request,'components/ui-kits/spiners.html', context)  
    

@login_required(login_url="/login_home")
def dropdown(request):
    context = { "breadcrumb":{"parent":"Ui Kits", "child":"dropdown"}}
    return render(request,'components/ui-kits/dropdown.html', context)   
    

@login_required(login_url="/login_home")
def accordion(request):
    context = { "breadcrumb":{"parent":"Ui Kits", "child":"accordion"}}
    return render(request,'components/ui-kits/accordion.html', context)    
    

@login_required(login_url="/login_home")
def bootstraptab(request):
    context = { "breadcrumb":{"parent":"Ui Kits", "child":"Bootstrap Tabs"}}
    return render(request,'components/ui-kits/bootstraptab.html', context)    
    

@login_required(login_url="/login_home")
def linetab(request):
    context = {"breadcrumb":{"parent":"Tabs", "child":"Line Tabs"}}
    return render(request,'components/ui-kits/linetab.html', context) 
            

@login_required(login_url="/login_home")
def navs(request):
    context = {"breadcrumb":{"parent":"Ui Kits", "child":"navs"}}
    return render(request,'components/ui-kits/navs.html', context)
        

@login_required(login_url="/login_home")
def shadow(request):
    context = {"breadcrumb":{"parent":"Ui Kits", "child":"Box Shadow"}}
    return render(request,'components/ui-kits/shadow.html', context)       
    

@login_required(login_url="/login_home")
def lists(request):
    context = {"breadcrumb":{"parent":"Ui Kits", "child":"Lists"}}
    return render(request,'components/ui-kits/lists.html', context) 


#-------------------------------Bonus Ui
@login_required(login_url="/login_home")
def scrollable(request):
    context = {"breadcrumb":{"parent":"Bonus Ui", "child":"Scrollable"}}
    return render(request,'components/bonus-ui/scrollable.html', context)
            

@login_required(login_url="/login_home")
def tree(request):
    context = {"breadcrumb":{"parent":"Bonus Ui", "child":"Tree View"}}
    return render(request,'components/bonus-ui/tree.html', context)
           

@login_required(login_url="/login_home")
def bootstrapnotify(request):
    context = {"breadcrumb":{"parent":"Bonus Ui", "child":"Bootstrap Notify"}}
    return render(request,'components/bonus-ui/bootstrapnotify.html', context)  
    

@login_required(login_url="/login_home")
def rating(request):
    context = {"breadcrumb":{"parent":"Bonus Ui", "child":"rating"}}
    return render(request,'components/bonus-ui/rating.html', context)
               

@login_required(login_url="/login_home")
def dropzone(request):
    context = {"breadcrumb":{"parent":"Bonus Ui", "child":"dropzone"}}
    return render(request,'components/bonus-ui/dropzone.html', context)    
    

@login_required(login_url="/login_home")
def tour(request):
    context = {"breadcrumb":{"parent":"Bonus Ui", "child":"tour"}}
    return render(request,'components/bonus-ui/tour.html', context)        
    

@login_required(login_url="/login_home")
def sweetalert2(request):
    context = {"breadcrumb":{"parent":"Bonus Ui", "child":"Sweet Alert"}}
    return render(request,'components/bonus-ui/sweetalert.html', context)    
    

@login_required(login_url="/login_home")
def animatedmodal(request):
    context = {"breadcrumb":{"parent":"Bonus Ui", "child":"Animated Modal"}}
    return render(request,'components/bonus-ui/animatedmodal.html', context)     
    

@login_required(login_url="/login_home")
def owlcarousel(request):
    context = {"breadcrumb":{"parent":"Bonus Ui", "child":"Owl Carousel"}}
    return render(request,'components/bonus-ui/owlcarousel.html', context)
              

@login_required(login_url="/login_home")
def ribbons(request):
    context = {"breadcrumb":{"parent":"Bonus Ui", "child":"Ribbons"}}
    return render(request,'components/bonus-ui/ribbons.html', context) 
             

@login_required(login_url="/login_home")
def pagination(request):
    context = {"breadcrumb":{"parent":"Bonus Ui", "child":"Pagination"}}
    return render(request,'components/bonus-ui/pagination.html', context)
        

@login_required(login_url="/login_home")
def steps(request):
    context = {"breadcrumb":{"parent":"Bonus Ui", "child":"Steps"}}
    return render(request,'components/bonus-ui/steps.html', context)
                

@login_required(login_url="/login_home")
def breadcrumb(request):
    context = {"breadcrumb":{"parent":"Bonus Ui", "child":"Breadcrumb"}}
    return render(request,'components/bonus-ui/breadcrumb.html', context)       
    

@login_required(login_url="/login_home")
def rangeslider(request):
    context = {"breadcrumb":{"parent":"Bonus Ui", "child":"Range Slider  "}}
    return render(request,'components/bonus-ui/rangeslider.html', context)     
    

@login_required(login_url="/login_home")
def imagecropper(request):
    context = {"breadcrumb":{"parent":"Bonus Ui", "child":"Image Cropper"}}
    return render(request,'components/bonus-ui/imagecropper.html', context)      
    

@login_required(login_url="/login_home")
def sticky(request):
    context = {"breadcrumb":{"parent":"Bonus Ui", "child":"Sticky"}}
    return render(request,'components/bonus-ui/sticky.html', context)        
    

@login_required(login_url="/login_home")
def basiccard(request):
    context = {"breadcrumb":{"parent":"Bonus Ui", "child":"Basic Card"}}
    return render(request,'components/bonus-ui/basiccard.html', context)
                    

@login_required(login_url="/login_home")
def creativecard(request):
    context = {"breadcrumb":{"parent":"Bonus Ui", "child":"Creative Card"}}
    return render(request,'components/bonus-ui/creativecard.html', context)  
       

@login_required(login_url="/login_home")
def tabbedcard(request):
    context = {"breadcrumb":{"parent":"Bonus Ui", "child":"Tabbed Card"}}
    return render(request,'components/bonus-ui/tabbedcard.html', context)        
       

@login_required(login_url="/login_home")
def draggablecard(request):
    context = {"breadcrumb":{"parent":"Bonus Ui", "child":"Draggable Card"}}
    return render(request,'components/bonus-ui/draggablecard.html', context)       
    

@login_required(login_url="/login_home")
def timeline1(request):
    context = {"breadcrumb":{"parent":"Bonus Ui", "child":"Timeline 1"}}
    return render(request,'components/bonus-ui/timeline1.html', context)        
    

@login_required(login_url="/login_home")
def timeline2(request):
    context = {"breadcrumb":{"parent":"Bonus Ui", "child":"Timeline 2"}}
    return render(request,'components/bonus-ui/timeline2.html', context)     

#------------------------------Builders
@login_required(login_url="/login_home")
def formbuilder1(request):
    context = {"breadcrumb":{"parent":"Builders", "child":"Form Builder 1"}}
    return render(request,'components/builders/formbuilder1.html', context)
            

@login_required(login_url="/login_home")
def formbuilder2(request):
    context = {"breadcrumb":{"parent":"Builders", "child":"Form Builder 2"}}
    return render(request,'components/builders/formbuilder2.html', context)     
    

@login_required(login_url="/login_home")
def pagebuild(request):
    context = {"breadcrumb":{"parent":"Builders", "child":"Page Builder"}}
    return render(request,'components/builders/pagebuild.html', context)
               

@login_required(login_url="/login_home")
def buttonbuilder(request):
    context = {"layout": "button-builder", "breadcrumb":{"parent":"Form Builder", "child":"Button Builder"}}
    return render(request,'components/builders/buttonbuilder.html', context)
    
#---------------------------------Animation
@login_required(login_url="/login_home")
def animate(request):
    context = {"breadcrumb":{"parent":"Animation", "child":"Animate"}}
    return render(request,'components/animation/animate.html', context)
            

@login_required(login_url="/login_home")
def scrollreval(request):
    context = {"breadcrumb":{"parent":"Animation", "child":"scroll reveal"}}
    return render(request,'components/animation/scrollreval.html', context)        
    

@login_required(login_url="/login_home")
def AOS(request):
    context = {"breadcrumb":{"parent":"Animation", "child":"AOS Animation"}}
    return render(request,'components/animation/AOS.html', context)
            

@login_required(login_url="/login_home")
def tilt(request):
    context = {"breadcrumb":{"parent":"Animation", "child":"Tilt Animation"}}
    return render(request,'components/animation/tilt.html', context)        
    

@login_required(login_url="/login_home")
def wow(request):
    context = {"breadcrumb":{"parent":"Animation", "child":"Wow Animation"}}
    return render(request,'components/animation/wow.html', context)        
    
#--------------------------Icons
@login_required(login_url="/login_home")
def flagicon(request):
    context = {"breadcrumb":{"parent":"Icons", "child":"Flag Icons"}}
    return render(request,'components/icons/flagicon.html', context) 
    

@login_required(login_url="/login_home")
def fontawesome(request):
    context = {"breadcrumb":{"parent":"Icons", "child":"Font Awesome Icon"}}
    return render(request,'components/icons/fontawesome.html', context) 
    

@login_required(login_url="/login_home")
def icoicon(request):
    context = {"breadcrumb":{"parent":"Ui Kits", "child":"ICO Icon"}}
    return render(request,'components/icons/icoicon.html', context) 
    

@login_required(login_url="/login_home")
def themify(request):
    context = {"breadcrumb":{"parent":"Icons", "child":"Themify Icon"}}
    return render(request,'components/icons/themify.html', context)  
    
@login_required(login_url="/login_home")
def feather(request):
    context = {"breadcrumb":{"parent":"Icons", "child":"Feather Icons"}}
    return render(request,'components/icons/feather.html', context)  
    

@login_required(login_url="/login_home")
def whether(request):
    context = {"breadcrumb":{"parent":"Icons", "child":"Whether Icon"}}
    return render(request,'components/icons/whether.html', context)  

#--------------------------------Buttons
@login_required(login_url="/login_home")
def buttons(request):
    context = {"breadcrumb":{"parent":"Buttons", "child":"Default Style"}}
    return render(request,'components/buttons/buttons.html', context)        
       

@login_required(login_url="/login_home")
def flat(request):
    context = {"breadcrumb":{"parent":"Buttons", "child":"Flat Buttons"}}
    return render(request,'components/buttons/flat.html', context)      
       

@login_required(login_url="/login_home")
def edge(request):
    context = {"breadcrumb":{"parent":"Buttons", "child":"edge"}}
    return render(request,'components/buttons/edge.html', context)
               

@login_required(login_url="/login_home")
def raised(request):
    context = {"breadcrumb":{"parent":"Buttons", "child":"Raised Buttons"}}
    return render(request,'components/buttons/raised.html', context)
          

@login_required(login_url="/login_home")
def group(request):
    context = {"breadcrumb":{"parent":"Buttons", "child":"Button Group"}}
    return render(request,'components/buttons/btn-group.html', context)        
         
#-------------------------------charts
@login_required(login_url="/login_home")
def echarts(request):
    context = {"breadcrumb":{"parent":"charts", "child":"Echarts"}}
    return render(request,'components/charts/echarts.html', context)
    

@login_required(login_url="/login_home")
def apex(request):
    context = {"breadcrumb":{"parent":"charts", "child":"Apex Chart"}}
    return render(request,'components/charts/apex.html', context)        
         
@login_required(login_url="/login_home")
def chartjs(request):
    context = {"breadcrumb":{"parent":"charts", "child":"ChartJS Chart"}}
    return render(request,'components/charts/chartjs.html', context)     
    

@login_required(login_url="/login_home")
def chartist(request):
    context = {"breadcrumb":{"parent":"charts", "child":"chartist"}}
    return render(request,'components/charts/chartist.html', context)   
         

@login_required(login_url="/login_home")
def flot(request):
    context = {"breadcrumb":{"parent":"charts", "child":"flot"}}
    return render(request,'components/charts/flot.html', context)   
    

@login_required(login_url="/login_home")
def google(request):
    context = {"breadcrumb":{"parent":"charts", "child":"Google Chart"}}
    return render(request,'components/charts/google.html', context)
           

@login_required(login_url="/login_home")
def knob(request):
    context = {"breadcrumb":{"parent":"charts", "child":"Knob Chart"}}
    return render(request,'components/charts/knob.html', context)     
       

@login_required(login_url="/login_home")
def morris(request):
    context = {"breadcrumb":{"parent":"charts", "child":"Morris Chart"}}
    return render(request,'components/charts/morris.html', context)
    

@login_required(login_url="/login_home")
def peity(request):
    context = {"breadcrumb":{"parent":"charts", "child":"Peity Chart"}}
    return render(request,'components/charts/peity.html', context)     
         

@login_required(login_url="/login_home")
def sparkline(request):
    context = {"breadcrumb":{"parent":"charts", "child":"sparkline"}}
    return render(request,'components/charts/sparkline.html', context)


#--------------------------------------gallery
@login_required(login_url="/login_home")
def gallery_grid(request):
    context = {"breadcrumb":{"parent":"Gallery", "child":"Gallery"}}    
    return render(request,'miscellaneous/gallery/gallery-grid/gallery.html',context)
    

@login_required(login_url="/login_home")
def grid_description(request):
    context = {"breadcrumb":{"parent":"Gallery", "child":"Gallery Grid With Description"}}    
    return render(request,'miscellaneous/gallery/gallery-grid-desc/gallery-with-description.html',context)
    

@login_required(login_url="/login_home")
def masonry_gallery(request):
    context = {"breadcrumb":{"parent":"Gallery", "child":"Masonry Gallery"}}    
    return render(request,'miscellaneous/gallery/masonry-gallery/gallery-masonry.html',context)
    

@login_required(login_url="/login_home")
def masonry_disc(request):
    context = {"breadcrumb":{"parent":"Gallery", "child":"Masonry Gallery With Description"}}    
    return render(request,'miscellaneous/gallery/masonry-with-desc/masonry-gallery-with-disc.html',context)
    

@login_required(login_url="/login_home")
def hover(request):
    context = {"breadcrumb":{"parent":"Gallery", "child":"Image Hover Effects"}}    
    return render(request,'miscellaneous/gallery/hover-effects/gallery-hover.html',context)


#------------------------------------Blog
@login_required(login_url="/login_home")
def blog_details(request):  
    context = {"breadcrumb":{"parent":"Blog", "child":"Blog Details"}}    
    return render(request,'miscellaneous/blog/blog-details/blog.html',context)
    

@login_required(login_url="/login_home")
def blog_single(request):
    context = {"breadcrumb":{"parent":"Blog", "child":"Blog Single"}}    
    return render(request,'miscellaneous/blog/blog-single/blog-single.html',context)
    

@login_required(login_url="/login_home")
def add_post(request):
    context = {"breadcrumb":{"parent":"Blog", "child":"Add Post"}}    
    return render(request,'miscellaneous/blog/add-post/add-post.html',context)
    
#--------------------------------------faq

@login_required(login_url="/login_home")
def FAQ(request):
    context = {"breadcrumb":{"parent":"FAQ", "child":"FAQ"}}    
    return render(request,'miscellaneous/FAQ/faq.html',context)
    
#---------------------------------job serach
@login_required(login_url="/login_home")
def job_cards(request):
    context = {"breadcrumb":{"parent":"Job Search", "child":"Cards View"}}    
    return render(request,'miscellaneous/job-search/cards-view/job-cards-view.html',context)
    

@login_required(login_url="/login_home")
def job_list(request):
    context = {"breadcrumb":{"parent":"Job Search", "child":"List View"}}    
    return render(request,'miscellaneous/job-search/list-view/job-list-view.html',context)
    

@login_required(login_url="/login_home")
def job_details(request):
    context = {"breadcrumb":{"parent":"Job Search", "child":"Job Details"}}    
    return render(request,'miscellaneous/job-search/job-details/job-details.html',context)
    

@login_required(login_url="/login_home")
def apply(request):
    context = {"breadcrumb":{"parent":"Job Search", "child":"Apply"}}    
    return render(request,'miscellaneous/job-search/apply/job-apply.html',context)


#------------------------------------Learning
@login_required(login_url="/login_home")
def learning_list(request):
    context = {"breadcrumb":{"parent":"Learning", "child":"Learning List"}}    
    return render(request,'miscellaneous/learning/learning-list/learning-list-view.html',context)
    
   
@login_required(login_url="/login_home")
def learning_detailed(request):
    context = {"breadcrumb":{"parent":"Learning", "child":"Detailed Course"}}    
    return render(request,'miscellaneous/learning/learning-detailed/learning-detailed.html',context)
    

#----------------------------------------Maps
@login_required(login_url="/login_home")
def maps_js(request):
    context = {"breadcrumb":{"parent":"Maps", "child":"Map JS"}}    
    return render(request,'miscellaneous/maps/maps-js/map-js.html',context)
    

@login_required(login_url="/login_home")
def vector_maps(request):
    context = {"breadcrumb":{"parent":"Maps", "child":"Vector Maps"}}
    return render(request,'miscellaneous/maps/vector-maps/vector-map.html',context)
    

#------------------------------------Editors
@login_required(login_url="/login_home")
def summernote(request):
    context = {"breadcrumb":{"parent":"Editors", "child":"Summer Note"}}    
    return render(request,'miscellaneous/editors/summer-note/summernote.html',context)
    

@login_required(login_url="/login_home")
def ckeditor(request):
    context = {"breadcrumb":{"parent":"Editors", "child":"Ck Editor"}}    
    return render(request,'miscellaneous/editors/ckeditor/ckeditor.html',context)
    

@login_required(login_url="/login_home")
def simple_mde(request):
    context = {"breadcrumb":{"parent":"Editors", "child":"MDE Editor"}}    
    return render(request,'miscellaneous/editors/simple-mde/simple-mde.html',context) 
    
@login_required(login_url="/login_home")
def ace_code(request):
    context = {"breadcrumb":{"parent":"Editors", "child":"ACE Code Editor"}}    
    return render(request,'miscellaneous/editors/ace-code/ace-code.html',context) 
    
#----------------------------knowledgeUi Kits
@login_required(login_url="/login_home")
def knowledgebase(request):
    context = {"breadcrumb":{"parent":"KnowledgeUi Kits", "child":"KnowledgeUi Kits"}}    
    return render(request,'miscellaneous/knowledgebase/knowledgebase.html',context)


#---------------------------------------------------------------------------------------
#-----------------------------support-ticket


@login_required(login_url="/login_home")
def support_ticket(request):
    context = { "breadcrumb":{"parent":"Apps", "child":"Support Ticket"}}
    return render(request,"miscellaneous/support-ticket/support-ticket.html",context)
      


#------------------------------------------Pages-------------------------------------

#---------------------------------------comingsoon
@login_required(login_url="/login_home")
def comingsoon(request):
    
    return render(request,'pages/others/comingsoon/comingsoon/comingsoon.html')
    

@login_required(login_url="/login_home")
def comingsoon_video(request):
    
    return render(request,'pages/others/comingsoon/comingsoon-video/comingsoon-bg-video.html')
    

@login_required(login_url="/login_home")
def comingsoon_img(request):
    
    return render(request,'pages/others/comingsoon/comingsoon-img/comingsoon-bg-img.html')
    
#-------------------------sample-page
@login_required(login_url="/login_home")
def sample_page(request):
    context = {"breadcrumb":{"parent":"Pages", "child":"Sample Page"}}    
    return render(request,'pages/sample-page/sample-page.html',context)
    
#--------------------------internationalization
@login_required(login_url="/login_home")
def internationalization(request):
    context = {"breadcrumb":{"parent":"Pages", "child":"Internationalization"}}
    return render(request,'pages/internationalization/internationalization.html',context)
    
#--------------------------starter-kit
@login_required(login_url="/login_home")
def starter_kit(request):
    
    return render(request,'pages/starter-kit/starter-kit.html')
    

#-----------------------------------------------others

# ------------------------------error page


@login_required(login_url="/login_home")
def error_400(request):
    
    return render(request,'pages/others/error-page/error-page/error-400.html')
    


@login_required(login_url="/login_home")
def error_401(request):
    
    return render(request,'pages/others/error-page/error-page/error-401.html')
    


@login_required(login_url="/login_home")
def error_403(request):
    
    return render(request,'pages/others/error-page/error-page/error-403.html')
    


@login_required(login_url="/login_home")
def error_404(request):
    
    return render(request,'pages/others/error-page/error-page/error-404.html')
    


@login_required(login_url="/login_home")
def error_500(request):
    
    return render(request,'pages/others/error-page/error-page/error-500.html')
    


@login_required(login_url="/login_home")
def error_503(request):
    
    return render(request,'pages/others/error-page/error-page/error-503.html')
    

#----------------------------------Authentication

@login_required(login_url="/login_home")
def login_one(request):
    
    return render(request,'pages/others/authentication/login-one/login-one.html')
    

@login_required(login_url="/login_home")
def login_simple(request):
    
    return render(request,'pages/others/authentication/login/login.html')


@login_required(login_url="/login_home")
def login_two(request):
    
    return render(request,'pages/others/authentication/login-two/login-two.html')
    


@login_required(login_url="/login_home")
def login_bs_validation(request):
    
    return render(request,'pages/others/authentication/login-bs-validation/login-bs-validation.html')
    


@login_required(login_url="/login_home")
def login_tt_validation(request):
    
    return render(request,'pages/others/authentication/login-bs-tt-validation/login-bs-tt-validation.html')
    
@login_required(login_url="/login_home")
def login_validation(request):
    
    return render(request,'pages/others/authentication/login-sa-validation/login-sa-validation.html')

@login_required(login_url="/login_home")
def sign_up(request):
    return render(request,'pages/others/authentication/sign-up/sign-up.html')  

@login_required(login_url="/login_home")
def sign_one(request):
    
    return render(request,'pages/others/authentication/sign-one/sign-up-one.html')
    

@login_required(login_url="/login_home")
def sign_two(request):
    return render(request,'pages/others/authentication/sign-two/sign-up-two.html')
    

@login_required(login_url="/login_home")
def sign_wizard(request):
    return render(request,'pages/others/authentication/sign-up-wizard/sign-up-wizard.html')    
    

@login_required(login_url="/login_home")
def unlock(request):
    
    return render(request,'pages/others/authentication/unlock/unlock.html')


@login_required
def dashboard(request):
     return render(request, 'dashboard.html')

def home(request):
    return render(request, 'signup.html')


def login_home(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
       
        
        if form.is_valid():
       
          username=form.cleaned_data.get('username')
          password=form.cleaned_data.get('password')
          user=authenticate(username=username,password=password)
          #print("je récupère le nom de l'utilisateur connecté",username)
          if user is not None:
            login(request,user)
            if 'next' in request.GET:
                nextPage = request.GET['next']
                return HttpResponseRedirect(nextPage)
            return redirect("index")
          else:
            messages.error(request,"Wrong credentials")
            return redirect("login_home")
        else:
            messages.error(request,"Wrong credentials")
            return redirect("login_home")

    else:
        form =AuthenticationForm()

       
    return render(request,'main-login.html',{"form":form,})


def logout_view(request):
    logout(request)
    return redirect('login_home')



def signup_home(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    elif request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        print("ok ok ok ok je suis connecté")
        user_exists = User.objects.filter(email=email).exists()
        if user_exists:  
            # Gérer le cas où l'utilisateur existe déjà
            # Par exemple, afficher un message d'erreur ou rediriger l'utilisateur
            return HttpResponse("Cet email est déjà associé à un compte.")
        else:
            new_user = User.objects.create_user(username=username, email=email, password=password)
            new_user.save()
            return redirect('index')

    
@login_required(login_url="/login_home")
def forget_password(request):
    
    return render(request,'pages/others/authentication/forget-password/forget-password.html')
    

@login_required(login_url="/login_home")
def reset_password(request):
    
    return render(request,'pages/others/authentication/reset-password/reset-password.html')    



@login_required(login_url="/login_home")
def maintenance(request):
    
    return render(request,'pages/others/authentication/maintenance/maintenance.html')



