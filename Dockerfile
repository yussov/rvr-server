FROM fedora:36

WORKDIR /app

RUN dnf -y install --refresh python3-aiohttp python3-requests python3-uvicorn python3-pydantic python3-fastapi python3-httpx python3-pytest  \
    python3-pip && \
    dnf clean all

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt && \
    dnf remove python3-pip -y && \
    dnf clean all

COPY request_via_request_server request_via_request_server
COPY tests tests
COPY setup.py .
COPY __init__.py .

ENV PYTHONPATH "${PYTHONPATH}:/app"


RUN python3 setup.py install \
    && python3 -m pytest /app/tests \
    && rm -rf /app/tests

ENTRYPOINT ["request_via_request_server"]