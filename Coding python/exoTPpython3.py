
note=int(50)

print("entrer votre note: ")

if note>=90:
    mention="Tres bien"

elif note>= 70:
    mention="bien"

elif note>=50:
    mention="passable"

else:
    mention="insuffisant"

print(f"votre mention est :{mention}")