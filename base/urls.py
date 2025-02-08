from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    # Core Pages
    path('', views.home, name="home"),
    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),

    # Room Management
    path('room/<str:pk>/', views.room, name="room"),
    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),

    # User Management
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('update-user/', views.updateUser, name="update-user"),

    # Message Management
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),
]