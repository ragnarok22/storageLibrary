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
    path('book/<int:pk>/detail/', views.BookDetailView.as_view(), name='book-detail'),
    path('book/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'),

    path('lending/create/', views.LendingCreateView.as_view(), name='lending-create'),
    path('lending/query/', views.LendingQueryView.as_view(), name='lending-query'),
    path('lending/<int:pk>/detail/', views.LendingDetailView.as_view(), name='lending-detail'),
    path('lending/<int:pk>/delete/', views.LendingDeleteView.as_view(), name='lending-delete'),

    path('bibliographic/create/', views.BibliographicPlanCreateView.as_view(), name='bibliographic-create'),
    path('bibliographic/list/', views.BibliographicPlanListView.as_view(), name='bibliographic-list'),
    path('bibliographic/<int:pk>/detail/', views.BibliographicPlanDetailView.as_view(), name='bibliographic-detail'),
    path('bibliographic/<int:pk>/update/', views.BibliographicPlanUpdateView.as_view(), name='bibliographic-update'),
    path('bibliographic/<int:pk>/delete/', views.BibliographicPlanDeleteView.as_view(), name='bibliographic-delete'),

    path('study/topic/create/', views.StudyTopicCreateView.as_view(), name='study-topic-create'),
    path('study/topic/list/', views.StudyTopicListView.as_view(), name='study-topic-list'),
    path('study/topic/<int:pk>/detail/', views.StudyTopicDetailView.as_view(), name='study-topic-detail'),
    path('study/topic/<int:pk>/update/', views.StudyTopicUpdateView.as_view(), name='study-topic-update'),
    path('study/topic/<int:pk>/delete/', views.StudyTopicDeleteView.as_view(), name='study-topic-delete'),
]
