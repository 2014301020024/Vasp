import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import ListedColormap
from matplotlib.ticker import MultipleLocator
from matplotlib import ticker
from matplotlib.ticker import FormatStrFormatter
from PIL import Image
import numpy as np

def sum_str(str1):
    len1 = len(str1)                  # 首先将字符串str1的长度赋值给len1
    sum1 = n = 0                      # 建立一个值为0的空变量sun     #建立一个值为0的空变量n
    for i in range(len1):             # 用i来遍历字符串的长度
        if 48 <= ord(str1[i]) <= 57:  # 判断字符ascii码是否在数字ascii值范围内
            n = n * 10                # n *= 10
            n = int(str1[i]) + n      # n += int(str1[i])
        else:
            sum1 = n + sum1           # sum += n
            n = 0
    sum1 = n + sum1
    return sum1

def list_number_in_str(str1):
    len1 = len(str1)                  # 首先将字符串str1的长度赋值给len1
    lst1 = []                         # 建立一个空列表lst1
    n = 0                             # 建立一个值为0的空变量n
    for i in range(len1):             # 用i来遍历字符串的长度
        if 48 <= ord(str1[i]) <= 57:  # 判断字符ascii码是否在数字ascii值范围内
            n = n * 10                # n *= 10
            n = int(str1[i]) + n      # n += int(str1[i])
        else:
            if n != 0:
                lst1.append(n)         # sum += n
                n = 0
    lst1.append(n)
    return lst1


def electric(total):
    total = [i.strip("\n") for i in total]
    scaling_factor = float(total[1])
    supercell = [i.strip(" ") for i in total[2:5]]
    volumn = float(supercell[0][:9]) * float(supercell[2][-10:]) * float(supercell[1][9:-10]) \
             * scaling_factor
    atom_count = sum_str(total[6])
    NGX = list_number_in_str(total[6 + 1 + 2 + atom_count])[0]
    NGY = list_number_in_str(total[6 + 1 + 2 + atom_count])[1]
    NGZ = list_number_in_str(total[6 + 1 + 2 + atom_count])[2]
    for i in total:
        if "augmentation occupancies" in i:
            end = total.index(i)
            break
    site_count = 5
    charge_density_str = [i.strip(" ") for i in total[6 + 1 + 2 + atom_count + 1:end]]
    lenth = int((len(charge_density_str[0]) - (site_count - 1)) / site_count)
    charge_density_list1 = []
    num = 0
    for i in charge_density_str[:-1]:
        for j in range(site_count):
            if num == 0:
                charge_density_list1.append(i[:(num + 1) * lenth])
            else:
                charge_density_list1.append((i[num * (lenth + 1):(num + 1) * (lenth + 1) - 1]))
            num += 1
        num = 0
    total_grid = NGX * NGY * NGZ
    input1 = (NGX * NGY * NGZ) % 5
    for j in range(input1):
        if num == 0:
            charge_density_list1.append(charge_density_str[-1][:(num + 1) * lenth])
        else:
            charge_density_list1.append((charge_density_str[-1][num * (lenth + 1):(num + 1) * (lenth + 1) - 1]))
        num += 1
    charge_density_list = []

    for i in charge_density_list1:
        if i[-3] == "+":
            charge_density_list.append(
                float(float(i[:-4]) * (10 ** int(i[-2:])) / total_grid))
        else:
            charge_density_list.append(
                float(float(i[:-4]) * (10 ** (-1 * int(i[-2:]))) / total_grid))
    electric = []
    for i in range(NGZ):
        if i == NGZ - 1:
            sum1 = sum(charge_density_list[i * NGX * NGY:])
        else:
            sum1 = sum(charge_density_list[i * NGX * NGY:(i + 1) * NGX * NGY])
        electric.append(sum1)
    return [electric, NGZ]


