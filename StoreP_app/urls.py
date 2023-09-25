from django.urls import path
from rest_framework import routers
from StoreP_app.views import RestroViewSet

default_router = routers.SimpleRouter()
default_router.register("restro", RestroViewSet, basename="restro")

urlpatterns = default_router.urls
