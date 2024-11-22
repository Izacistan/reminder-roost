from flask import Flask, render_template

app = Flask(__name__)

# Default route, so we do not get 404 error
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    # Run the app, with debug on, so we can see errors on screen.
    app.run(debug=True)