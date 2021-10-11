#!/usr/bin/env bash

# Script to create a Spatial Extension package for BigQuery

# * BQ_BUCKET


PACKAGE_TAG="$(git log -1 --format=%cd --date=short).$(git rev-parse --short HEAD)"
PACKAGE_NAME="carto-spatial-extension-bigquery"

PACKAGE_BUCKET="${BQ_BUCKET}/${PACKAGE_NAME}/bigquery/packages"

echo "Creating installation package $PACKAGE_BUCKET/$PACKAGE_NAME-$PACKAGE_TAG.zip"

SCRIPT_DIR=$( dirname "$0" )

ROOT_DIR=$SCRIPT_DIR/../..
DIST_DIR=$ROOT_DIR/dist

rm -rf $DIST_DIR
mkdir -p $DIST_DIR/libs

# Generate core modules
$SCRIPT_DIR/serialize_modules.sh $ROOT_DIR $DIST_DIR/core
cat $DIST_DIR/core/modules.sql >> $DIST_DIR/modules.sql
mv $DIST_DIR/core/libs/*/ $DIST_DIR/libs/
rm -rf $DIST_DIR/core

# Generate the package
cp $SCRIPT_DIR/package/README.md $DIST_DIR/
cp $SCRIPT_DIR/package/install_spatial_extension.sh $DIST_DIR/
CWD=$(pwd)
cd $DIST_DIR && zip -r $PACKAGE_NAME-$PACKAGE_TAG.zip * && cd $CWD

# Upload the package to the bucket
gsutil -h "Content-Type:application/zip" cp $DIST_DIR/$PACKAGE_NAME-$PACKAGE_TAG.zip "gs://$PACKAGE_BUCKET/"
