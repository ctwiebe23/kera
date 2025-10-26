SELECT  *
FROM    Person
     -- ^ Table in the parent scope
JOIN    Place a ON addressId = a.id
     -- ^ Table in the child scope overrides parent scope
JOIN    Place w ON workAddressId = w.id
     -- ^ Table in the child scope overrides parent scope
JOIN    Job j ON workId = j.id
     -- ^ Table in the child scope overrides parent scope;
