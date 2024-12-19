from ninja import Router
from ninja.errors import HttpError
from django.http import JsonResponse

from clients.schemas.auth_schemas import CompteLoginSchema, CompteRegisterSchema, CompteUpdateSchema, ResetPasswordSchema
from clients.services.auth_services import AuthService
from utils.get_ip_client import get_client_ip
from utils.jwt_handler import create_jwt, decode_jwt

auth_router = Router()

@auth_router.get("/user-info")
def user_info(request):
    token = request.COOKIES.get('token')
    if not token:
        raise HttpError(message="Token non fourni", status_code=401)

    user_data = decode_jwt(token)
    return {
        "id": user_data["id"],
        "email": user_data["email"],
        "is_active": user_data["is_active"],
        "is_suspended": user_data["is_suspended"]
    }


@auth_router.post("/register", auth=None)
def register(request, data: CompteRegisterSchema):
    ip_address = get_client_ip(request)
    try:
        user = AuthService.register(data, ip_address)
        return {"success": True, "user": user.email}
    except ValueError as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)

@auth_router.post("/login", auth=None)
def login(request, data: CompteLoginSchema):
    try:
        user = AuthService.login(data.email, data.password)
        token = create_jwt(user)

        response = JsonResponse({"success": True, "token": token})
        # Ajouter le cookie HTTPOnly
        response.set_cookie('token', token, httponly=True)
        return response
    except HttpError as e:
        return JsonResponse({"success": False, "error": str(e)}, status=e.status_code)


@auth_router.post("/reset-password", auth=None)
def reset_password(request, data: ResetPasswordSchema):
    try:
        user = AuthService.reset_password(data.email)
        return {"success": True, "message": f"Un email de réinitialisation a été envoyé à {user.email}"}
    except ValueError as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)


@auth_router.put("/update", auth=None)
def update_user(request, data: CompteUpdateSchema):
    user = request.user  # Récupérer l'utilisateur actuellement connecté
    ip_address = get_client_ip(request)
    try:
        updated_user = AuthService.update_user(user, data, ip_address)
        return {"success": True, "user": updated_user.email}
    except ValueError as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)