import gradio as gr

with gr.Blocks(css="#title { text-align: center; }") as demo:
    # 顶部标题和导入按钮
    with gr.Row():
        gr.Markdown("# 博客阅读助手", elem_id="title")

    with gr.Row():
        # 左侧：输入与历史记录
        with gr.Column(scale=1):
            gr.Textbox(label="输入 URL 或 JSON")
            gr.Dropdown(choices=["按批次", "按日期", "自定义分组"], label="选择分组方式")
            gr.Button("提交")
            gr.Markdown("## 历史记录")
            gr.Textbox(label="历史记录", lines=10)

        # 中间：预览
        with gr.Column(scale=3):
            # 上方窗口
            with gr.Column():
                gr.Image(label="网页预览", elem_id="url_preview")
            
            # 下方窗口
            with gr.Column():
                gr.Textbox(label="爬虫文本预览", lines=10, elem_id="crawler_output")

        # 右侧：大模型输出与问答
        with gr.Column(scale=2):
            gr.Markdown("## 大模型输出")
            gr.Textbox(label="评分", lines=10)
            gr.Markdown("## 文章问答")
            gr.Textbox(label="用户输入", lines=2)

    # 底部：导出和其他操作
    with gr.Row():
        with gr.Column(scale=4):
            with gr.Accordion("导出设置"):
                gr.Markdown("在这里选择导出选项")
            gr.Button("导出 JSON 数据")

    demo.launch(share=True)
