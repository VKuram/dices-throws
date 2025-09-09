from flask import Flask, request, render_template
from probability import Probability

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        try:
            dices_amount = int(request.form['dice'])
            dice_sides = int(request.form['faces'])
            rolls_amount = int(request.form['rolls'])
            target_number = int(request.form['target'])

            probability = Probability(dices_amount, dice_sides, rolls_amount, target_number)
            result = probability.get_probability()
        except Exception as e:
            result = f"Ошибка: {e}"

    return render_template("form.html", result=result)

if __name__ == '__main__':
    app.run(debug=True)
