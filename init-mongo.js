db.createUser({ user: "root", pwd: "pass", roles: [{ role: "dbAdmin", db: "mypydb" }] })