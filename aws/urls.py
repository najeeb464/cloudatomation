from django.urls import path
from rest_framework.routers import DefaultRouter,SimpleRouter
from .views import AccountConfigurationView,UserProfileView,S3ListView,S3ObjectListView,RDSListView,RDSDetailView,EC2ListView
router = SimpleRouter()
router.register(r'account/configure', AccountConfigurationView)
urlpatterns = [
    path('user/profile',UserProfileView.as_view()),
    path('<account_id>/s3/',S3ListView.as_view(),name="s3_list"),
    path("<account_id>/s3/<bucket_name>/objects/",S3ObjectListView.as_view(),name="s3_object_list"),
    path('<account_id>/rds/',RDSListView.as_view()),
    path('<account_id>/rds/<instance_arn>/',RDSDetailView.as_view()),
    path('<account_id>/ec2/',EC2ListView.as_view()),

]+router.urls
