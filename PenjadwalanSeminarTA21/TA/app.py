# from flask import Flask, render_template, request, redirect, url_for, send_file
# import pandas as pd
# import random
# from concurrent.futures import ProcessPoolExecutor
# import xlsxwriter
# import time
# import matplotlib.pyplot as plt
# import io
# import base64

# app = Flask(__name__)

# # Global variables to store temporary data
# global_df_kelompok = None
# global_df_hari = None
# global_df_jadwal_dosen = None
# global_df_jadwal_mahasiswa = None
# global_df_ruangan = None
# global_schedule = None
# global_tanggal_mulai = None
# global_tanggal_selesai = None
# global_best_accuracy = None
# global_best_fitness = None
# global_best_population = None
# global_num_iterations = None
# global_elapsed_time = None
# global_fitness_over_time = None

# class Seminar:
#     def __init__(self, kode_kelompok, nama_kelompok, dosen_pembimbing_1, dosen_pembimbing_2, dosen_penguji_1, dosen_penguji_2, days, rooms):
#         self.kode_kelompok = kode_kelompok
#         self.nama_kelompok = nama_kelompok
#         self.dosen_pembimbing_1 = dosen_pembimbing_1
#         self.dosen_pembimbing_2 = dosen_pembimbing_2
#         self.dosen_penguji_1 = dosen_penguji_1
#         self.dosen_penguji_2 = dosen_penguji_2
#         self.days = days
#         self.rooms = rooms
#         self.time = None
#         self.room = None
#         self.day = None

# # Define your time slots for seminars
# times = ["08:00-10:00", "09:00-11:00", "10:00-12:00", "13:00-15:00", "14:00-16:00", "15:00-17:00"]

# def calculate_fitness(schedule):
#     fitness = 0
#     for seminar in schedule:
#         for other_seminar in schedule:
#             if seminar != other_seminar and seminar.time == other_seminar.time and seminar.day == other_seminar.day and seminar.room == other_seminar.room:
#                 fitness -= 1
#     return fitness

# def calculate_accuracy(schedule):
#     total_seminars = len(schedule)
#     non_conflicting = total_seminars + calculate_fitness(schedule)
#     accuracy = (non_conflicting / total_seminars) * 100
#     return accuracy

# def buat_daftar_seminar(dataset, array_ruangan, array_hari):
#     seminar_list = []
#     for index, row in dataset.iterrows():
#         seminar = Seminar(row["kode"], row["kelompok"], row["dosen_pembimbing_1"], row["dosen_pembimbing_2"], row["dosen_penguji_1"], row["dosen_penguji_2"], array_hari, array_ruangan)
#         seminar_list.append(seminar)
#     return seminar_list

# def buat_jadwal(seminars, tanggal_mulai, tanggal_selesai, max_iterations=100):
#     best_schedule = None
#     best_fitness = float('-inf')
#     fitness_over_time = []

#     dates = pd.date_range(tanggal_mulai, tanggal_selesai).tolist()
#     times = ["08:00-10:00", "09:00-11:00", "10:00-12:00", "13:00-15:00", "14:00-16:00", "15:00-17:00"]

#     for iteration in range(max_iterations):
#         current_schedule = []
#         for seminar in seminars:
#             seminar.time = random.choice(times)
#             seminar.room = random.choice(seminar.rooms)
#             seminar.day = random.choice(dates).strftime("%Y-%m-%d")
#             current_schedule.append(seminar)

#         current_fitness = calculate_fitness(current_schedule)
#         fitness_over_time.append(current_fitness)

#         if current_fitness > best_fitness:
#             best_fitness = current_fitness
#             best_schedule = current_schedule.copy()

#     return best_schedule, best_fitness, fitness_over_time, iteration + 1

# def initialize_population(seminars, tanggal_mulai, tanggal_selesai, population_size=10):
#     population = []
#     dates = pd.date_range(tanggal_mulai, tanggal_selesai).tolist()
#     for _ in range(population_size):
#         schedule = []
#         for seminar in seminars:
#             seminar.time = random.choice(times)
#             seminar.room = random.choice(seminar.rooms)
#             seminar.day = random.choice(dates).strftime("%Y-%m-%d")
#             schedule.append(seminar)
#         population.append(schedule)
#     return population

# def select_population(population, num_parents):
#     parents = []
#     for _ in range(num_parents):
#         selected = random.choice(population)
#         parents.append(selected)
#     return parents

