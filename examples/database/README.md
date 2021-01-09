## login to the psql command line

`sudo -u postgres psql`

#### format output
if you want to generate html output, the command is `\pset format html`  
but you probably want the default format which is *aligned*

## create database and role

`CREATE DATABASE <application_database_name>;`  
`CREATE ROLE <application_unix_user> WITH LOGIN;`  
`\password <application_unix_user>`  
`GRANT ALL PRIVILEGES ON DATABASE <application_database_name> TO <application_unix_user>;`  

## change database

`\c <application_database_name>`

## create the database tables
`sudo -u postgres psql < create_database_tables.sql`

## sanity check
In order to be able to register, login to the psql command line
and insert your email address into the email_white_list table.

verify the database table schemas against the models in `models.py`,
and hopefully it matches what is below

## describe database 
`<application_database_name>=# \d`
<table border="1">
<caption>List of relations</caption>
<tr>
<th align="center">Schema</th>
<th align="center">Name</th>
<th align="center">Type</th>
<th align="center">Owner</th>
</tr>
<tr valign="top">
<td align="left">public</td>
<td align="left">contributor</td>
<td align="left">table</td>
<td align="left">application_unix_user</td>
</tr>
<tr valign="top">
<td align="left">public</td>
<td align="left">contributor_id_seq</td>
<td align="left">sequence</td>
<td align="left">application_unix_user</td>
</tr>
<tr valign="top">
<td align="left">public</td>
<td align="left">email_white_list</td>
<td align="left">table</td>
<td align="left">application_unix_user</td>
</tr>
<tr valign="top">
<td align="left">public</td>
<td align="left">email_white_list_id_seq</td>
<td align="left">sequence</td>
<td align="left">application_unix_user</td>
</tr>
<tr valign="top">
<td align="left">public</td>
<td align="left">photo</td>
<td align="left">table</td>
<td align="left">application_unix_user</td>
</tr>
<tr valign="top">
<td align="left">public</td>
<td align="left">photo_id_seq</td>
<td align="left">sequence</td>
<td align="left">application_unix_user</td>
</tr>
</table>
<p>(6 rows)<br />
</p>


## describe contributor table
`<application_database_name>=# \d contributor`
<table border="1">
<caption>Table &quot;public.contributor&quot;</caption>
<tr>
<th align="center">Column</th>
<th align="center">Type</th>
<th align="center">Collation</th>
<th align="center">Nullable</th>
<th align="center">Default</th>
</tr>
<tr valign="top">
<td align="left">id</td>
<td align="left">integer</td>
<td align="left">&nbsp; </td>
<td align="left">not null</td>
<td align="left">nextval('contributor_id_seq'::regclass)</td>
</tr>
<tr valign="top">
<td align="left">name</td>
<td align="left">character varying(64)</td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
</tr>
<tr valign="top">
<td align="left">email</td>
<td align="left">character varying(120)</td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
</tr>
<tr valign="top">
<td align="left">password_hash</td>
<td align="left">character varying(128)</td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
</tr>
<tr valign="top">
<td align="left">num_photos</td>
<td align="left">integer</td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
</tr>
<tr valign="top">
<td align="left">totp_key</td>
<td align="left">character(16)</td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
</tr>
<tr valign="top">
<td align="left">use_totp</td>
<td align="left">boolean</td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
<td align="left">false</td>
</tr>
</table>
<p>Indexes:<br />
&nbsp;&nbsp;&nbsp;&nbsp;&quot;contributor_pkey&quot; PRIMARY KEY, btree (id)<br />
&nbsp;&nbsp;&nbsp;&nbsp;&quot;contributor_email_key&quot; UNIQUE CONSTRAINT, btree (email)<br />
&nbsp;&nbsp;&nbsp;&nbsp;&quot;contributor_name_key&quot; UNIQUE CONSTRAINT, btree (name)<br />
</p>

