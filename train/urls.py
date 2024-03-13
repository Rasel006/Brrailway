from django.urls import path
from . import views


urlpatterns = [
    path('add/', views.add_train, name='add_train'),
    path('search/', views.search_train, name='search_train'),
    path('book/<int:train_id>/', views.book_ticket, name='book_ticket'),
    path('details/<int:id>',views.DetailsTrainView.as_view(), name='details_train'),
    path('purchase/<int:id>/', views.PurchaseView.as_view(), name='purchase_train'),
    path('delete_review/<int:pk>/', views.ReviewDeleteView.as_view(), name='delete_review'),
    path('review/update/<int:review_id>/', views.ReviewUpdateView.as_view(), name='update_review'),

]