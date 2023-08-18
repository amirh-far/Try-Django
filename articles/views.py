from django.shortcuts import render
from django.http import HttpResponse
from .models import Article
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

# You can certainly use this lib to do the rendering for you:
from django.shortcuts import render
# Create your views here.

def article_search_view(request):
    query_dict = request.GET
    # print(dir(request))
    query = query_dict.get("q")

    article_obj = None
    if query is not None:
        article_obj = Article.objects.get(id=query)

    context = {"object": article_obj}
    return render(request,"articles/search.html", context=context)

# def article_home_view(request):


#     HTML_RESPONSE = ""



#     return HttpResponse(HTML_RESPONSE)

def article_detail_view(request, id, *args, **argv):
    article_obj = None
    if id != None:
        article_obj = Article.objects.get(id=id)

    context = {
        "object" : article_obj
    }

    return render(request, "articles/detail.html", context=context)

@login_required
def article_create_view(request, *args, **argv):
    context = {"created" : False}
    if request.method == "POST":
        # Or can use the request.GET to get the values you need but you need to use the get method instead
        article_obj = Article()
        article_obj.title = request.POST.get("title")
        article_obj.content = request.POST.get("content")
        article_obj.save()
        # or you can do this line of code instead: Article.objects.create(title=title, content=)
        context["object"] = article_obj
        context["created"] = True
    # print(request.GET)

    return render(request, "articles/create.html", context=context)

    






