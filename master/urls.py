from django.urls import path
from master import views
urlpatterns = [
    path('company/', views.companyView, name="company"),
    path('send_mail/', views.MailSender, name="send_mail"), 
]
# #######@12345