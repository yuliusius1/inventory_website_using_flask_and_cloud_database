from flask import Flask, session, request, render_template, redirect, url_for
from connectdb import Database
import datetime

app = Flask(__name__)
app.secret_key = 'DatabaseGudangggg672019014'

@app.route('/', methods=['GET', 'POST'])
def index():
    
    if 'username' not in session.keys():
        return redirect(url_for('login'))

    conn = Database('ksb-2022')
    username = session['username']
    name = session['name']
    message = ""
    type = ""
    if request.method == 'POST':
        if 'tambah' in request.form:
            nama_barang = request.form['nama_barang']
            id_cat = request.form['id_cat']
            jumlah_barang = request.form['jumlah_barang']
            if nama_barang == '' or id_cat == '' or jumlah_barang == '':
                message = "Data tidak boleh kosong"
                type = "error"
            else:
                cek_barang, data_barang = conn.select("SELECT * FROM barang_672019014 WHERE nama_barang = '{}'".format(nama_barang))
                if cek_barang:
                    keterangan = "Gagal menambahkan barang " + str(nama_barang) + " karena sudah ada"
                    history = conn.execute("INSERT INTO history_activity_672019014(username,keterangan,times) VALUES('{}','{}','{}')".format(username, keterangan, datetime.datetime.now()))
                    message = keterangan
                    type = "error"
                else:
                    result = conn.execute("INSERT INTO barang_672019014(id_cat, nama_barang, stok_barang, status_barang) VALUES('{}','{}','{}','{}')".format(id_cat,nama_barang,jumlah_barang, 1))
                    if result[0]:
                        keterangan = "Berhasil menambahkan barang " + str(nama_barang)
                        history = conn.execute("INSERT INTO history_activity_672019014(username,keterangan,times) VALUES('{}','{}','{}')".format(username, keterangan, datetime.datetime.now()))
                        message = keterangan
                        type = "success"
                    else:
                        keterangan = "Gagal menambahkan barang " + str(nama_barang) + " karena " + str(result[1])
                        history = conn.execute("INSERT INTO history_activity_672019014(username,keterangan,times) VALUES('{}','{}','{}')".format(username, keterangan, datetime.datetime.now()))
                        message = keterangan
                        type = "error"
        elif 'edit' in request.form:
            id_barang = request.form['id_barang']
            nama_barang = request.form['nama_barang']
            id_cat = request.form['id_cat']
            status = 0
            if 'status' in request.form:
                status = 1
            if nama_barang == '' or id_cat == '':
                message = "Data tidak boleh kosong"
                type = "error"
            else:
                cek_barang, data_barang = conn.select("SELECT * FROM barang_672019014 WHERE id_barang = '{}'".format(id_barang))
                if cek_barang:
                    result = conn.execute("UPDATE barang_672019014 SET id_cat = '{}', nama_barang = '{}', status_barang = '{}' WHERE id_barang = '{}'".format(id_cat,nama_barang,status,id_barang))
                    if result[0]:
                        keterangan = "Berhasil mengubah barang " + str(nama_barang) + "dari (" + str(data_barang[0][1] ) + "," +  str( data_barang[0][2] ) + "," +  str( data_barang[0][3]) + ") menjadi (" + str(id_cat) + "," + str(nama_barang) + "," + str(status) + ")"
                        history = conn.execute("INSERT INTO history_activity_672019014(username,keterangan,times) VALUES('{}','{}','{}')".format(username, keterangan, datetime.datetime.now()))
                        message = keterangan
                        type = "success"
                    else:
                        keterangan = "Gagal mengubah barang " + str(nama_barang) + " karena " + str(result[1])
                        history = conn.execute("INSERT INTO history_activity_672019014(username,keterangan,times) VALUES('{}','{}','{}')".format(username, keterangan, datetime.datetime.now()))
                        message = keterangan
                        type = "error"
                else:
                    keterangan = "Gagal mengubah barang " + str(nama_barang) + " karena tidak ada"
                    history = conn.execute("INSERT INTO history_activity_672019014(username,keterangan,times) VALUES('{}','{}','{}')".format(username, keterangan, datetime.datetime.now()))
                    message = keterangan
                    type = "error"
        elif 'tambah_stok' in request.form:
            id_barang = request.form['id_barang']
            jumlah_stok = request.form['jumlah_stok']
            if jumlah_stok == '':
                message = "Data tidak boleh kosong"
                type = "error"
            else:
                cek_barang, data_barang = conn.select("SELECT * FROM barang_672019014 WHERE id_barang = '{}'".format(id_barang))
                if cek_barang:
                    result = conn.execute("UPDATE barang_672019014 SET stok_barang = stok_barang + '{}' WHERE id_barang = '{}'".format(jumlah_stok,id_barang))
                    if result[0]:
                        keterangan = "Berhasil Tambah Stok sebanyak " + str(jumlah_stok) + " " + "ke " + str(data_barang[0][2])
                        history = conn.execute("INSERT INTO history_activity_672019014(username,keterangan,times) VALUES('{}','{}','{}')".format(username, keterangan, datetime.datetime.now()))
                        message = keterangan
                        type = "success"
                    else:
                        keterangan = "Gagal Tambah Stok sebanyak " + str(jumlah_stok) + " " + "ke " + str(data_barang[0][2])
                        history = conn.execute("INSERT INTO history_activity_672019014(username,keterangan,times) VALUES('{}','{}','{}')".format(username, keterangan, datetime.datetime.now()))
                        message = keterangan
                        type = "error"
                else:
                    keterangan = "Gagal Tambah Stok sebanyak " + str(jumlah_stok) + " " + "ke " + str(data_barang[0][2]) + " karena barang tidak ada"
                    history = conn.execute("INSERT INTO history_activity_672019014(username,keterangan,times) VALUES('{}','{}','{}')".format(username, keterangan, datetime.datetime.now()))
                    message = keterangan
                    type = "error"
        elif 'kurang_stok' in request.form:
            id_barang = request.form['id_barang']
            jumlah_stok = request.form['jumlah_stok']
            if jumlah_stok == '':
                message = "Data tidak boleh kosong"
                type = "error"
            else:
                cek_barang, data_barang = conn.select("SELECT * FROM barang_672019014 WHERE id_barang = '{}'".format(id_barang))
                if cek_barang:
                    if(data_barang[0][3] < int(jumlah_stok)):
                        keterangan = "Gagal Kurang Stok sebanyak " + str(jumlah_stok) + " " + "ke " + str(data_barang[0][2]) + " karena stok barang tidak mencukupi"
                        history = conn.execute("INSERT INTO history_activity_672019014(username,keterangan,times) VALUES('{}','{}','{}')".format(username, keterangan, datetime.datetime.now()))
                        message = keterangan
                        type = "error"
                    else:
                        result = conn.execute("UPDATE barang_672019014 SET stok_barang = stok_barang - '{}' WHERE id_barang = '{}'".format(jumlah_stok,id_barang))
                        if result[0]:
                            keterangan = "Berhasil mengurangi Stok sebanyak " + str(jumlah_stok) + " " + "ke " + str(data_barang[0][2])
                            history = conn.execute("INSERT INTO history_activity_672019014(username,keterangan,times) VALUES('{}','{}','{}')".format(username, keterangan, datetime.datetime.now()))
                            message = keterangan
                            type = "success"
                        else:
                            keterangan = "Gagal mengurangi Stok sebanyak " + str(jumlah_stok) + " " + "ke " + str(data_barang[0][2])
                            history = conn.execute("INSERT INTO history_activity_672019014(username,keterangan,times) VALUES('{}','{}','{}')".format(username, keterangan, datetime.datetime.now()))
                            message = keterangan
                            type = "error"
                else:
                    keterangan = "Gagal mengurangi Stok sebanyak " + str(jumlah_stok) + " " + "ke " + str(data_barang[0][2]) + " karena barang tidak ada"
                    history = conn.execute("INSERT INTO history_activity_672019014(username,keterangan,times) VALUES('{}','{}','{}')".format(username, keterangan, datetime.datetime.now()))
                    message = keterangan
                    type = "error"
        elif 'hapus' in request.form:
            id_barang = request.form['id_barang']
            cek_barang, data_barang = conn.select("SELECT * FROM barang_672019014 WHERE id_barang = '{}'".format(id_barang))
            if cek_barang:
                result = conn.execute("DELETE FROM barang_672019014 WHERE id_barang = '{}'".format(id_barang))
                if result[0]:
                    keterangan = "Berhasil menghapus barang " + str(data_barang[0][2])
                    history = conn.execute("INSERT INTO history_activity_672019014(username,keterangan,times) VALUES('{}','{}','{}')".format(username, keterangan, datetime.datetime.now()))
                    message = "Barang " + data_barang[0][2] + " berhasil dihapus"
                    type = "success"
                else:
                    keterangan = "Gagal menghapus barang " + str(data_barang[0][2])
                    history = conn.execute("INSERT INTO history_activity_672019014(username,keterangan,times) VALUES('{}','{}','{}')".format(username, keterangan, datetime.datetime.now()))
                    message = "Barang " + data_barang[0][2] + " gagal dihapus" + str(result)
                    type = "error"
            else:
                keterangan = "Gagal menghapus barang " + str(data_barang[0][2]) + " karena barang tidak ada"
                history = conn.execute("INSERT INTO history_activity_672019014(username,keterangan,times) VALUES('{}','{}','{}')".format(username, keterangan, datetime.datetime.now()))
                message = keterangan
                type = "error"

    status_category, category = conn.select("SELECT * FROM cat_barang_672019014 WHERE status_kategori='{}' ORDER BY id_cat ASC".format(1))
    status_barang, barang = conn.select("SELECT barang_672019014.id_barang, barang_672019014.id_cat ,cat_barang_672019014.nama_kategori, barang_672019014.nama_barang, barang_672019014.stok_barang, barang_672019014.status_barang FROM cat_barang_672019014 INNER JOIN barang_672019014 ON cat_barang_672019014.id_cat=barang_672019014.id_cat order by barang_672019014.id_barang ASC")
    return render_template('index.html', username=name, barang=barang,category = category,message=message,type=type)


