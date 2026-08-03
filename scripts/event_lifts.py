# -*- coding: utf-8 -*-
import csv
from datetime import date
from collections import defaultdict

EXC_A = set("""节日活动--支付成功|节日活动--提交订单|节日活动-曝光|车况页-点击通知|设备信息-点击违停提示|云相册页-VIP入口点击|服务页-点击安装教程|车况页-功能区-点击ETC消费账单|车况页-点击停车记录|服务页-点击停车记录|车辆位置页-点击导航|电子围栏页-曝光|服务页-点击电子围栏|门店洗车-点击门店|停车详情页-点击导航按钮|服务页-点击一键加油|广告页-点击广告|车况页-点击小金条|免流量看车页-直播页曝光|服务页-点击驾驶数据|车况页-下拉地图|抓拍分享列表页面-AI总结次数上限弹窗""".split('|'))
EXC_I = set("""车况页-点击顶部跑马灯|节日活动--提交订单|节日活动-曝光|节日活动--支付成功|服务页-点击紧急救援|云相册页-VIP入口点击|服务页-点击特惠洗车|电子围栏页-曝光|服务页-点击电子围栏|车况页--ETC账单-点击更多|服务页-点击VIP专属权益|服务页-点击预约安装|云相册页-VIP弹窗点击|服务页-点击停车记录|服务页-点击驾驶数据|服务页-点击VIP充值|紧急救援页-曝光|车况页-功能区-点击VIP充值|停车详情页-点击导航按钮|服务页-点击ETC消费账单|车况页-点击驾驶数据|云相册页-VIP弹窗曝光|驾驶数据页-点击历史轨迹|系统-后台暂停|车况页-功能区-点击特惠洗车|免流量看车页-点击链接WiFi|车况页-功能区-点击免流量看车|车况页-点击小金条|抓拍分享列表页面-点击操作视频|抓拍分享列表页面-点击生成AI内容|门店洗车-点击门店|抓拍分享列表页面-点击图片视频|紧急时刻列表页面-点击分享|车况页-点击地图|抓拍分享列表页面-点击解说|车况页-功能区-点击云相册|云相册页-曝光|设备信息-点击违停提示""".split('|'))


def analyze(path, rel, exc, label):
    daily = defaultdict(lambda: defaultdict(int))
    with open(path, encoding='utf-8-sig') as f:
        rd = csv.reader(f)
        next(rd)
        for r in rd:
            try:
                d = date.fromisoformat(r[0])
            except ValueError:
                continue
            daily[(r[3], r[2])][d] += int(r[5])  # 独立用户数, keyed by (name, id)
    pre_days = (rel - date(2026, 6, 2)).days
    post_days = (date(2026, 8, 2) - rel).days + 1
    res = []
    for (ev, eid), dm in daily.items():
        if ev in exc:
            continue
        pre = sum(v for d, v in dm.items() if d < rel) / pre_days
        post = sum(v for d, v in dm.items() if d >= rel) / post_days
        if pre < 0.05 and post >= 0.5:
            res.append((ev, eid, pre, post, None))
            continue
        if post < 10:
            continue
        if pre == 0:
            continue
        lift = (post - pre) / pre * 100
        if lift > 10:
            res.append((ev, eid, pre, post, lift))
    res.sort(key=lambda x: -(x[4] if x[4] is not None else 1e9))
    print(f'==== {label} (pre 6/2~{rel} {pre_days}d, post {rel}~8/2 {post_days}d), {len(res)} events')
    for ev, eid, pre, post, lift in res:
        ls = 'NEW' if lift is None else f'{lift:+.1f}%'
        print(f'  {ev}|{eid}|{pre:.1f}|{post:.1f}|{ls}')


analyze('/Users/huisexiaoqi/Downloads/小万出行-Android_事件列表_20260602_20260802.csv', date(2026, 7, 14), EXC_A, 'Android')
analyze('/Users/huisexiaoqi/Downloads/小万出行-iOS-新-9月26日后_事件列表_20260602_20260802.csv', date(2026, 7, 23), EXC_I, 'iOS')
