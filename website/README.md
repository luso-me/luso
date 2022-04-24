# Local Dev

- create .env file in the same directory as this file with the following contents

```
API_URL=http://localhost:5000
ROLLUP_WATCH=true
```


## Starting Local Server

```shell
$> npm run json-server --port 5000
```

## commits

### jest / routify mock / svelte store issue

commit: 34f42382eec89ea58b9fbacaf9c8b94308526060

options:

- wait until routify v3 is released as that has better support for jest
- switch out jest for another framework (e.g. cypress / mocha [svelte default] / vitest)
- wait until svelte has better support for mocking stores

## cypress

### create local config

name: cypress.env.json

content:

```json
{
  "baseUrl": "http://localhost:7000",
  "jwtAccessToken": "<get_valid_jwt_token_from_svelte_store>",
  "userId": "<your_user_id>"
}
```


# axios

currently broken with version >= 0.22.0 [1]

[1] https://www.reddit.com/r/sveltejs/comments/qiityh/comment/hil1gkw/?utm_source=share&utm_medium=web2x&context=3


# Seeing warning like this

'<App>' was created with unknown prop 'name'
'<NotFound>' was created with unknown prop 'params'

[2] https://github.com/sveltejs/svelte/issues/4652

# Node Version

v14+