# def crossover(parent1, parent2):
#     point = random.randint(1, len(parent1) - 1)
#     child1 = parent1[:point] + parent2[point:]
#     child2 = parent2[:point] + parent1[point:]
#     return child1, child2

# def mutate(schedule, mutation_rate=0.1):
#     dates = pd.date_range(global_tanggal_mulai, global_tanggal_selesai).tolist()
#     for seminar in schedule:
#         if random.random() < mutation_rate:
#             seminar.time = random.choice(times)
#             seminar.room = random.choice(seminar.rooms)
#             seminar.day = random.choice(dates).strftime("%Y-%m-%d")

# def genetic_algorithm(seminars, tanggal_mulai, tanggal_selesai, population_size=10, max_generations=100, num_parents=5, mutation_rate=0.1):
#     population = initialize_population(seminars, tanggal_mulai, tanggal_selesai, population_size)
#     best_schedule = None
#     best_fitness = float('-inf')
#     fitness_over_generations = []

#     for generation in range(max_generations):
#         parents = select_population(population, num_parents)

#         for parent in parents:
#             population.remove(parent)

#         for i in range(0, len(parents), 2):
#             child1, child2 = crossover(parents[i], parents[i+1])
#             mutate(child1, mutation_rate)
#             mutate(child2, mutation_rate)
#             population.append(child1)
#             population.append(child2)

#         for schedule in population:
#             fitness = calculate_fitness(schedule)
#             if fitness > best_fitness:
#                 best_fitness = fitness
#                 best_schedule = schedule

#         fitness_over_generations.append(best_fitness)

#     return best_schedule, best_fitness, fitness_over_generations

# def cetak_jadwal(jadwal, filename):
#     wb = xlsxwriter.Workbook(filename)
#     ws = wb.add_worksheet("Jadwal Seminar")

#     header = ["Kelompok", "Nama Kelompok", "Dosen Pembimbing 1", "Dosen Pembimbing 2", "Dosen Penguji 1", "Dosen Penguji 2", "Waktu", "Ruangan", "Hari"]
#     for col, h in enumerate(header):
#         ws.write(0, col, h)

#     for row, seminar in enumerate(jadwal, 1):
#         ws.write(row, 0, str(seminar.kode_kelompok) if seminar.kode_kelompok is not None else "N/A")
#         ws.write(row, 1, str(seminar.nama_kelompok) if seminar.nama_kelompok is not None else "N/A")
#         ws.write(row, 2, str(seminar.dosen_pembimbing_1) if seminar.dosen_pembimbing_1 is not None else "N/A")
#         ws.write(row, 3, str(seminar.dosen_pembimbing_2) if seminar.dosen_pembimbing_2 is not None else "N/A")
#         ws.write(row, 4, str(seminar.dosen_penguji_1) if seminar.dosen_penguji_1 is not None else "N/A")
#         ws.write(row, 5, str(seminar.dosen_penguji_2) if seminar.dosen_penguji_2 is not None else "N/A")
#         ws.write(row, 6, str(seminar.time) if seminar.time is not None else "N/A")
#         ws.write(row, 7, str(seminar.room) if seminar.room is not None else "N/A")
#         ws.write(row, 8, str(seminar.day) if seminar.day is not None else "N/A")

#     wb.close()

# def cek_bentrok(schedule):
#     conflicts = []
#     for i, seminar1 in enumerate(schedule):
#         for j, seminar2 in enumerate(schedule):
#             if i < j and seminar1.time == seminar2.time and seminar1.day == seminar2.day and seminar1.room == seminar2.room:
#                 conflicts.append({
#                     "seminar1": seminar1.nama_kelompok,
#                     "seminar2": seminar2.nama_kelompok,
#                     "time": seminar1.time,
#                     "day": seminar1.day,
#                     "room": seminar1.room
#                 })
#     return conflicts

# @app.route("/")
# def index():
#     conflicts = cek_bentrok(global_schedule) if global_schedule else []
#     return render_template("index.html", schedule=global_schedule, best_accuracy=global_best_accuracy, best_fitness=global_best_fitness, best_population=global_best_population, num_iterations=global_num_iterations, elapsed_time=global_elapsed_time, fitness_over_time=global_fitness_over_time, conflicts=conflicts)

# @app.route("/upload", methods=["POST"])
# def upload_data():
#     global global_df_kelompok, global_df_hari, global_df_jadwal_dosen, global_df_jadwal_mahasiswa, global_df_ruangan, global_schedule, global_tanggal_mulai, global_tanggal_selesai, global_best_accuracy, global_best_fitness, global_best_population, global_num_iterations, global_elapsed_time, global_fitness_over_time

