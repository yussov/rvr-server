# request via request service
mini web server for sending REST requests through it

[![777.jpg](https://i.postimg.cc/T3kz6jxb/777.jpg)](https://postimg.cc/0zwWGwb5)


## API

```commandline
POST /curl/get  get request
Request body:
{
    url: str - target request
    answer_type: str - answer type (status_code, json, content, headers)
}
Response code: 200
```

```commandline
POST "/curl/get?proxy=true"  get request via proxy
Request body:
{
    url: str - target url
    answer_type: str - response type (status_code, json, content, headers)
    proxy_server: Proxy  - proxy server (url, port)
}
Response code: 200
```

```commandline
POST /curl/post  post request
Request body:
{
    url: str - target url
    answer_type: str - repsponse type (status_code, json, content, headers)
    data: dict[str, Any] - request data
}
Response code: 200
```

```commandline
POST /curl/post?proxy=true  post request via proxy
Request body:
{
    url: str - target url
    answer_type: str - response type (status_code, json, content, headers)
    data: dict[str, Any] - request data
    proxy_server: Proxy  - proxy server (url, port)
}
Response code: 200
```

```commandline
POST /doh  resolve dns over https
Request body :
{
    domain: str - domain to resolve
    doh_server: - DNS-over-HTTPS server
}
Response code: 200
Response body: Doh_response
```

```commandline
GET /ping  check service available
Response code: 200 
Response content: pong
```

## Objects
### Proxy
```json
{
  "proxy_url": str,
  "port": int,
}
```
### Doh_response

```json
{
  "doh_response": str
}
```

### Deploy

```commandline
docker build -t {server_name} .
docker run -ti -p 8080:8080 {server_name}
```