@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ""
    type = ""
    if 'username' in session.keys():
        return redirect(url_for('index'))
    if request.method == 'POST':
        conn = Database('ksb-2022')
        username = request.form['username']
        password = request.form['password']
        status, data = conn.select("SELECT * FROM users_672019014 WHERE username = '{}' AND pass = '{}'".format(username, password))
        if status:
            session['username'] = username
            session['name'] = data[0][1]
            return redirect(url_for('index'))
        else:
            message = "Username atau Password salah"
            type = "error"
            return render_template('login.html', message=message, type=type)
    return render_template('login.html', message=message, type=type)


@app.route('/riwayat', methods=['GET', 'POST'])
def riwayat():
    if 'username' not in session.keys():
        return redirect(url_for('login'))
    conn = Database('ksb-2022')
    status_history, history = conn.select("select * from history_activity_672019014 ORDER BY history_activity_672019014.times ASC")
    return render_template('riwayat.html',name = session['name'], history = history)

@app.route('/kategori_barang', methods=['GET', 'POST'])
def kategori_barang():
    if 'username' not in session.keys():
        return redirect(url_for('login'))
    conn = Database('ksb-2022')
    name = session['name']
    message = ""
    type = ""

    if request.method == 'POST':
        if 'tambah' in request.form:
            nama_kategori = request.form['nama_kategori']
            status, data = conn.select("SELECT * FROM cat_barang_672019014 WHERE nama_kategori = '{}'".format(nama_kategori))
            if status:
                keterangan = "Gagal menambah kategori barang " + str(nama_kategori) + " karena kategori sudah ada"
                history = conn.execute("INSERT INTO history_activity_672019014(username,keterangan,times) VALUES('{}','{}','{}')".format(name, keterangan, datetime.datetime.now()))
                message = keterangan
                type = "error"
            else:
                result = conn.execute("INSERT INTO cat_barang_672019014(nama_kategori,status_kategori) VALUES('{}','{}')".format(nama_kategori, 1))
                if result[0]:
                    keterangan = "Berhasil menambah kategori barang " + str(nama_kategori)
                    history = conn.execute("INSERT INTO history_activity_672019014(username,keterangan,times) VALUES('{}','{}','{}')".format(name, keterangan, datetime.datetime.now()))
                    message = keterangan
                    type = "success"
        elif 'edit' in request.form:
            id_cat = request.form['id_cat']
            nama_kategori = request.form['nama_kategori']
            status_cat = 0
            if 'status_kategori' in request.form:
                status_cat = 1
            status, data = conn.select("SELECT * FROM cat_barang_672019014 WHERE id_cat = '{}'".format(id_cat))
            if status:
                result = conn.execute("UPDATE cat_barang_672019014 SET nama_kategori = '{}', status_kategori = '{}' WHERE id_cat = '{}'".format(nama_kategori, status_cat, id_cat))
                if result[0]:
                    keterangan = "Berhasil mengubah kategori barang " + str(data[0][1]) + " menjadi " + str(nama_kategori)
                    history = conn.execute("INSERT INTO history_activity_672019014(username,keterangan,times) VALUES('{}','{}','{}')".format(name, keterangan, datetime.datetime.now()))
                    message = keterangan
                    type = "success"
                else:
                    keterangan = "Gagal mengubah kategori barang " + str(data[0][1]) + " menjadi " + str(nama_kategori)
                    history = conn.execute("INSERT INTO history_activity_672019014(username,keterangan,times) VALUES('{}','{}','{}')".format(name, keterangan, datetime.datetime.now()))
                    message = keterangan
                    type = "error"
        elif 'hapus' in request.form:
            id_cat = request.form['id_cat']
            status, data = conn.select("SELECT * FROM cat_barang_672019014 WHERE id_cat = '{}'".format(id_cat))
            if status:
                status_barang, barang = conn.select("SELECT * FROM barang_672019014 WHERE id_cat = '{}'".format(id_cat))
                if status_barang:
                    keterangan = "Gagal menghapus kategori barang " + str(data[0][1]) + " karena masih ada barang yang terkait"
                    history = conn.execute("INSERT INTO history_activity_672019014(username,keterangan,times) VALUES('{}','{}','{}')".format(name, keterangan, datetime.datetime.now()))
                    message = keterangan
                    type = "error"
                else:
                    result = conn.execute("DELETE FROM cat_barang_672019014 WHERE id_cat = '{}'".format(id_cat))
                    if result[0]:
                        keterangan = "Berhasil menghapus kategori barang " + str(data[0][1])
                        history = conn.execute("INSERT INTO history_activity_672019014(username,keterangan,times) VALUES('{}','{}','{}')".format(name, keterangan, datetime.datetime.now()))
                        message = keterangan
                        type = "success"
                    else:
                        keterangan = "Gagal menghapus kategori barang " + str(data[0][1])
                        history = conn.execute("INSERT INTO history_activity_672019014(username,keterangan,times) VALUES('{}','{}','{}')".format(name, keterangan, datetime.datetime.now()))
                        message = keterangan
                        type = "error"
                
    status_category, category = conn.select("SELECT * FROM cat_barang_672019014 ORDER BY id_cat ASC")
    return render_template('kategori_barang.html',name = name, category = category, message=message, type=type)

