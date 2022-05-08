import hmac
import requests
import hashlib
import json
from datetime import datetime, timezone

access_key = os.environ['COEFONT_KEY']
client_secret = os.environ['COEFONT_SECRET']

def request(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    if request.method == 'OPTIONS':
      headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600',
        }
      return ('', 204, headers)

    headers = {
        'Access-Control-Allow-Origin': '*',
    }
    if(request.headers['content-type'] == 'application/json'):
      request_json = request.get_json(silent=True)
      if request_json and 'text' in request_json:
          text = request_json['text']
          coefont = request_json['coefont']
      else:
        return('', 400,headers)
      date: str = str(int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()))
      data: str = json.dumps({
        'coefont': coefont,
        'text': text
      })
      signature = hmac.new(bytes(client_secret, 'utf-8'), (date+data).encode('utf-8'), hashlib.sha256).hexdigest()

      response = requests.post('https://api.coefont.cloud/v1/text2speech', data=data, headers={
        'Content-Type': 'application/json',
        'Authorization': access_key,
        'X-Coefont-Date': date,
        'X-Coefont-Content': signature
      })
      if response.status_code == 200:
        return(response.url, 200 , headers)
      else:
        return(str(response.status_code), 500,headers)
    return('', 400,headers)