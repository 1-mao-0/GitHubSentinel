import gradio as gr
from core.analyzer import SentinelAnalyzer
from core.channels import ChannelType

def create_ui():
    analyzer = SentinelAnalyzer()
    
    with gr.Blocks(title="GitHubSentinel v1.0", theme=gr.themes.Soft()) as ui:
        with gr.Tab("Dashboard"):
            gr.Markdown("# Real-time Threat Dashboard")
            alert_table = gr.Dataframe(headers=["Severity", "Title", "Source"])
        
        with gr.Tab("Configuration"):
            with gr.Row():
                chan_select = gr.CheckboxGroup(
                    choices=[c.value for c in ChannelType],
                    label="Active Channels"
                )
                severity_filter = gr.Slider(1, 5, label="Min Severity")
            
            with gr.Accordion("Channel Settings"):
                for chan in ChannelType:
                    with gr.Tab(chan.value.capitalize()):
                        gr.Interface(
                            self._build_channel_config(chan),
                            inputs="json",
                            outputs=None
                        )
        
        # 实时更新逻辑
        ui.load(
            fn=analyzer.get_latest_alerts,
            inputs=[chan_select, severity_filter],
            outputs=alert_table,
            every=300  # 每5分钟刷新
        )
    
    return ui
