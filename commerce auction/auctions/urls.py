from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newlist",views.newlist,name="newlist"),
    path("categories",views.categories,name="categories"),
    path("watchlist",views.watchlist,name="watchlist"),
    path("addtowatchlist/<int:listing_id>",
         views.addtowatchlist, name="addtowatchlist"),
    path("viewlisting/<int:listing_id>", views.viewlisting, name="view_listing"),
    path("addcomment/<int:listing_id>",views.addcomment,name="addcomment"),
    path("closebid/<int:listing_id>",views.closebid,name="closebid"),
    path("winlist",views.winlist,name="winlist"),
    path("category/<str:category>",views.category,name="category")
    

]

urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
