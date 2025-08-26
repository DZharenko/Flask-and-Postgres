from flask import Flask, render_template, url_for, abort, request, redirect, flash, get_flashed_messages
import json
from .models import SchoolRepository
import os



app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-dev')  # Безопаснее


# Инициализируем БД только если это не production
# if not os.environ.get('DATABASE_URL'):
#     from .database import init_db
#     init_db()



school_repo = SchoolRepository()

def validate(post):
    errors = {}
    name = post.get('name', '').strip()
    if not name:
        errors['name'] = "Can't be blank"
    type = post.get('type', '').strip()
    if not type:
        errors['type'] = "Can't be blank"
    return errors

@app.route("/")
def start_page():
    return render_template("index.html")

@app.route("/schools")
def schools_index():
    schools = school_repo.find_all()
    return render_template("schools/index.html", schools=schools)

@app.route("/schools/<id>")
def schools_show(id):
    school = school_repo.find_by_id(id)
    
    if not school:
        abort(404)
    
    return render_template("schools/show.html", school=school)

@app.errorhandler(404)
def not_found(error):
    return "Ooops, page not found", 404

@app.route("/schools/new")
def schools_new():
    school = {}
    errors = {}
    
    return render_template("schools/new.html", school=school, errors=errors)

@app.post("/schools")
def schools_post():
    # Извлекаем данные формы
    data = request.form.to_dict()
    
    # Проверяем корректность данных
    errors = validate(data)
    
    if errors:
        return render_template("schools/new.html", school=data, errors=errors), 422
    
    # Сохраняем школу через репозиторий
    school_repo.save(data)
    flash("Школа успешно добавлена", "success")
    return redirect(url_for("schools_index"))

@app.route("/schools/<id>/edit")
def schools_edit(id):
    school = school_repo.find_by_id(id)
    
    if not school:
        abort(404)
    
    errors = {}
    
    return render_template("schools/edit.html", school=school, errors=errors)

@app.route("/schools/<id>/patch", methods=["POST"])
def schools_patch(id):
    school = school_repo.find_by_id(id)
    
    if not school:
        abort(404)
    
    data = request.form.to_dict()
    errors = validate(data)
    
    if errors:
        return render_template("schools/edit.html", school=school, errors=errors), 422
    
    # Обновляем школу через репозиторий
    school_repo.update(id, data)
    flash("Школа успешно обновлена!", "success")
    return redirect(url_for("schools_index"))

@app.route("/schools/<id>/delete", methods=['POST'])
def schools_delete(id):
    school = school_repo.find_by_id(id)
    
    if not school:
        abort(404)
    
    # Удаляем школу через репозиторий
    school_repo.delete(id)
    flash("Школа удалена", "success")
    return redirect(url_for('schools_index'))


@app.route('/init-db')
def init_database():
    """Ручная инициализация БД для продакшена"""
    try:
        from .database import init_db
        init_db()
        return "Database initialized successfully!", 200
    except Exception as e:
        return f"Database initialization failed: {e}", 500



if __name__ == "__main__":
    app.run(debug=True)
