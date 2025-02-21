## 爬取YAML配置说明

### 
默认使用jquery的选择器方式进行选择

#### 基础配置
##### 通用
- 如有需要构造固定值，`selector`可以配置`@固定值内容`（需要加引号）

#### html
```
url: 
    selector: td:nth-child(1) a
    value_attr: href
```
- 默认字段，元素选择器及取值属性，其中属性填写属性名或text

##### json
```
url: 
    selector: qvd_code
```

与html对比，不需要value_attr  
`selector` 为json中的key  

###### `selector` 多级读取
采用`/`进行分割，如```data/data/list```
如data为list，需要按序号取，可使用`[序号]`，如`data/[0]/data`

###### `selector` 多key构造
使用`<|>`分割，如：
```
poc_status:
    selector: poc_flag<|>used_flag
```
无附加公式的情况下`poc_status`输出的结果：
```
{'poc_flag': xxx, 'used_flag':xxx}
```

###### 条件语句
如果是list，即多个同结构dict，支持条件语句，如  
```
poc_status:
    selector: value?label=CVSS 3.X
```

遍历list中的object，如果label字段值为CVSS 3.X，则提取value字段的值




#### map
值的映射处理，如
```
map:
    暂无可利用代码: ""
    POC 已公开: "PoC"
    EXP 已公开: "Exp"
    漏洞利用攻击武器化: "Exp"
```

#### exists_map
值的if True 映射处理，与map不同，该处理判断值是否为True，True则取前值，否则取后值，允许多个字段。  
一般搭配`choise_one`使用
如：
```
poc_status:
    selector: poc_flag<|>used_flag
    exists_map:
      used_flag: "Exp<|>"
      poc_flag: "PoC<|>"
```
在该示例中，先判断`used_flag`是否为True，如果为True，则`used_flag`值为Exp  
所以`poc_status`的值可能是：
```
{'used_flag': 'Exp', 'poc_flag': ''}
```


#### break_keyword
内容截断，只取截断前的内容。  
如果值是list，则分别识别开头字符串，匹配则取识别项之前所有项内容进行拼接  
如果值是str，则以`break_keyword`进行分割，并取分割左边内容
如：
```
break_keyword:
    - 影响版本
    - 受影响版本
    - 漏洞影响版本
    - 影响范围
    - 漏洞影响范围
    - 安全版本
```
示例内容：
```
Metabase是一个开源的数据分析和可视化工具，它可以帮助用户轻松地连接到各种数据源，包括数据库、云服务和API，然后使用直观的界面进行数据查询、分析和可视化。
据官方描述，Metabase 在 0.46.6.1 版本之前的开源版本和 1.46.6.1 版本之前的企业版本中存在远程代码执行漏洞，可导致攻击者在服务器上以运行 Metabase 服务器的权限执行任意代码。

安全版本
Metabase open source >= 0.46.6.1
Metabase Enterprise >= 1.46.6.1
```
截断结果：
```
Metabase是一个开源的数据分析和可视化工具，它可以帮助用户轻松地连接到各种数据源，包括数据库、云服务和API，然后使用直观的界面进行数据查询、分析和可视化。
据官方描述，Metabase 在 0.46.6.1 版本之前的开源版本和 1.46.6.1 版本之前的企业版本中存在远程代码执行漏洞，可导致攻击者在服务器上以运行 Metabase 服务器的权限执行任意代码。
```

#### split_tag
内容分隔，一般适用于数组字段（非数组字段会再次被合并）  
如：  
```
components:
    selector: qpe_prod_name
    split_tag: ','
```
处理完返回`list[str]`

#### build
对值进行再构造，当前仅支持替换处理  
如：
```
url: 
    selector: qvd_code
    build: https://nox.qianxin.com/vulnerability/detail/<url>
或
url: 
    selector: poc_flag<|>used_flag
    build: /vuldb/detail?id=<poc_flag>
```

#### choise_one
多个key的情况下，按顺序取第一个不为空的值  
即如果`selector`存在`<|>`则生成多个key的结果dict  
`choise_one`作用为取第一个不为空的值  
如生成多key的结果：
```
{'used_flag': 'Exp', 'poc_flag': ''}
```
如果配置`choise_one: true` 则最终取值为：`Exp`

#### choise_value_one
一般与`split_tag` 搭配使用，`choise_one`是多key维度，而`choise_value_one`是值为list的情况下针对值的处理  
自动取第一个不为空的值
如使用`split_tag`后返回值为：
```
['', '2']
```
如果配置`choise_value_one: true` 则最终取值为：`2`

### value_index
值为List的情况下，取第X个值(从1开始)
如：
```
value_index: 1
```
取第一个值

### clean_html_tag
如果为true，则清除html标签

### regx
正则匹配