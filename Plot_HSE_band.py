'''HSE band'''
'''需要自己写kpoint总数以及自己想要点的起始位置'''
# ----------------------------------------------------------------------------------------------------------------------
f = open('/Users/yuze/Desktop/vasprun.xml', 'r')
data = f.readlines()
kpoint = []

''' get the div kpoints on the k-path and record the total number '''
''' get the efermi '''
Start = 86
for i in data:
    a = i.strip('\n')
    if '<i name="efermi">' in i:
        efermi = float(i[i.find('"> ') + 2:i.find('</i>')])
    if '<set comment="kpoint ' + str(Start) + '">' in i:
        kpoint.append(data[data.index(i) + 1:data.index(i) + 38])
        Start += 1
total_kpoints = 265
kpoint.remove(kpoint[120])
kpoint.remove(kpoint[60])
" get band_data "
lines = []
line = []
num = 0
for i in range(len(kpoint[0])):
    for j in kpoint:
        line.append(float(j[num][12:24]) - efermi)
    lines.append(line)
    line = []
    num += 1
print(lines)

''' get the band_plot '''
# 178 is the total kpoints you need to make sure
x = np.linspace(0, 1, 178)
plt.figure(figsize=(20, 20), dpi=400)
for line in lines:
    plt.plot(x, line, color='navy', linewidth=2, ls="-")
plt.plot([0, 1], [0, 0], color='gray', linewidth=2, ls="--")
x_index = [1]
x_index_basic = 1/3
num = 0
for i in range(3):
    plt.plot([x_index_basic * num, x_index_basic * num], [-20, 20], color='gray', linewidth=3, ls=":")
    x_index.append(x_index_basic * num)
    num += 1
plt.text(0.85, -14, l,
         fontdict={'size': 70, 'family': 'Times New Roman'}, va='center', ha='center', color='black')
x_index.sort(reverse=False)
plt.ylabel("${E}$ - ${E_f}$ / ${eV}$", fontdict={'family': 'Times New Roman', 'size': 70})
plt.xlabel("Wavevector k", fontdict={'family': 'Times New Roman', 'size': 70})

# here are some kpoints way that you should make sure according to the reality
plt.yticks([5, 0, -5, -10, -15], ["5", "0", "-5", "-10", "-15"], size=50, family='Times New Roman')
plt.xticks(x_index, ["M", "Γ", "K", "M"], size=50, family='Times New Roman')
plt.xlim(0, 1)
plt.ylim(-15.2, 5)


plt.savefig('/Users/yuze/Desktop/Band.png', dpi=400)
plt.show()
