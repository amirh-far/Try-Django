"""
To render html web pages
"""
from django.http import HttpResponse
from articles.models import Article

article_obj = Article.objects.get(id=1)

HTML_STRING = f"""
<h1> {article_obj.title} id: {article_obj.id}</h1>

<p1> {article_obj.content} </p1>

"""



def home_view (request):
    """
    Take in a request (Django sends request)
    Return Html as a response (We picj to return the response)
    """
    return HttpResponse(HTML_STRING)