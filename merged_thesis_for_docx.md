---
title: "基于ACPs的图书个性化推荐系统设计与实现"
lang: zh-CN
...

本 科 毕 业 设 计（论 文）

题目：基于ACPs的图书个性化推荐系统设计与实现

\newpage

# 摘要

图书个性化推荐面临用户行为稀疏、语义信息复杂和多目标协调困难等挑战。本文提出一种基于 ACPs 协议的多智能体协作图书推荐方法，将推荐任务分解为画像建模、内容分析、策略仲裁和推荐执行四个协作子任务，通过标准化协议实现智能体间的稳定交互与在线演化。

本文设计了基于时间衰减与语义归纳的读者画像建模方法，对近 90 天行为事件进行衰减加权，并在低样本场景下引入大语言模型完成题材语义归纳。针对多目标排序协调问题，提出基于上下文赌博机的动态仲裁策略，根据用户状态和候选集特征自适应调整排序参数。系统实现了多路召回（FAISS 语义召回与 ALS 协同过滤召回）和 MMR 多样性重排机制，在保证准确性的同时提升推荐多样性。

在 Amazon Books 5-core 数据集上的实验表明，与最强基线 LightGCN 相比，本文系统的 Precision@10 提升 9.9%，Recall@10 提升 81.2%，NDCG@10 提升 57.5%，ILD 达到 0.969。消融实验验证了协同过滤召回、MMR 重排和决策仲裁的有效性，其中动态仲裁策略相比静态加权融合使 NDCG@10 提升 29.0%。实验也揭示了系统在推理时间（5秒 vs 15毫秒）和重排序性能方面的不足，为后续优化提供了方向。

关键词 个性化推荐；ACPs协议；多智能体协作；图书推荐；上下文赌博机

\newpage

# ABSTRACT

Personalized book recommendation faces challenges including sparse user behavior, complex semantic information, and difficulty in coordinating multiple objectives. This thesis proposes a multi-agent collaborative book recommendation method based on the ACPs protocol, decomposing the recommendation task into four collaborative subtasks: profile modeling, content analysis, strategy arbitration, and recommendation execution, achieving stable interaction and online evolution among agents through standardized protocols.

This thesis designs a reader profiling method based on time decay and semantic induction, applying decay weighting to behavior events within a 90-day window and introducing large language models for genre semantic induction in low-sample scenarios. To address multi-objective ranking coordination, a dynamic arbitration strategy based on contextual bandits is proposed, adaptively adjusting ranking parameters according to user states and candidate set features. The system implements multi-source recall (FAISS semantic recall and ALS collaborative filtering recall) and MMR diversity reranking mechanisms, improving recommendation diversity while ensuring accuracy.

Experiments on the Amazon Books 5-core dataset show that compared to the strongest baseline LightGCN, the proposed system achieves 9.9% improvement in Precision@10, 81.2% improvement in Recall@10, 57.5% improvement in NDCG@10, and ILD of 0.969. Ablation experiments validate the effectiveness of collaborative filtering recall, MMR reranking, and decision arbitration, with the dynamic arbitration strategy achieving 29.0% improvement in NDCG@10 compared to static weighted fusion. The experiments also reveal limitations in inference time (5s vs 15ms) and reranking performance, providing directions for future optimization.

KEY WORDS personalized recommendation; ACPs protocol; multi-agent collaboration; book recommendation; contextual bandit
