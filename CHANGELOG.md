v0.1.2 (Develop)
---
* Fixed bug when `route == '^$'` or `route == '/'`
* Removed adding `/` at the end of the route if it's not an exact route.
* Trim route with spaces. Ex: `'  news/today  '` => `'^news/today$'`
* Fixed bug when a route contained spaces and a slash at the end. Ej: '  /users/  '

v0.1.1
---
* Changed package description

v0.1.0
---
* Basic functionality