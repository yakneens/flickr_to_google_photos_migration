from __future__ import print_function

import logging
from pathlib import Path

from oauth2client import file, client, tools


def authorize_with_google():
    logger = logging.getLogger(__name__)

    # Setup the Photo v1 API
    SCOPES = 'https://www.googleapis.com/auth/photoslibrary https://www.googleapis.com/auth/photoslibrary.sharing'
    token_file = (Path().parent / "auth/google_token.json").resolve().as_posix()
    store = file.Storage(token_file)

    # creds = None
    # if not creds_file:
    flow = client.flow_from_clientsecrets((Path().parent / "auth/google_credentials.json").resolve().as_posix(), SCOPES)
    creds = tools.run_flow(flow, store)
    logger.info(f"creds: {creds}")
    store.put(creds)
    # else:
    #     creds = store.get()

    return creds


if __name__ == '__main__':
    authorize_with_google()
