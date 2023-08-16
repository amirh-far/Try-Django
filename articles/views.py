from django.shortcuts import render
from django.http import HttpResponse
from .models import Article
from django.template.loader import render_to_string

# You can certainly use this lib to do the rendering for you:
from django.shortcuts import render
# Create your views here.

def article_home_view(request):


    HTML_RESPONSE = ""



    return HttpResponse(HTML_RESPONSE)

def article_detail_view(request, id, *args, **argv):
    article_obj = None
    if id != None:
        article_obj = Article.objects.get(id=id)

    context = {
        "object" : article_obj
    }

    return render(request, "articles/detail.html", context=context)

    






