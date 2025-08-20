create table Person
( id int primary key auto_increment not null
, name varchar(31) 
, age int 
, gender varchar(15) 
, originId int 
, residenceId int 
, foreign key originId references Place(id)
, foreign key residenceId references Place(id)
)
;