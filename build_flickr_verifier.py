import flickr_api
import os
api_key=os.environ['FLICKR_API_KEY']
api_secret=os.environ['FLICKR_API_SECRET']

flickr_api.set_keys(api_key=api_key, api_secret=api_secret)
a = flickr_api.auth.AuthHandler()
url = a.get_authorization_url("read")
print(f"url: {url}")
verifier = input("Verifier code: ")

a.set_verifier(verifier)
a.save("flickr_credentials.dat")
