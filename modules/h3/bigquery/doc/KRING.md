### KRING

{{% bannerNote type="code" %}}
h3.KRING(origin, size)
{{%/ bannerNote %}}

**Description**

Returns all cell indexes in a **filled hexagonal k-ring** centered at the origin in no particular order.

* `origin`: `STRING` H3 cell index of the origin.
* `size`: `INT64` size of the ring (distance from the origin).

**Return type**

`ARRAY<STRING>`

{{% customSelector %}}
**Example**
{{%/ customSelector %}}

```sql
SELECT carto-os.h3.KRING('837b59fffffffff', 1);
-- 837b59fffffffff
-- 837b58fffffffff
-- 837b5bfffffffff
-- 837a66fffffffff
-- 837a64fffffffff
-- 837b4afffffffff
-- 837b5dfffffffff
```