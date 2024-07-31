import gradio as gr
import modules.scripts as scripts
from modules import shared
import csv
import json
import os
import random
import re

class BubblePrompterScript(scripts.Script):
    def __init__(self):
        super().__init__()
        self.categories_data = self.load_csv_files()

    def title(self):
        return "Bubble Prompter"

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        with gr.Group():
            with gr.Accordion("Bubble Prompter", open=False):
                input_text = gr.Textbox(label="Input", lines=3)
                output_text = gr.Textbox(label="Output", lines=3)
                
                with gr.Row():
                    category_dropdown = gr.Dropdown(choices=list(self.categories_data.keys()), label="Category")
                    subcategory_dropdown = gr.Dropdown(label="Subcategory")
                    word_dropdown = gr.Dropdown(label="Word")
                
                with gr.Row():
                    add_word_button = gr.Button("Add Word")
                    random_word_button = gr.Button("Add Random Word")
                
                with gr.Row():
                    replace_spaces_button = gr.Button("Replace Spaces")
                    replace_commas_button = gr.Button("Replace Commas")
                    remove_duplicates_button = gr.Button("Remove Duplicates")
                
                with gr.Row():
                    emphasize_button = gr.Button("Emphasize ()")
                    mitigate_button = gr.Button("Mitigate []")
                
                process_button = gr.Button("Process")

        category_dropdown.change(
            fn=self.update_subcategories,
            inputs=[category_dropdown],
            outputs=[subcategory_dropdown]
        )

        subcategory_dropdown.change(
            fn=self.update_words,
            inputs=[category_dropdown, subcategory_dropdown],
            outputs=[word_dropdown]
        )

        add_word_button.click(
            fn=self.add_word,
            inputs=[input_text, word_dropdown],
            outputs=[input_text]
        )

        random_word_button.click(
            fn=self.add_random_word,
            inputs=[input_text, category_dropdown],
            outputs=[input_text]
        )

        replace_spaces_button.click(
            fn=self.replace_spaces,
            inputs=[input_text],
            outputs=[input_text]
        )

        replace_commas_button.click(
            fn=self.replace_commas,
            inputs=[input_text],
            outputs=[input_text]
        )

        remove_duplicates_button.click(
            fn=self.remove_duplicates,
            inputs=[input_text],
            outputs=[input_text]
        )

        emphasize_button.click(
            fn=self.emphasize,
            inputs=[input_text],
            outputs=[input_text]
        )

        mitigate_button.click(
            fn=self.mitigate,
            inputs=[input_text],
            outputs=[input_text]
        )

        process_button.click(
            fn=self.process_text,
            inputs=[input_text],
            outputs=[output_text]
        )

        return [input_text, output_text]

    def load_csv_files(self):
        csv_files = [
            'Composition.csv', 'Body.csv', 'Clothes.csv', 'Activity.csv',
            'Objects.csv', 'Creatures.csv', 'Plants.csv', 'World.csv',
            'NSFW.csv', 'More.csv'
        ]
        categories_data = {}

        for file in csv_files:
            category_name = file.split('.')[0]
            categories_data[category_name] = self.process_csv_file(file)

        return categories_data

    def process_csv_file(self, file_name):
        file_path = os.path.join(scripts.basedir(), "extensions", "bubble_prompter", file_name)
        data = {}
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)
            for header in headers:
                data[header] = []
            for row in reader:
                for i, cell in enumerate(row):
                    if cell.strip():
                        data[headers[i]].append(cell.strip())
        return data

    def update_subcategories(self, category):
        return gr.Dropdown.update(choices=list(self.categories_data[category].keys()))

    def update_words(self, category, subcategory):
        return gr.Dropdown.update(choices=self.categories_data[category][subcategory])

    def add_word(self, current_text, word):
        if current_text:
            return f"{current_text}, {word}"
        return word

    def add_random_word(self, current_text, category):
        all_words = [word for subcat in self.categories_data[category].values() for word in subcat]
        random_word = random.choice(all_words)
        if current_text:
            return f"{current_text}, {random_word}"
        return random_word

    def replace_spaces(self, text):
        return text.replace(' ', ', ')

    def replace_commas(self, text):
        text = re.sub(r',{2,}', ',', text)  # Replace multiple commas with a single comma
        text = re.sub(r',\s*,', ',', text)  # Remove spaces between commas
        text = text.strip().strip(',')  # Remove leading/trailing commas
        text = re.sub(r',\s+', ', ', text)  # Ensure single space after commas
        return text

    def remove_duplicates(self, text):
        words = [word.strip() for word in text.split(',')]
        unique_words = list(dict.fromkeys(words))  # Preserve order
        return ', '.join(unique_words)

    def emphasize(self, text):
        words = text.split(',')
        emphasized_words = [f"({word.strip()})" for word in words]
        return ', '.join(emphasized_words)

    def mitigate(self, text):
        words = text.split(',')
        mitigated_words = [f"[{word.strip()}]" for word in words]
        return ', '.join(mitigated_words)

    def process_text(self, text):
        # Here you can add any final processing steps
        # For now, we'll just return the text as is
        return text

    def run(self, p, input_text, output_text):
        p.prompt = f"{p.prompt} {output_text}"
        return p