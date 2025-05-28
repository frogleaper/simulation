from flask import Flask, render_template, request, jsonify, send_file
import numpy as np
import matplotlib.pyplot as plt
from fpdf import FPDF
import io
import os
import tempfile

app = Flask(__name__)
last_data = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/simulate-auto")
def simulate_auto():
    arrivals = np.random.poisson(5, 60)
    return jsonify(arrivals.tolist())

@app.route("/simulate", methods=["POST"])
def simulate():
    data = request.get_json()
    try:
        arrivals = [int(x) for x in data.get("input_data", [])]
        if len(arrivals) != 60:
            return jsonify(error="Please provide exactly 60 hourly values."), 400

        single_channel_wait = [max(0, arrivals[i] - np.random.randint(3, 7)) for i in range(60)]
        multi_channel_wait = [max(0, arrivals[i] - np.random.randint(5, 10)) for i in range(60)]

        last_data["arrivals"] = arrivals
        last_data["single"] = single_channel_wait
        last_data["multi"] = multi_channel_wait

        return jsonify(original=arrivals, result=single_channel_wait, multi=multi_channel_wait)

    except Exception as e:
        return jsonify(error="Simulation failed. Check your input."), 500

@app.route("/export")
def export():
    if not last_data:
        return "No data to export", 400

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, txt="Bank Queueing Simulation Report", ln=1, align="C")

    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 10, txt="Name: ​🇨​​🇭​​🇮​​🇧​​🇺​​🇮​​🇰​​🇪​ ​🇴​​🇷​​🇦​​🇪​​🇰​​🇼​​🇺​​🇴​​🇹​​🇺 | Reg No: 2020374005", ln=1)
    pdf.cell(200, 10, txt="Case Study: Bank Queue - Single vs Multi Channel", ln=1)
    pdf.ln(5)

    pdf.set_font("Arial", "B", 10)
    pdf.cell(20, 8, "Hour", 1)
    pdf.cell(30, 8, "Arrivals", 1)
    pdf.cell(60, 8, "Single Channel Wait", 1)
    pdf.cell(60, 8, "Multi Channel Wait", 1)
    pdf.ln()

    pdf.set_font("Arial", "", 10)
    for i in range(60):
        if i % 12 == 0:
            pdf.set_font("Arial", "B", 10)
            pdf.cell(200, 8, f"Day {(i//12)+1}", ln=1)
            pdf.set_font("Arial", "", 10)

        pdf.cell(20, 8, f"{i+1}", 1)
        pdf.cell(30, 8, str(last_data["arrivals"][i]), 1)
        pdf.cell(60, 8, str(last_data["single"][i]), 1)
        pdf.cell(60, 8, str(last_data["multi"][i]), 1)
        pdf.ln()

    # Plot chart
    fig, ax = plt.subplots()
    ax.plot(last_data["arrivals"], label="Arrivals")
    ax.plot(last_data["single"], label="Single Channel Wait")
    ax.plot(last_data["multi"], label="Multi Channel Wait")
    ax.set_title("Bank Queue Forecast (60 Hours)")
    ax.set_xlabel("Hour")
    ax.set_ylabel("People")
    ax.legend()
    img_io = io.BytesIO()
    plt.tight_layout()
    plt.savefig(img_io, format="png")
    plt.close()
    img_io.seek(0)

    tmp_img = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    tmp_img.write(img_io.read())
    tmp_img.close()

    pdf.add_page()
    pdf.image(tmp_img.name, x=10, y=20, w=180)

    output = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(output.name)
    return send_file(output.name, as_attachment=True, download_name="bank_queue_report.pdf")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
