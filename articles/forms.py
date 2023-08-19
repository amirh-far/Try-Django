from django import forms

class ArticleForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField()

    def clean_title(self):
        cleaned_data = self.cleaned_data # Dictionary
        print(cleaned_data)
        cleaned_title = cleaned_data.get("title")
        if cleaned_title.strip().lower() == "yo":
            raise forms.ValidationError("This title is already taken")
        return cleaned_title