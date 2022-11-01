"""Library_mngmnt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from library import views
# from macpath import basename
# from library import views
# from macpath import basename

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register('library/books', views.BookViewSet, basename="books")
# router.register('library/users',views.UserViewSet, basename="users")

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/v1/token',obtain_auth_token),
    path('library/register', views.UserRegistrationView.as_view()),
    path('library/token', TokenObtainPairView.as_view()),
    path('library/token/refresh', TokenRefreshView.as_view()),
    path('library/user/issue', views.IssueBookView.as_view()),
    path('library/user/return/<int:id>', views.IssueBookView.as_view()),
    path('library/user/search', views.SearchView.as_view()),
    path('library/user/bookdetail/<int:id>', views.BookDetails.as_view()),


]+router.urls
