#!/usr/bin/env python3
"""生成第四章可视化图表（SVG格式）"""

from pathlib import Path
from typing import List, Sequence, Tuple, Any


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except Exception:
        return default


def _grouped_bar_svg(
    title: str,
    labels: Sequence[str],
    series: Sequence[Tuple[str, Sequence[float], str]],
    width: int = 1400,
    height: int = 760,
) -> str:
    """生成分组柱状图SVG"""
    left = 120
    top = 90
    bottom = 170
    right = 80
    plot_w = width - left - right
    plot_h = height - top - bottom
    n = max(1, len(labels))
    m = max(1, len(series))
    max_v = 1e-8
    for _, vals, _ in series:
        if vals:
            max_v = max(max_v, max(vals))
    group_w = plot_w / n
    bar_w = max(10, group_w / (m + 1.4))

    parts: List[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">',
        f'<rect width="{width}" height="{height}" fill="#ffffff"/>',
        f'<text x="{width/2:.1f}" y="44" text-anchor="middle" font-size="28" font-family="Arial">{title}</text>',
        f'<line x1="{left}" y1="{top+plot_h}" x2="{left+plot_w}" y2="{top+plot_h}" stroke="#111"/>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top+plot_h}" stroke="#111"/>',
    ]

    # 添加网格线和Y轴刻度
    for t in range(6):
        y = top + plot_h - (plot_h * t / 5.0)
        v = max_v * t / 5.0
        parts.append(f'<line x1="{left}" y1="{y:.2f}" x2="{left+plot_w}" y2="{y:.2f}" stroke="#e5e7eb"/>')
        parts.append(f'<text x="{left-12}" y="{y+4:.2f}" text-anchor="end" font-size="12" font-family="Arial">{v:.4f}</text>')

    # 绘制柱状图
    for i, label in enumerate(labels):
        gx = left + i * group_w
        for j, (_, vals, color) in enumerate(series):
            val = _safe_float(vals[i] if i < len(vals) else 0.0, 0.0)
            h = (val / max_v) * plot_h
            x = gx + (j + 0.3) * bar_w
            y = top + plot_h - h
            parts.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{bar_w:.2f}" height="{h:.2f}" fill="{color}"/>')

        # X轴标签
        cx = gx + (m * bar_w) / 2.0
        parts.append(
            f'<text x="{cx:.2f}" y="{top+plot_h+34:.2f}" text-anchor="middle" font-size="13" '
            f'font-family="Arial" transform="rotate(25 {cx:.2f},{top+plot_h+34:.2f})">{label}</text>'
        )

    # 图例
    lx = left + plot_w - 300
    ly = top + 20
    for name, _, color in series:
        parts.append(f'<rect x="{lx}" y="{ly-12}" width="18" height="10" fill="{color}"/>')
        parts.append(f'<text x="{lx+26}" y="{ly-2}" font-size="13" font-family="Arial">{name}</text>')
        ly += 22

    parts.append("</svg>")
    return "\n".join(parts)


def _multi_bar_svg(
    title: str,
    subplot_titles: Sequence[str],
    labels: Sequence[str],
    values_list: Sequence[Sequence[float]],
    width: int = 1600,
    height: int = 600,
) -> str:
    """生成多子图柱状图SVG"""
    n_subplots = len(subplot_titles)
    subplot_w = (width - 100) // n_subplots
    left_margin = 50
    top = 90
    bottom = 120

    parts: List[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">',
        f'<rect width="{width}" height="{height}" fill="#ffffff"/>',
        f'<text x="{width/2:.1f}" y="44" text-anchor="middle" font-size="28" font-family="Arial">{title}</text>',
    ]

    colors = ["#5470C6", "#91CC75", "#FAC858"]

    for subplot_idx, (subtitle, values) in enumerate(zip(subplot_titles, values_list)):
        subplot_left = left_margin + subplot_idx * subplot_w
        subplot_right = subplot_left + subplot_w - 40
        plot_w = subplot_right - subplot_left - 60
        plot_h = height - top - bottom

        # 子图标题
        parts.append(
            f'<text x="{subplot_left + plot_w/2 + 30:.1f}" y="{top-20}" text-anchor="middle" '
            f'font-size="16" font-family="Arial">{subtitle}</text>'
        )

        # 坐标轴
        parts.append(f'<line x1="{subplot_left+60}" y1="{top+plot_h}" x2="{subplot_right}" y2="{top+plot_h}" stroke="#111"/>')
        parts.append(f'<line x1="{subplot_left+60}" y1="{top}" x2="{subplot_left+60}" y2="{top+plot_h}" stroke="#111"/>')

        # 计算最大值
        max_v = max(values) if values else 1.0
        max_v = max(max_v, 1e-8)

        # 网格线和Y轴刻度
        for t in range(6):
            y = top + plot_h - (plot_h * t / 5.0)
            v = max_v * t / 5.0
            parts.append(f'<line x1="{subplot_left+60}" y1="{y:.2f}" x2="{subplot_right}" y2="{y:.2f}" stroke="#e5e7eb"/>')
            if subplot_idx == 0:  # 只在第一个子图显示Y轴刻度
                parts.append(f'<text x="{subplot_left+50}" y="{y+4:.2f}" text-anchor="end" font-size="11" font-family="Arial">{v:.3f}</text>')

        # 绘制柱状图
        n = len(labels)
        bar_w = max(10, plot_w / (n * 1.6))
        gap = (plot_w - n * bar_w) / max(1, n - 1) if n > 1 else 0

        for i, (label, value) in enumerate(zip(labels, values)):
            x = subplot_left + 60 + i * (bar_w + gap)
            h = (value / max_v) * plot_h
            y = top + plot_h - h
            color = colors[subplot_idx % len(colors)]
            parts.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{bar_w:.2f}" height="{h:.2f}" fill="{color}"/>')

            # X轴标签
            parts.append(
                f'<text x="{x + bar_w/2:.2f}" y="{top + plot_h + 28:.2f}" text-anchor="middle" font-size="10" '
                f'font-family="Arial" transform="rotate(25 {x + bar_w/2:.2f},{top + plot_h + 28:.2f})">{label}</text>'
            )

    parts.append("</svg>")
    return "\n".join(parts)


