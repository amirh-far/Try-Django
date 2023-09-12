from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory # model form for querysets
from django.http import HttpResponse 
from django.urls import reverse
from .models import Recipe, RecipeIngredient
from .forms import RecipeForm, RecipeIngredientForm
# we will implement the CRUD -> Create Retrieve Update Detail


@login_required
def recipe_list_view(request):
    qs = Recipe.objects.filter(user=request.user)
    context={"object_list": qs}
    return render(request, "recipes/list.html", context=context)

@login_required
def recipe_detail_view(request, id=None):
    hx_url = reverse("recipes:hx-detail", kwargs={"id": id})
    context = {"hx_url": hx_url}
    return render(request, "recipes/detail.html", context=context)
    # Previous way of doing things without htmx:
    # obj = get_object_or_404(Recipe, id=id, user=request.user)
    # context={"object": obj}
    # return render(request, "recipes/detail.html", context=context)


@login_required
def recipe_detail_hx_view(request, id=None):
    try:
        obj = Recipe.objects.get(id=id, user=request.user)
    except:
        obj = None
    if obj is None:
        return HttpResponse("Not found.")
    context={"object": obj}
    return render(request, "recipes/partials/detail.html", context=context)

@login_required
def recipe_create_view(request):
    form = RecipeForm(request.POST or None)
    context = {"form": form}
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        return redirect(obj.get_absolute_url())
    return render(request, "recipes/create-update.html", context=context)

@login_required
def recipe_update_view(request, id):
    obj = get_object_or_404(Recipe, id=id, user=request.user)
    form = RecipeForm(request.POST or None, instance=obj) # because we have this instance=obj we can see a pre filled form
    RecipeIngredientFormset = modelformset_factory(model=RecipeIngredient, form=RecipeIngredientForm, extra=0)
    qs = obj.recipeingredient_set.all()
    formset = RecipeIngredientFormset(request.POST or None, queryset=qs)
    context={"object": obj, "form": form, "formset": formset}  
    if all([form.is_valid(), formset.is_valid]):
        parent = form.save(commit=False)
        parent.save()
        for form in formset:
            child = form.save(commit=False)
            child.recipe = parent
            child.save()
        context["message"] = "Data saved."

    if request.htmx:
        return render(request, "recipes/partials/forms.html", context=context)

    return render(request, "recipes/create-update.html", context=context)