#     kelompok = request.files["kelompok"]
#     hari = request.files["hari"]
#     jadwal_dosen = request.files["jadwal_dosen"]
#     jadwal_mahasiswa = request.files["jadwal_mahasiswa"]
#     ruangan = request.files["ruangan"]
#     tanggal_mulai = request.form["tanggal_mulai"]
#     tanggal_selesai = request.form["tanggal_selesai"]

#     df_kelompok = pd.read_excel(kelompok)
#     df_hari = pd.read_excel(hari)
#     df_jadwal_dosen = pd.read_excel(jadwal_dosen)
#     df_jadwal_mahasiswa = pd.read_excel(jadwal_mahasiswa)
#     df_ruangan = pd.read_excel(ruangan)

#     # Clean column names
#     df_kelompok.columns = df_kelompok.columns.str.strip().str.lower().str.replace(' ', '_')
#     df_hari.columns = df_hari.columns.str.strip().str.lower().str.replace(' ', '_')
#     df_jadwal_dosen.columns = df_jadwal_dosen.columns.str.strip().str.lower().str.replace(' ', '_')
#     df_jadwal_mahasiswa.columns = df_jadwal_mahasiswa.columns.str.strip().str.lower().str.replace(' ', '_')
#     df_ruangan.columns = df_ruangan.columns.str.strip().str.lower().str.replace(' ', '_')

#     global_df_kelompok = df_kelompok
#     global_df_hari = df_hari
#     global_df_jadwal_dosen = df_jadwal_dosen
#     global_df_jadwal_mahasiswa = df_jadwal_mahasiswa
#     global_df_ruangan = df_ruangan
#     global_tanggal_mulai = tanggal_mulai
#     global_tanggal_selesai = tanggal_selesai

#     return redirect(url_for("tampilkan_jadwal"))

# @app.route("/display_schedule")
# def tampilkan_jadwal():
#     global global_schedule, global_tanggal_mulai, global_tanggal_selesai, global_best_accuracy, global_best_fitness, global_best_population, global_num_iterations, global_elapsed_time, global_fitness_over_time

#     if global_df_kelompok is None or global_df_hari is None or global_df_jadwal_dosen is None or global_df_jadwal_mahasiswa is None or global_df_ruangan is None:
#         return "Data belum lengkap diunggah", 400

#     array_ruangan = global_df_ruangan["ruangan"].tolist()
#     array_hari = global_df_hari["hari"].tolist()

#     seminars = buat_daftar_seminar(global_df_kelompok, array_ruangan, array_hari)

#     if not seminars:
#         return "Tidak ada seminar yang dapat dijadwalkan karena data kosong", 400

#     start_time = time.time()
#     with ProcessPoolExecutor() as executor:
#         future_schedule = executor.submit(buat_jadwal, seminars, global_tanggal_mulai, global_tanggal_selesai)
#         schedule, best_fitness, fitness_over_time, num_iterations = future_schedule.result()
#     end_time = time.time()

#     if not schedule:
#         return "Jadwal tidak dapat dibuat karena data kosong", 400

#     global_schedule = schedule
#     global_best_fitness = best_fitness
#     global_best_accuracy = calculate_accuracy(schedule)
#     global_best_population = num_iterations
#     global_num_iterations = num_iterations
#     global_elapsed_time = end_time - start_time
#     global_fitness_over_time = fitness_over_time

#     cetak_jadwal(schedule, "jadwal_seminar.xlsx")

#     return redirect(url_for("index"))

# @app.route("/generate_new_schedule")
# def generate_new_schedule():
#     return redirect(url_for("tampilkan_jadwal"))

# @app.route("/download_schedule")
# def download_schedule():
#     filename = "jadwal_seminar.xlsx"
#     return send_file(filename, as_attachment=True)

# @app.route("/plot_fitness")
# def plot_fitness():
#     global global_fitness_over_time

#     if global_fitness_over_time is None:
#         return "Tidak ada data untuk ditampilkan", 400

#     plt.figure()
#     plt.plot(global_fitness_over_time)
#     plt.xlabel("Generation")
#     plt.ylabel("Fitness")
#     plt.title("Fitness Over Generations")

#     img = io.BytesIO()
#     plt.savefig(img, format='png')
#     img.seek(0)
#     plot_url = base64.b64encode(img.getvalue()).decode()

#     return f'<img src="data:image/png;base64,{plot_url}"/>'

# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, send_file
import pandas as pd
import random
from concurrent.futures import ProcessPoolExecutor
import xlsxwriter
import time
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Define your time slots for seminars
times = [
    "08:00-10:00",
    "09:00-11:00",
    "10:00-12:00",
    "13:00-15:00",
    "14:00-16:00",
    "15:00-17:00",
]


class Seminar:
    def __init__(
        self,
        kode_kelompok,
        nama_kelompok,
        dosen_pembimbing_1,
        dosen_pembimbing_2,
        dosen_penguji_1,
        dosen_penguji_2,
        days,
        rooms,
    ):
        self.kode_kelompok = kode_kelompok
        self.nama_kelompok = nama_kelompok
        self.dosen_pembimbing_1 = dosen_pembimbing_1
        self.dosen_pembimbing_2 = dosen_pembimbing_2
        self.dosen_penguji_1 = dosen_penguji_1
        self.dosen_penguji_2 = dosen_penguji_2
        self.days = days
        self.rooms = rooms
        self.time = None
        self.room = None
        self.day = None


def calculate_fitness(schedule):
    fitness = 0
    for seminar in schedule:
        for other_seminar in schedule:
            if (
                seminar != other_seminar
                and seminar.time == other_seminar.time
                and seminar.day == other_seminar.day
                and seminar.room == other_seminar.room
            ):
                fitness -= 1
    return fitness


def calculate_accuracy(schedule):
    total_seminars = len(schedule)
    non_conflicting = total_seminars + calculate_fitness(schedule)
    accuracy = (non_conflicting / total_seminars) * 100
    return accuracy


def buat_daftar_seminar(dataset, array_ruangan, array_hari):
    seminar_list = []
    for index, row in dataset.iterrows():
        seminar = Seminar(
            row["kode"],
            row["kelompok"],
            row["dosen_pembimbing_1"],
            row["dosen_pembimbing_2"],
            row["dosen_penguji_1"],
            row["dosen_penguji_2"],
            array_hari,
            array_ruangan,
        )
        seminar_list.append(seminar)
    return seminar_list


def buat_jadwal(seminars, tanggal_mulai, tanggal_selesai, max_iterations=100):
    best_schedule = None
    best_fitness = float('-inf')
    fitness_over_time = []

    dates = pd.date_range(tanggal_mulai, tanggal_selesai).tolist()

    for iteration in range(max_iterations):
        current_schedule = []
        for seminar in seminars:
            while True:
                seminar.time = random.choice(times)
                seminar.room = random.choice(seminar.rooms)
                seminar.day = random.choice(dates).strftime("%Y-%m-%d")
                if not any(s.time == seminar.time and s.day == seminar.day and s.room == seminar.room for s in current_schedule):
                    break
            current_schedule.append(seminar)

        current_fitness = calculate_fitness(current_schedule)
        fitness_over_time.append(current_fitness)

        if current_fitness > best_fitness:
            best_fitness = current_fitness
            best_schedule = current_schedule.copy()

        if best_fitness == 0:  # No conflicts
            break

    return best_schedule, best_fitness, fitness_over_time, iteration + 1

def initialize_population(seminars, tanggal_mulai, tanggal_selesai, population_size=100):
    population = []
    dates = pd.date_range(tanggal_mulai, tanggal_selesai).tolist()
    for _ in range(population_size):
        schedule = []
        for seminar in seminars:
            seminar.time = random.choice(times)
            seminar.room = random.choice(seminar.rooms)
            seminar.day = random.choice(dates).strftime("%Y-%m-%d")
            schedule.append(seminar)
        population.append(schedule)
    return population


def select_population(population, num_parents):
    parents = random.sample(population, num_parents)
    return parents


def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

def mutate(schedule, mutation_rate=0.1):
    dates = pd.date_range(global_tanggal_mulai, global_tanggal_selesai).tolist()
    for seminar in schedule:
        if random.random() < mutation_rate:
            while True:
                new_time = random.choice(times)
                new_room = random.choice(seminar.rooms)
                new_day = random.choice(dates).strftime("%Y-%m-%d")
                if not any(s.time == new_time and s.day == new_day and s.room == new_room for s in schedule if s != seminar):
                    seminar.time = new_time
                    seminar.room = new_room
                    seminar.day = new_day
                    break

