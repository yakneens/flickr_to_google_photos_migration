import flickr_api
import os
flickr_api.set_keys(api_key=os.environ['FLICKR_API_KEY'], api_secret=os.environ['FLICKR_API_SECRET'])
a = flickr_api.auth.AuthHandler() # creates a new AuthHandler object
perms = "read" # set the required permissions
url = a.get_authorization_url(perms)
print(url)

#######

a.set_verifier("my_verifier")
flickr_api.set_auth_handler(a)
a.save("auth/flickr_auth_handler")