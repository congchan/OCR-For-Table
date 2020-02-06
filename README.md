## OCR For Table 
为了应对`2019-nCoV`各地交通要道的出入纸质登记表格的电子化归档处理而临时制作的OCR工具. 

## 流程思路
1. 图片预处理
1. 优图OCR接口处理 
1. 接口输出解码到本地excel

## 文件结构
|-- data: 图片位置

|-- output: 输出excel, 和图片同名

## 使用
1. `pip install -r requirements.txt`
1. 在`config.json`中配置腾讯云的密钥
1. 把图片复制到`data`文件夹
1. `python run_table_ocr.py`

## Requirements
* python3
* xlrd
* pandas
* tencentcloud-sdk
