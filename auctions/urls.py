from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    # path("", views.index, name="index"),
    path("", views.index, name='index'),

    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path('list-new-item', views.list_new_item, name="list-new-item"),
    path('thank-you', views.thank_you, name='thank-you'),
    path('<int:pk>', views.ItemCard.as_view(), name='item-card'),

    path('categories', views.Categories.as_view(), name='categories'),
    path('categories/<int:cat_id>', views.CategoriesList.as_view(), name='list-by-cat'),

    path('watchlist', views.Watchlist.as_view(), name='watchlist'),

    path('watchlist/<int:item_id>', views.add_to_watchlist, name='add-watch')

    # path('add-bid', login_required(views.AddBid.as_view()), name='add-bid'),
]
