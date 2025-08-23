CREATE PROCEDURE insert_into_Record
( p_create_date IN DATE
, p_update_date IN DATE
, p_id IN INTEGER
, p_content IN TEXT
)
BEGIN

    INSERT
    INTO    Record
            ( create_date
            , update_date
            , id
            , content
            )
    VALUES  ( p_create_date
            , p_update_date
            , p_id
            , p_content
            );

END insert_into_Record;
