FROM debian:11

# install python3 and pip
RUN apt-get update && apt-get install -y python3.9 python3-pip
RUN python3 -m pip install --upgrade pip
RUN pip cache purge

# add and change to non-root user in image
ENV HOME=/home/worker/app
RUN adduser --home ${HOME} --disabled-password worker
RUN chown worker:worker ${HOME}
USER worker

# Set the working directory for any following RUN, CMD, ENTRYPOINT, COPY and ADD instructions
WORKDIR ${HOME}

# copy requirement file & update python environment
COPY  requirements.txt ${HOME}/requirements.txt

# copy files
COPY ./lib ${HOME}/
ENV PYTHONPATH="${HOME}/app:${PYTHONPATH}"

# install dependencies
RUN pip install -r ${HOME}/requirements.txt
EXPOSE 8080
CMD ["python3", "main.py"]