def generate_figure_4_1():
    """图4-1：各方法准确性指标对比"""
    title = "Figure 4-1  Accuracy Metrics Comparison"
    labels = ["PopRec", "Content-Based", "Hybrid", "LightGCN", "Reading\nConcierge"]
    series = [
        ("Precision@10", [0.000600, 0.001050, 0.001300, 0.009100, 0.010000], "#5470C6"),
        ("Recall@10", [0.001792, 0.002726, 0.003578, 0.041394, 0.075000], "#91CC75"),
        ("NDCG@10", [0.001531, 0.002407, 0.003208, 0.023993, 0.037785], "#FAC858"),
    ]
    return _grouped_bar_svg(title, labels, series)


def generate_figure_4_2():
    """图4-2：消融实验准确性对比"""
    title = "Figure 4-2  Ablation Study Accuracy Comparison"
    labels = ["Full", "w/o CF", "w/o\nContent", "w/o\nMMR", "w/o\nArbiter", "w/o\nFeedback"]
    series = [
        ("Precision@10", [0.001000, 0.000200, 0.001000, 0.000600, 0.001000, 0.001000], "#5470C6"),
        ("Recall@10", [0.002958, 0.000125, 0.003044, 0.001458, 0.002833, 0.002958], "#91CC75"),
        ("NDCG@10", [0.002309, 0.000440, 0.002381, 0.001661, 0.001639, 0.002309], "#FAC858"),
    ]
    return _grouped_bar_svg(title, labels, series)


def generate_figure_4_3():
    """图4-3：消融实验多样性对比"""
    title = "Figure 4-3  Ablation Study Diversity Comparison"
    labels = ["Full", "w/o CF", "w/o\nContent", "w/o\nMMR", "w/o\nArbiter", "w/o\nFeedback"]
    subplot_titles = ["ILD", "Coverage", "Novelty"]
    values_list = [
        [0.969326, 0.954363, 0.968104, 0.810889, 0.978341, 0.969326],  # ILD
        [0.000670, 0.000879, 0.000291, 0.000751, 0.000372, 0.000670],  # Coverage
        [11.223756, 13.078116, 10.566534, 11.401945, 10.732025, 11.223756],  # Novelty
    ]
    return _multi_bar_svg(title, subplot_titles, labels, values_list)


def generate_figure_4_4():
    """图4-4：不同用户活跃度性能对比"""
    title = "Figure 4-4  Performance across User Activity Levels"
    labels = ["Low\n(5-10)", "Medium\n(11-20)", "High\n(20+)"]
    series = [
        ("Precision@10", [0.0009, 0.0011, 0.0012], "#5470C6"),
        ("Recall@10", [0.002125, 0.003188, 0.003562], "#91CC75"),
        ("NDCG@10", [0.001978, 0.002456, 0.002593], "#FAC858"),
    ]
    return _grouped_bar_svg(title, labels, series, width=1200, height=700)


def main():
    """生成所有图表"""
    output_dir = Path(__file__).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    figures = [
        ("chapter4_accuracy_comparison.svg", generate_figure_4_1()),
        ("chapter4_ablation_accuracy.svg", generate_figure_4_2()),
        ("chapter4_ablation_diversity.svg", generate_figure_4_3()),
        ("chapter4_user_activity_performance.svg", generate_figure_4_4()),
    ]

    for filename, svg_content in figures:
        output_path = output_dir / filename
        output_path.write_text(svg_content, encoding="utf-8")
        print(f"✓ Generated: {output_path}")

    print(f"\n✓ All 4 figures generated successfully in {output_dir}")


if __name__ == "__main__":
    main()
