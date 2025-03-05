from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from models import db, Test
from utils import whois_lookup, dns_lookup, ssl_certificate_check, calculate_score

app_routes = Blueprint("app_routes", __name__)

@app_routes.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        domain = request.form["domain"]
        ip = request.form["ip"]
        existing_entry = Test.query.filter_by(domain=domain, ip_address=ip).first()
        if not existing_entry:
            new_record = Test(domain=domain, ip_address=ip)
            db.session.add(new_record)
            db.session.commit()
        return redirect(url_for("app_routes.home"))
    all_records = Test.query.all()
    return render_template("index.html", allTest=all_records)

@app_routes.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    test = Test.query.get_or_404(id)
    if request.method == "POST":
        test.domain = request.form.get("domain", test.domain)
        test.ip_address = request.form.get("ip", test.ip_address)
        db.session.commit()
        flash("Record updated successfully", "success")
        return redirect(url_for("app_routes.home"))
    return render_template("update.html", test=test)

@app_routes.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    try:
        record = Test.query.get_or_404(id)
        db.session.delete(record)
        db.session.commit()
        flash("Record deleted successfully", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error: {str(e)}", "danger")
    return redirect(url_for("app_routes.home"))

@app_routes.route("/check-website", methods=["POST"])
def check_website():
    data = request.json
    domain = data.get("domain")
    js_ip = data.get("ip")
    if not domain or not js_ip:
        return jsonify({"error": "Invalid input"}), 400
    test_record = Test.query.filter_by(domain=domain).first()
    db_ip = test_record.ip_address if test_record and test_record.ip_address else None
    test_record = Test.query.filter_by(domain=domain).first()
    dns_info = dns_lookup(domain)
    print(f"DNS Lookup for {domain}: {dns_info}")  # Check what DNS is returning
    print(f"Database IP: {db_ip}")  # Check the stored IP


    score = 0
    dns_info = dns_lookup(domain)
    if dns_info and db_ip in dns_info:
        score += 100
        return jsonify({"domain": domain, "score": score})
    whois_info = whois_lookup(domain)
    ssl_info = ssl_certificate_check(domain)
    score = calculate_score(domain, whois_info, ssl_info, dns_info, js_ip, db_ip)
    authenticity = "Original" if score >= 75 else "Unverified"
    return jsonify({"domain": domain, "whois_info": str(whois_info) if whois_info else "Unavailable", 
                    "dns_info": dns_info, "ssl_info": ssl_info if ssl_info else "Unavailable", 
                    "score": score, "authenticity": authenticity})
