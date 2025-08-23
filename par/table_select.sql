select  *
from    Person
join    Place a on addressId = a.id
join    Place w on workAddressId = w.id
join    Job j on workId = j.id;
