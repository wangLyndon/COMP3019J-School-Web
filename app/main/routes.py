import logging
import os

import requests
from flask import redirect, url_for, flash, render_template, request, jsonify, current_app
from flask_login import current_user, login_user, logout_user, login_required
from pyexpat.errors import messages
from sqlalchemy import false
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.main import bp
from app.main.forms import ChangePasswordForm, MenuReviewForm, CreateMenuForm, EnrollForm, StudentProfileForm, \
    TeacherProfileForm, RestaurantStaffProfileForm, CreateModuleForm, AnnouncementForm
from app.models import *


@bp.route("/")
@bp.route("/index")
def index():
    # Use paging to display courses in pages
    currentPage = request.args.get("page", 1, type=int)
    currentPageAnnouncements = Announcement.query.order_by(Announcement.createTime.desc()).paginate(page=currentPage,
                                                                                                    per_page=10,
                                                                                                    error_out=False)
    announcements = currentPageAnnouncements.items
    return render_template("main/index.html", announcements=announcements,
                           currentPageAnnouncements=currentPageAnnouncements)


@bp.route("/announcement/<int:announcementId>")
def announcement(announcementId):
    announcement = Announcement.query.filter(Announcement.id == announcementId).first()
    if not announcement:
        return redirect(url_for("main.wrongPage"))
    return render_template("main/announcement.html", announcement=announcement)


@bp.route("/profile")
@login_required
def profile():
    return render_template("main/profile.html", user=current_user)


@bp.route("/deleteReview/<int:reviewId>", methods=["DELETE"])
@login_required
def deleteReview(reviewId):
    if current_user.role != "student" and current_user.role != "teacher":
        flash("You can not do that")
        return redirect(url_for("main.index"))

    review = MenuReview.query.filter(MenuReview.id == reviewId).first()
    if not review:
        return redirect(url_for("main.wrongPage"))

    logging.getLogger("menu").info(f"{current_user.username} delete a menu review, content: {review.reviewContent}")

    db.session.delete(review)
    db.session.commit()

    return jsonify({"message": "Successful delete!"})


@bp.route("/deleteAccount", methods=["DELETE"])
@login_required
def deleteAccount():
    user = User.query.filter(User.id == current_user.id).first()

    if not user:
        return redirect(url_for("main.wrongPage"))

    if current_user.role == "student":
        # Delete modules and reviews
        StudentModule.query.filter(StudentModule.studentId == user.id).delete()
        Student.query.filter(Student.userId == user.id).delete()
        MenuReview.query.filter(MenuReview.userId == user.id).delete()
        db.session.delete(user)
        db.session.commit()
    elif current_user.role == "teacher":
        # Delete reviews and modules
        modules = Module.query.filter(Module.teacherId == user.id)

        for module in modules:
            module.teacherId = None
        db.session.commit()

        Teacher.query.filter(Teacher.userId == user.id).delete()
        MenuReview.query.filter(MenuReview.userId == user.id).delete()
        db.session.delete(user)
        db.session.commit()
    elif current_user.role == "restaurantStaff":
        # Delete menus
        menus = Menu.query.filter(Menu.createdBy == user.id)

        for menu in menus:
            menu.createdBy = None
        db.session.commit()

        RestaurantStaff.query.filter(RestaurantStaff.userId == user.id).delete()
        db.session.delete(user)
        db.session.commit()
    else:
        db.session.delete(user)
        db.session.commit()

    logging.getLogger("account").info(f"{current_user.username} delete his/her account")

    return jsonify({"message": "Successful delete!"})


