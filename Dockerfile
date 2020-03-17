FROM python:3
LABEL maintainer="yamaguchi@atma.co.jp"

RUN pip install -U pip
ADD . .


RUN groupadd -g 1000 guruguru && \
    useradd -g guruguru -G sudo -m -s /bin/bash guruguru && \
    echo 'guruguru:guruguru' | chpasswd

RUN python setup.py sdist && \
  pip install $(ls dist/*.tar.gz)[test]

WORKDIR /workspace
RUN chown -R guruguru:guruguru /workspace
USER guruguru

CMD ["/bin/bash"]