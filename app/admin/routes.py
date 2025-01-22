import math

import requests
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required, current_user

from app.admin import bp
from app.admin.form import EditModuleForm
from app.models import *
from app.main.forms import *


@bp.route("/announcements")
@login_required
def announcements():
    if current_user.role != "admin":
        flash("You are not admin")
        return redirect(url_for("main.index"))

    currentPage = request.args.get("page", 1, type=int)
    currentPageAnnouncements = Announcement.query.order_by(Announcement.createTime.desc()).paginate(page=currentPage,
                                                                                                    per_page=10,
                                                                                                    error_out=False)
    announcements = currentPageAnnouncements.items

    return render_template("admin/announcements.html", announcements=announcements,
                           currentPageAnnouncements=currentPageAnnouncements)


@bp.route("/editAnnouncement/<int:announcementId>", methods=["GET", "POST"])
@login_required
def editAnnouncement(announcementId):
    if current_user.role != "admin":
        flash("You are not admin")
        return redirect(url_for("main.index"))

    announcement = Announcement.query.filter(Announcement.id == announcementId).first()
    if not announcement:
        return redirect(url_for("main.wrongPage"))

    form = AnnouncementForm()
    if form.validate_on_submit():
        # update the announcement
        announcement.title = form.title.data
        announcement.content = form.content.data
        db.session.commit()
        flash("Successful saved")
        return redirect(url_for("admin.announcements"))
    form.title.data = announcement.title
    form.content.data = announcement.content
    return render_template("admin/editAnnouncement.html", form=form)


@bp.route("/deleteAnnouncement/<int:announcementId>", methods=["DELETE"])
@login_required
def deleteAnnouncement(announcementId):
    if current_user.role != "admin":
        flash("You are not admin")
        return redirect(url_for("main.index"))

    announcement = Announcement.query.filter(Announcement.id == announcementId).first()
    if not announcement:
        return redirect(url_for("main.wrongPage"))
    db.session.delete(announcement)
    db.session.commit()

    return jsonify({"message": "Successful delete!"})


@bp.route("/menus")
@login_required
def menus():
    if current_user.role != "admin":
        flash("You are not admin")
        return redirect(url_for("main.index"))

    currentPage = request.args.get("page", 1, type=int)
    currentPageMenus = Menu.query.order_by(Menu.date.desc()).paginate(page=currentPage, per_page=10, error_out=False)
    menus = currentPageMenus.items

    return render_template("admin/menus.html", menus=menus, currentPageMenus=currentPageMenus)


@bp.route("/editMenu/<int:menuId>", methods=["GET", "POST"])
@login_required
def editMenu(menuId):
    if current_user.role != "admin":
        flash("You are not admin")
        return redirect(url_for("main.index"))

    menu = Menu.query.filter(Menu.id == menuId).first()
    if not menu:
        return redirect(url_for("main.wrongPage"))

    form = CreateMenuForm()
    if form.validate_on_submit():
        # update the announcement
        menu.date = form.date.data
        menu.breakfast = form.breakfast.data
        menu.lunch = form.lunch.data
        menu.dinner = form.dinner.data
        db.session.commit()
        flash("Successful saved")
        return redirect(url_for("admin.menus"))
    form.date.data = menu.date
    form.breakfast.data = menu.breakfast
    form.lunch.data = menu.lunch
    form.dinner.data = menu.dinner
    return render_template("admin/editMenu.html", form=form)


@bp.route("/deleteMenu/<int:menuId>", methods=["DELETE"])
@login_required
def deleteMenu(menuId):
    if current_user.role != "admin":
        flash("You are not admin")
        return redirect(url_for("main.index"))

    menu = Menu.query.filter(Menu.id == menuId).first()
    if not menu:
        return redirect(url_for("main.wrongPage"))
    # Delete its reviews
    MenuReview.query.filter(MenuReview.menuId == menuId).delete()
    db.session.delete(menu)
    db.session.commit()

    return jsonify({"message": "Successful delete!"})


