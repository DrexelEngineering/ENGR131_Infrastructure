# Build Docker Image

## Build Docker Image

```bash
envtag="2.0.0"
tagname=$envtag
docker build -t $dockeruser/$envcontainer:$envtag . &&
docker push $dockeruser/$envcontainer:$envtag &&
docker tag $dockeruser/$envcontainer:$envtag $dockeruser/$envcontainer:latest &&
docker push $dockeruser/$envcontainer:latest
```

## This will push to the gitlab registry

```bash
tagname=$envtag
docker build -t gitlab-registry.nrp-nautilus.io/$nrpgitlabuser/$envcontainer:$envtag . && docker push gitlab-registry.nrp-nautilus.io/$nrpgitlabuser/$envcontainer:$envtag && docker tag gitlab-registry.nrp-nautilus.io/$nrpgitlabuser/$envcontainer:$envtag gitlab-registry.nrp-nautilus.io/$nrpgitlabuser/$envcontainer:latest && docker push gitlab-registry.nrp-nautilus.io/$nrpgitlabuser/$envcontainer:latest
```
