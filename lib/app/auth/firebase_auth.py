import requests
from fastapi import Request, HTTPException, status
from cryptography.x509 import load_pem_x509_certificate
import jwt

# from lib import utils
from lib.app.core.config import settings


class AuthInterceptor():
    # settings from Firebase docu
    algorithm = "RS256"
    auth_url = "https://www.googleapis.com/robot/v1/metadata/x509/securetoken@system.gserviceaccount.com"
    auth_header = "Authorization"
    key_id = "kid"
    method = "Bearer"

    # audience
    audience = settings.PROJECT_ID

    def _auth_exception(msg: str):
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=msg,
        )


    def approve(request: Request) -> dict:
        #--------------------------------------------------------------
        # 1. check for the auth header and check its required structure:
        #    Authorization: Bearer <token>
        #-------------------------------------------------------------
        if (not request.headers.get(AuthInterceptor.auth_header)):
            AuthInterceptor._auth_exception("Received unauthorized request")

        auth_header = request.headers.get(AuthInterceptor.auth_header).split(" ")

        if (AuthInterceptor.method != auth_header[0] or len(auth_header) != 2):
            AuthInterceptor._auth_exception("Received invalid authorization method")

        token = auth_header[1]

        #----------------------------------------------------------------
        # 2. get the public key from Firebase
        #----------------------------------------------------------------
        # read jwt token header
        header = jwt.get_unverified_header(token)
        if (AuthInterceptor.algorithm != header["alg"]):
            AuthInterceptor._auth_exception("Invalid algorihm referenced in jwt token")

        # get public Firebase PEM certificates
        pem_certs = requests.get(AuthInterceptor.auth_url, headers={"Cache-Control": "no-cache"}).json()
        pem_cert : str = pem_certs[header[AuthInterceptor.key_id]]
        if (not pem_cert):
            AuthInterceptor._auth_exception("Invalid PEM certificate referenced in jwt token")

        # make an usable key. code snippet taken from here: https://pyjwt.readthedocs.io/en/stable/faq.html
        public_key = load_pem_x509_certificate(pem_cert.encode()).public_key()

        #-----------------------------------------------------------------
        # 3. decode the token and verfiy with the public key
        #-----------------------------------------------------------------
        try:
            verify_options = {
                "verify_signature": True,
                "require": ["exp", "iat", "phone_number"] # check that the phone claim is present
            }

            decoded_claims = jwt.decode(
                token,
                public_key,
                algorithms=[AuthInterceptor.algorithm],
                options = verify_options,
                audience = AuthInterceptor.audience,
            )
        except:
            AuthInterceptor._auth_exception("Bearer Token decoding unsuccessful")

        #-------------------------------------------------------------------
        # 4.make application specific checks
        #-------------------------------------------------------------------
        # check for valid number
        if (not decoded_claims["phone_number"]):
            AuthInterceptor._auth_exception("Bearer Token decoding for empty user")

        # auth sucessfully done
        return decoded_claims
