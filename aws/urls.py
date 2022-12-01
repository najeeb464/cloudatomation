from django.urls import path
from rest_framework.routers import DefaultRouter,SimpleRouter
from .views import AccountConfigurationView,UserProfileView,S3ListView,S3ObjectListView,RDSListView,RDSDetailView
router = SimpleRouter()
router.register(r'account/configure', AccountConfigurationView)
urlpatterns = [
    path('user/profile',UserProfileView.as_view()),
    path('s3/',S3ListView.as_view(),name="s3_list"),
    path("s3/<bucket_name>/objects/",S3ObjectListView.as_view(),name="s3_object_list"),
    path('rds/',RDSListView.as_view()),
    path('rds/<instance_arn>/',RDSListView.as_view()),

]+router.urls
