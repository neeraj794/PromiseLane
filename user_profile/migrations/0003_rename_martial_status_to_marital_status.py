from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0002_matrimonialprofile_is_active'),
    ]

    operations = [
        migrations.RenameField(
            model_name='matrimonialprofile',
            old_name='martial_status',
            new_name='marital_status',
        ),
    ]
