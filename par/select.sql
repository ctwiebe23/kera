select  *
from    ##table##
##joins{{
    join    ##table## ##alias## on ##join-on## = ##alias##.id
}};
