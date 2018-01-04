# Generated by Django 2.0.1 on 2018-01-04 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20170116_2236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='provider',
            name='status',
            field=models.CharField(choices=[('N', 'Aguardando moderação'), ('D', 'Em discussão'), ('P', 'Publicado'), ('R', 'Recusado'), ('E', 'Edição aguardando moderação'), ('O', 'Substituído por versão atualizada')], default='N', max_length=1, verbose_name='Status'),
        ),
    ]
