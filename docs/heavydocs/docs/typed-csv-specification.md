# Typed CSV Specification

## Rationale

The purpose of the typed csv specification is to build on the common csv (comma separated value) specification with a standard unambigious format.

The key issues with most csv files at present are:

* Character encodings are not defined
* The data has no type attributes, so `1` could be considered an integer, floating point number, or a string. File loaders often have to guess the type, and modelling software needs to be written to explicitly cast types.

## Example

An example of typed csv:

<pre>
# comment lines
@ author: name@domain.com
@ write_date: 2020_03_50
!,time,score,word,is_first,price,start_date,start_time
?,int,float,str,bool,dec,yyyy_mm_dd,hh_mm_ss
*,1,1.23,hello,Y,2.52,2020_03_28,14_20_40
</pre>

## Key Rules

* Typed CSV files are always encoded as UTF-8.
* All header names, header types and data rows must have the same length.
* The first character in the line determines the purpose of the line.
* The first character must be followed by a comma if it is `!`,`?` or `*`.
* the separator defaults to comma `,`.
* `@` can have a space between it and the metadata key.
* All meta data must be above the header row
* Rows must be in the following order: meta > header > types > data
* Comments can be placed anywhere and will be ignored
* Rows must end with a new line character `\n`

| Character | Purpose           | Notes  |
| :--------:|:-------------| -----:|
| \#        | comment | ignored |
| @         | metadata | for storing individual values, key and value are separated by a colon `:` |
| \!        | header | names of the columns in the data |
| ?         | data types | the type of data in the column |
| \*        | data row | a row of data values |

## Data Types

 * `int`: Integer (..., -3, -2, -1, 0, 1, 2, 3, ...)
 * `float`: Floating Point Number (13523.524), only decimal notation is supported
 * `str`: String/Text
 * `bool`: Boolean, using the following (case insensitive)
    - `T`, `1`, `Y`, `true` evaluate to True
    - `F`, `0`, `N`, `false`, evaluate to False
 * `dec`: Decimal for dealing with currency
 * `yyyy_mm_dd`: date
 * `hh_mm_ss`: time
 * `u_`: a user defined type
 
Data for number types (`int`, `float`, `dec`) can optionally have underscore characters (`_`) as thousand separators.  These will be ignored on processing.

## Metadata

A single whitespace ` ` can be added before the `@`. Thus the following are valid metadata and mean the same. Any trailing whitespace will be considered part of the key.

Any characters after the colon (`:`) will be considered part of the value, up until the new line.

The type of the value is not documented.

<pre>
@key:value
@ key:value
</pre>

### Reserved keys

Reserved keys are optional, but can enhance the stability of the data

* `@length`: The number of rows of data, as an integer, if this is supplied and the values does not match the number of data rows, an error will occur.
* `@separator`: The separator character(s)
* `@md5-checksum`: An 128bit MD5 checksum, presented as 32 hexadecimal digits (0-9a-f), this hash is based on a string containing header, types and data in the order they appear.  Metadata and comments are ignored. See [https://en.wikipedia.org/wiki/MD5](https://en.wikipedia.org/wiki/MD5) for details of MD5.

## Custom Separator

If the data is likely to contain commas, a custom separator can be specified by
`@separator` metadata item.  The separator can consist of one or more characters.

<pre>
@separator:^|^
</pre>

## Application specific types

A type beginning with `u_` is left to the application to process.

An example would be `u_yyyy_mm` which would store the year and month.

Caution should be taken to avoid name conflicts.



