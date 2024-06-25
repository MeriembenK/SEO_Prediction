from django.urls import path
from . import views
from .views import *
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    #-------------------------General(Dashboards,Widgets & Layout)---------------------------------------
    path('', home, name="home"),
    #path('register/', register, name='register'), 
    path('dashboard/', dashboard, name='dashboard'),
    path('index', views.index, name="index"),
    path('centre', views.index, name="centre"),
    path('url', views.url, name="url"),
    path('handle_keyword/', views.handle_keyword, name='handle_keyword'),
    path('delete_url_predected/', delete_url_predected, name='delete_url_predected'),
    #-------------------------General(Dashboards,Widgets & Layout)---------------------------------------
    path('dashboard_02.html', views.dashboard_02, name="dashboard_02"),
    path('online_course', views.online_course, name="online_course"),
    path('crypto', views.crypto, name="crypto"),


    # #-----------------------Widgets
    path('general_widget', views.general_widget, name="general_widget"),
    path('delete-tests/', views.delete_tests, name='delete_tests'),
    path('chart_widget', views.chart_widget, name="chart_widget"),

    #------------------------Layout
    path('box_layout', views.box_layout, name="box_layout"),
    path('layout_rtl', views.layout_rtl, name="layout_rtl"),
    path('layout_dark', views.layout_dark, name="layout_dark"),
    path('hide_on_scroll', views.hide_on_scroll, name="hide_on_scroll"),
    path('footer_light', views.footer_light, name="footer_light"),
    path('footer_dark', views.footer_dark, name="footer_dark"),
    path('footer_fixed', views.footer_fixed, name="footer_fixed"),

    #--------------------------------Applications---------------------------------

    #---------------------------Project
    path('projects', views.projects, name="projects"),
    path('projectcreate', views.projectcreate, name="projectcreate"), 

    #------------------------File Manager
    path('file_manager', views.file_manager, name="file_manager"),

    #------------------------Kanban Board
    path('kanban', views.kanban, name="kanban"),


     #--------------------------emails
    path('email_application', views.email_application, name="email_application"),
    path('email_compose', views.email_compose, name="email_compose"),

    #--------------------------------chat
    path('chat_app', views.chat_app, name="chat_app"),
    path('chat_video', views.chat_video, name="chat_video"),

    #---------------------------------user
    path('user_profile', views.user_profile, name="user_profile"),
    path('edit_profile', views.edit_profile, name="edit_profile"),
    path('user_cards', views.user_cards, name="user_cards"),

    #------------------------bookmark
    path('bookmark', views.bookmark, name="bookmark"),

    #------------------------contacts
    path('contacts', views.contacts, name="contacts"),

    #------------------------task
    path('task', views.task, name="task"),

    #------------------------calendar
    path('calendar_basic', views.calendar_basic, name="calendar_basic"),

    #------------------------social-app
    path('social_app', views.social_app, name="social_app"),
    #------------------------search
    path('search', views.search, name="search"),

    #--------------------------------Forms & Table-----------------------------------------------
    #--------------------------------Forms------------------------------------

    #------------------------form-controls
    path('form_validation', views.form_validation, name="form_validation"),
    path('base_input', views.base_input, name="base_input"),
    path('radio_checkbox_control', views.radio_checkbox_control, name="radio_checkbox_control"),
    path('input_group', views.input_group, name="input_group"),
    path('megaoptions', views.megaoptions, name="megaoptions"),

    #---------------------------form widgets
    path('datepicker', views.datepicker, name="datepicker"),
    path('time_picker', views.time_picker, name="time_picker"),
    path('datetimepicker', views.datetimepicker, name="datetimepicker"),
    path('daterangepicker', views.daterangepicker, name="daterangepicker"),
    path('touchspin', views.touchspin, name="touchspin"),
    path('select2', views.select2, name="select2"),
    path('switch', views.switch, name="switch"),
    path('typeahead', views.typeahead, name="typeahead"),
    path('clipboard', views.clipboard, name="clipboard"),
    
    #--------------------------------form layout
    path('default_form', views.default_form, name="default_form"),
    path('form_wizard_one', views.form_wizard_one, name="form_wizard_one"),
    path('form_wizard_two', views.form_wizard_two, name="form_wizard_two"),
    path('form_wizard_three', views.form_wizard_three, name="form_wizard_three"),

    #--------------------------------------Table--------------------------------------------------
    #------------------------bootstrap table
    path('basic_table', views.basic_table, name="basic_table"),
    path('sizing_table', views.sizing_table, name="sizing_table"),
    path('border_table', views.border_table, name="border_table"),
    path('styling_table', views.styling_table, name="styling_table"),
    path('table_components', views.table_components, name="table_components"),

    #-------------------------data table
    path('datatable_basic_init', views.datatable_basic_init, name="datatable_basic_init"),
    path('datatable_advance', views.datatable_advance, name="datatable_advance"),
    path('datatable_styling', views.datatable_styling, name="datatable_styling"),
    path('datatable_AJAX', views.datatable_AJAX, name="datatable_AJAX"),
    path('datatable_server_side', views.datatable_server_side, name="datatable_server_side"),
    path('datatable_plugin', views.datatable_plugin, name="datatable_plugin"),
    path('datatable_API', views.datatable_API, name="datatable_API"),
    path('datatable_data_source', views.datatable_data_source, name="datatable_data_source"),

    #---------------------------EXdata table
    path('ext_autofill', views.ext_autofill, name="ext_autofill"),
    path('ext_basic_button', views.ext_basic_button, name="ext_basic_button"),
    path('ext_col_reorder', views.ext_col_reorder, name="ext_col_reorder"),
    path('ext_fixed_header', views.ext_fixed_header, name="ext_fixed_header"),
    path('ext_html_5_data_export', views.ext_html_5_data_export, name="ext_html_5_data_export"),
    path('ext_key_table', views.ext_key_table, name="ext_key_table"),
    path('ext_responsive', views.ext_responsive, name="ext_responsive"),
    path('ext_row_reorder', views.ext_row_reorder, name="ext_row_reorder"),
    path('ext_scroller', views.ext_scroller, name="ext_scroller"),

    #-----------------------------jsgrid_table
    path('jsgrid_table', views.jsgrid_table, name="jsgrid_table"),

    #------------------Components------UI Components-----Elements ----------->

    #-----------------------------Ui kits
    path('statecolor', views.statecolor, name="statecolor"),
    path('typography', views.typography, name="typography"),
    path('avatars', views.avatars, name="avatars"),
    path('helper', views.helper, name="helper"),
    path('grid', views.grid, name="grid"),
    path('tag-pills', views.tagpills, name="tag-pills"),
    path('progressbar', views.progressbar, name="progressbar"),
    path('modal', views.modal, name="modal"),
    path('alert', views.alert, name="alert"),
    path('popover', views.popover, name="popover"),
    path('tooltip', views.tooltip, name="tooltip"),
    path('spiners', views.spiners, name="spiners"),
    path('dropdown', views.dropdown, name="dropdown"),
    path('accordion', views.accordion, name="accordion"),
    path('bootstraptab', views.bootstraptab, name="bootstraptab"),
    path('linetab', views.linetab, name="linetab"),
    path('navs', views.navs, name="navs"),
    path('shadow', views.shadow, name="shadow"),
    path('lists', views.lists, name="lists"),

    #-------------------------------Bonus Ui    
    path('scrollable/', views.scrollable, name="scrollable"),
    path('tree/', views.tree, name="tree"),
    path('bootstrapnotify/', views.bootstrapnotify, name="bootstrapnotify"),
    path('rating/', views.rating, name="rating"),
    path('dropzone/', views.dropzone, name="dropzone"),
    path('tour/', views.tour, name="tour"),
    path('sweetalert2', views.sweetalert2, name="sweetalert2"),
    path('animatedmodal/', views.animatedmodal, name="animatedmodal"),
    path('owlcarousel/', views.owlcarousel, name="owlcarousel"),
    path('ribbons/', views.ribbons, name="ribbons"),
    path('pagination/', views.pagination, name="pagination"),
    path('steps/', views.steps, name="steps"), 
    path('breadcrumb/', views.breadcrumb, name="breadcrumb"),
    path('rangeslider/', views.rangeslider, name="rangeslider"),
    path('imagecropper/', views.imagecropper, name="imagecropper"),
    path('sticky/', views.sticky, name="sticky"),
    path('basiccard/', views.basiccard, name="basiccard"),
    path('creativecard/', views.creativecard, name="creativecard"),
    path('tabbedcard/', views.tabbedcard, name="tabbedcard"),
    path('draggablecard/', views.draggablecard, name="draggablecard"),
    path('timeline1/', views.timeline1, name="timeline1"),
    path('timeline2/', views.timeline2, name="timeline2"),

    #------------------------------Builders
    path('formbuilder1/', views.formbuilder1, name="formbuilder1"),
    path('formbuilder2/', views.formbuilder2, name="formbuilder2"),
    path('pagebuild/', views.pagebuild, name="pagebuild"),
    path('buttonbuilder/', views.buttonbuilder, name="buttonbuilder"),

    #---------------------------------Animation    
    path('animate/', views.animate, name="animate"),
    path('scrollreval/', views.scrollreval, name="scrollreval"),
    path('AOS/', views.AOS, name="AOS"),
    path('tilt/', views.tilt, name="tilt"),
    path('wow/', views.wow, name="wow"),

    #--------------------------Icons
    path('flagicon/', views.flagicon, name="flagicon"),
    path('fontawesome/', views.fontawesome, name="fontawesome"),
    path('icoicon/', views.icoicon, name="icoicon"),
    path('themify/', views.themify, name="themify"),
    path('feather/', views.feather, name="feather"),
    path('whether/', views.whether, name="whether"),

    #--------------------------------Buttons
    path('buttons/', views.buttons, name="buttons"),
    path('flat/', views.flat, name="flat"),
    path('edge/', views.edge, name="edge"),
    path('raised/', views.raised, name="raised"),
    path('group', views.group, name="group"),
    path('echarts', views.echarts, name="echarts"),
    path('apex', views.apex, name="apex"),
    path('chartjs', views.chartjs, name="chartjs"),
    path('chartist', views.chartist, name="chartist"),
    path('flot', views.flot, name="flot"),
    path('google', views.google, name="google"),
    path('knob', views.knob, name="knob"),
    path('morris', views.morris, name="morris"),
    path('peity', views.peity, name="peity"),
    path('sparkline', views.sparkline, name="sparkline"),

    #----------------------------------------------------Pages-----------------------------------

    #-----------------sample-page
    path('sample_page', views.sample_page , name="sample_page"),

    #-----------------internationalization
    path('internationalization', views.internationalization, name="internationalization"),

   #----------------starter-kit
   path('starter_kit', views.starter_kit, name="starter_kit"),
 
   #--------------------Errror pae
   path('error_400', views.error_400, name="error_400"),
   path('error_401', views.error_401, name="error_401"),
   path('error_403', views.error_403, name="error_403"),
   path('error_404', views.error_404, name="error_404"),
   path('error_500', views.error_500, name="error_500"),
   path('error_503', views.error_503, name="error_503"),

   #---------------------Authentication
   path('login_simple', views.login_simple, name="login_simple"),
   path('login_one', views.login_one, name="login_one"),
   path('login_two', views.login_two, name="login_two"),
   path('login_bs_validation', views.login_bs_validation, name="login_bs_validation"),
   path('login_tt_validation', views.login_tt_validation, name="login_tt_validation"),
   path('login_validation', views.login_validation, name="login_validation"),
   path('sign_up/', views.sign_up, name="sign_up" ),
   path('sign_one', views.sign_one, name="sign_one" ),
   path('sign_two', views.sign_two, name="sign_two" ),
   path('sign_wizard', views.sign_wizard, name="sign_wizard"),
   path('unlock', views.unlock , name="unlock"),
   path('forget_password', views.forget_password, name="forget_password"),
   path('reset_password', views.reset_password, name="reset_password"),
   path('maintenance', views.maintenance, name="maintenance"),

   #---------------------------------------comingsoon

   path('comingsoon', views.comingsoon, name="comingsoon"),
   path('comingsoon_video', views.comingsoon_video, name="comingsoon_video"),
   path('comingsoon_img', views.comingsoon_img, name="comingsoon_img"),

