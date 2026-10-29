from django.utils import timezone

from .models import Card, Device, Permission, AccessLog


def _record_result(result, reason, user=None, card=None, door=None):
    AccessLog.objects.create(
        user=user,
        card=card,
        door=door,
        result=result,
        reason=reason
    )

    response = {
        'result': result,
        'reason': reason
    }

    if user is not None:
        response['user'] = user.id

    if door is not None:
        response['door'] = door.id

    return response


def _deny(reason, user=None, card=None, door=None):
    return _record_result(
        result='DENIED',
        reason=reason,
        user=user,
        card=card,
        door=door
    )


def check_access(card_uid, device_id):
    try:
        device = Device.objects.select_related('door').get(
            device_id=device_id
        )
    except Device.DoesNotExist:
        card = Card.objects.select_related('user').filter(
            uid=card_uid
        ).first()

        if card is not None:
            return _deny(
                'Dispositivo no encontrado',
                user=card.user,
                card=card
            )

        return _deny('Dispositivo no encontrado')

    device.last_seen = timezone.now()
    device.save(update_fields=['last_seen'])

    door = device.door

    try:
        card = Card.objects.select_related('user').get(uid=card_uid)
    except Card.DoesNotExist:
        return _deny(
            'Tarjeta no encontrada',
            door=door
        )

    user = card.user

    if not device.active:
        return _deny(
            'Dispositivo inactivo',
            user=user,
            card=card,
            door=door
        )

    if not card.active:
        return _deny(
            'Tarjeta inactiva',
            user=user,
            card=card,
            door=door
        )

    if not user.active:
        return _deny(
            'Usuario inactivo',
            user=user,
            card=card,
            door=door
        )

    if not door.active:
        return _deny(
            'Puerta inactiva',
            user=user,
            card=card,
            door=door
        )

    now = timezone.localtime()
    current_time = now.time().replace(tzinfo=None)

    days = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
    current_day = days[now.weekday()]
    previous_day = days[(now.weekday() - 1) % 7]

    permissions = Permission.objects.filter(
        user=user,
        door=door,
        active=True
    )

    authorized = False

    for permission in permissions:
        if permission.start_time <= permission.end_time:
            if (
                permission.day == current_day
                and permission.start_time <= current_time
                <= permission.end_time
            ):
                authorized = True
                break
        else:
            if (
                permission.day == current_day
                and current_time >= permission.start_time
            ):
                authorized = True
                break
            if (
                permission.day == previous_day
                and current_time <= permission.end_time
            ):
                authorized = True
                break
            
    if authorized:
        return _record_result(
            result='GRANTED',
            reason='Permiso válido',
            user=user,
            card=card,
            door=door
        )

    return _deny(
        'Sin permiso para este día y horario',
        user=user,
        card=card,
        door=door
    )