def sure_layer_place(CONTCAR):
    CONTCAR = [i.strip(" ") for i in [i.strip('\n') for i in CONTCAR]]
    c_coord = [round(float(i[40:58]), 4) for i in CONTCAR[9:99]]
    fixed_layer1, fixed_layer2 = [], []
    for i in range(9):
        fixed_layer1.append(c_coord[(i * 8) + 7])
        fixed_layer2.append(c_coord[(i * 8) + 6])
    layer_place1 = sum(fixed_layer1)/9
    layer_place2 = sum(fixed_layer2)/9
    absorb_place = sum(c_coord[72:])/18
    return [layer_place1, layer_place2, absorb_place]


''' kind one: according the peak of different charge density, integrate all subsequent spaces '''
# ---------------------------------------------------------------------------------------------------------------------
# metal_total = ["Ge", "Nb", "Ta", "Ag", 'Ti', 'W', "Al", "Mo"]
metal_total = ["Mo", "Al", "W", "Ti", 'Ag', 'Ta', "Nb", "Ge"]
charge_transfer_total = []

fig = plt.figure(figsize=(50, 80), dpi=200)
ax = plt.subplot(111)

''' plane-average electron difference '''
# num = 0
# for i in metal_total:
#     metal = i
#     f0 = open("/Users/yuze/Desktop/borophene/CONT/top/CONTCAR-" + i, "r")
#     CONTCAR = f0.readlines()
#     layer_place = sure_layer_place(CONTCAR)
#     f = open("/Users/yuze/Desktop/borophene/CHGCAR/top/" + metal + "/total/CHGCAR", 'r')
#     total = f.readlines()
#     energy_total = electric(total)
#     electric_total = energy_total[0]
#     f = open("/Users/yuze/Desktop/borophene/CHGCAR/top/" + metal + "/B/CHGCAR", 'r')
#     total1 = f.readlines()
#     surface_total = electric(total1)
#     electric_surface = surface_total[0]
#     f = open("/Users/yuze/Desktop/borophene/CHGCAR/top/" + metal + "/cd/CHGCAR", 'r')
#     total2 = f.readlines()
#     cd_total = electric(total2)
#     electric_cd = cd_total[0]
#     NGZ = energy_total[1]
#     different = [((i - electric_cd[electric_total.index(i)] - electric_surface[electric_total.index(i)]))
#                  for i in electric_total]
#     peak = max(different)
#     valley = min(different)
#     charge_transfer_accumlate = sum(different[different.index(peak):])
#     charge_transfer_total.append(charge_transfer_accumlate)
#     x_place = np.linspace(0, 1, NGZ)
#     plt.scatter([0.0550700029999973, 0.1192499989999973, 0.1834299980000011,
#                  0.2476200030000015, 0.3118000150000029, 0.3759800010000021],
#                 [0 + num,  0 + num, 0 + num, 0 + num, 0 + num, 0 + num], color='blue', s=300)
#     plt.scatter(layer_place[:2],
#                 [0 + num, 0 + num], color='blue', s=300)              #
#     plt.scatter(layer_place[2:3], [0 + num], color='blue', s=400)
#     plt.plot(x_place, [(i + num) for i in different], linewidth=5, color="royalblue")
#     plt.text(0.075, 0.2 + num, metal, size=100, weight="bold", alpha=0.5, ha='center', va='center')
#     # plt.fill_between([])
#     plt.plot([0, 1], [0 + num, 0 + num], ls=":", linewidth=4, color='gray')
#     num += 0.5

