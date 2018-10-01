from django.urls import path

from lending import views

app_name = 'lending'
urlpatterns = [
    path('list/', views.BookListView.as_view(), name='book-list'),
    path('student/list/', views.StudentListView.as_view(), name='student-query'),
    path('student/<int:pk>/detail/', views.StudentDetailView.as_view(), name='student-detail'),
]
