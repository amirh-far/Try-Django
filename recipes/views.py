from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory # model form for querysets
from django.http import HttpResponse, Http404
from django.urls import reverse
from .models import Recipe, RecipeIngredient
from .forms import RecipeForm, RecipeIngredientForm, RecipeIngredientImageForm
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

# @login_required
# def recipe_delete_view(request, id=None):
#     obj = get_object_or_404(Recipe, id=id, user=request.user)
#     if request.method == "POST":
#         obj.delete()
#         success_url = reverse("recipes:list")
#         return redirect(success_url)
#     context = { "object": obj}
#     return render(request, "recipes/delete.html", context=context)

@login_required
def recipe_delete_view(request, id=None): # hx view
    try:
        obj = Recipe.objects.get(id=id, user=request.user)
    except:
        obj = None
        if request.htmx:
            return HttpResponse("Not Found")
        return Http404
    if request.method == "POST":
        obj.delete()
        success_url = reverse("recipes:list")
        if request.htmx:
            headers = {
                "HX-Redirect": success_url
            }
            return HttpResponse("Success", headers=headers)
        return redirect(success_url)
    context = { "object": obj}
    return render(request, "recipes/delete.html", context=context)

# @login_required
# def recipe_ingredient_delete_view(request,parent_id=None, id=None):
#     obj = get_object_or_404(RecipeIngredient,recipe_id=parent_id, id=id, recipe__user=request.user)
#     if request.method == "POST":
#         obj.delete()
#         success_url = reverse("recipes:detail", kwargs={"id": parent_id})
#         return redirect(success_url)
#     context = { "object": obj}
#     return render(request, "recipes/delete.html", context=context)

@login_required
def recipe_ingredient_delete_view(request,parent_id=None, id=None): # hx view
    try:
        obj = RecipeIngredient.objects.get(recipe_id=parent_id, id=id, recipe__user=request.user)
    except:
        obj = None
        if request.htmx:
            return HttpResponse("Not Found")
        return Http404
    if request.method == "POST":
        name = obj.name
        obj.delete()
        success_url = reverse("recipes:detail", kwargs={"id": parent_id})
        if request.htmx:
            return render(request, 
                          "recipes/partials/ingredient-inline-delete-response.html",
                          {"name": name})
        return redirect(success_url)
    context = { "object": obj}
    return render(request, "recipes/delete.html", context=context)

@login_required
def recipe_detail_hx_view(request, id=None):
    if not request.htmx:
        raise Http404
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
        if request.htmx:
            headers = { 
                "HX-Push": obj.get_absolute_url()
            }
            # return HttpResponse("Created", headers=headers)
            context = {
                "object": obj
            }
            return render(request, "recipes/partials/detail.html", context=context)
    return render(request, "recipes/create-update.html", context=context)

@login_required
def recipe_update_view(request, id):
    obj = get_object_or_404(Recipe, id=id, user=request.user)
    form = RecipeForm(request.POST or None, instance=obj) # because we have this instance=obj we can see a pre filled form
    new_ingredient_url = reverse("recipes:hx-ingredient-create", kwargs={"parent_id": obj.id })

    # RecipeIngredientFormset = modelformset_factory(model=RecipeIngredient, form=RecipeIngredientForm, extra=0)
    # qs = obj.recipeingredient_set.all()
    # formset = RecipeIngredientFormset(request.POST or None, queryset=qs)
    context={
        "object": obj,
        "form": form,
        "new_ingredient_url" : new_ingredient_url,
        # "formset": formset,
        }  
    # if all([form.is_valid(), formset.is_valid]):
    #     parent = form.save(commit=False)
    #     parent.save()
    #     for form in formset:
    #         child = form.save(commit=False)
    #         child.recipe = parent
    #         child.save()
    #     context["message"] = "Data saved."

    if form.is_valid():
        form.save()
        context["message"] = "Data saved."

    if request.htmx:
        return render(request, "recipes/partials/forms.html", context=context)
    
    return render(request, "recipes/create-update.html", context=context)

@login_required
def recipe_ingredient_update_hx_view(request, parent_id=None, id=None):
    if not request.htmx:
        raise Http404
    try:
        parent_obj = Recipe.objects.get(id=parent_id, user=request.user)
    except:
        parent_obj = None
    if parent_obj is None:
        return HttpResponse("Not found.")
    
    instance = None
    if id is not None:
        try:
            instance = RecipeIngredient.objects.get(recipe=parent_obj, id=id)
        except:
            instance = None
    
    form = RecipeIngredientForm(request.POST or None, instance=instance)
    url = instance.get_hx_edit_url if instance else reverse("recipes:hx-ingredient-create", kwargs={"parent_id": parent_obj.id })
    context={"object": instance, "form": form, "url": url}
    
    if form.is_valid():
        new_obj = form.save(commit=False)
        # it want to say if a new ingredient is created it doesnt know which recipe it should be connected to
        # and we have to include the recipe for it
        if instance is None:
            new_obj.recipe = parent_obj
        new_obj.save()
        context["object"] = new_obj
        return render(request, "recipes/partials/ingredient-inline.html", context=context)

    return render(request, "recipes/partials/ingredient-form.html", context=context)

def recipe_ingredient_image_upload_view(request, parent_id):
    print(request.FILES.get("image"))
    try:
        parent_obj = Recipe.objects.get(id=parent_id, user=request.user)
    except:
        parent_obj = None
    if parent_obj is None:
        raise Http404                
    form = RecipeIngredientImageForm(request.POST or None, request.FILES or None)
    print(form.is_valid())
    if form.is_valid():
        obj = form.save(commit=False)
        obj.recipe = parent_obj
        # obj.recipe_id = parent_id the other way to do it
        obj.save()
    return render(request, "image-form.html", {"form": form})