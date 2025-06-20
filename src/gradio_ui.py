import gradio as gr
from core.hn_analyzer import HNAnalyzer

def build_hn_tab():
    analyzer = HNAnalyzer()
    
    with gr.Tab("HN 趋势分析"):
        with gr.Row():
            time_range = gr.Slider(1, 72, value=24, label="分析时间范围(小时)")
            btn = gr.Button("生成报告", variant="primary")
        
        report = gr.Markdown()
        btn.click(
            fn=lambda hrs: analyzer.generate_daily_report(hrs),
            inputs=time_range,
            outputs=report
        )

# 整合到原有UI
app = gr.Blocks()
build_hn_tab()  # 新增HN标签页
app.launch()
