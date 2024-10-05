from flask import Flask, render_template, request
import spacy

# Load the pre-trained NLP model with word embeddings
nlp = spacy.load("en_core_web_md")

# Define the categories and descriptions
categories = {
    "Transportation": "items related to the movement of people or goods, including vehicles, fuels, and public transport",
    "Plastics": "materials or items made of synthetic polymers, such as plastic bottles, bags, and containers",
    "Energy Consumption": "items or activities related to the usage of energy, such as gas, electricity, or fossil fuels",
    "Food production": "items related to growing, harvesting, or producing food, including agriculture, farming, and food processing",
    "Water usage": "items or activities related to the consumption or conservation of water, such as irrigation, plumbing, or water bills",
    "Housing and Construction": "items related to buildings, homes, or construction materials, including apartments, cement, and insulation",
    "Clothing and Textiles": "items related to garments, fabrics, or textile production, such as shirts, jeans, and sewing materials",
    "Travel and Tourism": "items or activities related to leisure travel, including plane tickets, hotels, and tourist attractions",
    "Personal care and Hygiene": "items used for personal grooming or hygiene, such as soap, shampoo, and cosmetics",
    "Packaging and Shipping": "items related to packaging materials or the shipping of goods, such as boxes, packaging tape, and crates"
}

def categorize_item(item, categories):
    item_doc = nlp(item.lower())
    best_match = None
    best_score = -1
    for category, description in categories.items():
        category_doc = nlp(description)
        similarity = item_doc.similarity(category_doc)
        if similarity > best_score:
            best_score = similarity
            best_match = category
    return best_match

def categorize(items):
    categorized_items = [(item, categorize_item(item, categories)) for item in items]
    return categorized_items

# Flask app setup
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user_input = request.form['user_input']  # Get the input from the form
        items = [item.strip() for item in user_input.split(',')]  # Split by commas and strip spaces
        categorized_items = categorize(items)  # Categorize each item

        # Render the result in the template
        return render_template('result.html', categorized_items=categorized_items)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
