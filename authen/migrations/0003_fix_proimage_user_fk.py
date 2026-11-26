from django.contrib.auth.models import User as DefaultUser
from django.db import migrations


def fix_proimage_user_fk(apps, schema_editor):
    connection = schema_editor.connection
    with connection.cursor() as cursor:
        table_names = connection.introspection.table_names(cursor)

    if 'auth_user' not in table_names:
        return

    ProImage = apps.get_model('authen', 'ProImage')
    CustomUser = apps.get_model('authen', 'CustomUser')
    quote_name = connection.ops.quote_name
    proimage_table = quote_name(ProImage._meta.db_table)
    custom_user_table = quote_name(CustomUser._meta.db_table)
    default_user_table = quote_name(DefaultUser._meta.db_table)

    with connection.cursor() as cursor:
        cursor.execute(
            f'''
            SELECT profile.id
            FROM {proimage_table} profile
            LEFT JOIN {default_user_table} old_user
                ON old_user.id = profile.user_id
            LEFT JOIN {custom_user_table} custom_user
                ON custom_user.username = old_user.username
            WHERE custom_user.id IS NULL
            '''
        )
        unmatched_profiles = [row[0] for row in cursor.fetchall()]
        if unmatched_profiles:
            raise RuntimeError(
                'Cannot migrate profile image user references; no matching '
                f'custom user exists for profile image IDs {unmatched_profiles}.'
            )

        cursor.execute(
            f'''
            UPDATE {proimage_table}
            SET user_id = (
                SELECT custom_user.id
                FROM {default_user_table} old_user
                JOIN {custom_user_table} custom_user
                    ON custom_user.username = old_user.username
                WHERE old_user.id = {proimage_table}.user_id
            )
            '''
        )

    old_field = ProImage._meta.get_field('user').clone()
    old_field.set_attributes_from_name('user')
    old_field.model = ProImage
    old_field.remote_field.model = DefaultUser
    schema_editor.alter_field(
        ProImage,
        old_field,
        ProImage._meta.get_field('user'),
        strict=True,
    )


class Migration(migrations.Migration):

    dependencies = [
        ('authen', '0002_customuser'),
    ]

    operations = [
        migrations.RunPython(fix_proimage_user_fk),
    ]
