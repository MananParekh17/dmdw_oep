from flask import Flask,render_template,request
import pickle
import numpy as np
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating = [round(x, 2) for x in popular_df['avg_rating'].values]                          
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['post'])

def recommend():
    # Get the user input from the form
    user_input = request.form.get('user_input')

    # Find the closest match for the user_input using fuzzy matching
    book_titles = pt.index.tolist()  # Assuming pt.index contains book titles
    closest_match = process.extractOne(user_input, book_titles, scorer=fuzz.token_sort_ratio)

    # Check if the similarity score is above a threshold (say 80)
    if closest_match[1] < 20:
        return render_template('recommend.html', data=None, message=f"No close match found for '{user_input}'. Please check your input.")

    # Use the closest matched book name
    matched_book_name = closest_match[0]

    # Fetch the index of the matched book
    index = np.where(pt.index == matched_book_name)[0][0]

    # Find similar items based on similarity scores
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    # Prepare the data for rendering in the template
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))  # Book Title
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))  # Author
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))  # Book Cover Image

        data.append(item)

    # Render the template and pass the recommended books data
    return render_template('recommend.html', data=data, message=None)

if __name__ == '__main__':
    app.run(debug=True) 