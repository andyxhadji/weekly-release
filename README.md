To build a new andyxhadji/hub image
===================================

```
docker build . -t andyxhadji/hub
docker login
docker push andyxhadji/hub
```

See image here: https://hub.docker.com/r/andyxhadji/hub

Note: Ensure you do this on a raspberry pi itself, for supported architecture.

### Roadmap

- [x] K3s on rpis (leader & worker)
- [x] Manual workflow for building Dockerfile and docker hub setup
- [x] Simple deployment for a web api with ingress
- [ ] Convert existing weekly-release to use python3
- [ ] Setup up all api keys in k3s cluster
- [ ] Import weekly-release code into web API
- [ ] Test weekly-release with dry-run & endpoint
- [ ] Simple weekly-release UI on the web
- [ ] Use for release!
