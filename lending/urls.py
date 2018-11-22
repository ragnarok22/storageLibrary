from django.urls import path

from lending import views

app_name = 'lending'
urlpatterns = [
    path('student/list/', views.StudentListView.as_view(), name='student-query'),
    path('student/create/', views.StudentCreateView.as_view(), name='student-create'),
    path('student/<int:pk>/update/', views.StudentUpdateView.as_view(), name='student-update'),
    path('student/<int:pk>/delete/', views.StudentDeleteView.as_view(), name='student-delete'),
    path('student/<int:pk>/detail/', views.StudentDetailView.as_view(), name='student-detail'),

    path('book/list/', views.BookListView.as_view(), name='book-list'),
    path('book/create/', views.BookCreateView.as_view(), name='book-create'),
    path('book/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'),
]
