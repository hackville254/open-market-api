from django.db.models.signals import pre_save
from django.dispatch import receiver
import uuid
from datetime import datetime

from banque.models import CompteBancaire


@receiver(pre_save, sender=CompteBancaire)
def generate_numero_compte(sender, instance, **kwargs):
    if not instance.numero_compte:
        last_compte = CompteBancaire.objects.order_by('-id').first()
        if last_compte:
            last_id = int(last_compte.numero_compte[3:])
            new_id = last_id + 1
        else:
            new_id = 1
        date_enregistrement = datetime.now().strftime('%d%m%Y')
        uuid_str = str(uuid.uuid4())[:5]
        uuid_str1 = str(uuid.uuid4())[:3]
        instance.numero_compte = f"OPM{uuid_str1}{new_id:04d}{date_enregistrement}{uuid_str}"