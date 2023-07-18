FROM python:3.9-alpine

LABEL maintainer="Puneet Matharu"
LABEL name="cmake-format-lint-action"
LABEL version="1.0.0"
LABEL repository="http://github.com/PuneetMatharu/cmake-format-lint-action"
LABEL homepage="http://github.com/PuneetMatharu/cmake-format-lint-action"

LABEL com.github.actions.name="cmake-format"
LABEL com.github.actions.description="Automatically formats CMake files to the required format."
LABEL com.github.actions.icon="code"
LABEL com.github.actions.color="blue"

RUN python -m pip install --no-cache-dir --upgrade pip && \
    python -m pip install --no-cache-dir \
        "Cython<3" \
        "cmakelang[YAML]==0.6.13"

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
