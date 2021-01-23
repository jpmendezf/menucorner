from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path

from . import views

urlpatterns = [
    path("", views.landing, name="landing"),
    path("login/", views.auth.login, name="login"),
    path("signup/", views.auth.signup, name="signup"),
    path("menus/", views.menu.menu_list, name="menu-list"),
    path("menus/<int:pk>/", views.menu.detail, name="menu-detail"),
    path("menus/create/", views.menu.create, name="menu-create"),
    path("menus/<int:pk>/delete/", views.menu.delete, name="menu-delete"),
    path("menus/<int:pk>/edit/", views.menu.edit, name="menu-edit"),
    path("menus/<int:pk>/question/", views.menu.lunch_create, name="menu-lunch-create"),
    path(
        "menus/<int:menu_pk>/lunch/<int:lunch_pk>/option/",
        views.menu.option_create,
        name="menu-option-create",
    ),
    path("menus/<int:pk>/start/", views.menu.start, name="menu-start"),
    path("menus/<int:menu_pk>/submit/<int:sub_pk>/", views.menu.submit, name="menu-submit"),
    path("menus/<int:pk>/thanks/", views.menu.thanks, name="menu-thanks"),
    path("admin", admin.site.urls),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls)),] + urlpatterns

