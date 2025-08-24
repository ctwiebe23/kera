SELECT  *
FROM    Person
JOIN    Place a ON addressId = a.id
JOIN    Place w ON workAddressId = w.id
JOIN    Job j ON workId = j.id;
