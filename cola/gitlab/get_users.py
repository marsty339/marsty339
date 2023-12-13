import gitlab
import xlrd
import xlwt


def get_all_users(gl):
    return gl.users.list(all=True, sort='asc')


def write_to_file(users, path):
    workbook = xlwt.Workbook(encoding='utf8')
    sheet1 = workbook.add_sheet('staff', cell_overwrite_ok=True)
    style_text_align_vert_center_horiz_center = xlwt.easyxf("align: vert centre, horiz centre, wrap True")
    sheet1.write(0, 0, 'id', style_text_align_vert_center_horiz_center)
    sheet1.write(0, 1, 'email', style_text_align_vert_center_horiz_center)
    sheet1.write(0, 2, 'name', style_text_align_vert_center_horiz_center)
    index = 1
    for user in users:
        print(user.id)
        sheet1.write(index, 0, user.id, style_text_align_vert_center_horiz_center)
        sheet1.write(index, 1, user.email, style_text_align_vert_center_horiz_center)
        sheet1.write(index, 2, user.name, style_text_align_vert_center_horiz_center)
        index += 1
    workbook.save(path)


def parse_xlsx(path):
    # Open file
    wb = xlrd.open_workbook(path)
    return wb.sheet_by_index(0)


def block_users(users):
    pass


def compare_users_by_mail(users1, users2):
    for user in users1:
        pass


if __name__ == '__main__':
    gl = gitlab.Gitlab('https://gitlab-ce.alauda.cn', private_token='gitlab——token')
    file_path = './gitlab_users.xlsx'

    staff = get_all_users(gl)
    # gitlab current users
    # print(len(staff))

    sheet = parse_xlsx("./staff.xlsx")
    # current developers
    # print(sheet.nrows)

    write_to_file(staff, file_path)
