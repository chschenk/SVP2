from django.urls import path
from .views import CompetitionListView, CompetitionCreateView, PriceCreateView, AwardCreateView, CompetitionDeleteView
from .views import GroupPriceCreateView, CompetitionUpdateView, WeaponListView, WeaponCreateView, WeaponDeleteView
from .views import WeaponUpdateView, CompetitionPerformView, ReleaseWeaponView

app_name = "competition"
urlpatterns = [
	path('', CompetitionListView.as_view(), name="list-competition"),
	path('create/', CompetitionCreateView.as_view(), name="create-competition"),
	path('edit/<int:pk>', CompetitionUpdateView.as_view(), name='edit-competition'),
	path('delete/<int:pk>', CompetitionDeleteView.as_view(), name="delete-competition"),
	path('perform/<int:pk>', CompetitionPerformView.as_view(), name="perform-competition"),
	path('perform/<int:pk>/release-weapon/<int:weapon_pk>', ReleaseWeaponView.as_view(), name="release-weapon"),
	#path('<int:competition_pk>/create-record/<int:weapon_pk>', SetWeaponRecordView.as_view(), name="create-weapon-record"),
	path('<int:competition_pk>/price/create/', PriceCreateView.as_view(), name="create-price"),
	path('<int:competition_pk>/group_price/create/', GroupPriceCreateView.as_view(), name="create-group_price"),
	path('<int:competition_pk>/award/create/', AwardCreateView.as_view(), name="create-award"),
	path('weapon/', WeaponListView.as_view(), name="list-weapon"),
	path('weapon/create/', WeaponCreateView.as_view(), name="create-weapon"),
	path('weapon/delete/<int:pk>', WeaponDeleteView.as_view(), name="delete-weapon"),
	path('weapon/edit/<int:pk>', WeaponUpdateView.as_view(), name="edit-weapon"),
]
