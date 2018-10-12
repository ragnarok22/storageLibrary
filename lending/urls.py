from django.urls import path

from lending import views

app_name = 'lending'
urlpatterns = [
    path('student/list/', views.StudentListView.as_view(), name='student-query'),
    path('student/<int:pk>/detail/', views.StudentDetailView.as_view(), name='student-detail'),

    path('book/list/', views.BookListView.as_view(), name='book-list'),
    path('book/create/', views.BookCreateView.as_view(), name='book-create'),
    path('book/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'),
]
