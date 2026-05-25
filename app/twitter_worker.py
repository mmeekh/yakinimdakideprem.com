import os
import time
import logging

from .twitter_bot import run_once


POLL_INTERVAL = int(float(os.getenv("TWITTER_POLL_INTERVAL", "300")))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def main():
    logging.info("Twitter worker başlatıldı. Aralık: %s sn", POLL_INTERVAL)
    while True:
        try:
            run_once()
        except Exception as exc:
            logging.error("Worker hata: %s", exc)
        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()
