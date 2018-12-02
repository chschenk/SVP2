from django.urls import path
from .views import CompetitionListView, CompetitionCreateView, PriceCreateView, AwardCreateView, CompetitionDeleteView
from .views import GroupPriceCreateView

app_name = "competition"
urlpatterns = [
	path('', CompetitionListView.as_view(), name="list-competition"),
	path('create/', CompetitionCreateView.as_view(), name="create-competition"),
	path('delete/<int:pk>', CompetitionDeleteView.as_view(), name="delete-competition"),
	path('<int:competition_pk>/price/create/', PriceCreateView.as_view(), name="create-price"),
	path('<int:competition_pk>/group_price/create/', GroupPriceCreateView.as_view(), name="create-group_price"),
	path('<int:competition_pk>/award/create/', AwardCreateView.as_view(), name="create-award"),
]
