import requests


class APIClient:
    def __init__(self, config):
        self.api_base_url = config.BASE_URL_API
        self.secondary_base_url = config.SECONDARY_BASE_URL
        self.username = config.USERNAME
        self.password = config.PASSWORD
        self.api_key = config.API_KEY
        self.api_secret = config.API_SECRET

    def _get_headers(self, use_secondary=False, token=None, api_key_secret=False):
        if api_key_secret:
            return {
                'Content-Type': 'application/json',
                'Api-Key': self.api_key,
                'Api-Secret': self.api_secret
            }
        elif token:
            return {
                'Content-Type': 'application/json',
                'Authorization': f"Bearer {token}"
            }
        else:
            return {
                'Content-Type': 'application/json',
                'Authorization': f"Basic {b64encode(f'{self.username}:{self.password}'.encode()).decode()}"
            }

    def _get_base_url(self, use_secondary=False):
        return self.secondary_base_url if use_secondary else self.api_base_url

    def _request(self, method, endpoint, params=None, json_data=None, use_secondary=False, token=None, api_key_secret=False):
        base_url = self._get_base_url(use_secondary)
        headers = self._get_headers(use_secondary, token, api_key_secret)
        url = f"{base_url}/{endpoint}"

        try:
            response = requests.request(
                method,
                url,
                headers=headers,
                params=params,
                json=json_data,
                verify=True
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"API request failed: {e}")
        
        return response

    def get(self, endpoint, params=None, **kwargs):
        return self._request("GET", endpoint, params=params, **kwargs)

    def post(self, endpoint, json_data=None, **kwargs):
        return self._request("POST", endpoint, json_data=json_data, **kwargs)

    def put(self, endpoint, params=None, json_data=None, **kwargs):
        return self._request("PUT", endpoint, params=params, json_data=json_data, **kwargs)

    def patch(self, endpoint, json_data=None, **kwargs):
        return self._request("PATCH", endpoint, json_data=json_data, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self._request("DELETE", endpoint, **kwargs)



#if have any customization in other http methods like head, options, trace, connect, etc. you can add them using if else statements parametreers can be used with args and kwrags read pytest.org documentation for args and kwargs