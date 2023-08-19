from django import forms
from .models import Article
class ArticleForm(forms.ModelForm):
    class Meta:
        # Describing the other parts of model form with meta class
        model = Article
        fields = ["title", "content"]
    def clean(self):
        data = self.cleaned_data
        title = data.get("title")
        content = data.get("content")
        #query set lookup:
        qs = Article.objects.filter(title__icontains=title)
        # print(qs)
        if qs.exists():
            self.add_error("title", f"The title \"{title}\" is already in use. Please pick another title.")
        return data



class OldArticleForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField()

    def clean_title(self):
        cleaned_data = self.cleaned_data # Dictionary
        print(cleaned_data)
        title = cleaned_data.get("title")
        # if title.strip().lower() == "yo":
        #     # Field Error:
        #     self.add_error("title", "this title is used")
            # Non Field Error:
            # raise forms.ValidationError("This title is already taken")
        return title
    def clean(self):
        cleaned_data = self.cleaned_data
        print("All data:", cleaned_data)
        title = cleaned_data.get("title")
        content = cleaned_data.get("content")
        if title.strip().lower() == "yo":
            self.add_error("title", "this title is used")
            # raise forms.ValidationError("This title is already taken")
        if title.strip().lower() == "yo" or content.strip().lower() == "yo":
            #Field Error:
            self.add_error("content", "Yo can not be in content. already used")
            #Non Field Error:
            raise forms.ValidationError("Title or content already taken")
        return cleaned_data
