"""Logger utility module.

프로젝트 전역에서 사용할 로거를 생성한다.
"""

import logging


def get_logger(name: str) -> logging.Logger:
    """지정한 이름의 로거를 반환한다."""
    # TODO: 파일 로깅, 로그 포맷, 로그 레벨 설정 파일화
    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(name)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.setLevel(logging.INFO)
    return logger
