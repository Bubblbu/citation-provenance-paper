class Scite:
    def __init__(self, api_key=None):
        self.url = "https://api.scite.ai/citations/citing/{}"
        self.session = requests.session()
        
        if api_key:
            self.headers = {"Authorization": f"Bearer {api_key}"}
        else:
            self.headers = None
        
    def doi(self, doi):
        r = self.session.get(self.url.format(doi), headers=self.headers)
        return r