# backend/app/models/mysql_models.py
from .. import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    # 角色：'user' 普通用户 | 'admin' 管理员（后台图谱管理接口校验）
    role = db.Column(db.String(20), nullable=False, default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    constitution_type = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    order_num = db.Column(db.Integer, nullable=False)


class AssessmentResult(db.Model):
    __tablename__ = 'assessment_results'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    answers = db.Column(db.JSON, nullable=False)
    primary_type = db.Column(db.String(20), nullable=False)
    secondary_types = db.Column(db.JSON)
    scores = db.Column(db.JSON, nullable=False)
    enhanced_recommendations = db.Column(db.JSON)  # 新增：存储AI增强推荐
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='results')


class UserAnswer(db.Model):
    __tablename__ = 'user_answers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    session_id = db.Column(db.String(50), nullable=False, index=True)
    question_id = db.Column(db.Integer, nullable=True)
    question_content = db.Column(db.Text, nullable=False)
    constitution_type = db.Column(db.String(20), nullable=True)
    answer_value = db.Column(db.Integer, nullable=False)
    is_followup = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='answers')