from django.shortcuts import render

from django.utils.safestring import mark_safe
import json
import ipdb

import logging

logger = logging.getLogger()

def index(request):
	logger.warning("am here index---------------------------------------->");
	return render(request, 'chat/index.html', {})


def room(request, room_name):
	logger.warning("am here room---------------------------------------->");
	return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })