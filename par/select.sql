SELECT  *
FROM    ##table##
     -- ^ Table in the parent scope
##joins{{
JOIN    ##table## ##alias## ON ##join-on## = ##alias##.id
     -- ^ Table in the child scope overrides parent scope
}};
