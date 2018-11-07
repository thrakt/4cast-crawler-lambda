# About project

I can't say that.

#### deploy

1. set up apex http://apex.run/
2. execut init to create iam role. input project name you like.
```
apex init
```
3. remove created `hello` project.
4. execute apex with variables:
```
apex deploy -s SESSIONID=...
```
5. set CloudWatch manually.
