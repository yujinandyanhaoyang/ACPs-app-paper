# 第四章可视化图说明

本目录需要包含以下可视化图文件：

## 1. chapter4_accuracy_comparison.png
**图 4-1 准确性指标对比**

展示 PopRec、Content-Based、Hybrid、LightGCN 和 Reading Concierge 五种方法在 Precision@10、Recall@10 和 NDCG@10 三个指标上的对比。

数据：
- PopRec: Precision@10=0.000600, Recall@10=0.001792, NDCG@10=0.001531
- Content-Based: Precision@10=0.001050, Recall@10=0.002726, NDCG@10=0.002407
- Hybrid: Precision@10=0.001300, Recall@10=0.003578, NDCG@10=0.003208
- LightGCN: Precision@10=0.009100, Recall@10=0.041394, NDCG@10=0.023993
- Reading Concierge: Precision@10=0.010000, Recall@10=0.075000, NDCG@10=0.037785

建议使用柱状图，三个指标并排展示。

## 2. chapter4_ablation_accuracy.png
**图 4-2 消融实验准确性对比**

展示 Full、w/o CF、w/o Content、w/o MMR、w/o Arbiter、w/o Feedback 六个变体在准确性指标上的对比。

数据：
- Full: Precision@10=0.001000, Recall@10=0.002958, NDCG@10=0.002309
- w/o CF: Precision@10=0.000200, Recall@10=0.000125, NDCG@10=0.000440
- w/o Content: Precision@10=0.001000, Recall@10=0.003044, NDCG@10=0.002381
- w/o MMR: Precision@10=0.000600, Recall@10=0.001458, NDCG@10=0.001661
- w/o Arbiter: Precision@10=0.001000, Recall@10=0.002833, NDCG@10=0.001639
- w/o Feedback: Precision@10=0.001000, Recall@10=0.002958, NDCG@10=0.002309

建议使用柱状图，三个指标并排展示。

## 3. chapter4_ablation_diversity.png
**图 4-3 消融实验多样性对比**

展示六个变体在 ILD、Coverage 和 Novelty 三个多样性指标上的对比。

数据：
- Full: ILD=0.969326, Coverage=0.000670, Novelty=11.223756
- w/o CF: ILD=0.954363, Coverage=0.000879, Novelty=13.078116
- w/o Content: ILD=0.968104, Coverage=0.000291, Novelty=10.566534
- w/o MMR: ILD=0.810889, Coverage=0.000751, Novelty=11.401945
- w/o Arbiter: ILD=0.978341, Coverage=0.000372, Novelty=10.732025
- w/o Feedback: ILD=0.969326, Coverage=0.000670, Novelty=11.223756

建议使用三个子图分别展示三个指标。

## 4. chapter4_user_activity_performance.png
**图 4-4 不同用户活跃度性能对比**

展示低活跃度（5-10条行为）、中活跃度（11-20条行为）和高活跃度（20+条行为）三组用户的推荐性能对比。

数据：
- 低活跃度: Precision@10=0.0009, Recall@10=0.002125, NDCG@10=0.001978
- 中活跃度: Precision@10=0.0011, Recall@10=0.003188, NDCG@10=0.002456
- 高活跃度: Precision@10=0.0012, Recall@10=0.003562, NDCG@10=0.002593

建议使用柱状图，三个指标并排展示。

---

## 生成方法

可以使用 Python + matplotlib 生成这些图表。由于当前环境限制，建议在本地环境或支持图形库的环境中生成。

示例代码见本目录下的 generate_figures.py（需要单独创建）。
