# Steak Funnnel Wrapper

## Queries Specification

Queries stored in YAML file format. Naming them is one of the key issues: queries usually called from outer sources so the name should be consistent. Following simple convention is crucial.

* Name of the query explains its content completely.
* Order of name parts 'event', 'any additional parameters', 'keywords'.
* Most query parts should be omitted if they're equal to default values or their usage is obvious.
* Default query:
    * `agg_field: user_id`
    * `type: elastic`
    * no Fonoteka events: either explicitly `NOT properties.app: Fonoteka` or using events not related to Fonoteka
    * not time based
* Name is snake_cased except keywords which are upper-case abbreviation
Valid abbreviations

|parmeter value|abberviation|
| ------------ |:----------:|
|`agg_field: properties.user_cookie`|Uc|
|`agg_field: properties.app_instance`|Ai|
|`agg_field: ip`|Ip|
|`agg_field: user_id` (only for several agg fields)|Ui|
|`type: hive`|H|
|`type: psql`|Ps|
|time based query - day|D|
|time based query - week|W|
|time based query - month|M|
|Fonoteak users included|F|

### Queries examples

~~~yaml
app_opened_android: # no need to specify anything since only default values are used
    type: elastic
    q: "NOT properties.app: fonoteka"
    index: cs-app_opened*
app_opened_android: # additional parameter
    type: elastic
    q: "NOT properties.app: fonoteka AND properties.os: android"
    index: cs-app_opened*
app_opened_android_vmetro: # two additional parameters
    type: elastic
    q: "NOT properties.app: fonoteka AND properties.os: android AND mat_info.sub_site:vmetro"
    index: cs-app_opened*    
app_opened_android_vmetro_Ai: # two additional parameters and a keyword
    type: elastic
    q: "NOT properties.app: fonoteka AND properties.os: android AND mat_info.sub_site:vmetro"
    index: cs-app_opened*
    agg_field: properties.app_instance
app_opened_android_vmetro_FAi: # keywords look better stacked, not separated by underscore
    type: elastic
    q: "properties.os: android AND mat_info.sub_site:vmetro"
    index: cs-app_opened*
    agg_field: properties.app_instance
app_opened_android_vmetro_FAiUi: # several agg fields
    type: elastic
    q: "properties.os: android AND mat_info.sub_site:vmetro"
    index: cs-app_opened*
    agg_fields: ["app_instance", "user_id"]
app_opened_android_vmetro_FAiUiW: # time based funnel
    type: elastic
    q: "properties.os: android AND mat_info.sub_site:vmetro"
    index: cs-app_opened*
    time_unit: week
    agg_fields: ["app_instance", "user_id"]
app_opened_android_vmetro_FAiUiW: # no need to specify technical settings like chunk_size or timeout 
    type: elastic
    q: "properties.os: android AND mat_info.sub_site:vmetro"
    index: cs-app_opened*
    time_unit: week
    chunk_size: 1000
    timeout: 10000
    agg_fields: ["app_instance", "user_id"]
app_opened_android_vmetro_FAiUiW: 
    name: app_opened_android_vmetro_FAiUiW # correct name of query helps much interpreting the results
    type: elastic
    q: "properties.os: android AND mat_info.sub_site:vmetro"
    index: cs-app_opened*
    time_unit: week
    chunk_size: 1000
    timeout: 10000
    agg_fields: ["app_instance", "user_id"]
~~~
