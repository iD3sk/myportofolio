from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0006_experience_liked_by"),
    ]

    operations = [
        migrations.AddField(
            model_name="achievements",
            name="liked_by",
            field=models.ManyToManyField(
                blank=True,
                related_name="liked_achievements",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
