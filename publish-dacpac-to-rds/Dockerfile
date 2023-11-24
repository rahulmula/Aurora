FROM ubuntu:latest

#Install dependencies
RUN apt-get update && \
    apt-get install -y unzip && \
    apt-get install libunwind8 && \
    apt-get install -y dotnet-sdk-7.0 && \
    DEBIAN_FRONTEND="noninteractive" apt-get install -y awscli && \ 
    apt-get install -y python3 && \ 
    apt-get install -y python3-pip
RUN mkdir /sqltools
COPY sqlpackage_linux.zip /sqltools/
RUN unzip /sqltools/sqlpackage_linux.zip -d /sqltools/
RUN rm -rf /sqltools/sqlpackage_linux.zip
RUN chmod a+x /sqltools/sqlpackage
COPY scripts/drawingmanager.sh  /drawingmanager.sh

ENV PATH="/sqltools/sqlpackage:${PATH}"


RUN mkdir -p ${LAMBDA_TASK_ROOT}/${FUNCTION_DIR}

COPY app/* ${LAMBDA_TASK_ROOT}/${FUNCTION_DIR}
RUN pip install \
        --target ${LAMBDA_TASK_ROOT}/${FUNCTION_DIR} \
        awslambdaric

ENTRYPOINT [ "/usr/bin/python3", "-m", "awslambdaric" ]
