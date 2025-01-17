### HEXRING

{{% bannerNote type="code" %}}
h3.HEXRING(origin, size)
{{%/ bannerNote %}}

**Description**

Returns all cell indexes in a **hollow hexagonal ring** centered at the origin in no particular order. Unlike [KRING](#kring), this function will throw an exception if there is a pentagon anywhere in the ring.

* `origin`: `STRING` H3 cell index of the origin.
* `size`: `INT64` size of the ring (distance from the origin).

**Return type**

`ARRAY<STRING>`

{{% customSelector %}}
**Example**
{{%/ customSelector %}}

```sql
SELECT carto-os.h3.HEXRING('837b59fffffffff', 1);
-- 837b5dfffffffff
-- 837b58fffffffff
-- 837b5bfffffffff
-- 837a66fffffffff
-- 837a64fffffffff
-- 837b4afffffffff
```