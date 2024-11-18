from flask import Flask, request, render_template
from TM.TMPengurangan import TMPengurangan
from TM.TMFaktorial import TMFaktorial
from TM.TMPembagian import TMPembagian

app = Flask(__name__)

def int_to_unary(n):
    return '0' * n

def unary_to_int(unary):
    return len(unary)

def TMCase1(m, n):
    result = []

    m_unary = int_to_unary(m)
    n_unary = int_to_unary(n)
    
    result.append(f"m (unary): {m_unary}")
    result.append(f"n (unary): {n_unary}")

    pengurangan_tape = m_unary + '1' + n_unary  
    result.append(f"Tape (m-n): {pengurangan_tape}")
    tm_pengurangan = TMPengurangan(tape=pengurangan_tape)
    tm_pengurangan.run()
    hasil_pengurangan_unary = tm_pengurangan.get_tape().split('1')[0]  
    result.append(f"Hasil (m-n) - unary: {hasil_pengurangan_unary}")

    hasil_pengurangan = unary_to_int(hasil_pengurangan_unary)
    result.append(f"Hasil (m-n): {hasil_pengurangan}")

    factorial_m_tape = m_unary + '1'  
    tm_faktorial_m = TMFaktorial(tape=factorial_m_tape)
    tm_faktorial_m.run()
    hasil_faktorial_m_unary = tm_faktorial_m.get_tape()
    result.append(f"Tape faktorial m: {factorial_m_tape}")
    result.append(f"Hasil faktorial m - unary: {hasil_faktorial_m_unary}")

    factorial_hasil_pengurangan_tape = int_to_unary(hasil_pengurangan) + '1'  
    tm_faktorial_hasil_pengurangan = TMFaktorial(tape=factorial_hasil_pengurangan_tape)
    tm_faktorial_hasil_pengurangan.run()
    hasil_faktorial_hasil_pengurangan_unary = tm_faktorial_hasil_pengurangan.get_tape()
    result.append(f"Tape faktorial (m-n): {factorial_hasil_pengurangan_tape}")
    result.append(f"Hasil faktorial (m-n) - unary: {hasil_faktorial_hasil_pengurangan_unary}")

    pembagian_tape = f'+{hasil_faktorial_hasil_pengurangan_unary}1+{hasil_faktorial_m_unary}1'
    result.append(f"Tape pembagian: {pembagian_tape}")
    tm_pembagian = TMPembagian(tape=pembagian_tape)
    tm_pembagian.run()
    hasil_pembagian_unary = tm_pembagian.get_tape()
    result.append(f"Hasil pembagian (unary): {hasil_pembagian_unary}")

    hasil_pembagian = unary_to_int(hasil_pembagian_unary)
    result.append(f"Hasil pembagian: {hasil_pembagian}")

    return result

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        m = int(request.form['m'])
        n = int(request.form['n'])
        result = TMCase1(m, n)
        return render_template('index.html', result=result)
    return render_template('index.html', result=None)

if __name__ == '__main__':
    app.run(debug=True)
