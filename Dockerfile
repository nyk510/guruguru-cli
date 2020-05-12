FROM python:3
LABEL maintainer="yamaguchi@atma.co.jp"

RUN pip install -U pip

RUN groupadd -g 1000 guruguru && \
    useradd -g guruguru -G sudo -m -s /bin/bash guruguru && \
    echo 'guruguru:guruguru' | chpasswd

WORKDIR /workspace
ADD . .
RUN chown -R guruguru:guruguru /workspace
USER guruguru
RUN python -m venv /home/guruguru/.venv
ENV PATH=/home/guruguru/.venv/bin/:${PATH}

RUN python setup.py sdist && \
  pip install $(ls dist/*.tar.gz)[test]

CMD ["/bin/bash"]
