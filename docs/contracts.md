# 资料与接口约定

## 领域记录
nodes 是当前追溯树，N2 与 N3 允许共享 physical unit，不代表结构树有多个父节点。rows 是按 observed_at 先后产生的核查回执，selection=directed 无随机入样保证，draw 是当时的序号，revokes 指向撤销的回执；实验室 sensitivity/specificity 已明示，不能把阳性直接当真实不合格。POST /quote 传 node、unit、draw，返回该版本是否可抽、条件抽取概率与不可变 receipt；概率不等于全程最终纳入率。POST /detail 传 node 返回祖先链。inactive 节点不接受新抽查。扩大检查不等于已证实总体异常率。

audit_policy.maximum_defect_rate 是允许缺陷率阈值0.05，error_budget 为可配置的公开名单错误预算0.05，population 是唯一实物而不是回执数。具体声明是逐节点、在线还是层级联合，应在分析输出中说明适用前提；历史定向送检不自动取得随机抽样资格。

## 冻结来源
GET /manifest 返回 release、digest、row_count、metadata。digest 对完整领域资料按 JSON 键排序、紧凑分隔和 UTF-8 计算 SHA-256。
GET /records 及后续 cursor 请求、POST /quote、POST /detail 都要求 If-Match 等于清单 release，否则返回 412。
游标仅用于所属版本，客户端不能自行猜测页数。source 进程在启动时固定加载 data/release.json。
业务请求成功返回 release、request、result；业务值非法返回 422，游标不合法返回 400，未知地址返回 404。
仅有资料概览与领域核价，不含方案选型、统计推断或预测能力。

## 已有消费接口
GET /health 返回 status=ok；GET /overview 返回 release、digest 与描述性 overview。
POST /quotes 的 JSON 为 release 和 request，结果转发来源方回执。
POST /reports 接受 release、source_digest、kind、result、receipts，返回内容寻址 id；相同内容重复保存得到同一 id。
GET /reports/{id} 返回 id 与原 payload，重启后仍可读，不重算来源资料；不存在时 404。
这些接口的字段和返回类型保持兼容，新增业务可以扩展而不改变旧档案内容。
数据数值保留原始精度；只有领域服务中已标注的金额按对应货币规则处理。
