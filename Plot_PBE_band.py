''' PBE band'''
# # --------------------------------------------------------------
import matplotlib.pyplot as plt
import numpy as np


f = open('/Users/yuze/Desktop/vasprun.xml', 'r')
data = f.readlines()
band_index = []

''' get the div kpoints on the k-path and record the total number '''
''' get the efermi '''
for i in data:
    a = i.strip('\n')
    if '<i name="divisions" type="int">' in i:
        div = int(i[37:42])
        div_index = data.index(i)
    if '<varray name="kpointlist" >' in i:
        kpointlist_index = data.index(i)
    if '<i name="efermi">' in i:
        efermi = float(i[i.find('"> ') + 2:i.find('</i>')])
high_symmetry_points_number = kpointlist_index - div_index - 3
total_kpoints = div * high_symmetry_points_number
remove_list = []
kpointlist_index1 = kpointlist_index

''' get the proportion of the every k-path and record the duplicate points'''
k_path = []
k_path.append(data[kpointlist_index1 + 1])
for i in range(high_symmetry_points_number):
    if data[kpointlist_index1 + div] == data[kpointlist_index1 + div + 1]:
        remove_list.append(kpointlist_index1 + div - kpointlist_index)
    if data[kpointlist_index1 + div] != data[kpointlist_index1 + div + 1]:
        if data[kpointlist_index1 + div + 1] != '  </varray>':
            k_path.append(data[kpointlist_index1 + div])
    if range(high_symmetry_points_number).index(i) != high_symmetry_points_number - 1:
        k_path.append(data[kpointlist_index1 + div])
    kpointlist_index1 += div
remove_list.sort(reverse=True)
# proportions = []
# for i in k_path:
#     proportion = math.sqrt((float(k_path[k_path.index(i) + 1][13:25]) - float(i[13:25])) ** 2 +
#                            (float(k_path[k_path.index(i) + 1][13:25]) - float(i[13:25])) ** 2 +
#                            (float(k_path[k_path.index(i) + 1][13:25]) - float(i[13:25])) ** 2)
#     proportions.append(proportion)

" get band_data "
kpoints_index = []
num = 0
for i in data:
    a = i.strip('\n')
    if '<set comment="kpoint' in i:
        kpoints_index.append(data.index(i))
        num += 1
        if num == total_kpoints:
            break
band_count = kpoints_index[1] - kpoints_index[0] - 2
band_data = []
num = 0
for i in range(len(kpoints_index)):
    kpoint = []
    for j in data[kpoints_index[num] + 1:kpoints_index[num] + band_count + 1]:
        kpoint.append(float(j.strip('\n')[12:20]))
    band_data.append(kpoint)
    num += 1
num = 0
for i in range(len(remove_list)):
    band_data.remove(band_data[remove_list[num]])
    num += 1
''' get the band_plot '''
lines = []
for i in range(len(band_data[0])):
    line = []
    for j in band_data:
        line.append(j[i] - efermi)
    lines.append(line)

x = np.linspace(0, 1, total_kpoints - len(remove_list))
plt.figure(figsize=(20, 20), dpi=400)
for line in lines:
    plt.plot(x, line, color='navy', linewidth=2, ls="-")

plt.plot([0, 1], [0, 0], color='gray', linewidth=2, ls="--")
x_index = [1]
x_index_basic = 1/high_symmetry_points_number
num = 0
for i in range(high_symmetry_points_number):
    plt.plot([x_index_basic * num, x_index_basic * num], [-20, 20], color='gray', linewidth=3, ls=":")
    x_index.append(x_index_basic * num)
    # plt.plot([sum(proportions[:num + 1]), sum(proportions[:num + 1])], [-10, 10],
    # color='gray', linewidth=1, ls=":")
    # add += proportions[num]
    num += 1
for line in lines:
    print(line[0])
plt.text(0.85, -14, l,
         fontdict={'size': 70, 'family': 'Times New Roman'}, va='center', ha='center', color='black')
x_index.sort(reverse=False)
plt.ylabel("${E}$ - ${E_f}$ / ${eV}$", fontdict={'family': 'Times New Roman', 'size': 50})
plt.xlabel("Wavevector k", fontdict={'family': 'Times New Roman', 'size': 40})
plt.yticks(np.linspace(-4.0, 3, 8), size=35, family='Times New Roman')
# plt.yticks([5, 0, -5, -10, -15], ["5", "0", "-5", "-10", "-15"], size=30, family='Times New Roman')
# plt.xticks(x_index, ["M", "Γ", "K", "M"], size=50, family='Times New Roman')

plt.xticks(x_index, ["Γ", "X", "W", "K", "Γ", 'L', "U", "W", "L", "K|U", "X"], size=35, family='Times New Roman')
plt.xlim(0, 1)
plt.ylim(-4, 3)

# plt.savefig('/Users/yuze/Desktop/Band_' + l + '.png', dpi=400)
plt.show()
