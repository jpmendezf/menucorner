from django.db import transaction
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.forms.formsets import formset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from ..models import Menu, Lunch, Answer, Submission
from ..forms import MenuForm, LunchForm, OptionForm, AnswerForm, BaseAnswerFormSet


@login_required
def menu_list(request):
    """User can view all their menus"""
    menus = Menu.objects.filter(creator=request.user).order_by("-created_at").all()
    return render(request, "menu/list.html", {"menu": menus})


@login_required
def detail(request, pk):
    """User can view an active menu"""
    try:
        menu = Menu.objects.prefetch_related("lunch_set__option_set").get(
            pk=pk, creator=request.user, is_active=True
        )
    except Menu.DoesNotExist:
        raise Http404()

    lunchs = menu.lunch_set.all()

    # Calculate the results.
    # This is a native implementation and it could be optimised to hit the database less.
    for lunch in lunchs:
        option_pks = lunch.option_set.values_list("pk", flat=True)
        total_answers = Answer.objects.filter(option_id__in=option_pks).count()
        for option in lunch.option_set.all():
            num_answers = Answer.objects.filter(option=option).count()
            option.percent = 100.0 * num_answers / total_answers if total_answers else 0

    host = request.get_host()
    public_path = reverse("menu-start", args=[pk])
    public_url = f"{request.scheme}://{host}{public_path}"
    num_submissions = menu.submission_set.filter(is_complete=True).count()
    return render(
        request,
        "menu/detail.html",
        {
            "menu": menu,
            "public_url": public_url,
            "lunchs": lunchs,
            "num_submissions": num_submissions,
        },
    )


@login_required
def create(request):
    """User can create a new menu"""
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.creator = request.user
            menu.save()
            return redirect("menu-edit", pk=menu.id)
    else:
        form = MenuForm()

    return render(request, "menu/create.html", {"form": form})


@login_required
def delete(request, pk):
    """User can delete an existing menu"""
    menu = get_object_or_404(Menu, pk=pk, creator=request.user)
    if request.method == "POST":
        menu.delete()

    return redirect("menu-list")


@login_required
def edit(request, pk):
    """User can add options of lunch to a draft menu, then acitvate the menu"""
    try:
        menu = Menu.objects.prefetch_related("lunch_set__option_set").get(
            pk=pk, creator=request.user, is_active=False
        )
    except Menu.DoesNotExist:
        raise Http404()

    if request.method == "POST":
        menu.is_active = True
        menu.save()
        return redirect("menu-detail", pk=pk)
    else:
        lunchs = menu.lunch_set.all()
        return render(request, "menu/edit.html", {"menu": menu, "lunchs": lunchs})


@login_required
def lunch_create(request, pk):
    """User can add an option to a draft menu"""
    menu = get_object_or_404(Menu, pk=pk, creator=request.user)
    if request.method == "POST":
        form = LunchForm(request.POST)
        if form.is_valid():
            lunch = form.save(commit=False)
            lunch.menu = menu
            lunch.save()
            return redirect("menu-option-create", menu_pk=pk, lunch_pk=lunch.pk)
    else:
        form = LunchForm()

    return render(request, "menu/lunch.html", {"menu": menu, "form": form})


@login_required
def option_create(request, menu_pk, lunch_pk):
    """User can add options to a lunch menu"""
    menu = get_object_or_404(Menu, pk=menu_pk, creator=request.user)
    lunch = Lunch.objects.get(pk=lunch_pk)
    if request.method == "POST":
        form = OptionForm(request.POST)
        if form.is_valid():
            option = form.save(commit=False)
            option.lunch_id = lunch_pk
            option.save()
    else:
        form = OptionForm()

    options = lunch.option_set.all()
    return render(
        request,
        "menu/options.html",
        {"menu": menu, "lunch": lunch, "options": options, "form": form},
    )


def start(request, pk):
    """User can start a menu"""
    menu = get_object_or_404(Menu, pk=pk, is_active=True)
    if request.method == "POST":
        sub = Submission.objects.create(menu=menu)
        return redirect("menu-submit", menu_pk=pk, sub_pk=sub.pk)

    return render(request, "menu/start.html", {"menu": menu})


def submit(request, menu_pk, sub_pk):
    """User submit their completed menu."""
    try:
        menu = Menu.objects.prefetch_related("lunch_set__option_set").get(
            pk=menu_pk, is_active=True
        )
    except Menu.DoesNotExist:
        raise Http404()

    try:
        sub = menu.submission_set.get(pk=sub_pk, is_complete=False)
    except Submission.DoesNotExist:
        raise Http404()

    lunchs = menu.lunch_set.all()
    options = [q.option_set.all() for q in lunchs]
    form_kwargs = {"empty_permitted": False, "options": options}
    AnswerFormSet = formset_factory(AnswerForm, extra=len(lunchs), formset=BaseAnswerFormSet)
    if request.method == "POST":
        formset = AnswerFormSet(request.POST, form_kwargs=form_kwargs)
        if formset.is_valid():
            with transaction.atomic():
                for form in formset:
                    Answer.objects.create(
                        option_id=form.cleaned_data["option"], submission_id=sub_pk,
                    )

                sub.is_complete = True
                sub.save()
            return redirect("menu-thanks", pk=menu_pk)

    else:
        formset = AnswerFormSet(form_kwargs=form_kwargs)

    lunch_forms = zip(lunchs, formset)
    return render(
        request,
        "menu/submit.html",
        {"menu": menu, "lunch_forms": lunch_forms, "formset": formset},
    )


def thanks(request, pk):
    """User receives a thank-you message."""
    menu = get_object_or_404(Menu, pk=pk, is_active=True)
    return render(request, "menu/thanks.html", {"menu": menu})
