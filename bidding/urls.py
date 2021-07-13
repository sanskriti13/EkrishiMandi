from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
path('index/',views.index,name="index"),
path('bid/',views.bid,name="bid"),
path('update/<int:id>/',views.updatebid,name="update"),
path('end/<int:id>/',views.updatebid,name="end"),
path('msp/',views.mspchart,name="msp"),
path('',views.home,name="home"),
path('about/',views.about,name="about")
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
