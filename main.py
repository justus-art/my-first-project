# main.py is known as the controller - since it controls the site
from flask import Flask, render_template, request, redirect
import psycopg2
conn = psycopg2.connect(
    user="postgres", password="Annkimani744", host="localhost", database="my_duka")
cur = conn.cursor()
app = Flask(__name__)

cur.execute("Create table if not exists products(id serial PRIMARY KEY, name VARCHAR(100), buying_price INT, selling_price INT, stock_quantity INT);")
cur.execute("Create table if not exists sales (id serial PRIMARY KEY, pid INT, quantity INT, created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(), CONSTRAINT myproduct FOREIGN KEY (pid) references products (id) on UPDATE cascade on DELETE restrict)")
conn.commit()


@app.route("/")
def index():
    return "hello world"


@app.route("/products", methods=["GET", "POST"])
def products():
    if request.method == "POST":
        name = request.form["name"]
        bp = request.form["buying_price"]
        sp = request.form["selling_price"]
        stock = request.form["stock"]
        print(name, bp, sp, stock)
        cur.execute(
            "insert into products (name,buying_price,selling_price,stock_quantity) values(%s,%s,%s,%s)", (name, bp, sp, stock))
        conn.commit()
        return redirect("/products")
    else:
        cur.execute("select * from products;")
        products = cur.fetchall()
        return render_template("products.html", products=products)

    @app.route("/sales", methods=["GET", "POST"])
    def sales():
        if request.method == "POST":
            pid = request.form["pid"]
            quantity = request.form["quantity"]
            cur.execute(
                "insert into sales (pid, quantity) values(%s,%s)", (pid, quantity))
            return redirect("/sales")
        else:
            cur.execute("select * from sales;")
            sales = cur.fetchall()
            return render_template("sales.html", sales=sales)

# sales route


@app.route("/sales")
def sales():
    if request.method=="POST":
        pid=request.form["pid"]
        quantity=request.form["quantity"]
        cur.execute("insert into sales (pid, quantity) values(%s, %s)", (pid, quantity))
        conn.commit()
        return redirect("/sales")
    else: 
        cur.execute("select * from sales;")
        sales=cur.fetchall()
        print(sales)
        return render_template("sales.html", sales=sales)


@app.route("/sales/<int:id>")
def sale(id):
    cur.execute("select * from sales where pid = %s", (id,))
    sales=cur.fetchall()
    return render_template("sales.html", sales=sales)

app.run(debug=True)