## describe photo table
`<application_database_name>=# \d photo`
<table border="1">
<caption>Table &quot;public.photo&quot;</caption>
<tr>
<th align="center">Column</th>
<th align="center">Type</th>
<th align="center">Collation</th>
<th align="center">Nullable</th>
<th align="center">Default</th>
</tr>
<tr valign="top">
<td align="left">id</td>
<td align="left">integer</td>
<td align="left">&nbsp; </td>
<td align="left">not null</td>
<td align="left">nextval('photo_id_seq'::regclass)</td>
</tr>
<tr valign="top">
<td align="left">photo_name</td>
<td align="left">character varying(120)</td>
<td align="left">&nbsp; </td>
<td align="left">not null</td>
<td align="left">&nbsp; </td>
</tr>
<tr valign="top">
<td align="left">contributor_id</td>
<td align="left">integer</td>
<td align="left">&nbsp; </td>
<td align="left">not null</td>
<td align="left">&nbsp; </td>
</tr>
<tr valign="top">
<td align="left">timestamp</td>
<td align="left">timestamp without time zone</td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
</tr>
<tr valign="top">
<td align="left">timestamp_int</td>
<td align="left">bigint</td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
</tr>
<tr valign="top">
<td align="left">photo_format</td>
<td align="left">character(12)</td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
</tr>
<tr valign="top">
<td align="left">photo_width</td>
<td align="left">integer</td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
</tr>
<tr valign="top">
<td align="left">photo_height</td>
<td align="left">integer</td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
</tr>
<tr valign="top">
<td align="left">photo_1280_width</td>
<td align="left">integer</td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
</tr>
<tr valign="top">
<td align="left">photo_1280_height</td>
<td align="left">integer</td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
</tr>
<tr valign="top">
<td align="left">photo_480_width</td>
<td align="left">integer</td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
</tr>
<tr valign="top">
<td align="left">photo_480_height</td>
<td align="left">integer</td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
</tr>
<tr valign="top">
<td align="left">Make</td>
<td align="left">character varying</td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
</tr>
<tr valign="top">
<td align="left">Model</td>
<td align="left">character varying</td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
</tr>
<tr valign="top">
<td align="left">Software</td>
<td align="left">character varying</td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
</tr>
<tr valign="top">
<td align="left">DateTime</td>
<td align="left">timestamp without time zone</td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
</tr>
<tr valign="top">
<td align="left">DateTimeOriginal</td>
<td align="left">timestamp without time zone</td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
</tr>
<tr valign="top">
<td align="left">DateTimeDigitized</td>
<td align="left">timestamp without time zone</td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
</tr>
<tr valign="top">
<td align="left">fnumber</td>
<td align="left">numeric</td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
</tr>
<tr valign="top">
<td align="left">DigitalZoomRatio</td>
<td align="left">numeric</td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
</tr>
<tr valign="top">
<td align="left">AspectRatio</td>
<td align="left">numeric</td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
</tr>
<tr valign="top">
<td align="left">photo_raw_size</td>
<td align="left">bigint</td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
</tr>
<tr valign="top">
<td align="left">photo_1280_size</td>
<td align="left">bigint</td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
</tr>
<tr valign="top">
<td align="left">photo_480_size</td>
<td align="left">bigint</td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
</tr>
<tr valign="top">
<td align="left">TimeZoneOffset</td>
<td align="left">integer</td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
</tr>
<tr valign="top">
<td align="left">GPSAltitude</td>
<td align="left">numeric</td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
</tr>
<tr valign="top">
<td align="left">GPSAboveSeaLevel</td>
<td align="left">boolean</td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
</tr>
<tr valign="top">
<td align="left">GPSLatitude</td>
<td align="left">numeric</td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
</tr>
<tr valign="top">
<td align="left">GPSLongitude</td>
<td align="left">numeric</td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
</tr>
</table>
<p>Indexes:<br />
&nbsp;&nbsp;&nbsp;&nbsp;&quot;photo_pkey&quot; PRIMARY KEY, btree (id)<br />
&nbsp;&nbsp;&nbsp;&nbsp;&quot;photo_photo_name_key&quot; UNIQUE CONSTRAINT, btree (photo_name)<br />
</p>


## describe email_white_list
`<application_database_name>=# \d email_white_list`
<table border="1">
<caption>Table &quot;public.email_white_list&quot;</caption>
<tr>
<th align="center">Column</th>
<th align="center">Type</th>
<th align="center">Collation</th>
<th align="center">Nullable</th>
<th align="center">Default</th>
</tr>
<tr valign="top">
<td align="left">id</td>
<td align="left">integer</td>
<td align="left">&nbsp; </td>
<td align="left">not null</td>
<td align="left">nextval('email_white_list_id_seq'::regclass)</td>
</tr>
<tr valign="top">
<td align="left">email</td>
<td align="left">character varying(120)</td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
</tr>
</table>
<p>Indexes:<br />
&nbsp;&nbsp;&nbsp;&nbsp;&quot;email_white_list_pkey&quot; PRIMARY KEY, btree (id)<br />
&nbsp;&nbsp;&nbsp;&nbsp;&quot;email_white_list_email_key&quot; UNIQUE CONSTRAINT, btree (email)<br />
</p>
