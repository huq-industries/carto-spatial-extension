### ISPENTAGON

{{% bannerNote type="code" %}}
h3.ISPENTAGON(index)
{{%/ bannerNote %}}

**Description**

Returns `true` if given H3 index is a pentagon. Returns `false` otherwise, even on invalid input.

* `index`: `STRING` The H3 cell index.

**Return type**

`BOOLEAN`

{{% customSelector %}}
**Example**
{{%/ customSelector %}}

```sql
SELECT carto-os.h3.ISPENTAGON('837b59fffffffff');
-- false
```

```sql
SELECT carto-os.h3.ISPENTAGON('8075fffffffffff');
-- true
```