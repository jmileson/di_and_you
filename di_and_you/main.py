from di_and_you.logger import logger


def mainv1():
    from .db import FactorDbV1

    logger.info("starting to load data")
    db = FactorDbV1()
    db.load_db()
    logger.info(f"loaded `{db.count()}` rows")

    result = db.find("Sentinel-2A")
    logger.info(f"got result `{result}`")

    logger.info("cleaning up db")
    db.cleanup()


def mainv2():
    from .csv_loader import URL, load_csv_v2
    from .db import DB_PATH, FactorDbV2, make_connection

    logger.info("starting to load data")
    # I could pass a class here if I wanted!
    # maybe I want to cache the file locally and check for a cached file
    # before hitting the network.  I can create a class that conforms to the
    # Session class interface and make that happen
    data = load_csv_v2(URL)

    # conn could be in memory at this point, the path is irrelevant
    # to the FactorDbV2 class and is an implementation detail of the database
    conn = make_connection(DB_PATH)
    db = FactorDbV2(conn, DB_PATH)
    db.load_db(data)
    logger.info(f"loaded `{db.count()}` rows")

    result = db.find("Sentinel-2A")
    logger.info(f"got result `{result}`")

    logger.info("cleaning up db")
    db.cleanup()


def main():
    mainv1()
    mainv2()


if __name__ == "__main__":
    main()
