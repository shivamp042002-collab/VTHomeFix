from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0002_workerapplication'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfoliophoto',
            name='category',
            field=models.CharField(choices=[('painting', 'Painting'), ('carpentry', 'Carpentry'), ('tiles', 'Tiles Fitting'), ('electrical', 'Electrical'), ('pop_ceiling', 'POP Ceiling'), ('other', 'Other')], default='other', max_length=30),
        ),
        migrations.AlterField(
            model_name='workerapplication',
            name='trade',
            field=models.CharField(choices=[('painting', 'Painting'), ('carpentry', 'Carpentry'), ('tiles', 'Tiles Fitting'), ('electrical', 'Electrical'), ('pop_ceiling', 'POP Ceiling'), ('plumbing', 'Plumbing'), ('other', 'Other')], default='other', max_length=30),
        ),
    ]
