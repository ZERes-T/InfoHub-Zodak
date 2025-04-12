from django import forms
from .models import Comment
from .models import Rating
from .models import Game

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ["title", "description", "cover", "rating", "total_votes", "favorites"]

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ["value"]
        widgets = {
            "value": forms.Select(choices=[(1, "★"), (2, "★★"), (3, "★★★"), (4, "★★★★"), (5, "★★★★★")])
        }
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Оставьте комментарий..."}),
        }
