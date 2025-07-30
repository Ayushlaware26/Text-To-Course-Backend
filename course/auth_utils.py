import json
from urllib.request import urlopen
from jose import jwt
from django.http import JsonResponse
from functools import wraps
from django.conf import settings

AUTH0_DOMAIN = getattr(settings, "AUTH0_DOMAIN", None)
API_IDENTIFIER = getattr(settings, "API_IDENTIFIER", None)
ALGORITHMS = ["RS256"]

# Download JWKS (public keys) from Auth0
jwks_url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
jwks = json.loads(urlopen(jwks_url).read())

def get_token_auth_header(request):
    """Extract token from Authorization header"""
    auth = request.headers.get("Authorization", None)
    if not auth:
        return None
    parts = auth.split()
    if parts[0].lower() != "bearer" or len(parts) != 2:
        return None
    return parts[1]

def require_auth(view_func):
    """Decorator to protect endpoints"""

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        token = get_token_auth_header(request)
        if not token:
            return JsonResponse({"error": "Authorization header missing"}, status=401)

        try:
            # Decode token
            unverified_header = jwt.get_unverified_header(token)
            rsa_key = {}
            for key in jwks["keys"]:
                if key["kid"] == unverified_header["kid"]:
                    rsa_key = {
                        "kty": key["kty"],
                        "kid": key["kid"],
                        "use": key["use"],
                        "n": key["n"],
                        "e": key["e"],
                    }
            if not rsa_key:
                return JsonResponse({"error": "Invalid header"}, status=401)

            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_IDENTIFIER,
                issuer=f"https://{AUTH0_DOMAIN}/",
            )

            # Attach user info to request
            request.auth_payload = payload
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=401)

        return view_func(request, *args, **kwargs)

    return wrapper
