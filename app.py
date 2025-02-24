from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/recommendation', methods=['GET'])
def home():
    return "Course Recommender API is running at /recommendation"

@app.route('/recommendation/recommend', methods=['POST'])
def get_recommendations():
    data = request.get_json()
    interests = data.get("interests", "")
    # Dummy response - replace with your real logic
    return jsonify({"message": f"Recommendations for {interests}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