num = 0
for i in metal_total:
    metal = i
    f0 = open("/Users/yuze/Desktop/borophene/CONT/hollow/CONTCAR-" + i, "r")
    CONTCAR = f0.readlines()
    layer_place = sure_layer_place(CONTCAR)
    f = open("/Users/yuze/Desktop/borophene/CHGCAR/hollow/" + metal + "/total/CHGCAR", 'r')
    total = f.readlines()
    energy_total = electric(total)
    electric_total = energy_total[0]
    f = open("/Users/yuze/Desktop/borophene/CHGCAR/hollow/" + metal + "/B/CHGCAR", 'r')
    total1 = f.readlines()
    surface_total = electric(total1)
    electric_surface = surface_total[0]
    f = open("/Users/yuze/Desktop/borophene/CHGCAR/hollow/" + metal + "/cd/CHGCAR", 'r')
    total2 = f.readlines()
    cd_total = electric(total2)
    electric_cd = cd_total[0]
    NGZ = energy_total[1]
    different = [((i - electric_cd[electric_total.index(i)] - electric_surface[electric_total.index(i)]))
                 for i in electric_total]
    peak = max(different)
    valley = min(different)
    charge_transfer_accumlate = sum(different[different.index(peak):])
    charge_transfer_total.append(charge_transfer_accumlate)
    print(charge_transfer_accumlate)
    x_place = np.linspace(0, 1, NGZ)
    plt.scatter([0.0550700029999973, 0.1192499989999973, 0.1834299980000011,
                 0.2476200030000015, 0.3118000150000029, 0.3759800010000021],
                [0 + num,  0 + num, 0 + num, 0 + num, 0 + num, 0 + num], color='blue', s=600)
    plt.scatter(layer_place[:2],
                [0 + num, 0 + num], color='blue', s=600)              #
    plt.scatter(layer_place[2:3], [0 + num], color='green', s=600)
    plt.plot(x_place, [(i + num) for i in different], linewidth=5, color="royalblue")
    plt.text(0.1, num - 0.15, metal, size=150, weight="bold", alpha=0.5, ha='center', va='center')
    # plt.fill_between([])
    plt.plot([0, 1], [0 + num, 0 + num], ls=":", linewidth=4, color='gray')
    num += 0.5

plt.xlabel("Fractional coordinates",
           fontdict={'family': 'Times New Roman', 'weight': 'bold', 'size': 180})
plt.ylabel('The relative plane-average electron difference/ e/Å',
           fontdict={'family': 'Times New Roman', 'weight': 'bold', 'size': 180})
plt.xticks(family='Times New Roman', size=100)
plt.yticks(family='Times New Roman', size=60)
ax1 = plt.gca()
ax1.spines['bottom'].set_linewidth(3)
ax1.spines['left'].set_linewidth(3)
ax1.spines['right'].set_linewidth(3)
ax1.spines['top'].set_linewidth(3)
plt.xlim([0.7, 0])
plt.ylim([-0.4, 3.7])
plt.yticks([])
# plt.savefig('/Users/yuze/Desktop/different_charge_transfer.png', dpi=200)
plt.show()

''' total charge transfer and electronegativity   '''
''' 1.  from the highest peak of different charge density between borophene and surface metal layer, 
        integrate all subsequent spaces '''
