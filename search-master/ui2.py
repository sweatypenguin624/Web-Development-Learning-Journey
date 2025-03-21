import gradio as gr
from main import checkAllClaims
import os
import tempfile
from process import processor

def create_url_blocks(urls):
    html = "<div class='sources-container'>"
    for url in urls:
        for u in url:
            html += f"""
            <div class="url-block" onclick="window.open('{u.get('url')}', '_blank')">
                <div class="url-title">{u.get('title')}</div>
                <div class="url-source">
                    <span>{u.get('url')}</span>
                </div>
            </div>
            """
    html += "</div>"
    return html

custom_css = """
.tab-nav {
    background-color: #f0f0f0;
    border-bottom: 1px solid #ccc;
    padding: 8px 8px 0 8px;
}

.tab-nav button {
    background-color: #e4e4e4;
    border: 1px solid #ccc;
    border-bottom: none;
    padding: 8px 16px;
    margin-right: 4px;
    border-radius: 4px 4px 0 0;
}

.tab-nav button.selected {
    background-color: white;
    border-bottom: 1px solid white;
    margin-bottom: -1px;
}

.navigation-bar {
    display: flex;
    align-items: center;
    padding: 8px;
    background-color: #f0f0f0;
    border-bottom: 1px solid #ccc;
}

.nav-buttons {
    display: flex;
    gap: 8px;
    margin-right: 16px;
}

.nav-button {
    padding: 4px 8px;
    background-color: #e4e4e4;
    border: 1px solid #ccc;
    border-radius: 4px;
    cursor: pointer;
}

.address-bar {
    flex-grow: 1;
    padding: 4px 8px;
    background-color: white;
    border: 1px solid #ccc;
    border-radius: 4px;
}

.sources-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.url-block {
    background-color: #f97316;
    color: white;
    padding: 10px;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
}

.url-block:hover {
    background-color: #ea580c;
}

.url-title {
    font-weight: bold;
    margin-bottom: 5px;
}

.url-source span {
    display: inline-block;
    word-break: break-all;
}

.url-source span:hover {
    text-decoration: underline;
}
"""

with gr.Blocks(
    theme=gr.themes.Base(
        primary_hue="orange",
        secondary_hue="orange",
        neutral_hue="orange",
    ),
    css=custom_css
) as demo:
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("<center><h1 class='text-orange-600'>Process Claims and Media Files</h1></center>")
            input_text = gr.Textbox(
                placeholder="Enter your claims code here...",
                label="Input",
                lines=10,
                elem_classes="border-orange-200 focus:border-orange-400"
            )
            with gr.Row():
                file_input = gr.File(
                    file_count="multiple",
                    label="Upload Files (Images or Audio)",
                    file_types=["image", "audio"],
                    elem_classes="border-orange-200"
                )
                submit_btn = gr.Button("Process", elem_classes="bg-orange-500 hover:bg-orange-600 text-white")
        
        with gr.Column(scale=1):
            with gr.Tabs() as tabs:
                with gr.Tab("Results"):
                    gr.Markdown("<center><h1 class='text-orange-600'>Results</h1></center>")
                    result = gr.Markdown(elem_classes="bg-orange-50 p-4 rounded-lg")
                
                with gr.Tab("Sources"):
                    gr.Markdown("<h2 class='text-orange-600'>Sources</h2>")
                    gr.Markdown("The sources used to arrive at the conclusions:")
                    sources_html = gr.HTML(elem_classes="mt-4")

    def process_and_update(text, files):
        markdown_result, searches = processor(text, files)
        print(searches)
        sources_html_content = create_url_blocks(searches)
        return markdown_result, sources_html_content

    submit_btn.click(
        fn=process_and_update,
        inputs=[input_text, file_input],
        outputs=[result, sources_html]
    )

demo.launch(share=True)

