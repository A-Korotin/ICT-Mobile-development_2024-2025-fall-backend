from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi_jwt import JwtAccessBearer, JwtAuthorizationCredentials
from sqlmodel import Session, select

from src.db.db import get_session
from src.model.user import User
from src.router.auth.dto import JwtDto, RegisterDto, LoginDto, AccountInfoDto, AccountInfoEditDto
from src.router.error_dto import ErrorDto
from src.util.crypt import get_password_hash, generate_jwt, verify_password_hash, JWT_SECRET

router = APIRouter()


@router.post("/register", response_model=JwtDto, status_code=201,
             responses={
                 201: {"model": JwtDto},
                 409: {"model": ErrorDto}
             })
def register(register_dto: RegisterDto, db: Session = Depends(get_session)) -> JwtDto:
    register_dto = RegisterDto.validate(register_dto)
    user: User = User(**register_dto.model_dump())

    existing: User | None = db.exec(select(User).where(User.username == user.username)).first()
    if existing is not None:
        raise HTTPException(status_code=409)

    user.password = get_password_hash(user.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return JwtDto(token=generate_jwt(user))


@router.post("/login", response_model=JwtDto, status_code=200,
             responses={
                 200: {"model": JwtDto},
                 401: {"model": ErrorDto}
             })
def login(login_dto: LoginDto, db: Session = Depends(get_session)) -> JwtDto:
    login_dto = LoginDto.validate(login_dto)
    existing: User | None = db.exec(select(User).where(User.username == login_dto.username)).first()
    if existing is None or existing.is_active is False:
        raise HTTPException(status_code=401)

    if not verify_password_hash(login_dto.password, existing.password):
        raise HTTPException(status_code=401)

    return JwtDto(token=generate_jwt(existing))


access_security = JwtAccessBearer(secret_key=JWT_SECRET, auto_error=True)


@router.get("/me", response_model=AccountInfoDto, status_code=200,
            responses={
                200: {"model": AccountInfoDto},
                401: {"model": ErrorDto}
            })
def get_self(credentials: JwtAuthorizationCredentials = Security(access_security),
             db: Session = Depends(get_session)) -> AccountInfoDto:
    existing: User | None = db.exec(select(User).where(User.username == credentials['username'])).first()
    if not existing:
        raise HTTPException(status_code=401)

    return AccountInfoDto(username=existing.username, name=existing.name, profile_picture=existing.profile_picture)


@router.patch("/me", response_model=AccountInfoDto, status_code=200,
              responses={
                  200: {"model": AccountInfoDto},
                  401: {"model": ErrorDto}
              })
def edit_self(edit_dto: AccountInfoEditDto, credentials: JwtAuthorizationCredentials = Security(access_security),
              db: Session = Depends(get_session)) -> AccountInfoDto:
    existing: User | None = db.exec(select(User).where(User.username == credentials['username'])).first()
    if not existing:
        raise HTTPException(status_code=401)

    if edit_dto.name is not None:
        existing.name = edit_dto.name

    if edit_dto.profile_picture is not None:
        existing.profile_picture = edit_dto.profile_picture

    if edit_dto.password is not None:
        existing.password = get_password_hash(edit_dto.password)

    db.add(existing)
    db.commit()
    db.refresh(existing)

    return AccountInfoDto(username=existing.username, name=existing.name, profile_picture=existing.profile_picture)


@router.delete("/me", response_model=None, status_code=204,
               responses={
                   204: {},
                   401: {"model": ErrorDto}
               })
def delete_self(credentials: JwtAuthorizationCredentials = Security(access_security),
                db: Session = Depends(get_session)) -> None:
    existing: User | None = db.exec(select(User).where(User.username == credentials['username'])).first()
    if not existing:
        raise HTTPException(status_code=401)

    existing.is_active = False

    db.add(existing)
    db.commit()
