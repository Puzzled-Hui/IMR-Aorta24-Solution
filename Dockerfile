#FROM --platform=linux/amd64 pytorch/pytorch
#FROM pytorch/pytorch:1.12.0-cuda11.3-cudnn8-runtime
FROM pytorch/pytorch:2.4.0-cuda12.1-cudnn9-runtime
#FROM pytorch/pytorch:2.3.1-cuda12.1-cudnn8-runtime

ENV PYTHONUNBUFFERED 1

RUN groupadd -r user && useradd -m --no-log-init -r -g user user
USER user

WORKDIR /opt/app

# Add the directory containing the scripts to PATH
ENV PATH="/home/user/.local/bin:$PATH"
ENV LD_LIBRARY_PATH="/usr/local/cuda/lib64:${LD_LIBRARY_PATH}"

#COPY --chown=user:user requirements.txt /opt/app/
#COPY --chown=user:user resources /opt/app/resources

## Copy all files from the
COPY --chown=user:user ./ /opt/app/

RUN pip install pip -U
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

RUN pip install -e .

RUN python -m pip install \
    --user \
    --no-cache-dir \
    --no-color \
    --requirement /opt/app/requirements.txt

#COPY --chown=user:user inference.py /opt/app/

ENTRYPOINT ["python", "inference.py"]