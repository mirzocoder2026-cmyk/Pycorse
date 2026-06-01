"""
MyCourse.tj — Насби автоматӣ
Иҷро кунед: python setup.py
"""
import os, sys, subprocess

def run(cmd):
    print(f"  ▶ {cmd}")
    return subprocess.run(cmd, shell=True).returncode == 0

print("\n" + "="*52)
print("  🎓  MyCourse.tj — Насби автоматӣ")
print("="*52)

print("\n📦 Насби Django...")
run("pip install Django>=4.2 Pillow")

print("\n🗄  Миграция ва база...")
run("python manage.py makemigrations users courses chat")
run("python manage.py migrate")

print("\n📂 Маълумоти намоишӣ...")
run("python manage.py loaddata courses/fixtures/initial_data.json")

print("\n👤 Сохтани администратор...")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mycourse.settings')
import django; django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin', email='admin@mycourse.tj', password='admin123',
        first_name='Администратор', role='admin')
    print("  ✅ admin / admin123 сохта шуд")
else:
    print("  ℹ️  Администратор аллакай мавҷуд аст")

print("\n📁 Static файлҳо...")
run("python manage.py collectstatic --noinput")

print("\n" + "="*52)
print("  ✅  Насб тамом шуд!")
print("="*52)
print("\n  🚀  python manage.py runserver")
print("  🌐  http://127.0.0.1:8000")
print("  ⚙️   http://127.0.0.1:8000/admin-panel/")
print("  🔑  admin / admin123")
print("="*52 + "\n")
