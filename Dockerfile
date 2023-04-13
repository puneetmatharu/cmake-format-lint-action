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

RUN pip3 install --upgrade pip && pip install "cmakelang[YAML]==0.6.13" && pip3 install pyyaml

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
