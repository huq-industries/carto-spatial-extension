----------------------------
-- Copyright (C) 2021 CARTO
----------------------------

CREATE OR REPLACE FUNCTION @@RS_PREFIX@@s2.RESOLUTION
(id INT8)
RETURNS INT4
IMMUTABLE
AS $$
    from @@RS_PREFIX@@s2Lib import get_resolution

    if id is None:
        raise Exception('NULL argument passed to UDF')
    
    return get_resolution(id)
    
$$ LANGUAGE plpythonu;
