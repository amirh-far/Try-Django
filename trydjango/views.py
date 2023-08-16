"""
To render html web pages
"""
from django.http import HttpResponse
from articles.models import Article
from django.template.loader import render_to_string

article_obj = Article.objects.get(id=1)
number_lis = [123, 432, 54, 6233]
article_queryset = Article.objects.all()

context = {
    "obj_queryset": article_queryset,
    "number_lis": number_lis,
    "object" : article_obj,
    "title" : article_obj.title,
    "content" : article_obj.content,
    "id" : article_obj.id
}
HTML_STRING = render_to_string("home-view.html", context=context)
# HTML_STRING = f"""
# <h1> {article_obj.title} id: {article_obj.id}</h1>

# <p1> {article_obj.content} </p1>

# """



def home_view (request):
    """
    Take in a request (Django sends request)
    Return Html as a response (We picj to return the response)
    """
    # print(request.__dict__) print the request
    return HttpResponse(HTML_STRING)