FROM golang:latest as builder  
RUN mkdir -p /src && cd /src && git clone https://github.com/monster1025/presence.git     .
WORKDIR /src
RUN go get -d
RUN CGO_ENABLED=0 go build -a -installsuffix cgo -o app .    


FROM alpine:latest  
WORKDIR /
ADD ./run.sh /run.sh
RUN chmod +x /run.sh
COPY --from=builder /src/app .
COPY --from=builder /src/static_html /static_html
CMD ["/run.sh"]