----------------------------
-- Copyright (C) 2021 CARTO
----------------------------

CREATE OR REPLACE FUNCTION @@RS_PREFIX@@s2.TOKEN_FROMID
(id INT8) 
RETURNS VARCHAR(MAX)
IMMUTABLE
AS $$
    from @@RS_PREFIX@@s2Lib import int64_id_to_token

    if id is None:
        raise Exception('NULL argument passed to UDF')
    
    return int64_id_to_token(id)
    
$$ LANGUAGE plpythonu;
