v0.2.0
---
* removed unnecesary `print()` statement.
* Added *pep8* recommendations.
* Added `:filename` pattern.
* Added `:uuid` pattern.
* Added `:query` pattern.
* Unregisted patterns are of type `:slug` by default.

v0.1.3
---
* Fixed fatal bug when using nested routes.

v0.1.2
---
* Fixed bug when `route == '^$'` or `route == '/'`
* Removed adding `/` at the end of the route if it's not an exact route.
* Trim route with spaces. Ex: `'  news/today  '` => `'^news/today$'`
* Fixed bug when a route ended with a slash and contained spaces. Ej: `'  /users/  '`

v0.1.1
---
* Changed package description

v0.1.0
---
* Basic functionality