# metal_total = ["Ge", "Nb", "Ta",
#                "Ag", 'Ti', 'W', "Al", "Mo"]
# for i in metal_total:
#     metal = i
#     f0 = open("/Users/yuze/Desktop/borophene/CONT/hollow/CONTCAR-" + i, "r")
#     CONTCAR = f0.readlines()
#     layer_place = sure_layer_place(CONTCAR)
#     f = open("/Users/yuze/Desktop/borophene/CHGCAR/hollow/" + metal + "/total/CHGCAR", 'r')
#     total = f.readlines()
#     energy_total = electric(total)
#     electric_total = energy_total[0]
#     f = open("/Users/yuze/Desktop/borophene/CHGCAR/hollow/" + metal + "/B/CHGCAR", 'r')
#     total1 = f.readlines()
#     surface_total = electric(total1)
#     electric_surface = surface_total[0]
#     f = open("/Users/yuze/Desktop/borophene/CHGCAR/hollow/" + metal + "/cd/CHGCAR", 'r')
#     total2 = f.readlines()
#     cd_total = electric(total2)
#     electric_cd = cd_total[0]
#
#     NGZ = energy_total[1]
#     different = [((i - electric_cd[electric_total.index(i)] - electric_surface[electric_total.index(i)]))
#                  for i in electric_total]
#     peak = max(different)
#     charge_transfer_accumlate = sum(different[different.index(peak):])
#     print(i)
#     print(peak)
#     print(charge_transfer_accumlate)
#     charge_transfer_total.append(charge_transfer_accumlate)
#
# fig = plt.figure(figsize=(30, 16), dpi=200)
# ax = plt.subplot(111)
# electronegativity = [2.01, 1.59, 1.51, 1.93, 1.54, 2.36, 1.61, 2.16]
# first_ion_energy = [762, 652.1, 761, 731, 658.8, 770, 577.5, 684.3]
# first_ion_energy = [(i * (10 ** 3))/(1.6 * (10 ** (-19)) * 6.023 * (10 ** 23)) for i in first_ion_energy]
# plt.scatter(electronegativity, charge_transfer_total, s=600, color="lime")
# plt.scatter(electronegativity, charge_transfer_total,
#             marker="o", c='', edgecolors='darkgreen', s=800, linewidths=6)
# # plt.plot(electronegativity, charge_transfer_total, linewidth=3, color="green", alpha=0.5,  label="Charge transfer")
# for i in metal_total:
#     plt.annotate(s=i, xy=(electronegativity[metal_total.index(i)], charge_transfer_total[metal_total.index(i)] - 0.03),
#                  size=60, ha='center', va='center', color='black', family='Times New Roman')
# # plt.fill_between([])
# # plt.plot([0, 1], [0, 0], ls=":", linewidth=4, color='gray')
# plt.xticks(family='Times New Roman', size=60)
# plt.yticks(family='Times New Roman', size=60)
#
# # plt.xticks(x_index, ["Ge", "Nb", "Ta", "Ag", 'Ti', "W", "Al", "Mo"],
# #            size=60, family='Times New Roman')
# # for i in x_index:
# #     plt.plot([i, i], [0, 1000], color="gray", alpha=0.5, linewidth=3, ls=":")
# plt.xlim(1.4, 2.5)
# plt.xlim(5.8, 8.2) first ion energy
# plt.ylim(0, 0.5)
# plt.xlabel(" electronegativity ",
#            fontdict={'family': 'Times New Roman', 'weight': 'bold', 'size': 80})
# plt.ylabel('charge transfer', fontdict={'family': 'Times New Roman', 'weight': 'bold', 'size': 80})
# # plt.legend(loc='upper right', fontsize=50)
# ax.xaxis.set_major_locator(MultipleLocator(0.25))
# ax.spines['bottom'].set_linewidth(3)
# ax.spines['left'].set_linewidth(3)
# ax.spines['right'].set_linewidth(3)
# ax.spines['top'].set_linewidth(3)
# ax.tick_params(which='major', width=4)
# ax.tick_params(which='major', length=15)
# ax.tick_params(which='minor', width=3)
# ax.tick_params(which='minor', length=10)
#
# plt.xticks(family='Times New Roman', size=60)
# plt.yticks(family='Times New Roman', weight='black', size=60)
# plt.tight_layout()
#
# plt.savefig("/Users/yuze/Desktop/electronegativity.png", dpi=400)
# plt.show()

# fig = plt.figure(figsize=(30, 16), dpi=200)


''' 2.  from the lowest point that lie in the middle scale of the borophene and the surface metal layer of 
        the total charge density distributed to decide the the start point of intergarating '''