@bp.route("/editProfile", methods=["GET", "POST"])
@login_required
def editProfile():
    if current_user.role == "admin":
        return redirect(url_for("main.wrongPage"))

    if current_user.role == "student":
        form = StudentProfileForm()
        if form.validate_on_submit():
            # Find if there is a student with the same id
            checkId = Student.query.filter(Student.studentId == form.studentId.data).first()
            if checkId and current_user.student.studentId != checkId.studentId:
                flash("This id is already register, change it")
                return redirect(url_for("main.editProfile"))

            # Find if there is a student with the same email
            checkEmail = User.query.filter(User.email == form.email.data).first()
            if checkEmail and current_user.email != checkEmail.email:
                flash("This email is already register, change it")
                return redirect(url_for("main.editProfile"))

            # Find if there is a student with the same phone
            checkPhone = User.query.filter(User.phoneNumber == form.phoneNumber.data).first()
            if checkPhone and current_user.phoneNumber != checkPhone.phoneNumber:
                flash("This phone number is already register, change it")
                return redirect(url_for("main.editProfile"))

            current_user.email = form.email.data
            current_user.phoneNumber = form.phoneNumber.data
            current_user.address = form.address.data
            current_user.student.studentId = form.studentId.data
            current_user.student.dormBuilding = form.dormBuilding.data
            current_user.student.dormRoom = form.dormRoom.data
            db.session.commit()
            flash("Successful saved")

            logging.getLogger("account").info(f"{current_user.username} edit his/her profile")

            return redirect(url_for("main.profile"))
        form.email.data = current_user.email
        form.phoneNumber.data = current_user.phoneNumber
        form.address.data = current_user.address
        form.studentId.data = current_user.student.studentId
        form.dormBuilding.data = current_user.student.dormBuilding
        form.dormRoom.data = current_user.student.dormRoom
        return render_template("main/editProfile.html", form=form)
    elif current_user.role == "teacher":
        form = TeacherProfileForm()
        if form.validate_on_submit():
            # Find if there is a teacher with the same id
            checkId = Teacher.query.filter(Teacher.teacherId == form.teacherId.data).first()
            if checkId and current_user.teacher.teacherId != checkId.teacherId:
                flash("This id is already register, change it")
                return redirect(url_for("main.editProfile"))

            # Find if there is a teacher with the same email
            checkEmail = User.query.filter(User.email == form.email.data).first()
            if checkEmail and current_user.email != checkEmail.email:
                flash("This email is already register, change it")
                return redirect(url_for("main.editProfile"))

            # Find if there is a teacher with the same phone
            checkPhone = User.query.filter(User.phoneNumber == form.phoneNumber.data).first()
            if checkPhone and current_user.phoneNumber != checkPhone.phoneNumber:
                flash("This phone number is already register, change it")
                return redirect(url_for("main.editProfile"))

            current_user.email = form.email.data
            current_user.phoneNumber = form.phoneNumber.data
            current_user.address = form.address.data
            current_user.teacher.teacherId = form.teacherId.data
            current_user.teacher.officeLocation = form.officeLocation.data
            db.session.commit()
            flash("Successful saved")

            logging.getLogger("account").info(f"{current_user.username} edit his/her profile")

            return redirect(url_for("main.profile"))
        form.email.data = current_user.email
        form.phoneNumber.data = current_user.phoneNumber
        form.address.data = current_user.address
        form.teacherId.data = current_user.teacher.teacherId
        form.officeLocation.data = current_user.teacher.officeLocation
        return render_template("main/editProfile.html", form=form)
    elif current_user.role == "restaurantStaff":
        form = RestaurantStaffProfileForm()
        if form.validate_on_submit():
            # Find if there is a restaurant staff with the same email
            checkEmail = User.query.filter(User.email == form.email.data).first()
            if checkEmail and current_user.email != checkEmail.email:
                flash("This email is already register, change it")
                return redirect(url_for("main.editProfile"))

            # Find if there is a restaurant staff with the same phone
            checkPhone = User.query.filter(User.phoneNumber == form.phoneNumber.data).first()
            if checkPhone and current_user.phoneNumber != checkPhone.phoneNumber:
                flash("This phone number is already register, change it")
                return redirect(url_for("main.editProfile"))

            current_user.email = form.email.data
            current_user.phoneNumber = form.phoneNumber.data
            current_user.address = form.address.data
            current_user.restaurantStaff.workSchedule = form.workSchedule.data
            db.session.commit()
            flash("Successful saved")

            logging.getLogger("account").info(f"{current_user.username} edit his/her profile")

            return redirect(url_for("main.profile"))
        form.email.data = current_user.email
        form.phoneNumber.data = current_user.phoneNumber
        form.address.data = current_user.address
        form.workSchedule.data = current_user.restaurantStaff.workSchedule
        return render_template("main/editProfile.html", form=form)


