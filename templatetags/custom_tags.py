from django import template
from core.models import Notification

register = template.Library()

@register.inclusion_tag('core/show_notification.html', takes__context=True)
def show_notifications(context):
    request_user = context['request'].user
    notifications = Notification.objects.filter(to_user=request_user).exclude(user_has_seen=True).order_by('-date')
    return {'notifications': notifications}