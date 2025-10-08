# app/settings.py
from __future__ import annotations
from dataclasses import dataclass
from configparser import ConfigParser
from pathlib import Path
import os

ENV_PATH = Path(__file__).resolve().parent.parent / ".env"  # à la racine du projet

def _load_config(path: Path) -> ConfigParser:
    cfg = ConfigParser()
    # Ne modifie pas la casse des clés
    cfg.optionxform = str  # type: ignore[attr-defined]
    if path.exists():
        cfg.read(path, encoding="utf-8")
    return cfg

def _get(cfg: ConfigParser, section: str, key: str, env_name: str | None = None, fallback: str | None = None) -> str | None:
    """
    Priorité: variable d'environnement > .env (INI) > fallback
    """
    if env_name is None:
        env_name = key  # ex: JWT_SECRET
    if (val := os.getenv(env_name)) not in (None, ""):
        return val
    if cfg.has_option(section, key):
        v = cfg.get(section, key)
        return v if v != "" else fallback
    return fallback

def _get_int(cfg: ConfigParser, section: str, key: str, env_name: str | None = None, fallback: int | None = None) -> int:
    val = _get(cfg, section, key, env_name=env_name, fallback=None)
    if val is None or val == "":
        if fallback is None:
            raise ValueError(f"Missing integer setting: [{section}] {key}")
        return fallback
    try:
        return int(val)
    except ValueError:
        raise ValueError(f"Invalid integer for [{section}] {key}: {val!r}")

def _get_list(cfg: ConfigParser, section: str, key: str, env_name: str | None = None, fallback: list[str] | None = None) -> list[str]:
    val = _get(cfg, section, key, env_name=env_name, fallback=None)
    if val is None:
        return fallback or []
    return [s.strip() for s in val.split(",") if s.strip()]

@dataclass(frozen=True)
class Settings:
    # DB
    database_url: str
    database_key: str

    # JWT
    jwt_secret: str
    jwt_alg: str
    access_token_expires_min: int
    refresh_token_expires_days: int

    # CORS
    cors_origins: list[str]

    # Stripe
    stripe_secret_key: str | None
    stripe_webhook_secret: str | None

def load_settings() -> Settings:
    cfg = _load_config(ENV_PATH)

    # --- DB ---
    # Tu as fourni:
    # [DB]
    # DATABASE_PASSWORD=...
    # DATABASE_URL=
    # On exige DATABASE_URL (plus simple). Si vide, on lève une erreur claire.
    database_url = _get(cfg, "DB", "DATABASE_URL", env_name="DATABASE_URL", fallback=None)
    database_key = _get(cfg, "DB", "DATABASE_KEY", env_name="DATABASE_KEY", fallback=None)
    if not database_url:
        # Message explicite pour éviter les surprises en runtime
        raise ValueError(
            "DATABASE_URL manquant. Exemple:\n"
            "postgresql+psycopg://USER:PASSWORD@HOST:5432/DBNAME\n"
            "→ Remplis [DB].DATABASE_URL dans .env ou exporte une variable d'env DATABASE_URL."
        )

    # --- JWT ---
    jwt_secret = _get(cfg, "JWT", "JWT_SECRET", env_name="JWT_SECRET", fallback=None)
    if not jwt_secret or jwt_secret == "change_me_super_secret":
        # Tu peux assouplir si tu veux autoriser la valeur par défaut
        raise ValueError("JWT_SECRET manquant ou valeur par défaut non sécurisée. Mets une vraie clé secrète dans [JWT].JWT_SECRET.")

    jwt_alg = _get(cfg, "JWT", "JWT_ALG", env_name="JWT_ALG", fallback="HS256") or "HS256"
    access_min = _get_int(cfg, "JWT", "ACCESS_TOKEN_EXPIRES_MIN", env_name="ACCESS_TOKEN_EXPIRES_MIN", fallback=15)
    refresh_days = _get_int(cfg, "JWT", "REFRESH_TOKEN_EXPIRES_DAYS", env_name="REFRESH_TOKEN_EXPIRES_DAYS", fallback=14)

    # --- CORS ---
    cors = _get_list(cfg, "CORS", "CORS_ORIGINS", env_name="CORS_ORIGINS", fallback=["http://localhost:5173", "http://localhost:3000"])

    # --- Stripe ---
    stripe_secret = _get(cfg, "Stripe", "STRIPE_SECRET_KEY", env_name="STRIPE_SECRET_KEY", fallback=None)
    stripe_wh = _get(cfg, "Stripe", "STRIPE_WEBHOOK_SECRET", env_name="STRIPE_WEBHOOK_SECRET", fallback=None)

    return Settings(
        database_url=database_url,
        database_key=database_key,
        jwt_secret=jwt_secret,
        jwt_alg=jwt_alg,
        access_token_expires_min=access_min,
        refresh_token_expires_days=refresh_days,
        cors_origins=cors,
        stripe_secret_key=stripe_secret,
        stripe_webhook_secret=stripe_wh,
    )

# Singleton accessible partout
settings = load_settings()