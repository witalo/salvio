import requests
import html
from django.http import JsonResponse
from http import HTTPStatus
from .models import *
import math
from django.contrib.auth.models import User
import json
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime
from django.db import DatabaseError, IntegrityError
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt


def query_api_amigo(document, type_document):
    context = {}
    if type_document == 'RUC':
        url = 'https://api.migo.pe/api/v1/ruc'
        params = {
            'token': 'GBk42s6qbluLcE2Jb2CFiainNpnqEDMRlio5nJjWrw5EVL1TrysTGfmdlV7k',
            'ruc': document,
        }
        headers = {
            "Accept": 'application/json',
        }
        r = requests.post(url, json=params, headers=headers)

        if r.status_code == 200:
            result = r.json()

            context = {
                'status': True,
                'ruc': result.get('ruc'),
                'business_name': html.unescape(result.get('nombre_o_razon_social')),
                'address': html.unescape(result.get('direccion')),
            }

        else:
            result = r.json()
            context = {
                'status': False,
                'errors': 'La consulta fue inconclusa',
            }

    return context
