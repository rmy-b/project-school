import os ,sys
import django
import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression



# Add project root to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")  # ⚠ change if project name is different
django.setup()

from details.models import Marks, Attendance

# ---------------------------
# Prepare training data
# ---------------------------

X = []  # features
y = []  # label (pass/fail)

marks_data = Marks.objects.select_related("student")

for m in marks_data:
    student = m.student

    total_classes = Attendance.objects.filter(student=student).count()
    present_classes = Attendance.objects.filter(student=student, status='P').count()

    if total_classes == 0:
        continue

    attendance_percent = (present_classes / total_classes) * 100
    marks_percent = m.total_marks

    # feature: [marks %, attendance %]
    X.append([marks_percent, attendance_percent])

    # label: 1 = pass, 0 = fail
    y.append(1 if marks_percent >= 50 else 0)

X = np.array(X)
y = np.array(y)

# ---------------------------
# Train model
# ---------------------------

model = LogisticRegression()
model.fit(X, y)

# ---------------------------
# Save model
# ---------------------------

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")
joblib.dump(model, MODEL_PATH)

print("Model trained and saved as model.pkl")