from django.shortcuts import render

from django.utils.safestring import mark_safe
import json

import logging

logger = logging.getLogger()


def index(request):
    logger.info("am here index---------------------------------------->")
    return render(request, 'chat/index.html', {})


def room(request, room_name):
    logger.info("am here room---------------------------------------->")
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })
