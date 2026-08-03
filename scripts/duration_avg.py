# -*- coding: utf-8 -*-
import csv

# 每档取区间中点（秒）；30分+ 主口径按 45 分钟、保守口径按 30 分钟
MIDS = [2, 7, 20.5, 45.5, 120, 390, 1200]
CAP_MAIN, CAP_LOW = 2700, 1800

FILES = {
    ('Android', '7/5'): '/Users/huisexiaoqi/Downloads/小万出行-Android_天_单次使用时长分布明细_20260705.csv',
    ('Android', '8/2'): '/Users/huisexiaoqi/Downloads/小万出行-Android_天_单次使用时长分布明细_20260802 (2).csv',
    ('iOS', '7/5'): '/Users/huisexiaoqi/Downloads/小万出行-iOS-新-9月26日后_天_单次使用时长分布明细_20260705.csv',
    ('iOS', '8/2'): '/Users/huisexiaoqi/Downloads/小万出行-iOS-新-9月26日后_天_单次使用时长分布明细_20260802 (2).csv',
}
DAU = {('Android', '7/5'): 12274, ('Android', '8/2'): 13384,
       ('iOS', '7/5'): 13673, ('iOS', '8/2'): 18495}

for key, path in FILES.items():
    with open(path, encoding='utf-8-sig') as f:
        rows = [r for r in csv.reader(f)][1:]
    counts = [int(r[1]) for r in rows]
    total = sum(counts)
    t_main = sum(c * m for c, m in zip(counts[:7], MIDS)) + counts[7] * CAP_MAIN
    t_low = sum(c * m for c, m in zip(counts[:7], MIDS)) + counts[7] * CAP_LOW
    dau = DAU[key]
    print(f'{key[0]} {key[1]}: sessions={total}  avg_session={t_main/total:.1f}s (low {t_low/total:.1f}s)  '
          f'daily_per_user={t_main/dau/60:.2f}min (low {t_low/dau/60:.2f}min)  launches_per_user={total/dau:.2f}')

print()
# 累计用户版本分布（8/2 快照）
for plat, path in [('Android', '/Users/huisexiaoqi/Downloads/小万出行-Android_天_版本_版本分布_20260802.csv'),
                   ('iOS', '/Users/huisexiaoqi/Downloads/小万出行-iOS-新-9月26日后_天_版本_版本分布_20260802.csv')]:
    with open(path, encoding='utf-8-sig') as f:
        rows = list(csv.reader(f))[1:]
    tot = next(r for r in rows if '总计' in r[0])
    data = sorted((r for r in rows if '总计' not in r[0]), key=lambda r: -int(r[2]))
    tc = int(tot[2])
    print(f'== {plat} 累计用户 {tc}（活跃 {tot[4]}，活跃率 {int(tot[4])/tc*100:.1f}%）')
    shown = 0
    for r in data[:8]:
        pct = int(r[2]) / tc * 100
        shown += pct
        print(f'  {r[1]:8} {int(r[2]):>7} ({pct:.1f}%)')
    print(f'  其他合计 {100-shown:.1f}%')
