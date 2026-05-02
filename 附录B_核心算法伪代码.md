# 附录B 核心算法伪代码

本附录提供系统中三个核心算法的伪代码描述。

## 算法B-1 时间衰减画像建模算法

**输入**：
- 用户近90天行为序列 $\mathcal{E} = \{e_1, e_2, \ldots, e_n\}$
- 时间衰减系数 $\lambda = 0.05$
- 暖启动阈值 $T_w = 20$（系统实现参数，详见第三章3.3节）
- 冷启动阈值 $T_c = 5$

**输出**：
- 画像向量 $\mathbf{p}_u \in \mathbb{R}^{256}$
- 置信度 $c_u \in [0, 1]$
- 题材偏好集合 $G_u$
- 策略建议 $s \in \{\text{explore}, \text{exploit}\}$

**算法步骤**：

```
1:  初始化特征向量 v_book ← 0, v_event ← 0, v_joint ← 0
2:  获取当前时间 t_now
3:  
4:  // 步骤1: 行为加权
5:  for each 事件 e_i ∈ E do
6:      计算时间间隔 Δt ← t_now - e_i.timestamp
7:      计算基础权重 w_e ← max(e_i.weight, e_i.rating, 0.1)
8:      计算衰减权重 s_e ← w_e · exp(-λ · Δt)
9:      
10:     // 步骤2: 特征映射与累加
11:     v_book ← v_book + s_e · hash(e_i.book_id, 256)
12:     v_event ← v_event + s_e · hash(e_i.event_type, 256)
13:     v_joint ← v_joint + s_e · hash((e_i.book_id, e_i.event_type), 256)
14: end for
15: 
16: // 步骤3: 加权融合与归一化
17: v_profile ← 0.50 · v_book + 0.30 · v_joint + 0.20 · v_event
18: p_u ← v_profile / ||v_profile||_2
19: 
20: // 步骤4: 题材偏好提取
21: G_u ← extract_genres(E)
22: if |G_u| < 3 or |E| < 10 then
23:     G_latent ← LLM_infer_genres(E)  // 调用LLM语义归纳
24:     G_u ← G_u ∪ G_latent
25: end if
26: 
27: // 步骤5: 置信度计算
28: n ← |E|
29: if n < T_c then
30:     c_u ← min(n / T_c · 0.25, 0.25)  // 冷启动用户
31:     s ← explore
32: else if n < T_w then
33:     c_u ← 0.25 + (n - T_c) / (T_w - T_c) · 0.75
34:     s ← explore
35: else
36:     c_u ← 1.0
37:     s ← exploit
38: end if
39: 
40: return p_u, c_u, G_u, s
```

---

## 算法B-2 上下文赌博机仲裁算法

**输入**：
- 画像置信度 $c_u$
- 内容提案权重建议 $\alpha_{\text{content}}^{\text{prop}}$
- 偏好散度 $\text{JSD}$
- 历史奖励记录 $\mathcal{R} = \{(a_i, r_i)\}$
- UCB探索系数 $C = 1.0$

**输出**：
- 语义相似度权重 $\alpha_{\text{sem}}$
- 协同过滤权重 $\alpha_{\text{cf}}$
- 新颖性权重 $\alpha_{\text{novel}}$
- 时效性权重 $\alpha_{\text{time}}$
- MMR多样性参数 $\lambda_{\text{mmr}}$

**算法步骤**：

