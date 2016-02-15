# Steak Funnel Wrapper

## Queries Specification

Queries stored in YAML file format. Naming them is one of the key issues: queries usually called from outer sources so the name should be consistent. Following simple convention is crucial.

* Name of the query explains its content completely.
* Order of name parts: *'event', 'any additional parameters', 'keywords'*.
* Most query parts should be omitted if they're equal to default values or their usage is obvious.
* Default query:
    * `agg_fields: user_id`
    * `type: elastic`
    * no Fonoteka events: either explicitly `NOT properties.app: Fonoteka` or using events not related to Fonoteka
    * not time based
* Name is snake_cased except keywords which are upper-case abbreviation
Valid abbreviations

|parmeter value|abberviation|
| ------------ |:----------:|
|`agg_fields: properties.user_cookie`|uc|
|`agg_fields: properties.app_instance`|ai|
|`agg_fields: ip`|Ip|
|`agg_fields: user_id` (only for several agg fields)|ui|
|`type: hive`|h|
|`type: psql`|ps|
|time based query - day|d|
|time based query - week|w|
|time based query - month|m|
|time based query - year|y|
|Fonoteka events included|f|

### Queries examples

~~~yaml
app_opened: # no need to specify anything since only default values are used
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
app_opened_android_vmetro_ai: # two additional parameters and a keyword
    type: elastic
    q: "NOT properties.app: fonoteka AND properties.os: android AND mat_info.sub_site:vmetro"
    index: cs-app_opened*
    agg_fields: properties.app_instance
app_opened_android_vmetro_f_ai: # keywords look better stacked, not separated by underscore
    type: elastic
    q: "properties.os: android AND mat_info.sub_site:vmetro"
    index: cs-app_opened*
    agg_fields: properties.app_instance
app_opened_android_vmetro_f_ai_ui: # several agg fields
    type: elastic
    q: "properties.os: android AND mat_info.sub_site:vmetro"
    index: cs-app_opened*
    agg_fields: ["app_instance", "user_id"]
app_opened_android_vmetro_f_ai_ui_w: # time based funnel
    type: elastic
    q: "properties.os: android AND mat_info.sub_site:vmetro"
    index: cs-app_opened*
    time_unit: week
    agg_fields: ["app_instance", "user_id"]
app_opened_android_vmetro_f_ai_ui_w: # no need to specify technical settings like chunk_size or timeout 
    type: elastic
    q: "properties.os: android AND mat_info.sub_site:vmetro"
    index: cs-app_opened*
    time_unit: week
    chunk_size: 1000
    timeout: 10000
    agg_fields: ["app_instance", "user_id"]
app_opened_android_vmetro_f_ai_ui_w: 
    name: app_opened_android_vmetro_f_ai_ui_w # correct name of query helps much interpreting the results
    type: elastic
    q: "properties.os: android AND mat_info.sub_site:vmetro"
    index: cs-app_opened*
    time_unit: week
    chunk_size: 1000
    timeout: 10000
    agg_fields: ["app_instance", "user_id"]
~~~