def genetic_algorithm(seminars, tanggal_mulai, tanggal_selesai, population_size=100, max_generations=100, num_parents=5, mutation_rate=0.1):
    population = initialize_population(seminars, tanggal_mulai, tanggal_selesai, population_size)
    best_schedule = None
    best_fitness = float('-inf')
    fitness_over_generations = []

    iteration = 0
    while iteration < max_generations:
        parents = select_population(population, num_parents)
        new_population = parents.copy()

        for i in range(0, len(parents), 2):
            if i + 1 < len(parents):
                child1, child2 = crossover(parents[i], parents[i + 1])
                mutate(child1, mutation_rate)
                mutate(child2, mutation_rate)
                new_population.append(child1)
                new_population.append(child2)

        population = []
        for schedule in new_population:
            conflicts = cek_bentrok(schedule)
            while conflicts:
                mutate(schedule, mutation_rate)
                conflicts = cek_bentrok(schedule)
            population.append(schedule)

            fitness = calculate_fitness(schedule)
            if fitness > best_fitness:
                best_fitness = fitness
                best_schedule = schedule

        fitness_over_generations.append(best_fitness)
        iteration += 1

        if best_fitness == 0:  # No conflicts
            break

    return best_schedule, best_fitness, fitness_over_generations

def cetak_jadwal(jadwal, filename):
    wb = xlsxwriter.Workbook(filename)
    ws = wb.add_worksheet("Jadwal Seminar")

    header = [
        "Kelompok",
        "Nama Kelompok",
        "Dosen Pembimbing 1",
        "Dosen Pembimbing 2",
        "Dosen Penguji 1",
        "Dosen Penguji 2",
        "Waktu",
        "Ruangan",
        "Hari",
    ]
    for col, h in enumerate(header):
        ws.write(0, col, h)

    for row, seminar in enumerate(jadwal, 1):
        ws.write(
            row,
            0,
            str(seminar.kode_kelompok) if seminar.kode_kelompok is not None else "N/A",
        )
        ws.write(
            row,
            1,
            str(seminar.nama_kelompok) if seminar.nama_kelompok is not None else "N/A",
        )
        ws.write(
            row,
            2,
            (
                str(seminar.dosen_pembimbing_1)
                if seminar.dosen_pembimbing_1 is not None
                else "N/A"
            ),
        )
        ws.write(
            row,
            3,
            (
                str(seminar.dosen_pembimbing_2)
                if seminar.dosen_pembimbing_2 is not None
                else "N/A"
            ),
        )
        ws.write(
            row,
            4,
            (
                str(seminar.dosen_penguji_1)
                if seminar.dosen_penguji_1 is not None
                else "N/A"
            ),
        )
        ws.write(
            row,
            5,
            (
                str(seminar.dosen_penguji_2)
                if seminar.dosen_penguji_2 is not None
                else "N/A"
            ),
        )
        ws.write(row, 6, str(seminar.time) if seminar.time is not None else "N/A")
        ws.write(row, 7, str(seminar.room) if seminar.room is not None else "N/A")
        ws.write(row, 8, str(seminar.day) if seminar.day is not None else "N/A")

    wb.close()


def cek_bentrok(schedule):
    conflicts = []
    for i, seminar1 in enumerate(schedule):
        for j, seminar2 in enumerate(schedule):
            if (
                i < j
                and seminar1.time == seminar2.time
                and seminar1.day == seminar2.day
                and seminar1.room == seminar2.room
            ):
                conflicts.append(
                    {
                        "seminar1": seminar1.nama_kelompok,
                        "seminar2": seminar2.nama_kelompok,
                        "time": seminar1.time,
                        "day": seminar1.day,
                        "room": seminar1.room,
                    }
                )
    return conflicts


@app.route("/")
def index():
    conflicts = cek_bentrok(global_schedule) if "global_schedule" in globals() else []
    return render_template(
        "index.html",
        schedule=globals().get("global_schedule"),
        best_accuracy=globals().get("global_best_accuracy"),
        best_fitness=globals().get("global_best_fitness"),
        best_population=globals().get("global_best_population"),
        num_iterations=globals().get("global_num_iterations"),
        elapsed_time=globals().get("global_elapsed_time"),
        fitness_over_time=globals().get("global_fitness_over_time"),
        conflicts=conflicts,
    )


