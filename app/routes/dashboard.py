import csv
import io
from flask import Blueprint, make_response, request, render_template, redirect, url_for, flash, Response
from app.models.comentario import Comentario
from flask_login import login_user, logout_user, login_required
from app.models.user_fake import UserFake
from urllib.parse import urlparse, urljoin

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    categoria = request.args.get("categoria")
    tag = request.args.get("tag")

    query = Comentario.query
    if categoria:
        query = query.filter_by(categoria=categoria)
    if tag:
        query = query.filter(Comentario.tags_funcionalidades.cast(str).ilike(f"%{tag}%"))

    comentarios = query.order_by(Comentario.criado_em.desc()).all()
    return render_template("dashboard.html", comentarios=comentarios)

@dashboard_bp.route("/dashboard/exportar")
@login_required
def exportar_csv():
    comentarios = Comentario.query.all()
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(["Texto", "Categoria", "Tags", "Confiança", "Criado em"])
    for c in comentarios:
        tags = ", ".join(c.tags_funcionalidades or []) if c.tags_funcionalidades else ""
        cw.writerow([c.texto, c.categoria, tags, c.confianca, c.criado_em])
    
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=comentarios.csv"
    output.headers["Content-type"] = "text/csv"
    return output

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc

@dashboard_bp.route("/login", methods=["GET", "POST"])
def login():
    next_page = request.args.get("next")
    
    if request.method == "POST":
        senha = request.form.get("senha")
        if senha == "admin123":
            user = UserFake(id="admin")
            login_user(user)

            if next_page and is_safe_url(next_page):
                return redirect(next_page)
            else:
                return redirect(url_for("dashboard.dashboard"))
        else:
            flash("Senha incorreta", "danger")

    return render_template("login.html", next=next_page)

@dashboard_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("dashboard.login"))
