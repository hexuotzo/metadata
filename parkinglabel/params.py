# -*- coding: utf-8 -*-

# LogEntry
ACTION_FLAG_NAME = (
    ('1', '增加'),
    ('2', '修改'),
    ('3', '删除'),
    ('4', '查询'),
    ('5', '导出'),
)


CATEGORY_STAT = (
    ('4', '待评审'),
    ('3', '待开发'),
    ('2', '待上线'),
    ('1', '已上线'),
    ('0', '已下线'),
    ('99', '已删除'),
)

BELONG_TO = (
    ('1', '图片'),
    ('2', 'Tile')
)
# 状态流转限制
# 待评审: 完成评审->待开发, 删除->已经删除
# 待开发: 开发->待上线, 删除->已经删除
# 待上线: 上线->已上线, 删除->已经删除
# 已上线: 下线->已下线, 删除->已经删除
# 已下线: 开发->待上线, 删除->已经删除
# 已删除: 无
TAG_STATUS_SETNEXT = {
    '4': [{'name': '完成评审', 'val': '3'}, {'name':'删除', 'val': '99'}],
    '3': [{'name': '开发', 'val': '2'}, {'name':'删除', 'val': '99'}],
    '2': [{'name': '上线', 'val': '1'}, {'name':'删除', 'val': '99'}],
    '1': [{'name': '下线', 'val': '0'}, {'name':'删除', 'val': '99'}],
    '0': [{'name': '开发', 'val': '2'}, {'name':'删除', 'val': '99'}],
    '99': []
}

VALID_TIME = (
    ('99999', '永久'),
    ('365', '一年'),
    ('183', '六个月'),
    ('90', '三个月'),
)

# 标签值类型
VALTYPES = (
    ('1', '字符串型'),
    ('2', '自定义型'),
    ('3', '数值型'),
)

# 标签更新频次
TAG_FREQ = (
    ('1', '每天更新一次'),
    ('2', '每周更新一次'),
    ('3', '每月更新一次'),
    ('4', '不更新'),
)

# 分页每页条数
PERPAGE = 20

# tags缓存
KEY_USERTAGS = 'usertags_all_tags'


# Elasticsearch DB
ES_HOSTS = ['10.27.106.225']
ES_PORT = 9200

# user client
USER_CLIENT = (
    ('up-aphone', 'aphone'),
    ('up-iphone', 'iphone'),
    # ('up-pcweb', 'PCWEB'),
    # ('up-phone', 'Phone'),
    # ('up-ipad', 'iPad'),
)


# 画像异常报警邮件
TO_MAILLIST = ['yougen@mgtv.com', 'haoran@mgtv.com']
USER_PROFILE_SIMPLE_ERROR_SUBJECT = u'用户画像标签数据缺失:%s'
USER_PROFILE_SIMPLE_ERROR_BODY = u'''
标签编码: %s
异常原因: 标签管理库查无此标签
用户终端: %s
用户ID: %s

请尽快补全信息
'''
# =====end=====


# 图表类型
CHART_TYPE = (
    ('line', '线图'),
    ('column', '柱图'),
    ('pie', '饼图'),
)

CHART_TYPE_DICT = dict(CHART_TYPE)

ELASTICSEARCH_TEMPLATE = {
    'size':0,
    "query": {
        "bool": {
            "must": [],
            "should": []
        }
    },
    'aggs':{
        'groupby':{
            'terms':{
                'field':''
            }
        }
    }
}