# 附录C 关键API接口说明

本附录说明系统中各智能体的关键API接口规范，基于ACPs协议的AIP（Agent Interaction Protocol）实现。

## C.1 AIP RPC通用接口

所有Partner智能体均实现统一的RPC接口，用于接收Leader的任务请求。

### C.1.1 接口路径

```
POST /rpc
```

### C.1.2 请求格式（RpcRequest）

```json
{
  "jsonrpc": "2.0",
  "id": "string",
  "method": "string",
  "params": {
    "task_id": "string",
    "command": "start | continue | complete | get | cancel",
    "skill": "string",
    "input_data": {
      "text_items": [
        {
          "content": "string",
          "metadata": {}
        }
      ],
      "structured_items": [
        {
          "data": {},
          "schema": "string"
        }
      ]
    },
    "context": {}
  }
}
```

### C.1.3 响应格式（RpcResponse）

```json
{
  "jsonrpc": "2.0",
  "id": "string",
  "result": {
    "task_id": "string",
    "state": "Accepted | Working | AwaitingCompletion | Completed | Failed",
    "output_data": {
      "text_items": [],
      "structured_items": []
    },
    "metadata": {}
  }
}
```

---

## C.2 读者画像提案智能体接口

### C.2.1 技能：build_profile

**功能**：根据用户历史行为生成画像向量、置信度和题材偏好。

**输入参数**：

| 参数名 | 类型 | 说明 |
|--------|------|------|
| user_id | string | 用户唯一标识 |
| time_window | int | 行为时间窗口（天），默认90 |
| lambda | float | 时间衰减系数，默认0.05 |

**输出参数**：

| 参数名 | 类型 | 说明 |
|--------|------|------|
| profile_vector | array[float] | 256维画像向量 |
| confidence | float | 置信度，范围[0, 1] |
| genres | array[string] | 题材偏好列表 |
| is_cold_start | boolean | 是否为冷启动用户 |
| strategy_suggestion | string | 策略建议：explore或exploit |

**示例调用**：

```json
{
  "skill": "build_profile",
  "input_data": {
    "structured_items": [
      {
        "data": {
          "user_id": "U12345",
          "time_window": 90,
          "lambda": 0.05
        }
      }
    ]
  }
}
```

---

## C.3 书目内容提案智能体接口

### C.3.1 技能：analyze_content

**功能**：分析候选书目内容，计算偏好对齐散度，生成内容权重建议。

**输入参数**：

| 参数名 | 类型 | 说明 |
|--------|------|------|
| candidates | array[object] | 候选书目列表 |
| user_genres | array[string] | 用户显式题材偏好 |
| behavior_genres | array[string] | 用户行为题材分布 |

**输出参数**：

| 参数名 | 类型 | 说明 |
|--------|------|------|
| content_weights | object | 内容权重建议 |
| jsd_score | float | Jensen-Shannon散度 |
| coverage_report | object | 候选集覆盖报告 |
| counter_proposal | object | 反提案（当散度过大时） |

**示例调用**：

```json
{
  "skill": "analyze_content",
  "input_data": {
    "structured_items": [
      {
        "data": {
          "candidates": [
            {
              "book_id": "B001",
              "title": "深度学习",
              "description": "...",
              "genres": ["计算机", "人工智能"]
            }
          ],
          "user_genres": ["人工智能", "机器学习"],
          "behavior_genres": ["计算机", "人工智能", "数学"]
        }
      }
    ]
  }
}
```

---

## C.4 推荐决策仲裁智能体接口

### C.4.1 技能：arbitrate_strategy

**功能**：基于画像提案和内容提案，使用上下文赌博机策略输出排序参数。

**输入参数**：

| 参数名 | 类型 | 说明 |
|--------|------|------|
| profile_proposal | object | 画像提案 |
| content_proposal | object | 内容提案 |
| context_type | string | 上下文类型 |

**输出参数**：

| 参数名 | 类型 | 说明 |
|--------|------|------|
| alpha_cf | float | 协同过滤权重 |
| alpha_content | float | 内容权重 |
| lambda_mmr | float | MMR多样性参数 |
| selected_arm | string | 选中的动作臂 |
| decision_metadata | object | 决策元数据 |