# metal_total = ["Li", "Ge", "Nb", "Ta",
#                "Ag", 'Ti', 'W', "Al", "Mo"]
# charge_transfer_point_total = []
# charge_transfer_peak_total = []
#
# fig = plt.figure(figsize=(30, 20), dpi=200)
# ax = plt.subplot(111)
# for i in metal_total:
#     metal = i
#     f0 = open("/Users/yuze/Desktop/CONT/hollow/CONTCAR-" + i, "r")
#     CONTCAR = f0.readlines()
#     layer_place = sure_layer_place(CONTCAR)
#     f = open("/Users/yuze/Desktop/CHGCAR/hollow/" + metal + "/total/CHGCAR", 'r')
#     total = f.readlines()
#     energy_total = electric(total)
#     electric_total = energy_total[0]
#     NGZ = energy_total[1]
#     x_place = np.linspace(0, 1, NGZ).tolist()
#     B_metal, total_c = [], []
#     for j in x_place:
#         if layer_place[0] <= j <= layer_place[2]:
#             B_metal.append(electric_total[x_place.index(j)])
#         if j < layer_place[0]:
#             total_c.append(electric_total[x_place.index(j)])
#     point_index = len(total_c) + B_metal.index(min(B_metal))
#     point_need = electric_total[len(total_c) + B_metal.index(min(B_metal))]
#     f = open("/Users/yuze/Desktop/CHGCAR/hollow/" + metal + "/B/CHGCAR", 'r')
#     total1 = f.readlines()
#     surface_total = electric(total1)
#     electric_surface = surface_total[0]
#     f = open("/Users/yuze/Desktop/CHGCAR/hollow/" + metal + "/cd/CHGCAR", 'r')
#     total2 = f.readlines()
#     cd_total = electric(total2)
#     electric_cd = cd_total[0]
#     different = [((i - electric_cd[electric_total.index(i)] - electric_surface[electric_total.index(i)]))
#                  for i in electric_total]
#     peak = max(different)
#     peak_index = different.index(peak)
#     charge_transfer_peak = sum(different[peak_index:])
#     charge_transfer_point = sum(different[point_index:])
#     print(peak_index, point_index)
#     print(charge_transfer_peak)
#     print(charge_transfer_point)
#     charge_transfer_peak_total.append(charge_transfer_peak)
#     charge_transfer_point_total.append(charge_transfer_point)
#
#
# electronegativity = [0.98, 2.01, 1.59, 1.51, 1.93, 1.54, 2.36, 1.61, 2.16]
# func = [2.93, 5, 4.36, 4, 4.74, 4.33, 4.45, 4.36, 4.55]
# first_ion_energy = [520.2, 762, 652.1, 761, 731, 658.8, 770, 577.5, 684.3]
# x_place = np.linspace(0, 1, NGZ)
# plt.scatter(func, charge_transfer_point_total, s=600, color="lime")
# plt.scatter(func, charge_transfer_point_total,
#             marker="o", c='', edgecolors='darkgreen', s=800, linewidths=6)
#
# plt.scatter(func, charge_transfer_peak_total, s=600, color="skyblue")
# plt.scatter(func, charge_transfer_peak_total,
#             marker="D", c='', edgecolors='darkblue', s=800, linewidths=6)
#
# for i in func:
#     plt.annotate(s=metal_total[func.index(i)],
#                  xy=(i, charge_transfer_peak_total[func.index(i)] - 0.03),
#                  size=30, ha='center', va='center', color='black', family='Times New Roman')
#     plt.annotate(s=metal_total[func.index(i)],
#                  xy=(i, charge_transfer_point_total[func.index(i)] - 0.03),
#                  size=30, ha='center', va='center', color='black', family='Times New Roman')
#
# plt.xticks(family='Times New Roman', size=60)
# plt.yticks(family='Times New Roman', size=60)
#
#
# # plt.xlim([500, 800])
# # plt.xlim([0.9, 2.5])
# # plt.ylim([-0.5, 1])
# plt.xlim([2.5, 5.5])
# plt.xlabel(" func/ eV ",
#            fontdict={'family': 'Times New Roman', 'weight': 'bold', 'size': 80})
# plt.ylabel('charge transfer/ e', fontdict={'family': 'Times New Roman', 'weight': 'bold', 'size': 80})
# # plt.legend(loc='lower left', fontsize=50)
#
# plt.savefig("/Users/yuze/Desktop/func.png", dpi=400)
# plt.show()
