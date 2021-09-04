from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

urlpatterns = [
    # path("", views.index, name="index"),
    path("", views.index, name='index'),

    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path('list-new-item', views.list_new_item, name="list-new-item"),
    path('thank-you', views.thank_you, name='thank-you'),
    path('<int:id>', views.item_page, name='item-page'),

    path('categories', views.Categories.as_view(), name='categories'),
    path('categories/<int:cat_id>', views.items_by_cat, name='list-by-cat'),

    path('watchlist', views.watchlist_items, name='watchlist'),

    path('watchlist/<int:item_id>', views.watchlist_manipulator, name='add-remove-watch'),

    path('add-bid/<int:item_id>', views.add_bid, name='add-bid'),

    path('close_listing/<int:item_id>', views.close_listing, name='close-listing'),

    path('add-comment/<int:item_id>', views.add_comment, name='add-comment')
]

urlpatterns += staticfiles_urlpatterns()