#------------------------------------------Miscellaneous----------------- -------------------------

#------------------------gallery

   path('gallery_grid', views.gallery_grid, name="gallery_grid"),
   path('grid_description', views.grid_description, name="grid_description"),
   path('masonry_gallery', views.masonry_gallery, name="masonry_gallery"),
   path('masonry_disc', views.masonry_disc, name="masonry_disc"),
   path('hover', views.hover, name="hover"),

#-------------------------Blog
   path('blog_details', views.blog_details, name="blog_details"),
   path('blog_single', views.blog_single, name="blog_single"),
   path('add_post', views.add_post, name="add_post"),

#-------------------------faq
   path('FAQ', views.FAQ, name="FAQ"),

#-------------------------job serch

   path('job_cards', views.job_cards, name="job_cards"),
   path('job_list', views.job_list, name="job_list"),
   path('job_details', views.job_details, name="job_details"),
   path('apply', views.apply, name="apply"),

#-------------------------Learning
   path('learning_list', views.learning_list, name="learning_list"),
   path('learning_detailed', views.learning_detailed, name="learning_detailed"),

#-------------------------maps
   path('maps_js', views.maps_js, name="maps_js"),
   path('vector_maps', views.vector_maps, name="vector_maps"),


#------------------------------------Editors
   path('summernote', views.summernote, name="summernote"),
   path('ckeditor', views.ckeditor, name="ckeditor"),
   path('simple_mde', views.simple_mde, name="simple_mde"),
   path('ace_code', views.ace_code, name="ace_code"),


#-----------------------------knowledgebase
   path('knowledgebase', views.knowledgebase, name="knowledgebase"),

#-----------------------------support-ticket
   path('support_ticket', views.support_ticket, name="support_ticket"),

#-----------------------------------------------------------------------------------

   path('signup_home',views.signup_home,name='signup_home'),
   path('login_home', views.login_home, name="login_home"),
   path('logout_view', views.logout_view, name="logout_view"),
  #---------------------Authentication
   path('signup_home',views.signup_home,name='signup_home'),
   path('login_home', views.login_home, name="login_home"),
   path('logout_view', views.logout_view, name="logout_view"),
   path('forget-password.html', views.forget_password, name='forget_password_html'),
   path('reset_password', views.reset_password, name="reset_password"),
    
    ]