@bp.route("/modules")
@login_required
def modules():
    if current_user.role != "admin":
        flash("You are not admin")
        return redirect(url_for("main.index"))

    # Use paging to display courses in pages
    currentPage = request.args.get("page", 1, type=int)
    currentPageModules = Module.query.paginate(page=currentPage, per_page=10, error_out=False)
    modules = currentPageModules.items
    return render_template("admin/modules.html", modules=modules, currentPageModules=currentPageModules)


@bp.route("/editModule/<int:moduleId>", methods=["GET", "POST"])
@login_required
def editModule(moduleId):
    if current_user.role != "admin":
        flash("You are not admin")
        return redirect(url_for("main.index"))

    module = Module.query.filter(Module.id == moduleId).first()
    if not module:
        return redirect(url_for("main.wrongPage"))

    form = EditModuleForm()
    if form.validate_on_submit():
        # update the announcement
        teachers = Teacher.query.all()
        for teacher in teachers:
            if teacher.userId == int(form.teacher.data):
                break
        else:
            flash("Teacher's userId wrong!")
            return redirect(url_for("admin.editModule", moduleId=moduleId))

        module.teacherId = int(form.teacher.data)
        module.moduleName = form.moduleName.data
        module.schedule = form.schedule.data
        module.location = form.location.data
        module.officeHours = form.officeHours.data
        db.session.commit()
        flash("Successful saved")
        return redirect(url_for("admin.modules"))

    if module.teacherId:
        form.teacher.data = module.teacherId
    else:
        form.teacher.data = "NULL"

    form.moduleName.data = module.moduleName
    form.schedule.data = module.schedule
    form.location.data = module.location
    form.officeHours.data = module.officeHours
    return render_template("admin/editModule.html", form=form)


@bp.route("/deleteModule/<int:moduleId>", methods=["DELETE"])
@login_required
def deleteModule(moduleId):
    if current_user.role != "admin":
        flash("You are not admin")
        return redirect(url_for("main.index"))

    module = Module.query.filter(Module.id == moduleId).first()
    if not module:
        return redirect(url_for("main.wrongPage"))
    # Delete module selection record
    StudentModule.query.filter(StudentModule.moduleId == moduleId).delete()
    db.session.delete(module)
    db.session.commit()

    return jsonify({"message": "Successful delete!"})


@bp.route("/users")
@login_required
def users():
    if current_user.role != "admin":
        flash("You are not admin")
        return redirect(url_for("main.index"))

    # Use paging to display courses in pages
    currentPage = request.args.get("page", 1, type=int)
    currentPageUser = User.query.filter(User.role != "admin").paginate(page=currentPage, per_page=10, error_out=False)
    users = currentPageUser.items

    return render_template("admin/users.html", users=users, currentPageUser=currentPageUser)


@bp.route("/ban/<int:userId>", methods=["POST"])
@login_required
def ban(userId):
    if current_user.role != "admin":
        flash("You are not admin")
        return redirect(url_for("main.index"))

    user = User.query.filter(User.id == userId).first()
    if not user:
        return redirect(url_for("main.wrongPage"))
    # Delete module selection record

    if user.ban != "Ban":
        user.ban = "Ban"
        db.session.commit()
        return jsonify({"message": "Successful ban!"})
    else:
        user.ban = "unBan"
        db.session.commit()
    return jsonify({"message": "Successful unban!"})


@bp.route("/chat", methods=["POST"])
@login_required
def chat():
    # Make sure other routes can also use chat

    message = request.get_json().get("message")

    headers = {
        "Content-Type": "application/json"
    }

    requestOptions = {
        "message": message
    }

    result = requests.post("http://localhost:5000/chat", headers=headers, json=requestOptions)

    return jsonify(result.json())


