---
title: Errors Reference
---

> This work is based on [Data Quality Spec](https://github.com/frictionlessdata/data-quality-spec)

This document provides a full reference to the Frictionless errors.

## Error

Code: `error` <br/>
Tags: `-` <br/>
Template: `{note}` <br/>
Description: `Error` <br/>


## Header Error

Code: `header-error` <br/>
Tags: `#header` <br/>
Template: `Cell Error` <br/>
Description: `Cell Error` <br/>


## Label Error

Code: `label-error` <br/>
Tags: `#header` <br/>
Template: `Label Error` <br/>
Description: `Label Error` <br/>


## Row Error

Code: `row-error` <br/>
Tags: `#content` <br/>
Template: `Row Error` <br/>
Description: `Row Error` <br/>


## Cell Error

Code: `cell-error` <br/>
Tags: `#content` <br/>
Template: `Cell Error` <br/>
Description: `Cell Error` <br/>


## Package Error

Code: `package-error` <br/>
Tags: `#general` <br/>
Template: `The data package has an error: {note}` <br/>
Description: `A validation cannot be processed.` <br/>


## Resource Error

Code: `resource-error` <br/>
Tags: `#general` <br/>
Template: `The data resource has an error: {note}` <br/>
Description: `A validation cannot be processed.` <br/>


## Pipeline Error

Code: `pipeline-error` <br/>
Tags: `#general` <br/>
Template: `The pipeline is not valid: {note}` <br/>
Description: `Provided pipeline is not valid.` <br/>


## Inquiry Error

Code: `inquiry-error` <br/>
Tags: `#general` <br/>
Template: `The inquiry is not valid: {note}` <br/>
Description: `Provided inquiry is not valid.` <br/>


## Report Error

Code: `report-error` <br/>
Tags: `#general` <br/>
Template: `The validation report has an error: {note}` <br/>
Description: `A validation cannot be presented.` <br/>


## Status Error

Code: `status-error` <br/>
Tags: `#general` <br/>
Template: `The status is not valid: {note}` <br/>
Description: `Provided status is not valid.` <br/>


## Task Error

Code: `task-error` <br/>
Tags: `#general` <br/>
Template: `The task has an error: {note}` <br/>
Description: `General task-level error.` <br/>


## Check Error

Code: `check-error` <br/>
Tags: `#general` <br/>
Template: `The validation check has an error: {note}` <br/>
Description: `A validation check cannot be created` <br/>


## Step Error

Code: `step-error` <br/>
Tags: `#general` <br/>
Template: `The transfrom step has an error: {note}` <br/>
Description: `A transform step cannot be finished` <br/>


## Storage Error

Code: `storage-error` <br/>
Tags: `#general` <br/>
Template: `The storage has an error: {note}` <br/>
Description: `A storage's operation cannot be performed` <br/>


## Source Error

Code: `source-error` <br/>
Tags: `#table` <br/>
Template: `The data source has not supported or has inconsistent contents: {note}` <br/>
Description: `Data reading error because of not supported or inconsistent contents.` <br/>


## Scheme Error

Code: `scheme-error` <br/>
Tags: `#table` <br/>
Template: `The data source could not be successfully loaded: {note}` <br/>
Description: `Data reading error because of incorrect scheme.` <br/>


## Format Error

Code: `format-error` <br/>
Tags: `#table` <br/>
Template: `The data source could not be successfully parsed: {note}` <br/>
Description: `Data reading error because of incorrect format.` <br/>


## Encoding Error

Code: `encoding-error` <br/>
Tags: `#table` <br/>
Template: `The data source could not be successfully decoded: {note}` <br/>
Description: `Data reading error because of an encoding problem.` <br/>


## Hashing Error

Code: `hashing-error` <br/>
Tags: `#table` <br/>
Template: `The data source could not be successfully hashed: {note}` <br/>
Description: `Data reading error because of a hashing problem.` <br/>


## Compression Error

Code: `compression-error` <br/>
Tags: `#table` <br/>
Template: `The data source could not be successfully decompressed: {note}` <br/>
Description: `Data reading error because of a decompression problem.` <br/>


## Control Error

Code: `control-error` <br/>
Tags: `#table #control` <br/>
Template: `Control object is not valid: {note}` <br/>
Description: `Provided control is not valid.` <br/>


## Dialect Error

Code: `dialect-error` <br/>
Tags: `#table #dialect` <br/>
Template: `Dialect object is not valid: {note}` <br/>
Description: `Provided dialect is not valid.` <br/>


## Layout Error

Code: `layout-error` <br/>
Tags: `#table #layout` <br/>
Template: `The data source could not be successfully described by the invalid Table Layout: {note}` <br/>
Description: `Provided layout is not valid.` <br/>


## Schema Error

Code: `schema-error` <br/>
Tags: `#table #schema` <br/>
Template: `The data source could not be successfully described by the invalid Table Schema: {note}` <br/>
Description: `Provided schema is not valid.` <br/>


## Field Error

Code: `field-error` <br/>
Tags: `#table schema #field` <br/>
Template: `The data source could not be successfully described by the invalid Table Schema: {note}` <br/>
Description: `Provided field is not valid.` <br/>


## Checksum Error

Code: `checksum-error` <br/>
Tags: `#table #checksum` <br/>
Template: `The data source does not match the expected checksum: {note}` <br/>
Description: `This error can happen if the data is corrupted.` <br/>


## Extra Label

Code: `extra-label` <br/>
Tags: `#header #structure` <br/>
Template: `There is an extra label "{label}" in header at position "{fieldPosition}"` <br/>
Description: `The header of the data source contains label that does not exist in the provided schema.` <br/>


## Missing Label

Code: `missing-label` <br/>
Tags: `#header #structure` <br/>
Template: `There is a missing label in the header's field "{fieldName}" at position "{fieldPosition}"` <br/>
Description: `Based on the schema there should be a label that is missing in the data's header.` <br/>


## Blank Label

Code: `blank-label` <br/>
Tags: `#header #structure` <br/>
Template: `Label in the header in field at position "{fieldPosition}" is blank` <br/>
Description: `A label in the header row is missing a value. Label should be provided and not be blank.` <br/>


## Duplicate Label

Code: `duplicate-label` <br/>
Tags: `#header #structure` <br/>
Template: `Label "{label}" in the header at position "{fieldPosition}" is duplicated to a label: {note}` <br/>
Description: `Two columns in the header row have the same value. Column names should be unique.` <br/>


## Blank Header

Code: `blank-header` <br/>
Tags: `#header #structure` <br/>
Template: `Header is completely blank` <br/>
Description: `This header is empty. A header should contain at least one value.` <br/>


## Incorrect Label

Code: `incorrect-label` <br/>
Tags: `#header #schema` <br/>
Template: `Label "{label}" in field {fieldName} at position "{fieldPosition}" does not match the field name in the schema` <br/>
Description: `One of the data source header does not match the field name defined in the schema.` <br/>


## Extra Cell

Code: `extra-cell` <br/>
Tags: `#content #structure` <br/>
Template: `Row at position "{rowPosition}" has an extra value in field at position "{fieldPosition}"` <br/>
Description: `This row has more values compared to the header row (the first row in the data source). A key concept is that all the rows in tabular data must have the same number of columns.` <br/>


## Missing Cell

Code: `missing-cell` <br/>
Tags: `#content #structure` <br/>
Template: `Row at position "{rowPosition}" has a missing cell in field "{fieldName}" at position "{fieldPosition}"` <br/>
Description: `This row has less values compared to the header row (the first row in the data source). A key concept is that all the rows in tabular data must have the same number of columns.` <br/>


## Blank Row

Code: `blank-row` <br/>
Tags: `#content #structure` <br/>
Template: `Row at position "{rowPosition}" is completely blank` <br/>
Description: `This row is empty. A row should contain at least one value.` <br/>


## Missing Cell

Code: `type-error` <br/>
Tags: `#content #schema` <br/>
Template: `The cell "{cell}" in row at position "{rowPosition}" and field "{fieldName}" at position "{fieldPosition}" has incompatible type: {note}` <br/>
Description: `The value does not match the schema type and format for this field.` <br/>


## Constraint Error

Code: `constraint-error` <br/>
Tags: `#content #schema` <br/>
Template: `The cell "{cell}" in row at position "{rowPosition}" and field "{fieldName}" at position "{fieldPosition}" does not conform to a constraint: {note}` <br/>
Description: `A field value does not conform to a constraint.` <br/>


## Unique Error

Code: `unique-error` <br/>
Tags: `#content #schema #integrity` <br/>
Template: `Row at position "{rowPosition}" has unique constraint violation in field "{fieldName}" at position "{fieldPosition}": {note}` <br/>
Description: `This field is a unique field but it contains a value that has been used in another row.` <br/>


## PrimaryKey Error

Code: `primary-key-error` <br/>
Tags: `#content #schema #integrity` <br/>
Template: `The row at position "{rowPosition}" does not conform to the primary key constraint: {note}` <br/>
Description: `Values in the primary key fields should be unique for every row` <br/>


## ForeignKey Error

Code: `foreign-key-error` <br/>
Tags: `#content #schema #integrity` <br/>
Template: `The row at position "{rowPosition}" does not conform to the foreign key constraint: {note}` <br/>
Description: `Values in the foreign key fields should exist in the reference table` <br/>


## Duplicate Row

Code: `duplicate-row` <br/>
Tags: `#content #heuristic` <br/>
Template: `Row at position {rowPosition} is duplicated: {note}` <br/>
Description: `The row is duplicated.` <br/>


## Deviated Value

Code: `deviated-value` <br/>
Tags: `#content #heuristic` <br/>
Template: `There is a possible error because the value is deviated: {note}` <br/>
Description: `The value is deviated.` <br/>


## Truncated Value

Code: `truncated-value` <br/>
Tags: `#content #heuristic` <br/>
Template: `The cell {cell} in row at position {rowPosition} and field {fieldName} at position {fieldPosition} has an error: {note}` <br/>
Description: `The value is possible truncated.` <br/>


## Blacklisted Value

Code: `blacklisted-value` <br/>
Tags: `#content #regulation` <br/>
Template: `The cell {cell} in row at position {rowPosition} and field {fieldName} at position {fieldPosition} has an error: {note}` <br/>
Description: `The value is blacklisted.` <br/>


## Sequential Value

Code: `sequential-value` <br/>
Tags: `#content #regulation` <br/>
Template: `The cell {cell} in row at position {rowPosition} and field {fieldName} at position {fieldPosition} has an error: {note}` <br/>
Description: `The value is not sequential.` <br/>


## Row Constraint

Code: `row-constraint` <br/>
Tags: `#content #regulation` <br/>
Template: `The row at position {rowPosition} has an error: {note}` <br/>
Description: `The value does not conform to the row constraint.` <br/>