from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'quick_note'

urlpatterns = [
    path('', views.home, name="homepage"),
    path('authenticate/signup/', csrf_exempt(views.signup), name="signup"),
    path('authenticate/verifysignup/',  csrf_exempt(views.verifysignup), name="verifysignup"),
    # path('authenticate/verifylogin/',  csrf_exempt(views.verify_login), name="verifylogin"),
    path('authenticate/activate_account/<uid64>/<token>/',  views.activate_account, name="activate_account"),
    path('authenticate/login/', views.userlogin, name="login"),
    path('authenticate/forgot_password/', views.forgot_password, name="forgot_password"),
    path('authenticate/password_reset/<uid64>/<token>/', views.password_reset, name="password_reset"),
    path('settings/', views.settings, name="settings"),
    path('mynotes/', views.mynotes, name="mynotes"),
    path('mynotes/search/', csrf_exempt(views.search_note), name="search_note"),
    path('mynotes/delete_note/<int:note_id>/', views.delete_note, name="delete_note"),
    path('publicnotes/u/<str:user_id>/<str:public_note_id>/', views.public_notes, name="public_notes"),
    path('mynotes/<int:note_id>/', views.note, name="note"),
    path('mynotes/generate_note_link/<int:note_id>/', views.generate_note_link, name="generate_note_link"),
    path('addnote/', csrf_exempt(views.addnote), name="addnote"),
    path('sharednotes/', views.sharednotes, name="sharednotes"),
    path('privatenotes/', views.privatenotes, name="privatenotes"),
    path('taskmanager/', views.taskmanager, name="taskmanager"),
    path('logout/', views.userLogout, name="logout"),

]