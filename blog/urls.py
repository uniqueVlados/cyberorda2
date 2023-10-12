from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView

)
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('my/', views.my_home, name='blog-my-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/schedule', views.schedule, name='post-schedule'),
    path('rating/', views.rating, name='rating'),
    # not render
    # path('save_tour/<str:game>/<str:tour>', views.save_tour, name='save-tour'),
    path('reload_filter/', views.reload_filter, name='reload_filter'),
    path('save_tour_1/', views.save_tour_1, name='save-tour-1'),
    path('save_tour_2/', views.save_tour_2, name='save-tour-2'),
    path('save_tour_3/', views.save_tour_3, name='save-tour-3'),
    path('save_tour_4/', views.save_tour_4, name='save-tour-4'),
    path('save_tour_5/', views.save_tour_5, name='save-tour-5'),
    path('save_tour_6/', views.save_tour_6, name='save-tour-6'),
    path('save_tour_7/', views.save_tour_7, name='save-tour-7'),
    path('save_tour_8/', views.save_tour_8, name='save-tour-8'),
    path('reset/<str:game>/<str:tour>', views.reset, name='reset'),
    path('new_files/', views.new_files, name='new-files'),
    path('results/<str:game>/<str:tour>', views.results, name='results'),
    path('del_dir_of_game/', views.del_dir_of_game, name='del_dir_of_game'),
    path('download/<str:game>/<str:tour>', views.download, name='download'),
    path('download_shedule/<str:game>/<str:tour>', views.download_shedule, name='download_shedule'),
]
