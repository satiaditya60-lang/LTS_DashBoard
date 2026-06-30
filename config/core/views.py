from django.shortcuts import render
import pandas as pd
#import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')   # Non-GUI backend

import matplotlib.pyplot as plt

import seaborn as sns

import os
from django.conf import settings
from sqlalchemy import create_engine


def home(request):

    engine = create_engine(
        'postgresql+psycopg2://postgres:aditya123@localhost:5432/lts_database'
    )

    df = pd.read_sql("SELECT * FROM lts_app_testexecution", engine)

    # FILTER (Power BI style slicer)
    selected_domain = request.GET.get("domain")

    if selected_domain and selected_domain != "":
        df = df[df['domain_used'] == selected_domain]

    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

    domain_concurrency = df.groupby('domain_used')['concurrency'].sum().reset_index()

    # ---------------------------
    # CHART 1 - Bar (Matplotlib)
    # ---------------------------
    plt.figure(figsize=(6,4))
    plt.bar(domain_concurrency['domain_used'], domain_concurrency['concurrency'])
    plt.title("Concurrency by Domain")
    plt.xticks(rotation=45)
    plt.tight_layout()
    chart1 = "chart1.png"
    plt.savefig(os.path.join(settings.MEDIA_ROOT, chart1))
    plt.close()

    # ---------------------------
    # CHART 2 - Seaborn Barplot
    # ---------------------------
    plt.figure(figsize=(6,4))
    sns.barplot(data=domain_concurrency, x='domain_used', y='concurrency')
    plt.title("Seaborn Domain Distribution")
    plt.xticks(rotation=45)
    plt.tight_layout()
    chart2 = "chart2.png"
    plt.savefig(os.path.join(settings.MEDIA_ROOT, chart2))
    plt.close()

    # ---------------------------
    # CHART 3 - Pie Chart (Matplotlib)
    # ---------------------------
    plt.figure(figsize=(5,5))
    plt.pie(domain_concurrency['concurrency'], labels=domain_concurrency['domain_used'], autopct='%1.1f%%')
    plt.title("Domain Share")
    chart3 = "chart3.png"
    plt.savefig(os.path.join(settings.MEDIA_ROOT, chart3))
    plt.close()

    # ---------------------------
    # CHART 4 - Line Chart
    # ---------------------------
    plt.figure(figsize=(6,4))
    plt.plot(domain_concurrency['domain_used'], domain_concurrency['concurrency'], marker='o')
    plt.title("Trend View")
    plt.xticks(rotation=45)
    plt.tight_layout()
    chart4 = "chart4.png"
    plt.savefig(os.path.join(settings.MEDIA_ROOT, chart4))
    plt.close()

    # KPIs
    context = {
        "total_records": len(df),
        "total_domains": df['domain_used'].nunique(),
        "total_concurrency": df['concurrency'].sum(),
        "avg_concurrency": df['concurrency'].mean(),

        "chart1_url": settings.MEDIA_URL + chart1,
        "chart2_url": settings.MEDIA_URL + chart2,
        "chart3_url": settings.MEDIA_URL + chart3,
        "chart4_url": settings.MEDIA_URL + chart4,

        "domains": df['domain_used'].unique()
    }

    return render(request, "home.html", context)