@bp.route("/editUser/<int:userId>", methods=["GET", "POST"])
@login_required
def editUser(userId):
    if current_user.role != "admin":
        flash("You are not admin")
        return redirect(url_for("main.index"))

    user = User.query.filter(User.id == userId).first()
    if not user:
        return redirect(url_for("main.wrongPage"))

    if user.role == "student":
        form = StudentProfileForm()
        if form.validate_on_submit():
            # Find if there is a student with the same id
            checkId = Student.query.filter(Student.studentId == form.studentId.data).first()
            if checkId and user.student.studentId != checkId.studentId:
                flash("This id is already register, change it")
                return redirect(url_for("admin.editUser"))

            # Find if there is a student with the same email
            checkEmail = User.query.filter(User.email == form.email.data).first()
            if checkEmail and user.email != checkEmail.email:
                flash("This email is already register, change it")
                return redirect(url_for("admin.editUser"))

            # Find if there is a student with the same phone
            checkPhone = User.query.filter(User.phoneNumber == form.phoneNumber.data).first()
            if checkPhone and user.phoneNumber != checkPhone.phoneNumber:
                flash("This phone number is already register, change it")
                return redirect(url_for("admin.editUser"))

            user.email = form.email.data
            user.phoneNumber = form.phoneNumber.data
            user.address = form.address.data
            user.student.studentId = form.studentId.data
            user.student.dormBuilding = form.dormBuilding.data
            user.student.dormRoom = form.dormRoom.data
            db.session.commit()
            flash("Successful saved")
            return redirect(url_for("admin.users"))
        form.email.data = user.email
        form.phoneNumber.data = user.phoneNumber
        form.address.data = user.address
        form.studentId.data = user.student.studentId
        form.dormBuilding.data = user.student.dormBuilding
        form.dormRoom.data = user.student.dormRoom
        return render_template("admin/editUsers.html", form=form, user=user)
    elif user.role == "teacher":
        form = TeacherProfileForm()
        if form.validate_on_submit():
            # Find if there is a teacher with the same id
            checkId = Teacher.query.filter(Teacher.teacherId == form.teacherId.data).first()
            if checkId and user.teacher.teacherId != checkId.teacherId:
                flash("This id is already register, change it")
                return redirect(url_for("admin.editUser"))

            # Find if there is a teacher with the same email
            checkEmail = User.query.filter(User.email == form.email.data).first()
            if checkEmail and user.email != checkEmail.email:
                flash("This email is already register, change it")
                return redirect(url_for("admin.editUser"))

            # Find if there is a teacher with the same phone
            checkPhone = User.query.filter(User.phoneNumber == form.phoneNumber.data).first()
            if checkPhone and user.phoneNumber != checkPhone.phoneNumber:
                flash("This phone number is already register, change it")
                return redirect(url_for("admin.editUser"))

            user.email = form.email.data
            user.phoneNumber = form.phoneNumber.data
            user.address = form.address.data
            user.teacher.teacherId = form.teacherId.data
            user.teacher.officeLocation = form.officeLocation.data
            db.session.commit()
            flash("Successful saved")
            return redirect(url_for("admin.users"))
        form.email.data = user.email
        form.phoneNumber.data = user.phoneNumber
        form.address.data = user.address
        form.teacherId.data = user.teacher.teacherId
        form.officeLocation.data = user.teacher.officeLocation
        return render_template("admin/editUsers.html", form=form, user=user)
    elif user.role == "restaurantStaff":
        form = RestaurantStaffProfileForm()
        if form.validate_on_submit():
            # Find if there is a restaurant staff with the same email
            checkEmail = User.query.filter(User.email == form.email.data).first()
            if checkEmail and user.email != checkEmail.email:
                flash("This email is already register, change it")
                return redirect(url_for("main.editProfile"))

            # Find if there is a restaurant staff with the same phone
            checkPhone = User.query.filter(User.phoneNumber == form.phoneNumber.data).first()
            if checkPhone and user.phoneNumber != checkPhone.phoneNumber:
                flash("This phone number is already register, change it")
                return redirect(url_for("main.editProfile"))

            user.email = form.email.data
            user.phoneNumber = form.phoneNumber.data
            user.address = form.address.data
            user.restaurantStaff.workSchedule = form.workSchedule.data
            db.session.commit()
            flash("Successful saved")
            return redirect(url_for("admin.users"))
        form.email.data = user.email
        form.phoneNumber.data = user.phoneNumber
        form.address.data = user.address
        form.workSchedule.data = user.restaurantStaff.workSchedule
        return render_template("admin/editUsers.html", form=form, user=user)


