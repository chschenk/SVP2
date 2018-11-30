from django.urls import path
from .views import ClubCreateView, ClubListView, ClubDeleteView, ClubDetailView, ClubUpdateView, ClubAutocompleteView
from .views import MemberCreateView, MemberDetailView, MemberDeleteView, MemberUpdateView, MemberAutocompleteView
app_name = "member"
urlpatterns = [
	path('create', MemberCreateView.as_view(), name="create-member"),
	path('create/<int:club_pk>', MemberCreateView.as_view(), name="create-club-member"),
	path('detail/<int:pk>', MemberDetailView.as_view(), name="detail-member"),
	path('edit/<int:pk>', MemberUpdateView.as_view(), name="edit-member"),
	path('delete/<int:pk>', MemberDeleteView.as_view(), name="delete-member"),
	path('autocomplete', MemberAutocompleteView.as_view(), name="autocomplete-member"),
    path('club/create/', ClubCreateView.as_view(), name="create-club"),
    path('club/', ClubListView.as_view(), name="list-club"),
	path('club/<int:pk>/', ClubDetailView.as_view(), name="detail-club"),
	path('club/<int:pk>/edit', ClubUpdateView.as_view(), name="edit-club"),
    path('club/<int:pk>/delete', ClubDeleteView.as_view(), name="delete-club"),
	path('club-autocomplete', ClubAutocompleteView.as_view(), name="autocomplete-club"),
]
