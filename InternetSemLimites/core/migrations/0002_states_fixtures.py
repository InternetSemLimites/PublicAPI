from csv import reader
from os import path
from django.conf import settings
from django.db import migrations


def create_states(apps, schema_editor):
    State = apps.get_model('core', 'State')
    fixture_file = ('InternetSemLimites', 'core', 'fixtures', 'states.csv')
    fixture_path = path.join(settings.BASE_DIR, *fixture_file)
    with open(fixture_path, encoding='utf-8') as fh:
        for line in reader(fh):
            State.objects.create(name=line[1], abbr=line[0])


def delete_states(apps, schema_editor):
    State = apps.get_model('core', 'State')
    for state in State.objects.all():
        state.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_states, delete_states),
    ]