@bp.route("/modules", methods=["GET", "POST"])
def modules():
    # Use paging to display courses in pages
    currentPage = request.args.get("page", 1, type=int)
    currentPageModules = Module.query.paginate(page=currentPage, per_page=10, error_out=False)
    modules = currentPageModules.items
    return render_template("main/modules.html", modules=modules, currentPageModules=currentPageModules)


@bp.route("/module/<int:moduleId>", methods=["GET", "POST"])
def module(moduleId):
    module = Module.query.filter(Module.id == moduleId).first()
    if not module:
        return redirect(url_for("main.wrongPage"))

    form = EnrollForm()

    if form.validate_on_submit():
        # Only students can operate enroll
        if not current_user.is_authenticated:
            flash("You need to login")
            return redirect(url_for("main.modules"))
        if current_user.role != "student":
            flash("Only student can enroll")
            return redirect(url_for("main.modules"))
        isEnroll = StudentModule.query.filter((StudentModule.studentId == current_user.student.userId),
                                              (StudentModule.moduleId == moduleId)).first()
        if isEnroll:
            flash("You already enroll in it")
        else:
            enroll = StudentModule(studentId=current_user.student.userId, moduleId=moduleId)
            db.session.add(enroll)
            db.session.commit()
            flash("Successful enroll")

        logging.getLogger("module").info(f"{current_user.username} enroll: {module.moduleName}")

        return redirect(url_for("main.modules"))

    if current_user.is_authenticated and current_user.role == "teacher":
        currentPage = request.args.get("page", 1, type=int)
        currentPageStudent = StudentModule.query.filter(StudentModule.moduleId == moduleId).paginate(page=currentPage,
                                                                                                     per_page=10,
                                                                                                     error_out=False)
        students = currentPageStudent.items
        return render_template("main/module.html", module=module, form=form, students=students,
                               currentPageStudent=currentPageStudent)

    return render_template("main/module.html", module=module, form=form)


@bp.route("/createModule", methods=["GET", "POST"])
@login_required
def createModule():
    # Not the teacher will return.
    if current_user.role != "teacher":
        flash("You can not create module")
        return redirect(url_for("main.index"))
    form = CreateModuleForm()
    if form.validate_on_submit():
        module = Module(moduleName=form.moduleName.data, schedule=form.schedule.data,
                        teacherId=current_user.teacher.userId,
                        location=form.location.data, officeHours=form.officeHours.data)
        db.session.add(module)
        db.session.commit()
        flash("Successful saved")

        logging.getLogger("module").info(f"{current_user.username} create module: {module.moduleName}")

        return redirect(url_for("main.modules"))
    return render_template("main/createModule.html", form=form)


@bp.route("/menus")
def menus():
    currentPage = request.args.get("page", 1, type=int)
    currentPageMenus = Menu.query.order_by(Menu.date.desc()).paginate(page=currentPage, per_page=10, error_out=False)
    menus = currentPageMenus.items
    return render_template("main/menus.html", menus=menus, currentPageMenus=currentPageMenus)


