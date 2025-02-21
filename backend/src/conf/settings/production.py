from src.conf.settings.app import AppSettings


class ProdAppSettings(AppSettings):
    title: str = "SEC.CAFE 安全咖啡 APIs"

    class Config(AppSettings.Config):
        env_file =  ".envs/prod.env", ".envs/prod.db.env"