@app.route('/users', methods=['GET', 'POST'])
def users():
    if 'username' not in session.keys():
        return redirect(url_for('login'))
    conn = Database('ksb-2022')
    username = session['username']
    name = session['name']
    message = ""
    type = ""

    if request.method == 'POST':
        if 'tambah' in request.form:
            nama_user = request.form['nama_user']
            username = request.form['username']
            password = request.form['password']
            repeat_password = request.form['repeat_password']

            if password != repeat_password:
                keterangan = "Gagal menambah user " + str(nama_user) + " karena password tidak sama"
                history = conn.execute("INSERT INTO history_activity_672019014(username,keterangan,times) VALUES('{}','{}','{}')".format(name, keterangan, datetime.datetime.now()))
                message = keterangan
                type = "error"
            else:
                status, data = conn.select("SELECT * FROM users_672019014 WHERE username = '{}'".format(username))
                if status:
                    keterangan = "Gagal menambah user " + str(username) + " karena user sudah ada"
                    history = conn.execute("INSERT INTO history_activity_672019014(username,keterangan,times) VALUES('{}','{}','{}')".format(name, keterangan, datetime.datetime.now()))
                    message = keterangan
                    type = "error"
                else:
                    result = conn.execute("INSERT INTO users_672019014(nama,username,pass) VALUES('{}','{}','{}')".format(nama_user,username, password))
                    if result[0]:
                        keterangan = "Berhasil menambah user " + str(username)
                        history = conn.execute("INSERT INTO history_activity_672019014(username,keterangan,times) VALUES('{}','{}','{}')".format(name, keterangan, datetime.datetime.now()))
                        message = keterangan
                        type = "success"
        elif 'edit' in request.form:
            id_user = request.form['id_user']
            nama_user = request.form['nama_user']
            username = request.form['username']
            status, data = conn.select("SELECT * FROM users_672019014 WHERE id_user = '{}'".format(id_user))
            if status:
                result = conn.execute("UPDATE users_672019014 SET nama = '{}' , username = '{}' WHERE id_user = '{}'".format(nama_user, username, id_user))
                if result[0]:
                    keterangan = "Berhasil mengubah user (" + str(data[0][2]) + " , "+ str(data[0][1])+ ") menjadi (" + str(username) + " , " + str(nama_user) + ")"
                    history = conn.execute("INSERT INTO history_activity_672019014(username,keterangan,times) VALUES('{}','{}','{}')".format(name, keterangan, datetime.datetime.now()))
                    message = keterangan
                    type = "success"
                else:
                    keterangan = "Gagal mengubah user user (" + str(data[0][2]) + " , "+ str(data[0][1])+ ") menjadi (" + str(username) + " , " + str(nama_user) + ")"
                    history = conn.execute("INSERT INTO history_activity_672019014(username,keterangan,times) VALUES('{}','{}','{}')".format(name, keterangan, datetime.datetime.now()))
                    message = keterangan
                    type = "error"
        elif 'hapus' in request.form:
            id_user = request.form['id_user']
            status, data = conn.select("SELECT * FROM users_672019014 WHERE id_user = '{}'".format(id_user))
            if status:
                result = conn.execute("DELETE FROM users_672019014 WHERE id_user = '{}'".format(id_user))
                if result[0]:
                    if(data[0][2] == username):
                        return redirect(url_for('logout'))
                    keterangan = "Berhasil menghapus user " + str(data[0][1])
                    history = conn.execute("INSERT INTO history_activity_672019014(username,keterangan,times) VALUES('{}','{}','{}')".format(name, keterangan, datetime.datetime.now()))
                    message = keterangan
                    type = "success"
                else:
                    keterangan = "Gagal menghapus user " + str(data[0][1])
                    history = conn.execute("INSERT INTO history_activity_672019014(username,keterangan,times) VALUES('{}','{}','{}')".format(name, keterangan, datetime.datetime.now()))
                    message = keterangan
                    type = "error"
    status_user, user = conn.select("SELECT * FROM users_672019014 ORDER BY id_user ASC")
    return render_template('list_user.html',name = name, users = user, username = username, message=message, type=type)

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    session.pop('name', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)