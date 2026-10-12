from django.contrib import admin
from django.urls import include, path

from blog import views as blog_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.urls")),
    path("pages/", include("pages.urls")),
    path("auth/registration/", blog_views.registration, name="registration"),
    path("auth/", include("django.contrib.auth.urls")),
]

handler403 = "pages.views.page_403"
handler404 = "pages.views.page_404"
handler500 = "pages.views.page_500"
