from rest_framework import renderers
import json

class UserRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        # Check if the response contains an error
        if isinstance(data, dict) and 'detail' in data and 'ErrorDetail' in str(data['detail']):
            response = json.dumps({'errors': data})
        else:
            response = json.dumps({'data': data})
        
        return response