@bp.route("/accountLog")
@login_required
def accountLog():

    if current_user.role != "admin":
        flash("You are not admin")
        return redirect(url_for("main.index"))

    currentPage = request.args.get("page", 1, type=int)

    lst = readLogFile("./app/log/login.log", currentPage)[0]
    totalPage = readLogFile("./app/log/login.log", currentPage)[1]

    return render_template("admin/accountLog.html", lst=lst, currentPage=currentPage, totalPage=totalPage)

@bp.route("/announcementLog")
@login_required
def announcementLog():

    if current_user.role != "admin":
        flash("You are not admin")
        return redirect(url_for("main.index"))

    currentPage = request.args.get("page", 1, type=int)

    lst = readLogFile("./app/log/announcement.log", currentPage)[0]
    totalPage = readLogFile("./app/log/announcement.log", currentPage)[1]

    return render_template("admin/announcementLog.html", lst=lst, currentPage=currentPage, totalPage=totalPage)


@bp.route("/errorLog")
@login_required
def errorLog():

    if current_user.role != "admin":
        flash("You are not admin")
        return redirect(url_for("main.index"))

    currentPage = request.args.get("page", 1, type=int)

    lst = readLogFile("./app/log/error.log", currentPage)[0]
    totalPage = readLogFile("./app/log/error.log", currentPage)[1]

    return render_template("admin/errorLog.html", lst=lst, currentPage=currentPage, totalPage=totalPage)


@bp.route("/loginLog")
@login_required
def loginLog():

    if current_user.role != "admin":
        flash("You are not admin")
        return redirect(url_for("main.index"))

    currentPage = request.args.get("page", 1, type=int)

    lst = readLogFile("./app/log/login.log", currentPage)[0]
    totalPage = readLogFile("./app/log/login.log", currentPage)[1]

    return render_template("admin/loginLog.html", lst=lst, currentPage=currentPage, totalPage=totalPage)


@bp.route("/menuLog")
@login_required
def menuLog():

    if current_user.role != "admin":
        flash("You are not admin")
        return redirect(url_for("main.index"))

    currentPage = request.args.get("page", 1, type=int)

    lst = readLogFile("./app/log/menu.log", currentPage)[0]
    totalPage = readLogFile("./app/log/menu.log", currentPage)[1]

    return render_template("admin/menuLog.html", lst=lst, currentPage=currentPage, totalPage=totalPage)


@bp.route("/moduleLog")
@login_required
def moduleLog():

    if current_user.role != "admin":
        flash("You are not admin")
        return redirect(url_for("main.index"))

    currentPage = request.args.get("page", 1, type=int)

    lst = readLogFile("./app/log/module.log", currentPage)[0]
    totalPage = readLogFile("./app/log/module.log", currentPage)[1]

    return render_template("admin/moduleLog.html", lst=lst, currentPage=currentPage, totalPage=totalPage)


@bp.route("/registerLog")
@login_required
def registerLog():

    if current_user.role != "admin":
        flash("You are not admin")
        return redirect(url_for("main.index"))

    currentPage = request.args.get("page", 1, type=int)

    lst = readLogFile("./app/log/register.log", currentPage)[0]
    totalPage = readLogFile("./app/log/register.log", currentPage)[1]

    return render_template("admin/registerLog.html", lst=lst, currentPage=currentPage, totalPage=totalPage)


def readLogFile(fileName, page):
    with open(fileName, "r") as log:
        lines = log.readlines()
        total = len(lines)
        lines = lines[::-1]
        start = (page - 1) * 10
        end = min(start + 10, total)
        return lines[start:end], math.ceil(total / 10)
