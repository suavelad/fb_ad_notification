from decouple import config


# Database url configuration
DATABASE_URL = (
    "postgresql+psycopg2://{username}:{password}@{host}:{port}/{db_name}".format(
        host=config("POSTGRES_HOST"),
        port=config("POSTGRES_PORT"),
        db_name=config("POSTGRES_DB"),
        username=config("POSTGRES_USER"),
        password=config("POSTGRES_PASSWORD"),
    )
)
