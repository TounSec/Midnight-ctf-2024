FROM scratch

WORKDIR /app
COPY ./Challenge/midnight /app/

ENTRYPOINT [ "/app/midnight" ]
