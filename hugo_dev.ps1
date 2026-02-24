$ErrorActionPreference = "Stop"

docker run --rm `
  -v ${PWD}:/src `
  -w /src `
  --entrypoint sh `
  hugomods/hugo:git `
  -lc "sh ./scripts/gen-git-history.sh --limit 10"

docker run --rm `
  -v ${PWD}:/src `
  -v ${HOME}/hugo_cache:/tmp/hugo_cache `
  -v ${PWD}/public:/site `
  -w /src `
  hugomods/hugo:git `
  --destination /site
