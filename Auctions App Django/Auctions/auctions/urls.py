from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create",views.create,name="create"),
    path("category",views.category,name="category"),
    path("watchedlist",views.watch,name="watch"),
    path("mylist",views.mylist,name="mylist"),
    path("auction/<int:list_id>",views.item,name="item"),
    path("comment/<int:list_id>",views.comment,name="comment"),
    path("category_sort/<str:category_kind>",views.category_sort,name="category_sort"),
    path("put_to_watch_list/<int:list_id>",views.put_to_watch_list,name="add_watch")

]
