from app import db, login
from flask_login import UserMixin
from datetime import datetime

@login.user_loader
def load_user(user_id):
    # Used to highlight current_user
    return User.query.get(int(user_id))

# User table
class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    passwordHash = db.Column(db.String(256), index=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    role = db.Column(db.String(20))
    phoneNumber = db.Column(db.String(11), index=True, unique=True, nullable=False)
    address = db.Column(db.String(200))
    ban = db.Column(db.String(10), default="unBan")

    # relating to other tables
    student = db.relationship("Student", backref="user", uselist=False)
    teacher = db.relationship("Teacher", backref="user", uselist=False)
    restaurantStaff = db.relationship("RestaurantStaff", backref="user", uselist=False)
    menuReviews = db.relationship("MenuReview", backref="user")

    def __init__(self, **kwargs):
        # Used to facilitate to create user class
        super().__init__(**kwargs)

# Students table
class Student(db.Model):
    __tablename__ = "students"

    userId = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    studentId = db.Column(db.String(20), unique=True)
    dormBuilding = db.Column(db.String(50))
    dormRoom = db.Column(db.String(10))

    # relating to student module
    modules = db.relationship("StudentModule", back_populates="student")

# Teacher table
class Teacher(db.Model):
    __tablename__ = "teachers"

    userId = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    teacherId = db.Column(db.String(20), unique=True)
    officeLocation = db.Column(db.String(50))

    # relating to module and announcement
    modules = db.relationship("Module", back_populates="teacher")
    announcements = db.relationship("Announcement", backref="teacher")

# Restaurant staff table
class RestaurantStaff(db.Model):
    __tablename__ = "restaurantStaff"

    userId = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    workSchedule = db.Column(db.String(100))

    # relating to menu
    menus = db.relationship("Menu", backref="creator")

# Module table
class Module(db.Model):
    __tablename__ = "modules"

    id = db.Column(db.Integer, primary_key=True)
    moduleName = db.Column(db.String(50))
    schedule = db.Column(db.String(50))
    teacherId = db.Column(db.Integer, db.ForeignKey("teachers.userId"))
    location = db.Column(db.String(100))
    officeHours = db.Column(db.String(100))

    # relating to teacher and student
    teacher = db.relationship("Teacher", back_populates="modules")
    students = db.relationship("StudentModule", back_populates="module")

# Student module table
class StudentModule(db.Model):
    __tablename__ = "studentModules"

    id = db.Column(db.Integer, primary_key=True)
    studentId = db.Column(db.Integer, db.ForeignKey("students.userId"))
    moduleId = db.Column(db.Integer, db.ForeignKey("modules.id"))

    # relating to module and student
    student = db.relationship("Student", back_populates="modules")
    module = db.relationship("Module", back_populates="students")

# Menu table
class Menu(db.Model):
    __tablename__ = "menus"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=datetime.utcnow)
    createdBy = db.Column(db.Integer, db.ForeignKey("restaurantStaff.userId"))
    createTime = db.Column(db.DateTime, default=datetime.utcnow)
    breakfast = db.Column(db.String(100), nullable=False)
    lunch = db.Column(db.String(100), nullable=False)
    dinner = db.Column(db.String(100), nullable=False)

    # relating to item and review
    # items = db.relationship("MenuItem", backref="menu")
    reviews = db.relationship("MenuReview", backref="menu")

# Menu item table
# class MenuItem(db.Model):
#     __tablename__ = "menuItems"
#
#     id = db.Column(db.Integer, primary_key=True)
#     menuId = db.Column(db.Integer, db.ForeignKey("menus.id"))
#     itemName = db.Column(db.String(100))
#     mealTime = db.Column(db.String(20))

# Menu review table
class MenuReview(db.Model):
    __tablename__ = "menuReviews"

    id = db.Column(db.Integer, primary_key=True)
    menuId = db.Column(db.Integer, db.ForeignKey("menus.id"))
    userId = db.Column(db.Integer, db.ForeignKey("users.id"))
    rating = db.Column(db.Integer)
    reviewContent = db.Column(db.String(500))
    createTime = db.Column(db.DateTime, default=datetime.utcnow)

# Announcement table
class Announcement(db.Model):
    __tablename__ = "announcements"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.String(500))
    createdBy = db.Column(db.Integer, db.ForeignKey("teachers.userId"))
    createTime = db.Column(db.DateTime, default=datetime.utcnow)