@bp.route("/menu/<int:menuId>", methods=["GET", "POST"])
def menu(menuId):
    menu = Menu.query.filter(Menu.id == menuId).first()
    if not menu:
        return redirect(url_for("main.wrongPage"))
    form = MenuReviewForm()
    if form.validate_on_submit():
        # Only teachers and students can review
        if current_user.is_authenticated and current_user.role in ["student", "teacher"]:
            review = MenuReview(menuId=menu.id, userId=current_user.id, rating=form.rating.data,
                                reviewContent=form.reviewContent.data, createTime=datetime.utcnow())
            db.session.add(review)
            db.session.commit()
            flash("Successful saved")

            logging.getLogger("menu").info(f"{current_user.username} review the menu: {menu.date}")

            return redirect(url_for("main.menu", menuId=menu.id))
        else:
            flash("You do not have permission to comment")
            return redirect(url_for("main.menu", menuId=menu.id))
    reviews = MenuReview.query.filter(MenuReview.menuId == menuId).all()
    return render_template("main/menu.html", menu=menu, form=form, reviews=reviews)


@bp.route("/createMenu", methods=["GET", "POST"])
@login_required
def createMenu():
    if current_user.role != "restaurantStaff":
        flash("Only restaurant staff can create menus")
        return redirect(url_for("main.index"))
    form = CreateMenuForm()
    if form.validate_on_submit():
        existingMenu = Menu.query.filter(Menu.date == form.date.data).first()
        if existingMenu:
            flash("A menu for this date already exists")
            return redirect(url_for("main.createMenu"))
        menu = Menu(date=form.date.data, createdBy=current_user.restaurantStaff.userId, breakfast=form.breakfast.data,
                    lunch=form.lunch.data, dinner=form.dinner.data)
        db.session.add(menu)
        db.session.commit()
        flash("Successful saved")

        logging.getLogger("menu").info(f"{current_user.username} create the menu: {menu.date}")

        return redirect(url_for("main.menus"))
    return render_template("main/createMenu.html", form=form)


@bp.route("/createAnnouncement", methods=["GET", "POST"])
@login_required
def createAnnouncement():
    if current_user.role != "teacher":
        flash("You can not create announcement")
        return redirect(url_for("main.index"))
    form = AnnouncementForm()
    if form.validate_on_submit():
        announcement = Announcement(title=form.title.data, content=form.content.data,
                                    createdBy=current_user.teacher.userId,
                                    createTime=datetime.utcnow())
        db.session.add(announcement)
        db.session.commit()
        flash("Successful saved")

        logging.getLogger("announcement").info(f"{current_user.username} create the announcement: {announcement.title}")

        return redirect(url_for("main.index"))
    return render_template("main/createAnnouncement.html", form=form)


@bp.route("/admin")
@login_required
def admin():
    if current_user.role != "admin":
        flash("You are not admin")
        return redirect(url_for("main.index"))
    return render_template("main/admin.html")


@bp.route("/changePassword", methods=["GET", "POST"])
@login_required
def changePassword():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not (check_password_hash(current_user.passwordHash, form.password.data)):
            flash("Old password is wrong!")
            return redirect(url_for("main.changePassword"))
        current_user.passwordHash = generate_password_hash(form.newPassword.data)
        db.session.commit()
        flash("Successful saved")

        logging.getLogger("account").info(f"{current_user.username} changes his/her password")

        return redirect(url_for("main.profile"))
    return render_template("main/changePassword.html", form=form)


@bp.route("/wrongPage")
def wrongPage():
    current_app.logger.error("A user visit wrong page!")
    return render_template("main/wrongPage.html")


@bp.route("/banPage")
def banPage():
    current_app.logger.error("A user that banned want to visit the web")
    return render_template("main/banPage.html")


@bp.route("/chat", methods=["POST", "GET"])
def chat():
    # Store the API in .env for security reasons
    API = os.environ.get("API")

    message = request.get_json().get("message")

    headers = {
        "Authorization": f"Bearer {API}",
        "Content-Type": "application/json"
    }

    requestOptions = {
        "messages": [
            {
                "role": "system",
                "content": message
            }
        ],
        "stream": False,
        "model": "gpt-3.5-turbo",
        "temperature": 0.5,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "top_p": 1
    }

    result = requests.post("https://xiaoai.plus/v1/chat/completions", headers=headers, json=requestOptions)

    return jsonify(result.json())
