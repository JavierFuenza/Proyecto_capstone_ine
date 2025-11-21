from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware para agregar headers HTTP de seguridad
    Corrige vulnerabilidades identificadas en el escaneo OWASP ZAP

    Mejoras aplicadas:
    - Eliminado wildcard https: de img-src, ahora solo 'self' y data:
    - Expandido Permissions-Policy con más restricciones
    - Agregado Cross-Origin-Opener-Policy para protección adicional
    - Mejorado CSP para API REST (sin necesidad de script/style en API)
    """

    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)

        # Content Security Policy (CSP) - Protección contra XSS
        # Para una API REST, no necesitamos script-src ni style-src complejos
        csp_directives = [
            "default-src 'self'",
            "script-src 'self'",
            "style-src 'self'",
            # Eliminado wildcard https: - solo permitir 'self' y data URIs
            "img-src 'self' data:",
            "font-src 'self' data:",
            "connect-src 'self'",
            "frame-src 'none'",
            "object-src 'none'",
            "base-uri 'self'",
            "form-action 'self'",
            "frame-ancestors 'none'",
            "upgrade-insecure-requests",
        ]
        response.headers["Content-Security-Policy"] = "; ".join(csp_directives)

        # X-Frame-Options - Protección contra clickjacking
        response.headers["X-Frame-Options"] = "DENY"

        # X-Content-Type-Options - Prevenir MIME sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"

        # Permissions-Policy - Controlar features del navegador
        # Política más restrictiva con más features bloqueadas
        permissions_policy = [
            "accelerometer=()",
            "ambient-light-sensor=()",
            "autoplay=()",
            "battery=()",
            "camera=()",
            "cross-origin-isolated=()",
            "display-capture=()",
            "document-domain=()",
            "encrypted-media=()",
            "execution-while-not-rendered=()",
            "execution-while-out-of-viewport=()",
            "fullscreen=()",
            "geolocation=()",
            "gyroscope=()",
            "keyboard-map=()",
            "magnetometer=()",
            "microphone=()",
            "midi=()",
            "navigation-override=()",
            "payment=()",
            "picture-in-picture=()",
            "publickey-credentials-get=()",
            "screen-wake-lock=()",
            "sync-xhr=()",
            "usb=()",
            "web-share=()",
            "xr-spatial-tracking=()",
        ]
        response.headers["Permissions-Policy"] = ", ".join(permissions_policy)

        # Cross-Origin-Resource-Policy - Protección contra ataques Spectre
        # Para una API, usar 'cross-origin' para permitir requests desde el frontend
        response.headers["Cross-Origin-Resource-Policy"] = "cross-origin"

        # Cross-Origin-Embedder-Policy - Aislamiento entre orígenes
        # Usar 'unsafe-none' para compatibilidad con CORS
        response.headers["Cross-Origin-Embedder-Policy"] = "unsafe-none"

        # Cross-Origin-Opener-Policy - Protección adicional contra Spectre
        response.headers["Cross-Origin-Opener-Policy"] = "same-origin"

        # Referrer-Policy - Controlar información del referrer
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Strict-Transport-Security - Forzar HTTPS (en producción)
        # Este header solo debe enviarse sobre HTTPS
        # Comentar en desarrollo local sin HTTPS
        if request.url.scheme == "https":
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains; preload"
            )

        # X-XSS-Protection - Protección legacy contra XSS (compatibilidad)
        response.headers["X-XSS-Protection"] = "1; mode=block"

        return response


def add_security_middleware(app: FastAPI):
    """Agregar middleware de seguridad a la aplicación FastAPI"""
    app.add_middleware(SecurityHeadersMiddleware)
