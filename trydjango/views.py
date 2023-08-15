"""
To render html web pages
"""
from django.http import HttpResponse
from articles.models import Article
from django.template.loader import render_to_string

article_obj = Article.objects.get(id=1)


context = {
    # "object" : article_obj,
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
    return HttpResponse(HTML_STRING)