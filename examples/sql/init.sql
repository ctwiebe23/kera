create table ##name##
( ##columns(\n, ){{ ##name## ##type## ##[is_pk]{{ primary key auto_increment not null }} }}
##columns{{ ##[fk_for]{{ , foreign key ##name## references ##fk_for##(id) }} }}
)
;