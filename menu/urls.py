from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.landing, name="landing"),
    path("login/", views.auth.login, name="login"),
    path("signup/", views.auth.signup, name="signup"),
    path("menus/", views.survey.survey_list, name="survey-list"),
    path("menus/<int:pk>/", views.survey.detail, name="survey-detail"),
    path("menus/create/", views.survey.create, name="survey-create"),
    path("menus/<int:pk>/delete/", views.survey.delete, name="survey-delete"),
    path("menus/<int:pk>/edit/", views.survey.edit, name="survey-edit"),
    path("menus/<int:pk>/question/", views.survey.question_create, name="survey-question-create"),
    path(
        "menus/<int:survey_pk>/question/<int:question_pk>/option/",
        views.survey.option_create,
        name="survey-option-create",
    ),
    path("menus/<int:pk>/start/", views.survey.start, name="survey-start"),
    path("menus/<int:survey_pk>/submit/<int:sub_pk>/", views.survey.submit, name="survey-submit"),
    path("menus/<int:pk>/thanks/", views.survey.thanks, name="survey-thanks"),
    path("admin", admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls)),] + urlpatterns

