from django.shortcuts import render
from django.db.models import Q
# from django.http import HttpResponse
from .models import Article
# from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm
from django.http import Http404
# You can certainly use this lib to do the rendering for you:
from django.shortcuts import render, redirect



def article_search_view(request):
    query = request.GET.get("q")
    if query is not None:
        lookups = Q(content__icontains=query) | Q(title__icontains=query)
        qs = Article.objects.filter(lookups)

    context = {"object_list": qs}
    return render(request,"articles/search.html", context=context)
# old search view:
# def article_search_view(request):
#     query_dict = request.GET
#     # print(dir(request))
#     query = query_dict.get("q")

#     article_obj = None
#     if query is not None:
#         article_obj = Article.objects.get(id=query)

#     context = {"object": article_obj}
#     return render(request,"articles/search.html", context=context)


def article_detail_view(request, slug, *args, **argv):
    article_obj = None
    if slug is not None:
        try:
            article_obj = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise Http404
        # we have done a lot of things to prevent this exception but its better to have it in case something goes wrong!
        except Article.MultipleObjectsReturned:
            article_obj = Article.objects.filter(slug=slug).first()
        except:
            raise Http404 
    context = {
        "object" : article_obj
    }

    return render(request, "articles/detail.html", context=context)



@login_required
def article_create_view(request, *args, **argv):
    context = {"created" : False}
    form = ArticleForm(request.POST or None)
    context = {"form": form}
    # print(dir(form))
    if form.is_valid():
        article_obj = form.save()
        #To avoid duplicate files:
        context["form"] = ArticleForm()
        context["object"] = article_obj
        return redirect("article-detail", slug=article_obj.slug)
        # context["created"] = True
    # print(request.GET)

    return render(request, "articles/create.html", context=context)

# Old way to create Obj and save:
# @login_required
# def article_create_view(request, *args, **argv):
#     context = {"created" : False}
#     form = ArticleForm(request.POST or None)
#     context = {"form": form}
#     print(dir(form))
#     if form.is_valid():

    #     title = form.cleaned_data.get("title")
    #     content = form.cleaned_data.get("content")
    # # Or can use the request.GET to get the values you need but you need to use the get method instead
    # # print(dir(for("title")))
    #     print(form.__getitem__("title"), form.__getitem__("content"))

    #     article_obj = Article()
    #     article_obj.title = title
    #     article_obj.content = content
    #     article_obj.save()
        # or you can do this line of code instead: Article.objects.create(title=title, content=)
    #     context["object"] = article_obj
    #     context["created"] = True
    # print(request.GET)

    # return render(request, "articles/create.html", context=context)