@app.route("/upload", methods=["POST"])
def upload_data():
    kelompok = request.files.get("kelompok")
    hari = request.files.get("hari")
    jadwal_dosen = request.files.get("jadwal_dosen")
    jadwal_mahasiswa = request.files.get("jadwal_mahasiswa")
    ruangan = request.files.get("ruangan")
    tanggal_mulai = request.form.get("tanggal_mulai")
    tanggal_selesai = request.form.get("tanggal_selesai")

    if not all(
        [
            kelompok,
            hari,
            jadwal_dosen,
            jadwal_mahasiswa,
            ruangan,
            tanggal_mulai,
            tanggal_selesai,
        ]
    ):
        return "Semua file dan tanggal harus diunggah", 400

    df_kelompok = pd.read_excel(kelompok)
    df_hari = pd.read_excel(hari)
    df_jadwal_dosen = pd.read_excel(jadwal_dosen)
    df_jadwal_mahasiswa = pd.read_excel(jadwal_mahasiswa)
    df_ruangan = pd.read_excel(ruangan)

    # Clean column names
    df_kelompok.columns = (
        df_kelompok.columns.str.strip().str.lower().str.replace(" ", "_")
    )
    df_hari.columns = df_hari.columns.str.strip().str.lower().str.replace(" ", "_")
    df_jadwal_dosen.columns = (
        df_jadwal_dosen.columns.str.strip().str.lower().str.replace(" ", "_")
    )
    df_jadwal_mahasiswa.columns = (
        df_jadwal_mahasiswa.columns.str.strip().str.lower().str.replace(" ", "_")
    )
    df_ruangan.columns = (
        df_ruangan.columns.str.strip().str.lower().str.replace(" ", "_")
    )

    global_vars = globals()
    global_vars.update(
        {
            "global_df_kelompok": df_kelompok,
            "global_df_hari": df_hari,
            "global_df_jadwal_dosen": df_jadwal_dosen,
            "global_df_jadwal_mahasiswa": df_jadwal_mahasiswa,
            "global_df_ruangan": df_ruangan,
            "global_tanggal_mulai": tanggal_mulai,
            "global_tanggal_selesai": tanggal_selesai,
        }
    )

    return redirect(url_for("tampilkan_jadwal"))


@app.route("/display_schedule")
def tampilkan_jadwal():
    global_vars = globals()
    df_kelompok = global_vars.get("global_df_kelompok")
    df_hari = global_vars.get("global_df_hari")
    df_jadwal_dosen = global_vars.get("global_df_jadwal_dosen")
    df_jadwal_mahasiswa = global_vars.get("global_df_jadwal_mahasiswa")
    df_ruangan = global_vars.get("global_df_ruangan")

    if any(
        [
            df_kelompok.empty,
            df_hari.empty,
            df_jadwal_dosen.empty,
            df_jadwal_mahasiswa.empty,
            df_ruangan.empty,
        ]
    ):
        return "Data belum lengkap diunggah", 400

    array_ruangan = df_ruangan["ruangan"].tolist()
    array_hari = df_hari["hari"].tolist()

    seminars = buat_daftar_seminar(df_kelompok, array_ruangan, array_hari)

    if not seminars:
        return "Tidak ada seminar yang dapat dijadwalkan karena data kosong", 400

    start_time = time.time()
    with ProcessPoolExecutor() as executor:
        future_schedule = executor.submit(
            buat_jadwal,
            seminars,
            global_vars["global_tanggal_mulai"],
            global_vars["global_tanggal_selesai"],
        )
        schedule, best_fitness, fitness_over_time, num_iterations = (
            future_schedule.result()
        )
    end_time = time.time()

    if not schedule:
        return "Jadwal tidak dapat dibuat karena data kosong", 400

    global_vars.update(
        {
            "global_schedule": schedule,
            "global_best_fitness": best_fitness,
            "global_best_accuracy": calculate_accuracy(schedule),
            "global_best_population": num_iterations,
            "global_num_iterations": num_iterations,
            "global_elapsed_time": end_time - start_time,
            "global_fitness_over_time": fitness_over_time,
        }
    )

    cetak_jadwal(schedule, "jadwal_seminar.xlsx")

    return redirect(url_for("index"))


@app.route("/generate_new_schedule")
def generate_new_schedule():
    return redirect(url_for("tampilkan_jadwal"))


@app.route("/download_schedule")
def download_schedule():
    filename = "jadwal_seminar.xlsx"
    return send_file(filename, as_attachment=True)


@app.route("/plot_fitness")
def plot_fitness():
    global_fitness_over_time = globals().get("global_fitness_over_time")

    if not global_fitness_over_time:
        return "Tidak ada data untuk ditampilkan", 400

    plt.figure()
    plt.plot(global_fitness_over_time)
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.title("Fitness Over Generations")

    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return f'<img src="data:image/png;base64,{plot_url}"/>'


if __name__ == "__main__":
    app.run(debug=True)
