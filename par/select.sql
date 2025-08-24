SELECT  *
FROM    ##table##
##joins{{
    JOIN    ##table## ##alias## ON ##join-on## = ##alias##.id
}};
