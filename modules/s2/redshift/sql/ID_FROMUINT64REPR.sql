----------------------------
-- Copyright (C) 2021 CARTO
----------------------------

CREATE OR REPLACE FUNCTION @@RS_PREFIX@@s2.ID_FROMUINT64REPR
(uid VARCHAR(MAX)) 
RETURNS INT8
IMMUTABLE
AS $$
    from @@RS_PREFIX@@s2Lib import uint64_to_int64

    if uid is None:
        raise Exception('NULL argument passed to UDF')
    
    return uint64_to_int64(int(uid))
    
$$ LANGUAGE plpythonu;