```
1:  // 步骤1: 质量门控
2:  if c_u < 0.6 then
3:      发送证据请求到画像智能体和内容智能体
4:      更新 c_u 和 JSD
5:  end if
6:  
7:  // 步骤2: 构建上下文特征
8:  x ← [c_u, JSD, |候选集|, 平均内容完整度]
9:  
10: // 步骤3: 计算各臂的UCB得分
11: for each 臂 a ∈ {arm_1, arm_2, ..., arm_K} do
12:     n_a ← count(a, R)  // 臂a被选择的次数
13:     if n_a == 0 then
14:         UCB_a ← +∞
15:     else
16:         μ_a ← mean_reward(a, R)  // 臂a的平均奖励
17:         UCB_a ← μ_a + C · sqrt(log(|R|) / n_a)
18:     end if
19: end for
20: 
21: // 步骤4: 选择最优臂
22: a_best ← argmax_a UCB_a
23: 
24: // 步骤5: 根据选中臂生成排序参数
25: if a_best == arm_cf_dominant then
26:     α_sem ← 0.1, α_cf ← 0.6, α_novel ← 0.2, α_time ← 0.1, λ_mmr ← 0.7
27: else if a_best == arm_balanced then
28:     α_sem ← 0.25, α_cf ← 0.4, α_novel ← 0.2, α_time ← 0.15, λ_mmr ← 0.5
29: else if a_best == arm_content_dominant then
30:     α_sem ← 0.5, α_cf ← 0.2, α_novel ← 0.2, α_time ← 0.1, λ_mmr ← 0.6
31: else if a_best == arm_explore then
32:     α_sem ← 0.2, α_cf ← 0.3, α_novel ← 0.4, α_time ← 0.1, λ_mmr ← 0.3
33: else if a_best == arm_conservative then
34:     α_sem ← 0.15, α_cf ← 0.5, α_novel ← 0.15, α_time ← 0.2, λ_mmr ← 0.7
35: end if
36: // 注：此处展示五个典型臂的参数配置，完整实现见第三章3.5节
37: 
38: // 步骤6: 置信度惩罚
39: if c_u < 0.6 then
40:     α_cf ← α_cf · 0.7
41:     α_sem ← α_sem · 0.7
42:     // 重新归一化权重
43:     sum ← α_sem + α_cf + α_novel + α_time
44:     α_sem ← α_sem / sum
45:     α_cf ← α_cf / sum
46:     α_novel ← α_novel / sum
47:     α_time ← α_time / sum
48: end if
49: 
50: // 步骤7: 记录决策
51: 保存 (a_best, x) 到决策历史
52: 
53: return α_sem, α_cf, α_novel, α_time, λ_mmr
```

---

## 算法B-3 MMR多样性重排算法

**输入**：
- 候选集 $\mathcal{C} = \{d_1, d_2, \ldots, d_m\}$
- 相关性得分 $\text{Rel}(d_i)$，$i = 1, \ldots, m$
- 内容相似度矩阵 $\text{Sim}(d_i, d_j)$
- 多样性参数 $\lambda \in [0, 1]$
- 目标列表长度 $K$

**输出**：
- 重排后的推荐列表 $\mathcal{L} = [d_{i_1}, d_{i_2}, \ldots, d_{i_K}]$

**算法步骤**：

```
1:  初始化已选集合 S ← ∅
2:  初始化候选池 C ← C
3:  
4:  // 步骤1: 选择相关性最高的书目作为第一个
5:  d_first ← argmax_{d ∈ C} Rel(d)
6:  S ← S ∪ {d_first}
7:  C ← C \ {d_first}
8:  
9:  // 步骤2: 迭代选择剩余K-1个书目
10: while |S| < K and C ≠ ∅ do
11:     // 计算每个候选的MMR得分
12:     for each d_i ∈ C do
13:         max_sim ← max_{d_j ∈ S} Sim(d_i, d_j)
14:         MMR(d_i) ← λ · Rel(d_i) - (1 - λ) · max_sim
15:     end for
16:     
17:     // 选择MMR得分最高的书目
18:     d_best ← argmax_{d ∈ C} MMR(d)
19:     S ← S ∪ {d_best}
20:     C ← C \ {d_best}
21: end while
22: 
23: return S
```

**说明**：
- 当 $\lambda = 1$ 时，算法退化为纯相关性排序
- 当 $\lambda = 0$ 时，算法完全优化多样性
- 实际系统中 $\lambda$ 由仲裁智能体动态决定，通常取值范围为 $[0.3, 0.7]$
