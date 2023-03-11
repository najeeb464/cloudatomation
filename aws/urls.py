from django.urls import path
from rest_framework.routers import DefaultRouter,SimpleRouter
from .views import (AccountConfigurationView,UserProfileView,
                    S3ListView,S3ObjectListView,RDSListView,
                    RDSDetailView,EC2ListView,EC2Start,EC2Stop,
                    S3StatsView,RDSGraphView,EC2GraphView,ChangeAccountStatus,AccountStatus,EC2StateStatsView,
                    Ec2FilterChoices,RDSFilterChoices,S3GraphView)
router = SimpleRouter()
router.register(r'account/configure', AccountConfigurationView)
urlpatterns = [
    path('user/profile'                             ,UserProfileView.as_view()),
    path('<account_id>/s3/'                         ,S3ListView.as_view(),name="s3_list"),
    path("<account_id>/s3/<bucket_name>/objects/"   ,S3ObjectListView.as_view(),name="s3_object_list"),
    path('<account_id>/rds/graph/'                  ,RDSGraphView.as_view()),
    path('<account_id>/rds/'                        ,RDSListView.as_view()),
    path('<account_id>/rds/<instance_arn>/'         ,RDSDetailView.as_view()),
    path('<account_id>/ec2/'                        ,EC2ListView.as_view()),
    path('<account_id>/ec2/graph/'                  ,EC2GraphView.as_view()),
    path('<account_id>/ec2/<instance_id>/stop/'     ,EC2Stop.as_view(),name="ec2_stop"),
    path('<account_id>/ec2/<instance_id>/start/'    ,EC2Start.as_view(),name="ec2_start"),
    path('<account_id>/ec2/state/statistics/'       ,EC2StateStatsView.as_view(),name="ec2_status_stast"),
    path('<account_id>/s3/graph/'                  ,S3GraphView.as_view()),


    
    path('<account_id>/s3/stast/'                   ,S3StatsView.as_view()),
    path('<account_id>/change/status/'              ,ChangeAccountStatus.as_view()),
    path('<account_id>/ec2/filter/choices'          ,Ec2FilterChoices.as_view()),
     path('<account_id>/rds/filter/choices'         ,RDSFilterChoices.as_view()),
    path('check/account/'                           ,AccountStatus.as_view()),
    


]+router.urls
