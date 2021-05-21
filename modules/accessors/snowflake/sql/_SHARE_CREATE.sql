----------------------------
-- Copyright (C) 2021 CARTO
----------------------------

USE @@SF_DATABASE@@;

CREATE SHARE IF NOT EXISTS @@SF_SHARE_PUBLIC@@;
grant usage on database @@SF_DATABASE@@ to share @@SF_SHARE_PUBLIC@@;
grant usage on schema @@SF_DATABASE@@.@@SF_SCHEMA@@ to share @@SF_SHARE_PUBLIC@@;

grant usage on function @@SF_PREFIX@@accessors.ST_ENVELOPE(ARRAY) to share @@SF_SHARE_PUBLIC@@;
grant usage on function @@SF_PREFIX@@accessors.VERSION() to share @@SF_SHARE_PUBLIC@@;