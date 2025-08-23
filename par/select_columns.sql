CREATE PROCEDURE insert_into_##table##
( ##columns(\n, ){{
    p_##name## IN ##type##
  }}
)
BEGIN

    INSERT
    INTO    ##table##
            ( ##columns(\n            , ){{
                ##name##
              }}
            )
    VALUES  ( ##columns(\n            , ){{
                p_##name##
              }}
            );

END insert_into_##table##;
