# Generated by Django 3.2.7 on 2021-10-29 09:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderHistory',
            fields=[
                ('createdatmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.createdatmodel')),
                ('total_sum', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='order', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'order_history',
                'ordering': ['-created_at'],
            },
            bases=('main.createdatmodel',),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('createdatmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.createdatmodel')),
                ('total_sum', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('order_status', model_utils.fields.StatusField(choices=[('Готовится к отправке', 'Готовится к отправке'), ('Находится в пути', 'Находится в пути'), ('Ожидает клиента на почте', 'Ожидает клиента на почте'), ('Доставлен', 'Доставлен')], default='Готовится к отправке', max_length=100, no_check_for_status=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'order',
                'ordering': ['-created_at'],
            },
            bases=('main.createdatmodel',),
        ),
    ]