**示例调用**：

```json
{
  "skill": "arbitrate_strategy",
  "input_data": {
    "structured_items": [
      {
        "data": {
          "profile_proposal": {
            "confidence": 0.8,
            "strategy_suggestion": "exploit"
          },
          "content_proposal": {
            "jsd_score": 0.3,
            "content_weights": {"alpha_content": 0.4}
          },
          "context_type": "high_conf_low_div"
        }
      }
    ]
  }
}
```

---

## C.5 推荐引擎执行智能体接口

### C.5.1 技能：execute_recommendation

**功能**：执行候选召回、排序、MMR重排和解释生成，返回最终推荐列表。

**输入参数**：

| 参数名 | 类型 | 说明 |
|--------|------|------|
| user_id | string | 用户标识 |
| profile_vector | array[float] | 画像向量 |
| alpha_cf | float | 协同过滤权重 |
| alpha_content | float | 内容权重 |
| lambda_mmr | float | MMR参数 |
| top_k | int | 返回结果数量，默认10 |

**输出参数**：

| 参数名 | 类型 | 说明 |
|--------|------|------|
| recommendations | array[object] | 推荐书目列表 |
| explanations | array[string] | 推荐解释 |
| metrics | object | 推荐指标（多样性、覆盖率等） |

**示例调用**：

```json
{
  "skill": "execute_recommendation",
  "input_data": {
    "structured_items": [
      {
        "data": {
          "user_id": "U12345",
          "profile_vector": [0.1, 0.2, ...],
          "alpha_cf": 0.6,
          "alpha_content": 0.4,
          "lambda_mmr": 0.5,
          "top_k": 10
        }
      }
    ]
  }
}
```

---

## C.6 反馈智能体接口

### C.6.1 技能：process_feedback

**功能**：处理用户反馈事件，计算奖励信号，触发画像更新和模型重训。

**输入参数**：

| 参数名 | 类型 | 说明 |
|--------|------|------|
| user_id | string | 用户标识 |
| session_id | string | 会话标识 |
| feedback_events | array[object] | 反馈事件列表 |

**反馈事件格式**：

```json
{
  "event_type": "view | click | rate | finish | skip",
  "book_id": "string",
  "timestamp": "ISO8601",
  "rating": "float (optional)",
  "duration": "int (optional)"
}
```

**输出参数**：

| 参数名 | 类型 | 说明 |
|--------|------|------|
| reward | float | 计算的奖励值 |
| updates_triggered | array[string] | 触发的更新类型 |
| update_status | object | 更新状态 |

**示例调用**：

```json
{
  "skill": "process_feedback",
  "input_data": {
    "structured_items": [
      {
        "data": {
          "user_id": "U12345",
          "session_id": "S67890",
          "feedback_events": [
            {
              "event_type": "click",
              "book_id": "B001",
              "timestamp": "2024-05-01T10:30:00Z"
            },
            {
              "event_type": "rate",
              "book_id": "B001",
              "timestamp": "2024-05-01T10:35:00Z",
              "rating": 4.5
            }
          ]
        }
      }
    ]
  }
}
```

---

## C.7 接口调用流程

典型的推荐请求调用流程如下：

```
1. Leader接收用户请求
2. Leader → reader_profile_agent.build_profile()
3. Leader → book_content_agent.analyze_content()
4. Leader → recommendation_decision_agent.arbitrate_strategy()
5. Leader → recommendation_engine_agent.execute_recommendation()
6. Leader返回推荐结果给用户
7. 用户产生反馈 → feedback_agent.process_feedback()
8. feedback_agent触发画像更新和仲裁更新
```

## C.8 错误处理

所有接口在发生错误时返回标准错误响应：

```json
{
  "jsonrpc": "2.0",
  "id": "string",
  "error": {
    "code": -32000,
    "message": "错误描述",
    "data": {
      "detail": "详细错误信息"
    }
  }
}
```

常见错误码：
- `-32600`: 无效请求
- `-32601`: 方法不存在
- `-32602`: 无效参数
- `-32603`: 内部错误
- `-32000`: 业务逻辑错误
