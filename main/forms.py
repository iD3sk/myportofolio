from django.forms import ModelForm, TextInput, Textarea, CharField

from main.models import Experience

class ExperienceForm(ModelForm):
    skills = CharField(
        label="Skills",
        required=False,
        widget=Textarea(
            attrs={
                "placeholder": "Python, Django, Leadership",
                "rows": 3,
                "class": "w-full rounded-md border-2 border-accent bg-paper px-4 py-3 text-ink",
            }
        ),
    )

    class Meta:
        model = Experience
        fields = [
            "title",
            "organization",
            "org_logo",
            "location",
            "description",
            "started_at",
            "ended_at",
            "skills",
        ]

        labels = {
            "title": "Experience's name",
            "organization": "Organization",
            "org_logo": "Organization logo",
            "location": "Location",
            "description": "Experience's description",
            "started_at": "Start",
            "ended_at": "End",
            "skills": "Skills",            
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Teaching Assistant",
                    "maxlength": 255,
                    "class": "w-full rounded-md border-2 border-accent bg-paper px-4 py-3 text-ink outline-none transition focus:border-primary focus:ring-2 focus:ring-primary/30",
                }
            ),
            "organization": TextInput(
                attrs={
                    "placeholder": "Universitas Indonesia",
                    "maxlength": 255,
                    "class": "w-full rounded-md border-2 border-accent bg-paper px-4 py-3 text-ink outline-none transition focus:border-primary focus:ring-2 focus:ring-primary/30",
                }
            ),
            "org_logo": TextInput(
                attrs={
                    "placeholder": "Path atau URL logo organisasi",
                    "maxlength": 255,
                    "class": "w-full rounded-md border-2 border-accent bg-paper px-4 py-3 text-ink outline-none transition focus:border-primary focus:ring-2 focus:ring-primary/30",
                }
            ),
            "location": TextInput(
                attrs={
                    "placeholder": "Depok, Indonesia",
                    "maxlength": 255,
                    "class": "w-full rounded-md border-2 border-accent bg-paper px-4 py-3 text-ink outline-none transition focus:border-primary focus:ring-2 focus:ring-primary/30",
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Deskripsi pengalaman",
                    "rows": 5,
                    "class": "w-full rounded-md border-2 border-accent bg-paper px-4 py-3 text-ink outline-none transition focus:border-primary focus:ring-2 focus:ring-primary/30",
                }
            ),
            "started_at": TextInput(
                attrs={
                    "type": "date",
                    "class": "w-full rounded-md border-2 border-accent bg-paper px-4 py-3 text-ink outline-none transition focus:border-primary focus:ring-2 focus:ring-primary/30",
                }
            ),
            "ended_at": TextInput(
                attrs={
                    "type": "date",
                    "class": "w-full rounded-md border-2 border-accent bg-paper px-4 py-3 text-ink outline-none transition focus:border-primary focus:ring-2 focus:ring-primary/30",
                }
            ),
        }
