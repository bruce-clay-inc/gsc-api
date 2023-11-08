import datetime
import requests
from datetime import date, timedelta
from collections import defaultdict
from http import HTTPStatus
import json
from django.views import View
from urllib.parse import quote_plus
from django.http.response import JsonResponse
from .models import Search_Console

class SyncDataView(View):
    """ View to Sync GSC Data with the Database """

    def post(self, request):
        post_data = json.loads(request.body) if request.body else request.POST
        access_token = post_data.get('access_token')        
        gsc_site = post_data.get('gsc_site')        

        if access_token is None:
            return JsonResponse({'status': 'error', 'message': 'no access token supplied'}, status=HTTPStatus.BAD_REQUEST)
        
        endpoint = f'https://www.googleapis.com/webmasters/v3/sites/{quote_plus(gsc_site)}/searchAnalytics/query'
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        start_date = datetime.date(2023, 9, 1)
        end_date = datetime.date(2023, 9, 30)
        parameters = {
            'startDate': datetime.datetime.strftime(start_date,'%Y-%m-%d'),
            'endDate': datetime.datetime.strftime(end_date,'%Y-%m-%d'),
            'dimensions': ['date','page','query'],
            'rowLimit': 25000, 
            'startRow': 0
        }

        data = []
        while True:
            r = requests.post(endpoint, headers=headers, json=parameters)
            if r.status_code == 403:
                # Implement re-authorization here
                pass
            elif r.status_code == 200:
                this_data = r.json()
                data.extend(this_data.get('rows', []))
                parameters['startRow'] += parameters['rowLimit']
                if 'rows' not in this_data:
                    break
            else:
                raise Exception(f'Invalid response from API: {r.status_code} {r.text}')
        
        for d in data:
            impressions = d['impressions'],
            ctr = d['ctr'],
            position = d['position'],
            date = d['date'],
            keyword = d['query'],
            clicks = d['clicks'],
            sc, created = Search_Console.objects.update_or_create(
                date=date, 
                query=keyword, 
                site=gsc_site,
                defaults={"ctr": ctr, "impressions": impressions, "clicks": clicks,"position": position, "date": date}
            )            

        return JsonResponse({'status': 'accepted'}, status=HTTPStatus.ACCEPTED)