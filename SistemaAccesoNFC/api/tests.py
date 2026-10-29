from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from .models import (
    User,
    Card,
    Door,
    Permission,
    Device,
    AccessLog
)
from .services import check_access


class AccessCheckTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            name='Usuario',
            surname='Prueba',
            email='prueba@example.com',
            role='student',
            active=True
        )

        self.card = Card.objects.create(
            uid='TEST123456',
            user=self.user,
            active=True
        )

        self.door = Door.objects.create(
            name='Puerta de prueba',
            location='Laboratorio',
            active=True
        )

        self.device = Device.objects.create(
            name='ESP32 de prueba',
            device_id='ESP32-TEST-001',
            door=self.door,
            active=True
        )

        self.permission = Permission.objects.create(
            user=self.user,
            door=self.door,
            day=self.current_day(),
            start_time='00:00:00',
            end_time='23:59:59',
            active=True
        )

    @staticmethod
    def current_day():
        days = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
        return days[timezone.localtime().weekday()]

    def test_access_granted_with_valid_permission(self):
        result = check_access(
            card_uid='TEST123456',
            device_id='ESP32-TEST-001'
        )

        self.assertEqual(result['result'], 'GRANTED')
        self.assertTrue(
            AccessLog.objects.filter(result='GRANTED').exists()
        )

    def test_access_denied_for_unknown_card(self):
        result = check_access(
            card_uid='UNKNOWN',
            device_id='ESP32-TEST-001'
        )

        self.assertEqual(result['result'], 'DENIED')
        self.assertEqual(
            result['reason'],
            'Tarjeta no encontrada'
        )

    def test_access_denied_for_inactive_card(self):
        self.card.active = False
        self.card.save()

        result = check_access(
            card_uid='TEST123456',
            device_id='ESP32-TEST-001'
        )

        self.assertEqual(result['result'], 'DENIED')
        self.assertEqual(result['reason'], 'Tarjeta inactiva')

    def test_access_denied_for_inactive_user(self):
        self.user.active = False
        self.user.save()

        result = check_access(
            card_uid='TEST123456',
            device_id='ESP32-TEST-001'
        )

        self.assertEqual(result['result'], 'DENIED')
        self.assertEqual(result['reason'], 'Usuario inactivo')

    def test_access_denied_for_inactive_door(self):
        self.door.active = False
        self.door.save()

        result = check_access(
            card_uid='TEST123456',
            device_id='ESP32-TEST-001'
        )

        self.assertEqual(result['result'], 'DENIED')
        self.assertEqual(result['reason'], 'Puerta inactiva')

    def test_access_denied_without_permission(self):
        self.permission.active = False
        self.permission.save()

        result = check_access(
            card_uid='TEST123456',
            device_id='ESP32-TEST-001'
        )

        self.assertEqual(result['result'], 'DENIED')
        self.assertTrue(
            AccessLog.objects.filter(result='DENIED').exists()
        )
    
    
    def test_access_denied_for_inactive_device(self):
        self.device.active = False
        self.device.save()

        result = check_access(
            card_uid='TEST123456',
            device_id='ESP32-TEST-001'
        )

        self.assertEqual(result['result'], 'DENIED')
        self.assertEqual(result['reason'], 'Dispositivo inactivo')
        self.assertTrue(
            AccessLog.objects.filter(
                result='DENIED',
                reason='Dispositivo inactivo'
            ).exists()
        )

    def test_unknown_card_is_logged(self):
        result = check_access(
            card_uid='UNKNOWN',
            device_id='ESP32-TEST-001'
        )

        self.assertEqual(result['result'], 'DENIED')
        self.assertEqual(result['reason'], 'Tarjeta no encontrada')
        self.assertTrue(
            AccessLog.objects.filter(
                card__isnull=True,
                door=self.door,
                reason='Tarjeta no encontrada'
            ).exists()
        )

    def test_unknown_device_is_logged(self):
        result = check_access(
            card_uid='TEST123456',
            device_id='ESP32-UNKNOWN'
        )

        self.assertEqual(result['result'], 'DENIED')
        self.assertEqual(result['reason'], 'Dispositivo no encontrado')
        self.assertTrue(
            AccessLog.objects.filter(
                card=self.card,
                door__isnull=True,
                reason='Dispositivo no encontrado'
            ).exists()
        )